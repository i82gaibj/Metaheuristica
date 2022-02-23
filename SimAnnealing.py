import random
import math
import time
import os


def evaluarSolucion(datos, solucion):
    longitud = 0
    for i in range(len(solucion)):
        longitud += datos[solucion[i - 1]][solucion[i]]
    return longitud

def obtenerVecino(solucion, datos):
    ##Obtención de los vecinos
    vecinos = []
    l=len(solucion)
    for i in range(l):
        for j in range(i+1, l):
            n = solucion.copy()
            n[i] = solucion[j]
            n[j] = solucion[i]
            vecinos.append(n)

    ##Obtengo un vecino aleatorio
    vecino=vecinos[random.randint(0, len(vecinos) - 1)]
    longitud = evaluarSolucion(datos, vecino)

    return vecino, longitud

def simAnnealing(datos,t0,maxUnImprovement):
    t=t0
    l=len(datos)
    ##Creamos una solucion aleatoria
    ciudades = list(range(l))
    solucion = []
    for i in range(l):
        ciudad = ciudades[random.randint(0, len(ciudades) - 1)]
        solucion.append(ciudad)
        ciudades.remove(ciudad)
    longitud = evaluarSolucion(datos, solucion)
    #print("Longitud de la ruta: ", longitud)
    #print("Temperatura: ", t)

    it=0
    unimprovement = 0

    bestSol = solucion
    bestLen = longitud
    while t > 0.05 and it < 5000:
        ##Obtenemos un vecino al azar
        vecino = obtenerVecino(solucion, datos)
        incremento = vecino[1]-longitud

        if incremento < 0:
            longitud = vecino[1]
            solucion = vecino[0]
            unimprovement = 0

            if longitud < bestLen:
                bestSol = solucion
                bestLen = longitud

        elif random.random() < math.exp(-abs(incremento) / t):
            longitud = vecino[1]
            solucion = vecino[0]
            unimprovement = 0

            if longitud < bestLen:
                bestSol = solucion
                bestLen = longitud
        else:
            unimprovement += 1

        it+=1
        t=0.99*t

        #Different annealing functions (not compatible with reheating unless we reset it)
        #t = logAnnealing(t0, alpha, it)
        #t = geometricAnnealing(t0, alpha, it)
        #t = linearAnnealing(t0, alpha, it)


        #Reheating
        #https://academicjournals.org/journal/IJPS/article-full-text-pdf/D6CF1F025890
        if unimprovement >= maxUnImprovement:
            unimprovement = 0
            t = t0

        # My own approach to reheating, didn't work well
        #if t/t0 < 0.1 and random.random() < 0.01:
        #    print("reheat " + str(t) + " " + str(2*t))
        #    t *= 5

        #print("Longitud de la ruta: ", longitud)
        #print("Temperatura: ", t)
    return bestSol, bestLen

def simAnnealing2(datos,t0):
    t=t0
    l=len(datos)
    ##Creamos una solucion aleatoria
    ciudades = list(range(l))
    solucion = []
    for i in range(l):
        ciudad = ciudades[random.randint(0, len(ciudades) - 1)]
        solucion.append(ciudad)
        ciudades.remove(ciudad)
    longitud = evaluarSolucion(datos, solucion)


    it=0
    while t > 0.05:
        ##Obtenemos un vecino al azar
        vecino = obtenerVecino(solucion, datos)
        incremento = vecino[1]-longitud

        if incremento < 0:
            longitud = vecino[1]
            solucion = vecino[0]
        elif random.random() < math.exp(-abs(incremento) / t):
            longitud = vecino[1]
            solucion = vecino[0]

        it+=1
        t=0.99*t

    return solucion, longitud

def main():

    aux_dataset = []
    dataset = []
    with open ("Datos.txt", "r") as f:
        for i in range(5, 51,5):
            linea = f.readline()
            print(linea)
            aux_f = []
            for j in range(0,i):
                f_contents = f.readline()
                f_contents = f_contents[1:-3]
                print(f_contents)
                numbers = [int(n) for n in f_contents.split(", ")]
                aux_f.append(numbers)

                if(j == i-1):
                    dataset.append(aux_f)

    print(dataset)
    maxUnImprovement = 400
    t0 = 10

    iterations = 1000
    results = []
    for datos in dataset:
        print("N: " + str(len(datos)))
        distances = []

        bestDist = math.inf
        worstDist = 0
        sumDist, sum_time = 0,0
        for j in range(iterations):
            start_time = time.time()
            s = simAnnealing2(datos, t0)
            end_time = time.time()
            sum_time += (end_time - start_time)
            distances.append(s[1])
            sumDist += s[1]
            if (s[1] < bestDist):
                bestDist = s[1]
            elif (s[1] > worstDist):
                worstDist = s[1]

        optimalOccurrences = distances.count(bestDist)
        results.append([len(datos), bestDist, worstDist, sumDist / iterations, optimalOccurrences, sum_time / iterations])

    # Export data to csv file
    with open("results.csv", "w") as file:
        file.write(",".join(
            ["Nodos", "Mejor Distancia", "Peor Distancia", "Distancia Media", "Frec. mejor frecuencia", "Tiempo Medio\n"]))
        for res in results:
            file.write(",".join([str(e) for e in res]) + "\n")


if __name__ == "__main__":
    main()
