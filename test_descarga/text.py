import pandas as pd
import os
import wget
import ssl
import fitz
import ocrmypdf

# This restores the same behavior as before.
#context = ssl._create_unverified_context()

ssl._create_default_https_context = ssl._create_unverified_context

###################################
###################################
###################################

#Base de datos

#Base completa
latam = pd.read_excel('/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/test_descarga/TodoLatam2.xlsx')
#filtro columnas de interés
latam = latam.loc[:,['País', 'Entidad','Tipo convocatoria', 'Título', 'Links pdf', 'Link']]
#limpieza de categorías
latam.replace({'Tipo convocatoria': 'Índices/Evaluación'}, {'Tipo convocatoria': 'Índices-Evaluación'}, regex=True, inplace=True)
latam.replace({'Tipo convocatoria': 'Investigación/Innovación'}, {'Tipo convocatoria': 'Investigación-Innovación'}, regex=True, inplace=True)

######################

pais = 'Colombia'
pais_select = latam.loc[latam['País']==pais]

#tipo convocatorial
#for convocarioria in tipo_convocatoria:
entidad = pais_select['Entidad'].unique().tolist()
#tipo de voncocatoria
tipo_convocatoria = pais_select['Tipo convocatoria'].unique().tolist()



#Crea ID por tipo de convocatoria
base_final_conv = pd.DataFrame()
for conv in tipo_convocatoria:
    df_conv = pais_select.loc[pais_select['Tipo convocatoria'] == conv]
    cant = []
    for count, proy in enumerate(df_conv['Título']):
        num = count+1
        cant.append(num)
    
    df_conv['id_proy_convocatoria'] = cant

    base_final_conv = pd.concat([base_final_conv, df_conv])


#Crea ID por tipo de entidad

base_final_ent = pd.DataFrame()

for ent in entidad:
    df_ent = base_final_conv.loc[base_final_conv['Entidad'] == ent]
    cant = []
    for count, proy in enumerate(df_ent['Título']):
        num = count+1
        cant.append(num)
    
    df_ent['id_proy_ent'] = cant

    base_final_ent = pd.concat([base_final_ent, df_ent])

base_final_ent

# Crea ID por tipo de pais

cant = []
for count, proy in enumerate(base_final_ent['Título']):
    num = count+1
    cant.append(num)

base_final_ent['id_proy'] = cant

pais_select = base_final_ent

#Elimina puntos
titulos = []
for i in pais_select['Título']:
    titulos.append(i.strip('.'))
pais_select['Título'] = titulos

#########################################
#########################################
#########################################

## Identifica el indice de los archivos ya creados
base_pais = '/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/test_descarga/' + pais
try:
    avance = [int(dir.split('text')[-1].split('.')[0]) for dir in os.listdir(base_pais) if dir.startswith('text')]
    ult = sorted(avance)[-1]
except:
    ult = 0

pais_select = pais_select.loc[pais_select['id_proy']>ult]
pais_select = pais_select.reset_index(drop=True)



##########################################
##########################################
##########################################
### Crea Carpeta País

directorio_base = '/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/test_descarga'
pais = 'Colombia'

try:
    os.mkdir(directorio_base+ '/' + pais)
except:
    pass

###################
#Crea carpeta de entidades

base_pais = '/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/test_descarga/' + pais

entidades = []
for ent in entidad:
        #Crea carpeta de estado del proyecto
    try:
        base_entidad = base_pais+ '/' + ent
        entidades.append(base_entidad)
        try:
            os.mkdir(base_entidad)
        except:
            pass
    except FileExistsError:
        continue 

############################
#Crea carpeta por tipo de proyecto
tipo_convocatorias= []
bases_proyectos = []
proyectos = []
#Entidades
for ent in entidades:
    #Convocatorias
    for convocatoria in tipo_convocatoria:
        
        base_tipo_convocatoria = ent+ '/' + convocatoria
        tipo_convocatorias.append(base_tipo_convocatoria)
        try:
            os.mkdir(base_tipo_convocatoria)
        except:
            pass

        #####
        #Crea carpeta por proyecto
        tipo_proyecto = pais_select.loc[pais_select['Tipo convocatoria']==convocatoria]
        #Proyectos

        for count, proyecto in enumerate(tipo_proyecto['Título']):
            
            base_proyecto1 = base_tipo_convocatoria+ '/' + str(count+1) + '.' + proyecto[0:150]
            base_proyecto = base_tipo_convocatoria+ '/' + str(count+1) + '.' + proyecto

            try:
                os.mkdir(base_proyecto1)
            except:
                pass
            bases_proyectos.append(base_proyecto)    # Descarga archivos

            proyectos.append(proyecto)

################################
################################
################################

### Descarga pdfs y convierte en txt
for base_proyecto in bases_proyectos:
    texto_proyecto = ''
    
    tit = base_proyecto.split('/')[-1][2::]

    proyecto = pais_select.loc[pais_select['Título'].str.startswith(tit)]
    proyecto = proyecto.reset_index(drop=True)
    
    try:
        pdfs_brutos = proyecto['Links pdf'][0].split(', ')
        pdfs = [pdf for pdf in pdfs_brutos if pdf.endswith('.pdf')]

        kk = base_proyecto.split('/')
        base = ''
        for b in kk[:9]:
            base = base + b + '/'

        base = '/' + base+base_proyecto.split('/')[-1][0:152]
        base = base[1::]

        for count_link, pdf in enumerate(pdfs):

            path = base  + '/' + str(count_link+1) + '.' + pdf.split('/')[-1]        
            wget.download(pdf, path)
            doc = fitz.open(path)

            if len(doc) > 8:
                ### Ejecuta OCR
                doc.close()
                try:
                    ocrmypdf.ocr(path, path)
                except:
                    pass

            doc = fitz.open(path)

            #Pagina por pagina y extrae txto
            
            for pagina in doc:
                text = pagina.getText()#.encode('utf8')
                texto_proyecto = texto_proyecto + str(text) + ' '

            doc.close()
        
        texto_proyecto = texto_proyecto.strip(' ')
    except:
        pass
    ########### TXT

    entidad = base_proyecto.split('/')[7]
    estado = base_proyecto.split('/')[8]
    


    proy = pais_select.loc[pais_select['Título'] == tit]
    proy = proy.reset_index(drop=True)

    ## TXT Pais

    nom_txt_pais = base_pais+'/'+ 'text' + str(proy['id_proy'][0]) + '.txt'
    txt_pais = open(nom_txt_pais, 'w')
    txt_pais.write(str(texto_proyecto))
    txt_pais.close()

    ##TXT entidad

    nom_txt_entidad = base_pais + '/' + entidad +'/'+ 'text' + str(proy['id_proy_ent'][0]) + '.txt'
    txt_entidad = open(nom_txt_entidad, 'w')
    txt_entidad.write(str(texto_proyecto))
    txt_entidad.close()

    ##TXT Estado
    
    nom_txt_estado = base_pais + '/' + entidad + '/' + estado +'/'+ 'text' + str(proy['id_proy_convocatoria'][0]) + '.txt'
    txt_estado = open(nom_txt_estado, 'w')
    txt_estado.write(str(texto_proyecto))
    txt_estado.close()