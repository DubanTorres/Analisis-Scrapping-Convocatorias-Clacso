""" Este script extrae información de los campos del HTML 
    del cvlac a partir de una base de datos inicial de los perfiles
"""
# Importar librerias/Modulos
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from lxml import html
import scrapy
import time


# Extrae metadatos de la página semilla
def pag_principal():
    n = 'todas'
    link = 'https://minciencias.gov.co/convocatorias/' + n
    #requests.packages.urllib3.disable_warnings()

    encabezados = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    }

    resp = requests.get(link, headers=encabezados, verify=False)
    resp = resp.text

    #soup = get_Soup('https://minciencias.gov.co/convocatorias/todas')
    parser = html.fromstring(resp)

    return parser

#Título
def titulo(parser):
    titulo = parser.xpath('//table[@class="views-table cols-5"]/tbody/tr/td[@class="views-field views-field-title"]/a/text()')
    return titulo

# Descripción
def descripcion(parser):
    
    descripcion = []
    for x in range(0,6):

        #descrip = parser.xpath('//table/tbody/tr[' + str(x) + ']/td[' + str(x) + ']/text()')
        descrip = parser.xpath('//table/tbody/tr['+str(x)+']/td[3]/text()')
        descripcion.append(descrip)
    decrip = []
    for x in descripcion[1:6]:
        des = x[0].strip()
        decrip.append(des) 

    
    return decrip

#Presupuesto
def cuantia(parser):
    cuantia = parser.xpath('//td[@class="views-field views-field-field-cuantia"]/text()')
    presupuesto = []
    for x in cuantia:
        x = x.strip()
        presupuesto.append(x)
    return presupuesto

#Fecha Apertura
def fecha_apertura(parser):
    
    fecha_apertura = parser.xpath('//table/tbody/tr//td[@class="views-field views-field-field-fecha-de-apertura"]/span/text()')
    fe_aper = []
    for x in fecha_apertura:
        x = x.strip()
        if x != '':
            fe_aper.append(x.strip())
    
    if len(fe_aper) < 5:
        fecha_apertura = parser.xpath('//table/tbody/tr//td[@class="views-field views-field-field-fecha-de-apertura"]//text()')
        fe_aper = []
        for x in fecha_apertura:
            x = x.strip()
            if x != '':
                fe_aper.append(x.strip())

    if len(fe_aper) < 5:
        fe_aper = []
        for x in range(0,6):
            fecha_apertura = parser.xpath('//table/tbody/tr[' + str(x) + ']/td[5]/text()')
            if len(fecha_apertura) == 0:
                x = ''
            else:
                for x in fecha_apertura:
                    x = x.strip()
                    #if x != '':
                    fe_aper.append(x.strip())

    return fe_aper

#Links scrapy vertical
def links_vertical(link):

    encabezados = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        }

    resp = requests.get(link, headers=encabezados, verify=False)
    resp = resp.text

    response = scrapy.Selector(text=resp)
    
    final = response.xpath('//td[@class="views-field views-field-title"]/a/@href').getall()
    
    link = 'https://minciencias.gov.co'
    links = []
    for x in final:
        if x.startswith('http://'): 
            links.append(x)
        elif x.startswith('https://'): 
            links.append(x)
        else:
            links.append(link+x)
    return links

# Extrae última página
def ult_page(url):    
    
    encabezados = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        }

    resp = requests.get(url, headers=encabezados, verify=False)
    resp = resp.text    

    response = scrapy.Selector(text=resp)

    ult = response.xpath('//li[@class="pager-last last"]/a/@href').getall()

    ult2 = ult[0].split('=')[1]
    
    return ult2

### Vertical
def pag_vertical(link):
    try:
        encabezados = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        }

        resp = requests.get(link, headers=encabezados, verify=False)
        resp = resp.text

        #soup = get_Soup('https://minciencias.gov.co/convocatorias/todas')
        parser = html.fromstring(resp)
    except:
        parser = 'http://www.rutanmedellin.org/es/actualidad/noticias/item/abierta-convocatoria-para-solucionar-retos-energeticos-empresariales'


    return parser

#Extrae Objetivo
def objetivo(parser):
    try:
        objetivo = parser.xpath('//div[@class="field-items"][2]/div[@class="field-item even"]/text()')
        objetivo_pro = objetivo[0].strip()
    except IndexError:
        objetivo_pro = ''
    except AttributeError:
        objetivo_pro = ''
    return objetivo_pro

# Extrae Público Objetivo
def publico_objetivo(parser):
    try:
        diri_a = parser.xpath('//div[@class="body2-convocatorias"]//div[@class="field-item even"]//text()')

        n=0
        dirigido_a = ''

        for elemento in diri_a:
            elemento = elemento.strip()
            if elemento != '':
                dirigido_a = dirigido_a + ' ' + elemento
                n+=1

        dirigido_a.strip()
    except AttributeError:
        dirigido_a = ''
    return dirigido_a

# Extrae estado de la convocatoria
def estado(parser):
    try:
        estado = parser.xpath('//div[@class="sub-sub-panel panel-state-tex"]/p/text()')
        estado = estado[0] + ' ' + estado[1]
    except IndexError:
        estado = ''
    except AttributeError:
        estado = ''
    return estado

# Extrae Fecha de cierre
def fechas_cierre(parser):
    
    try:
        marcas = parser.xpath('//tr/td[@class="views-field views-field-field-numero"]/text()')
        estados = []
        fecha2 = ''
        for i in marcas:
            estados.append(i.strip())
            
        for x in range(len(estados)):
            marca = parser.xpath('//tr/td[@class="views-field views-field-field-numero"][1]/text()')[x]
            if marca.strip() in estados:
                fecha = parser.xpath('//tr/td[@class="views-field views-field-body"]/text()')[x]
                if marca.strip() == 'Cierre':
                    fecha2 = fecha.strip()
                    break
                else:
                    fecha2 = ''
    except IndexError:
        fecha2 = ''
    except AttributeError:
        fecha2 = ''

    return fecha2.strip()

# Extrae fecha de Resultados preliminares
def fechas_resultados_preliminares(parser):
    
    try:
        marcas = parser.xpath('//tr/td[@class="views-field views-field-field-numero"]/text()')
        estados = []
        fecha2 = ''
        for i in marcas:
            estados.append(i.strip())
            
        for x in range(len(estados)):
            marca = parser.xpath('//tr/td[@class="views-field views-field-field-numero"][1]/text()')[x]
            if marca.strip() in estados:
                fecha = parser.xpath('//tr/td[@class="views-field views-field-body"]/text()')[x]
                if marca.strip() == 'Publicación de resultados preliminares':
                    fecha2 = fecha.strip()
                    break
                else:
                    fecha2 = ''
    except IndexError:
        fecha2 = ''
    except AttributeError:
        fecha2 = ''
                
    return fecha2.strip()

#Extrae Fecha de públicación de resultados
def fechas_publicacion_resultados_definitivos(parser):
    try:
        marcas = parser.xpath('//tr/td[@class="views-field views-field-field-numero"]/text()')
        estados = []
        fecha2 = ''
        for i in marcas:
            estados.append(i.strip())

        for x in range(len(estados)):
            marca = parser.xpath('//tr/td[@class="views-field views-field-field-numero"][1]/text()')[x]
            if marca.strip() in estados:
                fecha = parser.xpath('//tr/td[@class="views-field views-field-body"]/text()')[x]
                if marca.strip() == 'Publicación de resultados definitivos' or marca.strip() == 'Publicación de resultados  definitivos':
                    fecha2 = fecha.strip()
                    break
                else:
                    fecha2 = ''
    except IndexError:
        fecha2 = ''
    except AttributeError:
        fecha2 = ''
        
    return fecha2.strip()

# Extrae links de pdfs
def links_pdf(link):
    encabezados = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        }

    resp = requests.get(link, headers=encabezados, verify=False)
    resp = resp.text    

    response = scrapy.Selector(text=resp)

    links = response.xpath('//span[@class="file"]/a/@href').getall()
    
    urls = ''
    for link in links:
        urls = urls + ', ' + link
    
    urls = urls[2::]

    return urls

# Extrae parser de página horizontal
def pag_horizontal(link):
    
    
    encabezados = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    }

    resp = requests.get(link, headers=encabezados, verify=False)
    resp = resp.text

    #soup = get_Soup('https://minciencias.gov.co/convocatorias/todas')
    parser = html.fromstring(resp)

    return parser
"""
Genera función integran de scrapy de colciencias (Colombia)
"""

# Función integradora
def colombia():
    #   Página principal
    #   Configuración
    colombia = pd.DataFrame()
    parser = pag_principal()
    
    #   Extracción página principal

    tit = titulo(parser)
    desc = descripcion(parser)
    cuant = cuantia(parser)
    aper = fecha_apertura(parser)
    links = links_vertical('https://minciencias.gov.co/convocatorias/todas')
    
    #Vertical Primera página
    obj = []
    pub_objetivo = []
    est= []
    fe_cierre = []
    fe_preliminares = []
    fe_definitivos = []
    pdf = []
    

    for link in links:
        parser = pag_vertical(link)

        obj.append(objetivo(parser))
        pub_objetivo.append(publico_objetivo(parser))
        est.append(estado(parser))
        fe_cierre.append(fechas_cierre(parser))
        fe_preliminares.append(fechas_resultados_preliminares(parser))
        fe_definitivos.append(fechas_publicacion_resultados_definitivos(parser))
        pdf.append(links_pdf(link))
    
        #   CSV
    colombia['Título'] = tit
    colombia['Descripción'] = desc
    colombia['Objetivo'] = obj
    colombia['Cuantia'] = cuant
    colombia['Fecha Apertura'] = aper
    colombia['Fecha Cierre'] = fe_cierre
    colombia['Fecha Resultados Preliminares'] = fe_preliminares
    colombia['Fecha Publicación Resultados Definitivos'] = fe_definitivos
    colombia['Link'] = links
    colombia['Público Objetivo'] = pub_objetivo
    colombia['Estado de la Convocatoria'] = est
    colombia['Links pdf'] = pdf

    #Horizontal
    ult = ult_page('https://minciencias.gov.co/convocatorias/todas?page=1')

    for pag in range(1, int(ult)):
        
        print(pag)
        
        url = 'https://minciencias.gov.co/convocatorias/todas?page=' + str(pag)
        horizontal = pd.DataFrame()
        parser = pag_horizontal(url)
        

            #   Extracción página principal

        tit = titulo(parser)
        desc = descripcion(parser)
        cuant = cuantia(parser)
        aper = fecha_apertura(parser)
        links = links_vertical(url)
            
            #Vertical Primera página
        obj = []
        pub_objetivo = []
        est= []
        fe_cierre = []
        fe_preliminares = []
        fe_definitivos = []
        pdf = []
  
        for link in links:
            parser = pag_vertical(link)

            obj.append(objetivo(parser))
            pub_objetivo.append(publico_objetivo(parser))
            est.append(estado(parser))
            fe_cierre.append(fechas_cierre(parser))
            fe_preliminares.append(fechas_resultados_preliminares(parser))
            fe_definitivos.append(fechas_publicacion_resultados_definitivos(parser))
            pdf.append(links_pdf(link))
            

                        #   CSV
        horizontal['Título'] = tit
        horizontal['Descripción'] = desc
        horizontal['Objetivo'] = obj
        horizontal['Cuantia'] = cuant
        horizontal['Fecha Apertura'] = aper
        horizontal['Fecha Cierre'] = fe_cierre
        horizontal['Fecha Resultados Preliminares'] = fe_preliminares
        horizontal['Fecha Publicación Resultados Definitivos'] = fe_definitivos
        horizontal['Link'] = links
        horizontal['Público Objetivo'] = pub_objetivo
        horizontal['Estado de la Convocatoria'] = est
        horizontal['Links pdf'] = pdf

        colombia = colombia.append(horizontal)
        colombia.reset_index(drop=True, inplace=True)
        

    return colombia


Base_de_datos = colombia()

Base_de_datos.to_csv('Colombia.csv')