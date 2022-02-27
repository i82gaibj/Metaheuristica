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

def simAnnealing(datos,t0,limit_un_improvement):
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
    un_improvement = 0

    best_solution = solucion
    best_longitud = longitud
    while t > 0.05 and it < 5000: #ponemos iteraciones para no caer en un bucle infinito al recalentar

        ##Obtenemos un vecino al azar
        vecino = obtenerVecino(solucion, datos)
        incremento = vecino[1]-longitud

        if incremento < 0:
            longitud = vecino[1]
            solucion = vecino[0]
            un_improvement = 0

            if longitud < best_longitud:
                best_solution = solucion
                best_longitud = longitud

        elif random.random() < math.exp(-abs(incremento) / t):
            longitud = vecino[1]
            solucion = vecino[0]
            un_improvement = 0

            if longitud < best_longitud: #añadimos comprobación para ver cual solucion aceptar
                best_solution = solucion
                best_longitud = longitud
        else:
            un_improvement += 1

        it+=1
        t=0.99*t

        #comprobacion del umbral y recalentamiento
        if un_improvement >= limit_un_improvement:
            un_improvement = 0
            t = t0

    return best_solution, best_longitud

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
    while t > 0.05 and it < 10000:
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


        #t = logAnnealing(t0, 0.04, it)
        #t = geometricAnnealing(t0, 0.65, it)
        #t = linearAnnealing(t0, 0.01, it)
        #t = cauchyAnneling(t0,0.65 ,it)


    return solucion, longitud

#Las 4 funciones de enfriamiento usadas

def logaritmic_Annealing(t0, alpha, k):
    return alpha * t0 / math.log(1+k)

def geometric_Annealing(t0, alpha, k):
    return alpha**k * t0

def linear_Annealing(t0, alpha, k):
    return t0 - alpha * k

def cauchy_Anneling(t0, alpha, k):
    return alpha * t0 / k




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
    #Establecemos el limite del umbral de temperatura para recalentar
    limit_un_improvement = 800
    t0 = 10

    iterations = 1000
    results = []
    for datos in dataset:
        print("N: " + str(len(datos)))
        distances = []

        best_distance = math.inf
        worst_distance = 0
        sum_distance, sum_time = 0,0
        for j in range(iterations):
            start_time = time.time()
            s = simAnnealing(datos, t0, limit_un_improvement)
            end_time = time.time()
            sum_time += (end_time - start_time)
            distances.append(s[1])
            sum_distance += s[1]
            if (s[1] < best_distance):
                best_distance = s[1]
            elif (s[1] > worst_distance):
                worst_distance = s[1]

        optimal_occurrences = distances.count(best_distance)
        results.append([len(datos), best_distance, worst_distance, sum_distance / iterations, optimal_occurrences, sum_time * 1000])

    # Export data to csv file
    with open("sim_anneling_improved_800.csv", "w") as file:
        file.write(",".join(
            ["Nodos", "Mejor Distancia", "Peor Distancia", "Distancia Media", "Frec. mejor frecuencia", "Tiempo Medio\n"]))
        for res in results:
            file.write(",".join([str(e) for e in res]) + "\n")


if __name__ == "__main__":
    main()
