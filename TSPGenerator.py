import random

def generador(nCiudades):
    tsp = []
    for i in range(nCiudades):
        distancias = []
        for j in range(nCiudades):
            if j == i:
                distancias.append(0)
            elif j < i:
                distancias.append(tsp[j][i])
            else:
                distancias.append(random.randint(10, 1000))
        tsp.append(distancias)
    return tsp

def algoritmo(nodos):








    tsp = generador(nodos)
    return tsp


def main():

    with open("Datos.txt", "w") as f:
        pass

    nodos_min = input("¿Cuantas ciudades quieres generar como minimo?: ")
    nodos_min = int(nodos_min)
    nodos_max = input("¿Cuantas ciudades quieres generar como maximo?: ")
    nodos_max = int(nodos_max)
    incremento = input("¿Cuanto quieres que vaya incrementando?: ")
    incremento = int(incremento)


    for i in range(nodos_min, nodos_max, incremento):
        datos = algoritmo(i)
        with open("Datos.txt", "a") as file:
            titulor =  "longitud = " + str(i) + "\n"
            file.write(titulor)
            for key in datos:
                ciudad = key
                filas =  str(ciudad) + "," + "\n"

                file.write(filas)



if __name__ == "__main__":
    main()
