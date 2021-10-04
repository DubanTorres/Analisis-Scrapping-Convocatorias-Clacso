import pandas as pd
import os


"""
Prepara Archivos
"""
textos = os.listdir('/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/data/2. Textos Geneales')
bdd = pd.read_csv('/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/data/Latam3.csv')
bdd = bdd.loc[bdd['Tipo convocatoria'] == 'Investigación-Innovación']

"""
Tokens español
"""
gramas_esp = pd.read_csv('/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/data/Gramas_final.csv')

# Convierte ods en lista
class_ods_esp = []
for list_osd in gramas_esp['ODS']:
    list_osd = list_osd.lower().replace(':', ';').split(';')
    list_osd2 = []
    for o in list_osd:
        if o == 'rabajo decente y crecimiento económico' or o == 'trabajo decente y crecimiento económico' or o == 'trabajo decente y crecimiento económic':
            o = 'trabajo decente y crecimiento económico'
        
        if o == 'igualdad de género' or o == 'gualdad de género' or o == 'igualdad de genero':
            o = 'igualdad de género'
        
        if o == 'industria, innovación e infraestructuras' or o == 'industria, innovación e infraestructura':
            o = 'industria, innovación e infraestructuras'

        if o == 'paz, justicia e instituciones solidas' or o == 'paz, justicia e instituciones sólidas' or o == 'paz, justicia e instituciones sólida':
            o = 'paz, justicia e instituciones sólidas'

        if 'producción y consumo' in o:
            o = 'producción y consumo responsable'

        if o == 'ciudades y comunidades sostenibles' or o == 'ciudades y comunidades sostenible' or o == 'ciudades y comunidades sostenible':
            o = 'ciudades y comunidades sostenibles'
        
        if o == 'alianzas para lograr los objetivos' or o == 'alianza para lograr los objetivos':
            o = 'alianza para lograr los objetivos'
        
        if o == 'reducción de desigualdade' or o == 'reducción de las desigualdades' or o == 'reducción de desigualdades':
            o = 'reducción de desigualdades'

        if o == 'vida de ecosistemas terrestres' or o == 'vida de ecosistemas terrestre':
            o = 'vida de ecosistemas terrestres'

        o = o.strip()
        list_osd2.append(o)
    
    class_ods_esp.append(list_osd2)

gramas_esp['ODS'] = class_ods_esp



"""
Tokens portugues
"""
gramas_por = pd.read_csv('/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/data/Gramas_protugues.csv')

# convierte Ods en lista
class_ods_por = []

for list_osd in gramas_por['ODS']:

    list_osd = list_osd.lower().split(';')
    list_osd2 = []
    for o in list_osd:
        if o == 'rabajo decente y crecimiento económico' or o == 'trabajo decente y crecimiento económico' or o == 'trabajo decente y crecimiento económic':
            o = 'trabajo decente y crecimiento económico'
        
        if o == 'igualdad de género' or o == 'gualdad de género' or o == 'igualdad de genero':
            o = 'igualdad de género'
        
        if o == 'industria, innovación e infraestructuras' or o == 'industria, innovación e infraestructura':
            o = 'industria, innovación e infraestructuras'

        if o == 'paz, justicia e instituciones solidas' or o == 'paz, justicia e instituciones sólidas' or o == 'paz, justicia e instituciones sólida':
            o = 'paz, justicia e instituciones sólidas'

        if 'producción y consumo' in o:
            o = 'producción y consumo responsable'

        if o == 'ciudades y comunidades sostenibles' or o == 'ciudades y comunidades sostenible' or o == 'ciudades y comunidades sostenible':
            o = 'ciudades y comunidades sostenibles'
        
        if o == 'alianzas para lograr los objetivos' or o == 'alianza para lograr los objetivos':
            o = 'alianza para lograr los objetivos'
        
        if o == 'reducción de desigualdade' or o == 'reducción de las desigualdades' or o == 'reducción de desigualdades':
            o = 'reducción de desigualdades'

        if o == 'vida de ecosistemas terrestres' or o == 'vida de ecosistemas terrestre':
            o = 'vida de ecosistemas terrestres'
        o = o.strip()
        list_osd2.append(o.lower())
    
    class_ods_por.append(list_osd2)

gramas_por['ODS'] = class_ods_por


"""
Elimina las tildes
"""
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("Á", "A"),
        ("É", "E"),
        ("Í", "I"),
        ("Ó", "O"),
        ("Ú", "U")
    )
    for a, b in replacements:
        s = s.replace(a, b)
        
    return s


"""
Crea matriz de tokens en textos
"""

txt_inv = bdd['ID Proyecto'].tolist()
entidad = bdd['País'].tolist()
entidad.index('Brasil')
gramas_esp = gramas_esp[gramas_esp['ODS'].isnull() == False]


path_base = '/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/data/2. Textos Geneales'

# matriz = pd.read_csv('/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/data/Matriz_Clasificación_ODS.csv')

matriz = pd.DataFrame()

n = 0
for i in txt_inv:
    n+=1
    print(str(n * 100 / len(txt_inv)))
    print(n)
    
    txt = open(path_base + '/' + i , 'r')
    txt = str(normalize(txt.read())).replace('\n', ' ').split('.')
    ## Va Palabra por palabra
    """
    Define variables por ODS
    """
    pobreza = ''
    pobreza_num= 0 

    hambre = ''
    hambre_num = 0

    salud = ''
    salud_num = 0

    educacion = ''
    educacion_num = 0

    genero = ''
    genero_num = 0

    agua = ''
    agua_num = 0

    energia = ''
    energia_num = 0

    trabajo = ''
    trabajo_num = 0

    industria = ''
    industria_num = 0

    desigualdades = ''
    desigualdades_num = 0

    sostenibles = ''
    sostenibles_num = 0

    producción_consumo = ''
    producción_consumo_num = 0

    clima = ''
    clima_num = 0

    submarina = ''
    submarina_num = 0

    terrestres = ''
    terrestres_num = 0

    paz = ''
    paz_num = 0

    alianza = ''
    alianza_num = 0

    if entidad[txt_inv.index(i)] != 'Brasil':
    

        for t in range(len(txt)):
            i_split = txt[t].split()

            for grama in i_split:
                grama = str(grama).lower()            
                if grama in gramas_esp['Gramas'].tolist() and grama.isalpha() and grama.isdigit() == False:
                    
                    for id_token in range(len(gramas_esp)):
                        if grama == gramas_esp['Gramas'][id_token]:
                            
                            if 'educación de calidad' in gramas_esp['ODS'][id_token]:
                                educacion = educacion + txt[t]+ '\n'
                                educacion_num +=1

                            if 'fin de la pobreza' in gramas_esp['ODS'][id_token]:
                                pobreza = pobreza + txt[t]+'\n'
                                pobreza_num +=1

                            if 'salud y bienestar' in gramas_esp['ODS'][id_token]:
                                salud = salud + txt[t]+'\n'
                                salud_num +=1

                            if 'igualdad de género' in gramas_esp['ODS'][id_token]:
                                genero = genero + txt[t]+'\n'
                                genero_num +=1

                            if 'agua limpia y saneamiento' in gramas_esp['ODS'][id_token]:
                                agua = agua + txt[t]+'\n'
                                agua_num +=1

                            if 'energía asequible y no contaminante' in gramas_esp['ODS'][id_token]:
                                energia = energia + txt[t]+'\n'
                                energia_num +=1

                            if 'trabajo decente y crecimiento económico' in gramas_esp['ODS'][id_token]:
                                trabajo = trabajo + txt[t]+'\n'
                                trabajo_num +=1

                            if 'industria, innovación e infraestructuras' in gramas_esp['ODS'][id_token]:
                                industria = industria + txt[t]+'\n'
                                industria_num+=1

                            if 'reducción de desigualdades' in gramas_esp['ODS'][id_token]:
                                desigualdades = desigualdades + txt[t]+'\n'
                                desigualdades_num +=1

                            if 'ciudades y comunidades sostenibles' in gramas_esp['ODS'][id_token]:
                                sostenibles = sostenibles + txt[t]+'\n'
                                sostenibles_num +=1

                            if 'producción y consumo responsable' in gramas_esp['ODS'][id_token]:
                                producción_consumo = producción_consumo + txt[t]+'\n'
                                producción_consumo_num +=1

                            if 'acción por el clima' in gramas_esp['ODS'][id_token]:
                                clima = clima + txt[t]+'\n'
                                clima_num +=1

                            if 'vida submarina' in gramas_esp['ODS'][id_token]:
                                submarina = submarina + txt[t]+'\n'
                                submarina_num +=1

                            if 'vida de ecosistemas terrestres' in gramas_esp['ODS'][id_token]:
                                terrestres = terrestres + txt[t]+'\n'
                                terrestres_num +=1

                            if 'paz, justicia e instituciones sólidas' in gramas_esp['ODS'][id_token]:
                                paz = paz + txt[t]+'\n'
                                paz_num +=1

                            if 'alianza para lograr los objetivos' in gramas_esp['ODS'][id_token]:
                                alianza = alianza + txt[t]+'\n'
                                alianza_num+=1

                            if 'hambre cero' in gramas_esp['ODS'][id_token]:
                                hambre = hambre + txt[t]+'\n'
                                hambre_num+=1

                else:
                    continue

        registro = pd.DataFrame()
        registro['ID Documento'] = [i]
        registro['Fin de la pobreza'] = [pobreza_num]
        registro['TXT Fin de la pobreza'] = [pobreza]
        registro['Hambre cero'] = [hambre_num]
        registro['TXT Hambre cero'] = [hambre]
        registro['Salud y bienestar'] = [salud_num]
        registro['TXT Salud y bienestar'] = [salud]
        registro['Educación de calidad'] = [educacion_num]
        registro['TXT Educación de calidad'] = [educacion]
        registro['Igualdad de género'] = [genero_num]
        registro['TXT Igualdad de género'] = [genero]
        registro['Agua limpia y saneamiento'] = [agua_num]
        registro['TXT Agua limpia y saneamiento'] = [agua]
        registro['Energía asequible y no contaminante'] = [energia_num]
        registro['TXT Energía asequible y no contaminante'] = [energia]
        registro['Trabajo decente y crecimiento económico'] = [trabajo_num]
        registro['TXT Trabajo decente y crecimiento económico'] = [trabajo]
        registro['Industria, innovación e infraestructuras'] = [industria_num]
        registro['TXT Industria, innovación e infraestructuras'] = [industria]
        registro['Reducción de desigualdades'] = [desigualdades_num]
        registro['TXT Reducción de desigualdades'] = [desigualdades]
        registro['Ciudades y comunidades sostenibles'] = [sostenibles_num]
        registro['TXT Ciudades y comunidades sostenibles'] = [sostenibles]
        registro['Producción y consumo responsable'] = [producción_consumo_num]
        registro['TXT Producción y consumo responsable'] = [producción_consumo]
        registro['Acción por el clima'] = [clima_num]
        registro['TXT Acción por el clima'] = [clima]
        registro['Vida submarina'] = [submarina_num]
        registro['TXT Vida submarina'] = [submarina]
        registro['Vida de ecosistemas terrestres'] = [terrestres_num]
        registro['TXT Vida de ecosistemas terrestres'] = [terrestres]
        registro['Paz, justicia e instituciones sólidas'] = [paz_num]
        registro['TXT Paz, justicia e instituciones sólidas'] = [paz]
        registro['Alianza para lograr los objetivos'] = [alianza_num]
        registro['TXT Alianza para lograr los objetivos'] = [alianza]
        
        matriz = pd.concat([matriz, registro])
        matriz = matriz.reset_index(drop=True)
        matriz.to_csv('/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/data/Matriz_Clasificación_ODS.csv')
    
    else:

        for t in range(len(txt)):
            i_split = txt[t].split()

            for grama in i_split:
                grama = str(grama).lower()            
                if grama.lower() in gramas_por['Gramas'].tolist():
                    
                    for id_token in range(len(gramas_por)):
                        if grama.lower() == gramas_por['Gramas'][id_token] and grama.isalpha() and grama.isdigit() == False:
                            
                            if 'educación de calidad' in gramas_por['ODS'][id_token]:
                                educacion = educacion + txt[t]+ '\n'
                                educacion_num +=1

                            if 'fin de la pobreza' in gramas_por['ODS'][id_token]:
                                pobreza = pobreza + txt[t]+'\n'
                                pobreza_num +=1

                            if 'salud y bienestar' in gramas_por['ODS'][id_token]:
                                salud = salud + txt[t]+'\n'
                                salud_num +=1

                            if 'igualdad de género' in gramas_por['ODS'][id_token]:
                                genero = genero + txt[t]+'\n'
                                genero_num +=1

                            if 'agua limpia y saneamiento' in gramas_por['ODS'][id_token]:
                                agua = agua + txt[t]+'\n'
                                agua_num +=1

                            if 'energía asequible y no contaminante' in gramas_por['ODS'][id_token]:
                                energia = energia + txt[t]+'\n'
                                energia_num +=1

                            if 'trabajo decente y crecimiento económico' in gramas_por['ODS'][id_token]:
                                trabajo = trabajo + txt[t]+'\n'
                                trabajo_num +=1

                            if 'industria, innovación e infraestructuras' in gramas_por['ODS'][id_token]:
                                industria = industria + txt[t]+'\n'
                                industria_num+=1

                            if 'reducción de desigualdades' in gramas_por['ODS'][id_token]:
                                desigualdades = desigualdades + txt[t]+'\n'
                                desigualdades_num +=1

                            if 'ciudades y comunidades sostenibles' in gramas_por['ODS'][id_token]:
                                sostenibles = sostenibles + txt[t]+'\n'
                                sostenibles_num +=1

                            if 'producción y consumo responsable' in gramas_por['ODS'][id_token]:
                                producción_consumo = producción_consumo + txt[t]+'\n'
                                producción_consumo_num +=1

                            if 'acción por el clima' in gramas_por['ODS'][id_token]:
                                clima = clima + txt[t]+'\n'
                                clima_num +=1

                            if 'vida submarina' in gramas_por['ODS'][id_token]:
                                submarina = submarina + txt[t]+'\n'
                                submarina_num +=1

                            if 'vida de ecosistemas terrestres' in gramas_por['ODS'][id_token]:
                                terrestres = terrestres + txt[t]+'\n'
                                terrestres_num +=1

                            if 'paz, justicia e instituciones sólidas' in gramas_por['ODS'][id_token]:
                                paz = paz + txt[t]+'\n'
                                paz_num +=1

                            if 'alianza para lograr los objetivos' in gramas_por['ODS'][id_token]:
                                alianza = alianza + txt[t]+'\n'
                                alianza_num+=1

                            if 'hambre cero' in gramas_por['ODS'][id_token]:
                                hambre = hambre + txt[t]+'\n'
                                hambre_num+=1

                else:
                    continue

                        #elif gramas_esp['ODS'][id_token].lower() == 'hambre cero':

        registro = pd.DataFrame()
        registro['ID Documento'] = [i]
        registro['Fin de la pobreza'] = [pobreza_num]
        registro['TXT Fin de la pobreza'] = [pobreza]
        registro['Hambre cero'] = [hambre_num]
        registro['TXT Hambre cero'] = [hambre]
        registro['Salud y bienestar'] = [salud_num]
        registro['TXT Salud y bienestar'] = [salud]
        registro['Educación de calidad'] = [educacion_num]
        registro['TXT Educación de calidad'] = [educacion]
        registro['Igualdad de género'] = [genero_num]
        registro['TXT Igualdad de género'] = [genero]
        registro['Agua limpia y saneamiento'] = [agua_num]
        registro['TXT Agua limpia y saneamiento'] = [agua]
        registro['Energía asequible y no contaminante'] = [energia_num]
        registro['TXT Energía asequible y no contaminante'] = [energia]
        registro['Trabajo decente y crecimiento económico'] = [trabajo_num]
        registro['TXT Trabajo decente y crecimiento económico'] = [trabajo]
        registro['Industria, innovación e infraestructuras'] = [industria_num]
        registro['TXT Industria, innovación e infraestructuras'] = [industria]
        registro['Reducción de desigualdades'] = [desigualdades_num]
        registro['TXT Reducción de desigualdades'] = [desigualdades]
        registro['Ciudades y comunidades sostenibles'] = [sostenibles_num]
        registro['TXT Ciudades y comunidades sostenibles'] = [sostenibles]
        registro['Producción y consumo responsable'] = [producción_consumo_num]
        registro['TXT Producción y consumo responsable'] = [producción_consumo]
        registro['Acción por el clima'] = [clima_num]
        registro['TXT Acción por el clima'] = [clima]
        registro['Vida submarina'] = [submarina_num]
        registro['TXT Vida submarina'] = [submarina]
        registro['Vida de ecosistemas terrestres'] = [terrestres_num]
        registro['TXT Vida de ecosistemas terrestres'] = [terrestres]
        registro['Paz, justicia e instituciones sólidas'] = [paz_num]
        registro['TXT Paz, justicia e instituciones sólidas'] = [paz]
        registro['Alianza para lograr los objetivos'] = [alianza_num]
        registro['TXT Alianza para lograr los objetivos'] = [alianza]
        
        matriz = pd.concat([matriz, registro])
        matriz = matriz.reset_index(drop=True)
        matriz.to_csv('/home/duban/Workspace/Analisis-Scrapping-Convocatorias-Clacso/data/Matriz_Clasificación_ODS.csv')

