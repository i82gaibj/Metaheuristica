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


def hillClimbingMejorada(datos):
    l = len(datos)
    Minlongitud = float('inf')
    ciudades = list(range(l))
    solucion = []
    for i in range(l):
        x = random.randint(0, len(ciudades) - 1)
        ciudad = ciudades[x]
        solucion.append(ciudad)
        ciudades.remove(ciudad)
    longitud = evaluarSolucion(datos, solucion)

    vecino = obtenerMejorVecino(solucion, datos)
    contador = 1
    while vecino[1] < longitud:
        solucion = vecino[0]
        longitud = vecino[1]
        vecino = obtenerMejorVecino(solucion, datos)
        contador = contador + 1
    # So far the Hill Climbing algorithm remains

    # Now the improvement begins
    while contador + 2 < (len(datos) - 1):
        # We obtain a permutation of the solution
        aux = contador
        aux1 = 0
        Newsolucion = []

        for y in range(l):
            if aux < (len(datos) - 1):
                Newsolucion.append(solucion[aux])
                aux = aux + 1
            else:
                Newsolucion.append(solucion[aux1])
                aux1 = aux1 + 1

        Auxlongitud = evaluarSolucion(datos, Newsolucion)

        # We compare if the new solution is better than the one we already had
        if Auxlongitud < Minlongitud:
            Auxvecino = obtenerMejorVecino(Newsolucion, datos)
            contador = contador + 2
            while Auxvecino[1] < Auxlongitud:
                Newsolucion = Auxvecino[0]
                Auxlongitud = Auxvecino[1]
                Auxvecino = obtenerMejorVecino(Newsolucion, datos)
                contador = contador + 1
            Minlongitud = Auxlongitud

        contador = contador + 1

    # Returns best solution found
    if Minlongitud < longitud:
        return Newsolucion, Auxlongitud
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
    for i in range(5, 15):
        datos = generador(i)
        with open("Datos.txt", "a") as file:
            titulor = "ciudad, longitud\n"
            file.write(titulor)
            for key in datos:
                ciudad = key
                filas = str(ciudad) + "," + "\n"
                file.write(filas)
        distances = []
        bestDist = math.inf
        worstDist = 0
        sumDist = 0
        Auxdistances = []
        AuxbestDist = math.inf
        AuxworstDist = 0
        AuxsumDist = 0
    		
        
        for j in range(iterations):
            #Calls the HillClimbing algorithm
            s = hillClimbing(datos)
            distances.append(s[1])
            sumDist += s[1]
            if (s[1] < bestDist):
                bestDist = s[1]
            elif (s[1] > worstDist):
                worstDist = s[1]
            print("hola1")
            #Calls the improved version using the same data
            e = hillClimbingMejorada(datos)
            Auxdistances.append(e[1])
            AuxsumDist += e[1]
            if (e[1] < AuxbestDist):
                AuxbestDist = e[1]
            elif (e[1] > AuxworstDist):
                AuxworstDist = e[1]

            print("hola2")
        optimalOccurrences = distances.count(bestDist)
        AuxoptimalOccurrences = Auxdistances.count(AuxbestDist)
        results.append([i, bestDist, worstDist, sumDist / iterations, optimalOccurrences, optimalOccurrences / iterations, AuxbestDist, AuxworstDist, AuxsumDist / iterations, AuxoptimalOccurrences, AuxoptimalOccurrences / iterations])
	
    #Export data to .csv file
    with open("HillClimbingResults.csv", "w") as file:
        file.write(",".join(["N", "Best distance", "Worst Distance", "Average Distance", "Optimal occurrences", "Optimal average", "Best UP distance", "Worst UP distance", "Average UP Distance", "Optimal UP ocurrences", "Optimal UP average\n"]))
        for res in results:
            file.write(",".join([str(e) for e in res]) + "\n")


if __name__ == "__main__":
    main()
