import random
import math
import time
from TSPGenerator import generador

#evaluamos la solucion
def evaluarSolucion(datos, solucion):
    longitud = 0
    for i in range(len(solucion)):
        longitud += datos[solucion[i - 1]][solucion[i]]
    return longitud

def obtenerMejorVecino(solucion, datos):
    ##Obtención de los vecinos
    vecinos = []
    l=len(solucion)
    for i in range(l):
        for j in range(i+1, l):
            n = solucion.copy()
            n[i] = solucion[j]
            n[j] = solucion[i]
            vecinos.append(n)

    ##Obtención del mejor vecino
    mejorVecino = vecinos[0]
    mejorLongitud = evaluarSolucion(datos, mejorVecino)
    for vecino in vecinos:
        longitud = evaluarSolucion(datos, vecino)
        if longitud < mejorLongitud:
            mejorLongitud = longitud
            mejorVecino = vecino
    return mejorVecino, mejorLongitud


def hillClimbingImproved(datos):
    l = len(datos)
    longitud_min = float('inf')
    ciudades = list(range(l))
    solucion = []
    for i in range(l):
        x = random.randint(0, len(ciudades) - 1)
        ciudad = ciudades[x]
        solucion.append(ciudad)
        ciudades.remove(ciudad)
    longitud = evaluarSolucion(datos, solucion)

    vecino = obtenerMejorVecino(solucion, datos)
    cont = 1
    while vecino[1] < longitud:
        solucion = vecino[0]
        longitud = vecino[1]
        vecino = obtenerMejorVecino(solucion, datos)
        cont = cont + 1
    # So far the Hill Climbing algorithm remains

    # Now the improvement begins
    while cont + 2 < (len(datos) - 1):
        # We obtain a permutation of the solution
        aux_cont = cont
        aux_cont_2 = 0
        nueva_solucion = []

        for y in range(l):
            if aux_cont < (len(datos) - 1):
                nueva_solucion.append(solucion[aux_cont])
                aux_cont += 1
            else:
                nueva_solucion.append(solucion[aux_cont_2])
                aux_cont_2 += 1

        aux_longitud = evaluarSolucion(datos, nueva_solucion)

        # We compare if the new solution is better than the one we already had
        if aux_longitud < longitud_min:
            cont = cont + 2
            aux_vecino = obtenerMejorVecino(nueva_solucion, datos)

            while aux_vecino[1] < aux_longitud:
                nueva_solucion = aux_vecino[0]
                aux_longitud = aux_vecino[1]
                aux_vecino = obtenerMejorVecino(nueva_solucion, datos)
                cont += 1
            longitud_min = aux_longitud

        cont += 1

    # Returns best solution found
    if longitud_min < longitud:
        return nueva_solucion, aux_longitud
    else:
        return solucion, longitud



#algoritmo Hill Climbing simple sin mejoras
def hillClimbing(datos):
    l=len(datos)
    ##Creamos una solucion aleatoria
    ciudades = list(range(l))
    solucion = []
    for i in range(l):
        ciudad = ciudades[random.randint(0, len(ciudades) - 1)]
        solucion.append(ciudad)
        ciudades.remove(ciudad)
    longitud = evaluarSolucion(datos, solucion)

    ##Obtenemos el mejor vecino hasta que no haya vecinos mejores
    vecino = obtenerMejorVecino(solucion, datos)
    while vecino[1] < longitud:
        solucion = vecino[0]
        longitud = vecino[1]

        vecino = obtenerMejorVecino(solucion, datos)

    return solucion, longitud


def main():


    iterations = 1000
    results = []
    aux_dataset = []

    dataset = []
    with open ("Datos.txt", "r") as f:
        for i in range(5, 10):
            linea = f.readline()
            datos = []
            for j in range(0,i):
                f_contents = f.readline()
                f_contents = f_contents[1:-3]
                numbers = [int(n) for n in f_contents.split(", ")]
                datos.append(numbers)


            distances, aux_distances = [], []
            best_dist, aux_best_dist = math.inf, math.inf
            worst_dist, aux_worst_dist, aux_sum_dist, sum_dist, sum_time, aux_sum_time = 0,0,0,0,0,0


            for j in range(iterations):
                #Calls the HillClimbing algorithm
                start_time = time.time()
                s = hillClimbing(datos)
                end_time = time.time()
                sum_time += (end_time - start_time)
                distances.append(s[1])
                sum_dist += s[1]
                if (s[1] < best_dist):
                    best_dist = s[1]
                elif (s[1] > worst_dist):
                    worst_dist = s[1]

                #Calls the improved version using the same data
                aux_start_time = time.time()
                e = hillClimbingImproved(datos)
                aux_end_time = time.time()
                aux_sum_time += (aux_end_time - aux_start_time)
                aux_distances.append(e[1])
                aux_sum_dist += e[1]
                if (e[1] < aux_best_dist):
                    aux_best_dist = e[1]
                elif (e[1] > aux_worst_dist):
                    aux_worst_dist = e[1]


            optimal_occurrences = distances.count(best_dist)
            aux_optimal_occurrences = aux_distances.count(aux_best_dist)
            results.append([i, best_dist, worst_dist, sum_dist / iterations, optimal_occurrences, aux_best_dist, aux_worst_dist, aux_sum_dist / iterations, aux_optimal_occurrences, sum_time*1000, aux_sum_time * 1000])

    #Export data to .csv file
    with open("HillClimbingResults.csv", "w") as file:
        file.write(",".join(["Nodos", "Mejor Distancia", "Peor Distancia", "Distancia Media", "Frec. mejor distancia", "Mejor distancia (mejorada)", "Peor distancia (mejorada)", "Distancia Media (mejorada)", "Frec. mejor distancia (mejorada)", "Tiempo medio", "Tiempo medio (mejorado)\n"]))
        for res in results:
            file.write(",".join([str(s) for s in res]) + "\n")




if __name__ == "__main__":
    main()