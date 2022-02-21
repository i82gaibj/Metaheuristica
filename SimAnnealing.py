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

def simAnnealing(datos,t0):
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
    print("Longitud de la ruta: ", longitud)
    print("Temperatura: ", t)

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
        print("Longitud de la ruta: ", longitud)
        print("Temperatura: ", t)
    return solucion, longitud

def main():

    with open ("Datos.txt", "r") as f:
        for i in range(5, 10):
            joder = f.readline()
            gay = "["
            for j in range(0,i):
                f_contents = f.readline()
                gay = str(gay) + str(f_contents)

                if(j == i-1):
                    gay = str(gay) + "]"
                print("vez ", j)
                print (gay)






if __name__ == "__main__":
    main()
