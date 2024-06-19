# Vector de ciudades
CIUDADES = ["Alicante","Barcelona","Bilbao","Caceres","Cadiz","Cordoba",
"Coruna","Girona","Huelva","Leon","Madrid","Murcia","Oviedo",
"Pamplona","Donostia","Sevilla","Tarragona","Toledo","Valencia",
"Zaragoza"]
# Matriz de distancias
M = [
[0,515,817,675,688,525,1031,615,703,855,422,75,873,673,766,609,417,411,166,498],
[515,0,620,918,1284,908,1118,100,1140,784,621,590,902,437,529,1046,98,692,349,296],
[817,620,0,605,1058,795,644,720,939,359,395,796,304,159,119,993,555,466,633,324],
[675,918,605,0,369,319,683,1018,323,407,297,654,525,650,679,264,831,264,636,622],
[688,1284,1058,369,0,263,1072,1384,219,796,663,613,914,1070,1132,125,1059,583,808,988],
[525,908,795,319,263,0,995,1008,232,733,400,444,851,807,869,138,796,320,545,725],
[1031,1118,644,683,1072,995,0,1218,1006,334,609,1010,340,738,763,947,1064,675,961,833],
[615,100,720,1018,1384,1008,1218,0,1240,884,721,690,1002,537,629,1146,198,792,449,396],
[703,1140,939,323,219,232,1006,1240,0,730,632,628,821,1039,1101,94,1029,552,791,957],
[855,784,359,407,796,733,334,884,730,0,333,734,118,404,433,671,719,392,685,488],
[422,621,395,297,663,400,609,721,632,333,0,401,451,407,469,538,534,71,352,325],
[75,590,796,654,613,444,1010,690,628,734,401,0,852,714,807,534,492,390,241,539],
[873,902,304,525,914,851,340,1002,821,118,451,852,0,463,423,789,835,510,803,604],
[673,437,159,650,1070,807,738,537,1039,404,407,714,463,0,92,945,372,478,501,175],
[766,529,119,679,1132,869,763,629,1101,433,469,807,423,92,0,1007,464,540,594,268],
[609,1046,993,264,125,138,947,1146,94,671,538,534,789,945,1007,0,949,458,697,863],
[417,98,555,831,1059,796,1064,198,1029,719,534,492,835,372,464,949,0,605,251,231],
[411,692,466,264,583,320,675,792,552,392,71,390,510,478,540,458,605,0,372,396],
[166,349,633,636,808,545,961,449,791,685,352,241,803,501,594,697,251,372,0,326],
[498,296,324,622,988,725,833,396,957,488,325,539,604,175,268,863,231,396,326,0]
]

############### DATOS DE ENTRADA MÁS PEQUEÑOS ###############
# CIUDADES = ["Alicante", "Barcelona", "Madrid", "Sevilla", "Valencia"]


# M = [
#     [0, 515, 422, 766, 417],   
#     [515, 0, 581, 1046, 692], 
#     [422, 581, 0, 531, 352],
#     [766, 1046, 531, 0, 539],
#     [417, 692, 352, 539, 0]  
# ]
###############  ###############



TAM_POBLACION = 10

import random
import sys
import time
from pwn import *




####################################### OBTENCION DE LA POBLACION INICIAL #######################################


def sacar_poblacion(ciudad_inicial):

    # Definir la función de inicialización de un individuo
    def inicializar_individuo():

        # Generar una permutación aleatoria de las ciudades, por ejemplo excluyendo Pamplona
        ciudades_sin_ciudad_inicial = CIUDADES[:]
        ciudades_sin_ciudad_inicial.remove(ciudad_inicial)
        ruta_sin_ciudad_inicial = random.sample(ciudades_sin_ciudad_inicial, len(CIUDADES) - 1)

        # Agregar la ciudad inicial al principio y al final de la ruta
        ruta_completa = [ciudad_inicial] + ruta_sin_ciudad_inicial + [ciudad_inicial]
        return ruta_completa

    poblacion = []
    for _ in range(TAM_POBLACION):
        poblacion.append(inicializar_individuo())

    return poblacion


####################################### OBTENCION DEL FITNESS #######################################

def calcular_costo_ruta(poblacion, ciudad_inicial):
    costes_poblacion = []
    for i in range(len(poblacion)):
        ruta = poblacion[i]
        costo_total = 0

        # Iterar sobre cada par de ciudades en la ruta
        for i in range(len(ruta) - 1):
            ciudad_actual = ruta[i]
            siguiente_ciudad = ruta[i + 1]

            # Obtener el costo de viajar de la ciudad actual a la siguiente ciudad
            costo_viaje = M[CIUDADES.index(ciudad_actual)][CIUDADES.index(siguiente_ciudad)]
            costo_total += costo_viaje

        # Sumar el costo de regresar a la ciudad inicial desde la última ciudad
        costo_total += M[CIUDADES.index(ruta[-1])][CIUDADES.index(ciudad_inicial)]
        costes_poblacion.append(1/costo_total)
    return costes_poblacion




####################################### METODOS DE OBTENCIÓN DE PADRES ############################################################

#-=-=-=-=-=-=-# METODO DEL TORENO #-=-=-=-=-=-=-#
def seleccion_por_torneo(poblacion, k):
    seleccionados = random.sample(poblacion, k)
    ganador = min(seleccionados)
    return poblacion.index(ganador)

#-=-=-=-=-=-=-# METODO DE LA RULETA #-=-=-=-=-=-=-#
def seleccion_por_ruleta(poblacion):
    ganador = random.choice(poblacion)
    return poblacion.index(ganador)




####################################### CRUZAMINETOS ############################################################

#==============================# CRUZAMIENTO POR CICLOS #==============================#

def cruzamietno_por_ciclos(padre1, padre2, ciudad_inicial):
    hijo = [''] * len(padre1)
    hijo[0] = ciudad_inicial
    hijo[-1] = ciudad_inicial

    turno = 1
    ultimo_indice_de_inicio = 1

    while (cruzamiento_incompleto(hijo)):
        if (turno == 1):
            while (ya_existe_un_elemento_en_el_siguiente_indice_de_inicio(hijo, ultimo_indice_de_inicio)):
                ultimo_indice_de_inicio+=1

            hijo[ultimo_indice_de_inicio] = padre1[ultimo_indice_de_inicio]
            indice_del_elemento_a_examinar = ultimo_indice_de_inicio

            while (1):
                elemento_a_examinar = padre2[indice_del_elemento_a_examinar]
                if (ya_existe_el_elemento_en_el_hijo(hijo, elemento_a_examinar)):
                    turno = 2
                    break
                
                indice_del_elemento_a_examinar = padre1.index(elemento_a_examinar)
                hijo[indice_del_elemento_a_examinar] = elemento_a_examinar


        elif (turno == 2):
            while (ya_existe_un_elemento_en_el_siguiente_indice_de_inicio(hijo, ultimo_indice_de_inicio)):
                ultimo_indice_de_inicio+=1

            hijo[ultimo_indice_de_inicio] = padre2[ultimo_indice_de_inicio]
            indice_del_elemento_a_examinar = ultimo_indice_de_inicio

            while (1):
                elemento_a_examinar = padre1[indice_del_elemento_a_examinar]
                if (ya_existe_el_elemento_en_el_hijo(hijo, elemento_a_examinar)):
                    turno = 1
                    break
                
                indice_del_elemento_a_examinar = padre2.index(elemento_a_examinar)
                hijo[indice_del_elemento_a_examinar] = elemento_a_examinar


        else:
            print(f"[!] Se ha produdciod un error en la variable de turno = {turno}")
            sys.exit(1)

    return hijo



def cruzamiento_incompleto(hijo):
    for i in hijo:
        if (i == ''):
            return True
    return False

def ya_existe_el_elemento_en_el_hijo(hijo, elemento):
    return elemento in hijo
    
def ya_existe_un_elemento_en_el_siguiente_indice_de_inicio(hijo, indice):
    return hijo[indice] != ''
    



#==============================# CRUZAMIENTO PARCIALMENTE MAPEADO #==============================#

def cruzamineto_parcialmente_mapeado(padre1, padre2, ciudad_inicial):
    hijo = [''] * len(padre1)
    hijo[0] = ciudad_inicial
    hijo[-1] = ciudad_inicial

    inicio_zona_confort = random.randint(1, len(hijo)-2)
    fin_zona_confort = random.randint(1, len(hijo)-2)

    rellenar_zona_confort_con_padre1(hijo, padre1, inicio_zona_confort, fin_zona_confort)

    for i in range(inicio_zona_confort, fin_zona_confort):
        elemento_a_colocar = padre2[i]

        if (ya_existe_el_elemento_en_el_hijo(hijo, elemento_a_colocar)):
            continue

        indice_del_espejo_del_elemento_a_colocar = inicio_zona_confort
        espejo_del_elemento_a_colocar = padre1[i]
        indice_del_espejo_del_elemento_a_colocar = padre2.index(espejo_del_elemento_a_colocar)

        while (ya_hay_un_elemento_en_el_indice_del_hijo(hijo, indice_del_espejo_del_elemento_a_colocar)):
            espejo_del_elemento_a_colocar = padre1[indice_del_espejo_del_elemento_a_colocar]
            indice_del_espejo_del_elemento_a_colocar = padre2.index(espejo_del_elemento_a_colocar)
        
        hijo[indice_del_espejo_del_elemento_a_colocar] = elemento_a_colocar

    rellenar_restante_con_padre2(hijo, padre2)

    return hijo


def ya_hay_un_elemento_en_el_indice_del_hijo(hijo, indice_del_espejo_del_elemento_a_colocar):
    return (hijo[indice_del_espejo_del_elemento_a_colocar] != '')

def rellenar_zona_confort_con_padre1(hijo, padre1, inicio, fin):
    for i in range(inicio, fin):
        hijo[i] = padre1[i]

def rellenar_restante_con_padre2(hijo, padre2):
    for i in range(len(hijo)):
        if (hijo[i] == ''):
            hijo[i] = padre2[i]



####################################### MUTACION #######################################

#-=-=-=-=-=-=-# MUTACION POR INTERCAMBIO #-=-=-=-=-=-=-#
def mutacion_por_intecambio(hijo):
    mutacion = hijo[:]

    pos1 = random.randint(1, len(hijo)-2)
    pos2 = random.randint(1, len(hijo)-2)

    mutacion[pos1], mutacion[pos2] = mutacion[pos2], mutacion[pos1] 

    return mutacion


#-=-=-=-=-=-=-# MUTACION POR INSERCION #-=-=-=-=-=-=-#
def mutacion_por_insercion(hijo):
    mutacion = hijo[:]

    pos1 = random.randint(1, len(hijo)-2)
    pos2 = random.randint(1, len(hijo)-2)

    while (pos1 == pos2):
        pos1 = random.randint(1, len(hijo)-2)
        pos2 = random.randint(1, len(hijo)-2)

    if pos2 < pos1:
        pos1, pos2 = pos2, pos1

    if (pos1+1 == pos2):
        return mutacion
    
    mutacion[pos1+1] = mutacion[pos2]
    for i in range(pos1+1, pos2):
        mutacion[i+1] = hijo[i]

    return mutacion


#-=-=-=-=-=-=-# MUTACION POR SACUDIDA #-=-=-=-=-=-=-#
def mutacion_por_sacudida(hijo):
    mutacion = hijo[:]

    pos1 = random.randint(1, len(hijo)-2)
    pos2 = random.randint(1, len(hijo)-2)

    while (pos1 == pos2):
        pos1 = random.randint(1, len(hijo)-2)
        pos2 = random.randint(1, len(hijo)-2)

    if pos2 < pos1:
        pos1, pos2 = pos2, pos1

    numeros_aleatorios = []
    while(len(numeros_aleatorios) != (pos2+1-pos1)):

        numero_aleatorio = random.randint(pos1, pos2)
        while(numero_aleatorio in numeros_aleatorios):
            numero_aleatorio = random.randint(pos1, pos2)

        numeros_aleatorios.append(numero_aleatorio)

    for i in range(pos1, pos2+1):
        mutacion[i] = hijo[numeros_aleatorios[i-pos1]]

    return mutacion


####################################### SELECCION DE SUPERVIVIENTES #######################################

def seleccion_reemplazando_basando_en_el_fitness(poblacion, hijo1_mutado, hijo2_mutado, ciudad_inicial):
    poblacion.append(hijo1_mutado)
    poblacion.append(hijo2_mutado)


    costes_nueva_poblacion = calcular_costo_ruta(poblacion, ciudad_inicial)

    for _ in range(2):
        individuo_a_eliminar = min(costes_nueva_poblacion)
        indice_individuo_a_eliminar = costes_nueva_poblacion.index(individuo_a_eliminar)

        costes_nueva_poblacion.pop(indice_individuo_a_eliminar)
        poblacion.pop(indice_individuo_a_eliminar)

    return poblacion




####################################### FUNCIONES AUXILIARES #######################################

def mostrar_resultados(poblacion, ciudad_inicial):

    costo_mejor_poblacion = calcular_costo_ruta(poblacion, ciudad_inicial)
    costo_mejor_individuo = max(costo_mejor_poblacion)
    indice_mejor_individuo_costo = costo_mejor_poblacion.index(costo_mejor_individuo)
    mejor_ruta = poblacion[indice_mejor_individuo_costo]

    costo_mejor_individuo = round(costo_mejor_individuo, 7)
    return int(1/costo_mejor_individuo), costo_mejor_individuo, mejor_ruta


def eleccion_de_mejores_hijos(mutaciones, ciudad_inicial):

    costes_de_mutaciones = calcular_costo_ruta(mutaciones, ciudad_inicial)

    coste_hijo1 = max(costes_de_mutaciones)
    indice_hijo1 = costes_de_mutaciones.index(coste_hijo1)
    hijo1 = mutaciones[indice_hijo1]
    costes_de_mutaciones.remove(coste_hijo1)

    coste_hijo2 = max(costes_de_mutaciones)
    indice_hijo2 = costes_de_mutaciones.index(coste_hijo2)

    if indice_hijo2 >= indice_hijo1:
        indice_hijo2+=1

    hijo2 = mutaciones[indice_hijo2]

    
    return hijo1, hijo2

def obtener_indices_ciudades(lista_ciudades):
    indices = []
    for ciudad in lista_ciudades:
        if ciudad in CIUDADES:
            indice = CIUDADES.index(ciudad)
            indices.append(indice)
        else:
            print(f"La ciudad '{ciudad}' no se encuentra en la lista de ciudades.")
            indices.append(None)  # Si la ciudad no está en la lista, se añade None al resultado
    return indices


def mostrar_titulo():
    print(' ____            _     _                            _      _         _        _             _       ')
    print('|  _ \ _ __ ___ | |__ | | ___ _ __ ___   __ _    __| | ___| | __   _(_) __ _ (_) __ _ _ __ | |_ ___ ')
    print("| |_) | '__/ _ \| '_ \| |/ _ \ '_ ` _ \ / _` |  / _` |/ _ \ | \ \ / / |/ _` || |/ _` | '_ \| __/ _ \ ")
    print('|  __/| | | (_) | |_) | |  __/ | | | | | (_| | | (_| |  __/ |  \ V /| | (_| || | (_| | | | | ||  __/')
    print('|_|   |_|  \___/|_.__/|_|\___|_| |_| |_|\__,_|  \__,_|\___|_|   \_/ |_|\__,_|/ |\__,_|_| |_|\__\___|')
    print('                                                                           |__/                     ')

    print('\n\n╔═╗┌─┐┬─┐  ╔═╗┌┐┌┌┬┐┌─┐┬─┐  ╔╦╗┌─┐┌┐┌┬─┐┌─┐┌─┐┬  ')
    print('╠═╝│ │├┬┘  ╠═╣│││ ││├┤ ├┬┘  ║║║│ ││││├┬┘├┤ ├─┤│  ')
    print('╩  └─┘┴└─  ╩ ╩┘└┘─┴┘└─┘┴└─  ╩ ╩└─┘┘└┘┴└─└─┘┴ ┴┴─┘')
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n')



####################################### MAIN ############################################################

def main():

    mostrar_titulo()

    ciudad_inicial=""
    k = 0
    iteraciones = 0

    while (ciudad_inicial not in CIUDADES):
        ciudad_inicial = str(input(f'\t[+] Introduce la ciudad de inicio y fin:    '))

    while (k < 1 or k > TAM_POBLACION):
        k = int(input(f"\t[+] Introduce un valor para 'K' mayor que 0 y menor que {TAM_POBLACION}:    "))
    
    while (iteraciones <= 0):
        iteraciones = int(input(f"\t[+] Introduce la cantidad de iteraciones que desas probar:    "))

    print("\n\n")

    p1 = log.progress("Problema del viajante")

    msg = f"Iniciando algoritmo genetico para: \n\t[+] Ciudad inicial: {ciudad_inicial} \n\t[+] k: {k} \n\t[+] Iteraciones: {iteraciones}"
    p1.status(msg)
    time.sleep(8)


    poblacion = sacar_poblacion(ciudad_inicial)

    for i in range(iteraciones):

        costes_poblacion = calcular_costo_ruta(poblacion, ciudad_inicial)

        mutaciones = []


    ############ METODO DEL TORNEO ############
        indice_ganador_torneo1 = seleccion_por_torneo(costes_poblacion, k)
        indice_ganador_torneo2 = seleccion_por_torneo(costes_poblacion, k)

        hijo_torneo_ciclos1 = cruzamietno_por_ciclos(poblacion[indice_ganador_torneo1], poblacion[indice_ganador_torneo2], ciudad_inicial)
        hijo_torneo_ciclos2 = cruzamietno_por_ciclos(poblacion[indice_ganador_torneo2], poblacion[indice_ganador_torneo1], ciudad_inicial)


        mutaciones.append(mutacion_por_intecambio(hijo_torneo_ciclos1))
        mutaciones.append(mutacion_por_intecambio(hijo_torneo_ciclos2))

        mutaciones.append(mutacion_por_insercion(hijo_torneo_ciclos1))
        mutaciones.append(mutacion_por_insercion(hijo_torneo_ciclos2))

        mutaciones.append(mutacion_por_sacudida(hijo_torneo_ciclos1)) 
        mutaciones.append(mutacion_por_sacudida(hijo_torneo_ciclos2)) 



        hijo_torneo_mapeado1 = cruzamineto_parcialmente_mapeado(poblacion[indice_ganador_torneo1], poblacion[indice_ganador_torneo2], ciudad_inicial)
        hijo_torneo_mapeado2 = cruzamineto_parcialmente_mapeado(poblacion[indice_ganador_torneo2], poblacion[indice_ganador_torneo1], ciudad_inicial)

        
        mutaciones.append(mutacion_por_intecambio(hijo_torneo_mapeado1))
        mutaciones.append(mutacion_por_intecambio(hijo_torneo_mapeado2))

        mutaciones.append(mutacion_por_insercion(hijo_torneo_mapeado1))
        mutaciones.append(mutacion_por_insercion(hijo_torneo_mapeado2))

        mutaciones.append(mutacion_por_sacudida(hijo_torneo_mapeado1)) 
        mutaciones.append(mutacion_por_sacudida(hijo_torneo_mapeado2)) 
    ###### FIN METODO DEL TORNEO ######


    ############ METODO DE LA RULETA ############
        indice_ganador_ruleta1 = seleccion_por_ruleta(costes_poblacion)
        indice_ganador_ruleta2 = seleccion_por_ruleta(costes_poblacion)

        hijo_torneo_ciclos1 = cruzamietno_por_ciclos(poblacion[indice_ganador_ruleta1], poblacion[indice_ganador_ruleta2], ciudad_inicial)
        hijo_torneo_ciclos2 = cruzamietno_por_ciclos(poblacion[indice_ganador_ruleta2], poblacion[indice_ganador_ruleta1], ciudad_inicial)

        
        mutaciones.append(mutacion_por_intecambio(hijo_torneo_ciclos1))
        mutaciones.append(mutacion_por_intecambio(hijo_torneo_ciclos2))

        mutaciones.append(mutacion_por_insercion(hijo_torneo_ciclos1))
        mutaciones.append(mutacion_por_insercion(hijo_torneo_ciclos2))

        mutaciones.append(mutacion_por_sacudida(hijo_torneo_ciclos1)) 
        mutaciones.append(mutacion_por_sacudida(hijo_torneo_ciclos2)) 



        hijo_torneo_mapeado1 = cruzamineto_parcialmente_mapeado(poblacion[indice_ganador_ruleta1], poblacion[indice_ganador_ruleta2], ciudad_inicial)
        hijo_torneo_mapeado2 = cruzamineto_parcialmente_mapeado(poblacion[indice_ganador_ruleta2], poblacion[indice_ganador_ruleta1], ciudad_inicial)

        
        mutaciones.append(mutacion_por_intecambio(hijo_torneo_mapeado1))
        mutaciones.append(mutacion_por_intecambio(hijo_torneo_mapeado2))

        mutaciones.append(mutacion_por_insercion(hijo_torneo_mapeado1))
        mutaciones.append(mutacion_por_insercion(hijo_torneo_mapeado2))

        mutaciones.append(mutacion_por_sacudida(hijo_torneo_mapeado1)) 
        mutaciones.append(mutacion_por_sacudida(hijo_torneo_mapeado2)) 
    ###### FIN METODO DE LA RULETA ######


        mejor_hijo1, mejor_hijo2 = eleccion_de_mejores_hijos(mutaciones, ciudad_inicial)


        poblacion = seleccion_reemplazando_basando_en_el_fitness(poblacion, mejor_hijo1, mejor_hijo2, ciudad_inicial)


        coste_mejor_ruta, fitness_mejor_ruta, mejor_ruta = mostrar_resultados(poblacion, ciudad_inicial)

        msg = f"[{i}/{iteraciones}] -> coste={coste_mejor_ruta}, fitnes={fitness_mejor_ruta}. Ruta examinada:\n{mejor_ruta} "
        p1.status(msg)


    msg = f"Mejor ruta con coste={coste_mejor_ruta} y fitness={fitness_mejor_ruta} es:\n{mejor_ruta}\n\n"
    p1.success(msg)
    


if __name__ == "__main__":
    main()

