import pandas as pd
import os
import wget
import ssl
import fitz
import ocrmypdf
import urllib.request
import requests

opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': USER_AGENT}


# This restores the same behavior as before.
#context = ssl._create_unverified_context()

ssl._create_default_https_context = ssl._create_unverified_context

###################################
###################################
###################################

#Base de datos

#Base completa
latam = pd.read_excel('/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/test_descarga/Latam3.xlsx')
#filtro columnas de interés
#latam = latam.loc[:,['País', 'Entidad','Tipo convocatoria', 'Título', 'Links pdf', 'Link']]
#limpieza de categorías
latam.replace({'Tipo convocatoria': 'Índices/Evaluación'}, {'Tipo convocatoria': 'Índices-Evaluación'}, regex=True, inplace=True)
latam.replace({'Tipo convocatoria': 'Investigación/Innovación'}, {'Tipo convocatoria': 'Investigación-Innovación'}, regex=True, inplace=True)
latam.columns
######################

pais = 'Brasil'
pais_select = latam.loc[latam['País']==pais]

#tipo convocatorial
#for convocarioria in tipo_convocatoria:
entidad = pais_select['Entidad'].unique().tolist()
#tipo de voncocatoria
pais_select = pais_select.replace('Concurso/Premio', 'Concurso-Premio')
tipo_convocatoria = pais_select['Tipo convocatoria'].unique().tolist()




#Elimina puntos
titulos = []
for count, i in enumerate(pais_select['Título']):
    titulos.append(str(count+1) + str(i).strip('.').replace('/', '-'))

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

pais_select
##########################################
##########################################
##########################################
### Crea Carpetas

directorio_base = '/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/test_descarga'

for i in range(len(pais_select)):

    try:
        os.mkdir(base_pais)
    except:
        pass

    try:
        os.mkdir(base_pais+ '/' + pais_select['Entidad'][i])
    except:
        pass

    try:
        os.mkdir(base_pais+ '/' + pais_select['Entidad'][i] + '/' + pais_select['Tipo convocatoria'][i])
    except:
        pass

    try:
        os.mkdir(base_pais+ '/' + pais_select['Entidad'][i] + '/' + pais_select['Tipo convocatoria'][i] + '/' + pais_select['Título'][i][0:150])
    except:
        pass


########################
########################
########################
######## Path ##########
bases_proyectos = []
for i in range(len(pais_select)):
    path_proy = base_pais + '/' + pais_select['Entidad'][i] + '/' + pais_select['Tipo convocatoria'][i] + '/' + pais_select['Título'][i]
    bases_proyectos.append(path_proy)

################################
################################
################################

bases_proyectos
### Descarga pdfs y convierte en txt
for base_proyecto in bases_proyectos:
    texto_proyecto = ''
    
    tit = base_proyecto.split('/')[-1]

    proyecto = pais_select.loc[pais_select['Título'] == tit]
    proyecto = proyecto.reset_index(drop=True)

    try:
        pdfs = proyecto['Links pdf'][0].split(', ')
        #pdfs = [pdf for pdf in pdfs_brutos if pdf.endswith('.pdf')]
        pdfs
        
        kk = base_proyecto.split('/')
        base = ''
        for b in kk[:9]:
            base = base + b + '/'
        base = '/' + base+proyecto['Título'][0][0:150] #+ proyecto['id_proy_convocatoria']
        base = base[1::]
        
        for count_link, pdf in enumerate(pdfs):

            path = base + '/' + str(count_link+1) + '-' + pdf.split('/')[-1]  
            
            #wget.download(pdf, path)
            try:
                if path.endswith('.pdf') == False and path.endswith('.docx') == False and path.endswith('.doc') == False:
                    path= path + '.pdf'
                    urllib.request.urlretrieve(pdf, path)
                else:
                    urllib.request.urlretrieve(pdf, path)
            except:
                try:
                    wget.download(pdf, path)
                except:
                    print('Error en la descarga')
                    pass

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
    
    ## TXT Pais
    nom_txt_pais = base_pais+'/'+ 'text' + str(int(proyecto['id_proy'][0])) + '.txt'
    txt_pais = open(nom_txt_pais, 'w')
    txt_pais.write(str(texto_proyecto))
    txt_pais.close()

    ##TXT entidad

    nom_txt_entidad = base_pais + '/' + entidad +'/'+ 'text' + str(int(proyecto['id_proy_ent'][0])) + '.txt'
    txt_entidad = open(nom_txt_entidad, 'w')
    txt_entidad.write(str(texto_proyecto))
    txt_entidad.close()

    ##TXT Estado
    
    nom_txt_estado = base_pais + '/' + entidad + '/' + estado +'/'+ 'text' + str(int(proyecto['id_proy_convocatoria'][0])) + '.txt'
    txt_estado = open(nom_txt_estado, 'w')
    txt_estado.write(str(texto_proyecto))
    txt_estado.close()
