import RPi.GPIO as GPIO          
from time import sleep



class Motor:
    en1=25
    en2=22

    in1=23
    in2=24

    in3=17
    in4=27
    def __init__(self,setup=False):
        if setup:
            self.setup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.en1,GPIO.OUT)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        self.p1=GPIO.PWM(self.en1,1000)
        self.p1.start(50)


        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in3,GPIO.OUT)
        GPIO.setup(self.in4,GPIO.OUT)
        GPIO.setup(self.en2,GPIO.OUT)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
        self.p2=GPIO.PWM(self.en2,1000)
        self.p2.start(50)

    def setup(self):
        self.en1=int(input("Enter Enable 1 :"))
        self.en2=int(input("Enter Enable 2 :"))

        self.in1=int(input("Enter Input 1 :"))
        self.in2=int(input("Enter Input 2 :"))

        self.in3=int(input("Enter Input 3 :"))
        self.in4=int(input("Enter Input 4 :"))

    def userControl(self,what):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
        if what=='up':
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)

            GPIO.output(self.in3,GPIO.HIGH)
            GPIO.output(self.in4,GPIO.LOW)

        elif what=='down':
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.HIGH)

            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.HIGH)
        elif what=='left':
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.HIGH)

            GPIO.output(self.in3,GPIO.HIGH)
            GPIO.output(self.in4,GPIO.LOW)
        elif what=='right':
            GPIO.output(self.in1,GPIO.HIGH)
            GPIO.output(self.in2,GPIO.LOW)

            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.HIGH)
        else:
            GPIO.output(self.in1,GPIO.LOW)
            GPIO.output(self.in2,GPIO.LOW)
            GPIO.output(self.in3,GPIO.LOW)
            GPIO.output(self.in4,GPIO.LOW)

    def AIControl(self,what,duration):
        if what=='up':
            self.forward(duration)
        elif what=='down':
            self.backward(duration)
        elif what=='left':
            self.left(duration)
        elif what=='right':
            self.right(duration)
        else:
            self.threeSixty()

    def stop(self):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)


    def forward(self,time):

        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)

        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)

        sleep(time)

        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

        pass
    
    def backward(self,time):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)

        sleep(time)
        
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

    def right(self,time):
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)

        sleep(time)
        
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

    def left(self,time):
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)

        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        

        sleep(time)
        
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

    def threeSixty(self):
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)

        sleep(5)
        
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)

        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)

        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        

        sleep(5)
        
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)

        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
        pass


    def power(self,power):
        self.p1.ChangeDutyCycle(power)
        self.p2.ChangeDutyCycle(power)


if __name__=="__main__":
    Motor()
