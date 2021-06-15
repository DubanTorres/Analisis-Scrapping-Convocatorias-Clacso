import pandas as pd
import os
import wget
import ssl
import fitz
import ocrmypdf

ssl._create_default_https_context = ssl._create_unverified_context

#Base completa
latam = pd.read_excel('/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/test_descarga/TodoLatam2.xlsx')
#filtro columnas de interés
latam = latam.loc[:,['País', 'Entidad','Tipo convocatoria', 'Título', 'Links pdf', 'Link']]
#limpieza de categorías
latam.replace({'Tipo convocatoria': 'Índices/Evaluación'}, {'Tipo convocatoria': 'Índices-Evaluación'}, regex=True, inplace=True)
latam.replace({'Tipo convocatoria': 'Investigación/Innovación'}, {'Tipo convocatoria': 'Investigación-Innovación'}, regex=True, inplace=True)

######################
## Paises
#paises = latam['País'].unique().tolist()
#for pais in paises:
pais = 'Colombia'
pais_select = latam.loc[latam['País']==pais]
pais_select = pais_select[0:10]
#tipo convocatorial
tipo_convocatoria = pais_select['Tipo convocatoria'].unique().tolist()
#for convocarioria in tipo_convocatoria:
entidad = pais_select['Entidad'].unique().tolist()

##########################################
n_pais=1
### Crea Carpeta País

directorio_base = '/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/test_descarga'
pais = 'Colombia'

os.mkdir(directorio_base+ '/' + pais)

###################
#Crea carpeta de entidades


base_pais = '/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/test_descarga/' + pais


entidades = []
for ent in entidad:
        #Crea carpeta de estado del proyecto
    try:
        base_entidad = base_pais+ '/' + ent
        entidades.append(base_entidad)
        os.mkdir(base_entidad)
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
        os.mkdir(base_tipo_convocatoria)

        #####
        #Crea carpeta por proyecto
        tipo_proyecto = pais_select.loc[pais_select['Tipo convocatoria']==convocatoria]
        #Proyectos

        
        for count, proyecto in enumerate(tipo_proyecto['Título']):
            
            base_proyecto = base_tipo_convocatoria+ '/' + str(count+1) + '.' + proyecto[0:150]
            os.mkdir(base_proyecto)
            bases_proyectos.append(base_proyecto)    # Descarga archivos

            proyectos.append(proyecto)


#tipo_proyecto = pais_select.loc[pais_select['Tipo convocatoria']==convocatoria]
            
            
# for proyecto in proyectos:

#     proyecto_pdf = tipo_proyecto.loc[tipo_proyecto['Título']==proyecto]

#     for count_proyecto, alist_link in enumerate(proyecto_pdf['Links pdf']):

#         pdfs_brutos = alist_link.split(', ')
#         pdfs = [pdf for pdf in pdfs_brutos if pdf.endswith('.pdf')]

##################


texto_proyecto = ''
n_proyecto = 1 

for base_proyecto in bases_proyectos:
    
    tit = base_proyecto.split('/')[-1].split('.')[1]

    proyecto = pais_select.loc[pais_select['Título'].str.startswith(tit)]
    proyecto = proyecto.reset_index(drop=True)
    #print(proyecto['Links pdf'])
    pdfs_brutos = proyecto['Links pdf'][0].split(', ')

    pdfs = [pdf for pdf in pdfs_brutos if pdf.endswith('.pdf')]

    for count_link, pdf in enumerate(pdfs):
        
        path = base_proyecto  + '/' + str(count_link+1) + '.' + pdf.split('/')[-1]
        
        wget.download(pdf, path)
        ### Ejecuta OCR
        try:
            ocrmypdf.ocr(path, path) #deskew=True)
        except:
            doc = fitz.open(path)

        doc = fitz.open(path)

        #Pagina por pagina y extrae txto
        
        for pagina in doc:
            text = pagina.getText()#.encode('utf8')
            texto_proyecto = texto_proyecto + str(text) + ' '
        texto_proyecto = texto_proyecto.strip(' ')

        doc.close()
    
    ## TXT Pais

    nom_txt_pais = base_pais+'/'+ 'text' + str(n_pais) + '.txt'
    txt_pais = open(nom_txt_pais, 'w')
    txt_pais.write(str(texto_proyecto))
    txt_pais.close()
    n_pais+=1

    ##TXT entidad
    ### Tal vez toque entidad por entidad con un if
    nom_txt_entidad = base_pais + '/' + base_proyecto.split('/')[7] +'/'+ 'text' + str(n_pais) + '.txt'
    txt_entidad = open(nom_txt_entidad, 'w')
    txt_entidad.write(str(texto_proyecto))
    txt_entidad.close()
    n_pais+=1

    ## TXT Proyecto por estado 
    ###Tal vez se pueda unir con el de arriba

    nom_txt_proyecto = base_pais + '/' + base_proyecto.split('/')[8]+ '/'+ 'text' + str(n_proyecto) + '.txt'
    txt_proyecto = open(nom_txt_proyecto, 'w')
    txt_proyecto.write(str(texto_proyecto))
    txt_proyecto.close()
    n_proyecto+=1

#base_proyecto
        

# #tipo_proyecto.loc[tipo_proyecto['Título'].str.startswith(tit)]
# proyecto = tipo_proyecto.loc[tipo_proyecto['Título'].str.startswith(tit)]
# pdfs_brutos = proyecto['Links pdf']
# pdfs_brutos

# proyecto
#base_pais              
#bases_proyectos[0].split('/')[8]
          
                
                
        #         for count_proyecto, alist_link in enumerate(proyecto_pdf['Links pdf']):
                    
        #             pdfs_brutos = alist_link.split(', ')
        #              # Selecciona solo pdfs
        #             pdfs = [pdf for pdf in pdfs_brutos if pdf.endswith('.pdf')]

        #             texto_proyecto = ''
        #             #n_proyecto = 0 

        #             #Recorre los pdfs
        #             for count_link, pdf in enumerate(pdfs):
        #                 path = base_proyecto  + '/' + str(count_link+1) + '.' + pdf.split('/')[-1]
        #                 wget.download(pdf, path)
        #                 ### Ejecuta OCR
        #                 try:
        #                     ocrmypdf.ocr(path, path, deskew=True)
        #                 except:
        #                     doc = fitz.open(path)

        #                 doc = fitz.open(path)

        #                 #Pagina por pagina y extrae txto
                        
        #                 for pagina in doc:
        #                     text = pagina.getText()#.encode('utf8')
        #                     texto_proyecto = texto_proyecto + str(text) + ' '
        #                 texto_proyecto = texto_proyecto.strip(' ')
        #                 #doc.close()

        #             nom_txt = 'text' + str(n_proyecto) + '.txt'
        #             n_proyecto+=1
        #             print(nom_txt)
        #             print(count_proyecto)
        #             print(n_proyecto)   
        #         #txt = open(nom_txt, 'w')
        #         #txt.write(str(texto_proyecto))
        #         #txt.close()
        #         #n_proyecto+=1

        # except FileExistsError:
        #     continue