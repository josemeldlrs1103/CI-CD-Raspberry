#Used Libraries
import RPi.GPIO as GPIO
import time
#GPIO initial adjustments
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#Input pins
Entrance=14
B4=15
B3=18
B2=23
B1=24
ParkL=25
GPIO.setup(Entrance,GPIO.IN)
GPIO.setup(B4,GPIO.IN)
GPIO.setup(B3,GPIO.IN)
GPIO.setup(B2,GPIO.IN)
GPIO.setup(B1,GPIO.IN)
GPIO.setup(ParkL,GPIO.IN)
#Output pins
Wait=22
A=10
B=9
C=11
D=5
E=6
F=13
G=19
Mainlight=26
GPIO.setup(Wait,GPIO.OUT)
GPIO.output(Wait,False)
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
GPIO.setup(Mainlight,GPIO.OUT)
GPIO.output(Mainlight,False)
#Inputs to Decimal number 
def getBinary():
    Posiciones=[B4,B3,B2,B1]
    Cadena=""
    for Posicion in Posiciones:
        if(GPIO.input(Posicion)):
            Cadena=Cadena+"1"
        else:
            Cadena=Cadena+"0"
    return int(Cadena,2)
#Parking Class
class Parking:
    def __init__(self,numb, state, time):
        self.Number = numb
        self.Status = state
        self.LastChange = time
#Creation and filling of a list of parking spaces
OpenTime = time.strftime("%c")
ParkingLots = []
for x in range(16):
    ParkingLots.append(Parking(x,'Empty',OpenTime))
#Eliminar variables que no se usarán.
del x
del OpenTime
#Main program
while(True):
    #When a car is sensed
    if(not GPIO.input(Entrance)):
        RemainingSpace = 16
        for Lot in ParkingLots:
            if (Lot.Status ==  'Occupied'):
                RemainingSpace -= 1
        if (RemainingSpace==0): print('There are no available spaces, please come back later')
        else:
            #List of available spaces
            Available = []
            for Lot in ParkingLots:
                if (Lot.Status ==  'Empty'):
                    print('Parking ' + str(Lot.Number) + ' available')
                    Available.append(Lot.Number)
            Parked=False
            print("Go ahead and choose one parking lot")
            while(Parked == False):
                ParkingSpace = getBinary()
                if(not GPIO.input(ParkL)):
                   if (ParkingSpace in Available):
                       for element in ParkingLots:
                           if(element.Number == ParkingSpace):
                               element.Status = "Occupied"
                               element.LastChange = time.strftime("%c")
                               Parked=True
                               break
    else:
        ParkNumber = getBinary()
        if(ParkNumber == 0):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,False)
        elif(ParkNumber == 1):
            GPIO.output(A,False)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,False)
            GPIO.output(F,False)
            GPIO.output(G,False)
        elif(ParkNumber == 2):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,False)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,False)
            GPIO.output(G,True)
        elif(ParkNumber == 3):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,False)
            GPIO.output(F,False)
            GPIO.output(G,True)
        elif(ParkNumber == 4):
            GPIO.output(A,False)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,False)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(ParkNumber == 5):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,False)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(ParkNumber == 6):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(ParkNumber == 7):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,False)
            GPIO.output(F,False)
            GPIO.output(G,False)
        elif(ParkNumber == 8):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(ParkNumber == 9):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,False)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(ParkNumber == 10):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(ParkNumber == 11):
            GPIO.output(A,False)
            GPIO.output(B,False)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(ParkNumber == 12):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,False)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,False)
        elif(ParkNumber == 13):
            GPIO.output(A,False)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,False)
            GPIO.output(G,True)
        elif(ParkNumber == 14):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,False)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
        elif(ParkNumber == 15):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,False)
            GPIO.output(D,False)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
GPIO.cleanup()
