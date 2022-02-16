import random
import math

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
    datos = [
[0, 190, 116, 399, 198, 75, 524, 983, 866, 878, 533, 625, 957, 193, 380, 922, 808, 287, 721, 560]
,
[190, 0, 809, 508, 559, 872, 759, 788, 420, 466, 750, 175, 239, 190, 373, 635, 758, 541, 418, 948]
,
[116, 809, 0, 687, 837, 710, 609, 803, 434, 650, 814, 480, 358, 390, 473, 116, 579, 990, 861, 785]
,
[399, 508, 687, 0, 429, 366, 894, 162, 937, 460, 838, 556, 480, 258, 117, 79, 307, 461, 661, 504]
,
[198, 559, 837, 429, 0, 587, 909, 86, 587, 43, 415, 47, 898, 833, 296, 859, 395, 993, 620, 923]
,
[75, 872, 710, 366, 587, 0, 430, 980, 68, 834, 876, 301, 396, 859, 167, 165, 572, 965, 193, 919]
,
[524, 759, 609, 894, 909, 430, 0, 515, 674, 338, 444, 305, 463, 429, 879, 977, 701, 210, 542, 189]
,
[983, 788, 803, 162, 86, 980, 515, 0, 192, 393, 637, 206, 877, 476, 950, 786, 489, 868, 779, 667]
,
[866, 420, 434, 937, 587, 68, 674, 192, 0, 791, 905, 360, 484, 790, 884, 739, 974, 147, 600, 606]
,
[878, 466, 650, 460, 43, 834, 338, 393, 791, 0, 203, 842, 586, 600, 408, 746, 390, 425, 835, 423]
,
[533, 750, 814, 838, 415, 876, 444, 637, 905, 203, 0, 165, 467, 610, 155, 239, 162, 615, 684, 650]
,
[625, 175, 480, 556, 47, 301, 305, 206, 360, 842, 165, 0, 565, 26, 802, 58, 372, 365, 421, 74]
,
[957, 239, 358, 480, 898, 396, 463, 877, 484, 586, 467, 565, 0, 739, 936, 143, 317, 170, 339, 260]
,
[193, 190, 390, 258, 833, 859, 429, 476, 790, 600, 610, 26, 739, 0, 180, 40, 767, 343, 952, 770]
,
[380, 373, 473, 117, 296, 167, 879, 950, 884, 408, 155, 802, 936, 180, 0, 496, 232, 194, 570, 423]
,
[922, 635, 116, 79, 859, 165, 977, 786, 739, 746, 239, 58, 143, 40, 496, 0, 634, 558, 949, 777]
,
[808, 758, 579, 307, 395, 572, 701, 489, 974, 390, 162, 372, 317, 767, 232, 634, 0, 155, 908, 81]
,
[287, 541, 990, 461, 993, 965, 210, 868, 147, 425, 615, 365, 170, 343, 194, 558, 155, 0, 994, 859]
,
[721, 418, 861, 661, 620, 193, 542, 779, 600, 835, 684, 421, 339, 952, 570, 949, 908, 994, 0, 630]
,
[560, 948, 785, 504, 923, 919, 189, 667, 606, 423, 650, 74, 260, 770, 423, 777, 81, 859, 630, 0]


    ]
    t0=10

    s=simAnnealing(datos,t0)
    print("--------------")
    print("Solucion final: ",s[0])
    print("Longitud de la ruta final: ",s[1])

if __name__ == "__main__":
    main()
