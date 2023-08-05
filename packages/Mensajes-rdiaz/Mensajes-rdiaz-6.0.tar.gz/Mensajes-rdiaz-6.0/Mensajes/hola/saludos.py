import numpy as np


def saludar():
    print("Hola, te saludo desde saludos.saludar()")

def prueba():
    print("Esta es una NUEVA prueba de una nueva Versión 6.0")

def generar_array(numeros):
    return np.arange(numeros)

class Saludo:
    def __init__(self):
        print("Hola, te saludo desde Saludo.__init")



if __name__ == "__main__":
    print(generar_array(5))