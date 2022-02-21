import random
import math
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

    datos = []
    iterations = 1000
    results = []

    for i in range(5, 10):
        datos = generador(i)
        with open("Datos.txt", "a") as file:
            titulor = "longitud = " + str(i) + "\n"
            file.write(titulor)
            cont = len(datos)
            for key in datos:
                cont -= 1
                ciudad = key
                if (cont != 0):
                    filas = str(ciudad) + "," + "\n" + "\n"
                else:
                    filas = str(ciudad) + "\n" + "\n"
                file.write(filas)

        distances = []
        best_dist = math.inf
        worst_dist = 0
        sum_dist = 0
        aux_distances = []
        aux_best_dist = math.inf
        aux_worst_dist = 0
        aux_sum_dist = 0

        for j in range(iterations):
            #Calls the HillClimbing algorithm
            s = hillClimbing(datos)
            distances.append(s[1])
            sum_dist += s[1]
            if (s[1] < best_dist):
                best_dist = s[1]
            elif (s[1] > worst_dist):
                worst_dist = s[1]
            print("hola1")
            #Calls the improved version using the same data
            e = hillClimbingImproved(datos)
            aux_distances.append(e[1])
            aux_sum_dist += e[1]
            if (e[1] < aux_best_dist):
                aux_best_dist = e[1]
            elif (e[1] > aux_worst_dist):
                aux_worst_dist = e[1]

            print("hola2")
        optimal_occurrences = distances.count(best_dist)
        aux_optimal_occurrences = aux_distances.count(aux_best_dist)
        results.append([i, best_dist, worst_dist, sum_dist / iterations, optimal_occurrences, optimal_occurrences / iterations, aux_best_dist, aux_worst_dist, aux_sum_dist / iterations, aux_optimal_occurrences, aux_optimal_occurrences / iterations])

    #Export data to .csv file
    with open("HillClimbingResults.csv", "w") as file:
        file.write(",".join(["N", "Best distance", "Worst Distance", "Average Distance", "Optimal occurrences", "Optimal average", "Best UP distance", "Worst UP distance", "Average UP Distance", "Optimal UP ocurrences", "Optimal UP average\n"]))
        for res in results:
            file.write(",".join([str(s) for s in res]) + "\n")


if __name__ == "__main__":
    main()
