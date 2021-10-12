#Librerías utilizadas
import RPi.GPIO as GPIO
import time
# Ajustes Iniciales GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Configuración de pines de entradas de datos
Entrada=14
B4=15
B3=18
B2=23
B1=24
Espacio=25
GPIO.setup(Entrada,GPIO.IN)
GPIO.setup(B4,GPIO.IN)
GPIO.setup(B3,GPIO.IN)
GPIO.setup(B2,GPIO.IN)
GPIO.setup(B1,GPIO.IN)
GPIO.setup(Espacio,GPIO.IN)
# Configuración de pines de salida de datos
A=10
B=9
C=11
D=5
E=6
F=13
G=19
GPIO.setup(A,GPIO.OUT)
GPIO.output(A,False)
GPIO.setup(B,GPIO.OUT)
GPIO.output(B,False)
GPIO.setup(C,GPIO.OUT)
GPIO.output(C,False)
GPIO.setup(D,GPIO.OUT)
GPIO.output(D,False)
GPIO.setup(E,GPIO.OUT)
GPIO.output(E,False)
GPIO.setup(F,GPIO.OUT)
GPIO.output(F,False)
GPIO.setup(G,GPIO.OUT)
GPIO.output(G,False)
#Inicio del programa de registro de ingreso y salida de autos
        
def getBinary():
    Posiciones=[B4,B3,B2,B1]
    Cadena=""
    for Posicion in Posiciones:
        if(GPIO.input(Posicion)):
            Cadena=Cadena+"1"
        else:
            Cadena=Cadena+"0"
    return int(Cadena,2)
while(True):
    if(not GPIO.input(Entrada)):
        print("Vehículo ingresó " + time.strftime("%c"))
    else:
        NumParqueo = getBinary()
        if(NumParqueo == 0):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,False)
        elif(NumParqueo == 1):
            GPIO.output(A,False)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,False)
            GPIO.output(F,False)
            GPIO.output(G,False)
        elif(NumParqueo == 2):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,False)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,False)
            GPIO.output(G,True)
        elif(NumParqueo == 3):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,False)
            GPIO.output(F,False)
            GPIO.output(G,True)
        elif(NumParqueo == 4):
            GPIO.output(A,False)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,False)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(NumParqueo == 5):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,False)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(NumParqueo == 6):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(NumParqueo == 7):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,False)
            GPIO.output(F,False)
            GPIO.output(G,False)
        elif(NumParqueo == 8):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(NumParqueo == 9):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,False)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(NumParqueo == 10):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(NumParqueo == 11):
            GPIO.output(A,False)
            GPIO.output(B,False)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(NumParqueo == 12):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,False)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,False)
        elif(NumParqueo == 13):
            GPIO.output(A,False)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,False)
            GPIO.output(G,True)
        elif(NumParqueo == 14):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,False)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(NumParqueo == 15):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,False)
            GPIO.output(D,False)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
GPIO.cleanup()