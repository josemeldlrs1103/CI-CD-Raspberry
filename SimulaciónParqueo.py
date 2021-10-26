#Used Libraries
import RPi.GPIO as GPIO
import time
import requests
import json
import argparse

#Libraries used to control MAX7219 8x8 LED matrix
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas


#Defining the api-endpoint
API_ENDPOINT = "https://k1pnqqmf3k.execute-api.us-east-2.amazonaws.com/QRGenerator/qrgenerator"


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

#Set pins as input
GPIO.setup(Entrance,GPIO.IN)
GPIO.setup(B4,GPIO.IN)
GPIO.setup(B3,GPIO.IN)
GPIO.setup(B2,GPIO.IN)
GPIO.setup(B1,GPIO.IN)
GPIO.setup(ParkL,GPIO.IN)

#Output pins
Wait=17
A=27
B=22
C=9
D=5
E=6
F=13
G=19
Mainlight=26

#Set pins as output and turn off
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

#Convert for pins div switch to decimal number
def getBinary():
    Positions=[B4,B3,B2,B1]
    stChain=""
    for Position in Positions:
        if(GPIO.input(Position)):
            stChain=stChain+"1"
        else:
            stChain=stChain+"0"
    return int(stChain,2)

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
    
#Method to autosend data to post API
def writeData(pnumber,status):
    print(pnumber + status)
    x = {
        "Park_Number": pnumber,
        "Status": status
        }
    # sending post request and saving response as response object
    r = requests.post(url = API_ENDPOINT, data = json.dumps(x))
    
    
#Delete variables that won't be used
del x
del OpenTime

#Method to print parking map
def ParkingMap(n, block_orientation, rotate, Parkings):
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=rotate or 1)
    print("Created device")
    
    #Print parking spaces wether available or not
    with canvas(device) as draw:
        draw.point((1,0), fill="white")
        draw.point((3,0), fill="white")
        draw.point((5,0), fill="white")
        draw.point((7,0), fill="white")
        draw.point((1,2), fill="white")
        draw.point((3,2), fill="white")
        draw.point((5,2), fill="white")
        draw.point((7,2), fill="white")
        draw.point((1,4), fill="white")
        draw.point((3,4), fill="white")
        draw.point((5,4), fill="white")
        draw.point((7,4), fill="white")
        draw.point((1,6), fill="white")
        draw.point((3,6), fill="white")
        draw.point((5,6), fill="white")
        draw.point((7,6), fill="white")
        
        #Print parking spaces if available
        for individual in Parkings:
            ColumnMod = individual.Number % 4
            
            #Calculate j dimension
            if(ColumnMod == 0):
               Column=1 
            elif(ColumnMod == 1):
                Column=3
            elif(ColumnMod == 2):
                Column=5
            elif(ColumnMod == 3):
                Column=7
            
            #Calculate i dimension
            if(individual.Number in range(0,3,1)):
                Row=1
            elif(individual.Number in range(4,7,1)):
                Row=3
            elif(individual.Number in range(8,11,1)):
                Row=5
            elif(individual.Number in range(12,15,1)):
                Row=7
                
            #Print parking conditionally
            if(individual.Status == "Occupied"):
                draw.point((Column,Row), fill="white")
            else:
                draw.point((Column,Row), fill="black")


#Main program
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')

    args = parser.parse_args()
    
while(True):
    
    #When a car is sensed
    if(not GPIO.input(Entrance)):
        
        #Turn on wait signal
        GPIO.output(Wait,True)
        
        #Count remaining spaces
        RemainingSpace = 16
        for Lot in ParkingLots:
            if (Lot.Status ==  'Occupied'):
                RemainingSpace -= 1
                
        #If there are no available parking lots
        if (RemainingSpace==0): print('There are no available spaces, please come back later')
        
        #Parking lots available register the customer entrance
        else:
            
            #List of available spaces
            Available = []
            for Lot in ParkingLots:
                if (Lot.Status ==  'Empty'):
                    print('Parking ' + str(Lot.Number) + ' available')
                    Available.append(Lot.Number)
                    
            #Wait the customer to park
            Parked=False
            print("Go ahead and choose one parking lot")
            while(Parked == False):
                ParkingSpace = getBinary()
                
                #Check if the customer is trying to park in an available space
                if(not GPIO.input(ParkL)):
                    
                   #Register parking time 
                   if (ParkingSpace in Available):
                       ParkingLots[ParkingSpace].Status = 'Occupied'
                       ParkingLots[ParkingSpace].LastChange = time.strftime("%c")
                       #Log register into Dynamo DB
                       writeData(str(ParkingSpace),' Occupied')
                       Parked=True
                       GPIO.output(Wait,False)
                       
                    #Ask customer to move to an available space
                   else:
                       print("Please move to an available space")
                       
    #There are no custermers on queue to enter the parking lot
    else:
        
        #Get parking space number to check if available
        ParkNumber = getBinary()
        
        #Set 0 on display
        if(ParkNumber == 0):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,False)
            
        #Set 1 on display
        elif(ParkNumber == 1):
            GPIO.output(A,False)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,False)
            GPIO.output(F,False)
            GPIO.output(G,False)
            
        #Set 2 on display
        elif(ParkNumber == 2):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,False)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,False)
            GPIO.output(G,True)
        
        #Set 3 on display
        elif(ParkNumber == 3):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,False)
            GPIO.output(F,False)
            GPIO.output(G,True)
            
        #Set 4 on display
        elif(ParkNumber == 4):
            GPIO.output(A,False)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,False)
            GPIO.output(F,True)
            GPIO.output(G,True)
            
        #Set 5 on display
        elif(ParkNumber == 5):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,False)
            GPIO.output(F,True)
            GPIO.output(G,True)
            
        #Set 6 on display
        elif(ParkNumber == 6):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
            
        #Set 7 on display
        elif(ParkNumber == 7):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,False)
            GPIO.output(F,False)
            GPIO.output(G,False)
            
        #Set 8 on display
        elif(ParkNumber == 8):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
            
        #Set 9 on display
        elif(ParkNumber == 9):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,False)
            GPIO.output(F,True)
            GPIO.output(G,True)
            
        #Set 10 on display (A)
        elif(ParkNumber == 10):
            GPIO.output(A,True)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,False)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
            
        #Set 11 on display (B)
        elif(ParkNumber == 11):
            GPIO.output(A,False)
            GPIO.output(B,False)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
            
        #Set 12 on display (C)
        elif(ParkNumber == 12):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,False)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,False)
            
        #Set 13 on display (D)
        elif(ParkNumber == 13):
            GPIO.output(A,False)
            GPIO.output(B,True)
            GPIO.output(C,True)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,False)
            GPIO.output(G,True)
        
        #Set 14 on display (E)
        elif(ParkNumber == 14):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,False)
            GPIO.output(D,True)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
            
        #Set 15 on display (F)
        elif(ParkNumber == 15):
            GPIO.output(A,True)
            GPIO.output(B,False)
            GPIO.output(C,False)
            GPIO.output(D,False)
            GPIO.output(E,True)
            GPIO.output(F,True)
            GPIO.output(G,True)
            
        #Car is leaving parking space
        Occupied = []
        for Lot in ParkingLots:
            if (Lot.Status ==  'Occupied'):
                Occupied.append(Lot.Number)
                
        #Register space as available
        if(GPIO.input(ParkL)):
            if (ParkNumber in Occupied):
                       ParkingLots[ParkNumber].Status = 'Empty'
                       ParkingLots[ParkNumber].LastChange = time.strftime("%c")
                       writeData(str(ParkNumber),' Empty')
                       print("Parking "+str(ParkNumber)+" is now available")
                       
        #Print parking map
        ParkingMap(args.cascaded, args.block_orientation, args.rotate, ParkingLots)
            
GPIO.cleanup()
