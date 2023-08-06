#creamos la carpeta que contenga en el paquete test y cada script tenga el nombre test_algo
# #Como distribuir paquetes
#importamos unittest
import unittest
#importamos el generar array y numpy
import numpy as np
from mensajes.hola.saludos import generar_array


class PruebasHola(unittest.TestCase): #definimos la calse pruebas de hola de unittest, en testcase
    def test_generar_array(self): #definimos el test de generar array
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6))



#Distribucion local

#from mensajes.hola.saludos import saludar
#from mensajes.adios.despedidas import Despedida

#saludar()
#Despedida()