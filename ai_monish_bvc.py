from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3 as tts
import threading
import time
import openai
import os
from io import BytesIO
import sys
sys.path.append("./oled")
import display
model = Model("vosk-model-en-in-0.5")
# wakeWordRecog=KaldiRecognizer(model,16000,'["mard","mard"]')
recognizer = KaldiRecognizer(model, 16000)
flag=True


class Timer:
    def __init__(self):
        self.commandName = "SetTimer"
        self.inputFormat = '{<TimeInSeconds>}'
        self.engine = tts.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.engine.setProperty('voice', 'english_rp+f4')

    def func(self,tsec):
        time.sleep(tsec)
        if self.engine._inLoop:
            self.engine.endLoop()
        self.engine.say("Time is Up")
        self.engine.runAndWait()


    def process(self, inputObj):
        str_time=''
        if len(inputObj)==1:
            str_time=inputObj.values()[0]
        else:
            try:
                str_time = inputObj['TimeInSeconds']
            except:
                str_time='5'
        tsec = int(str_time)
        thread = threading.Thread(target=self.func, args=(tsec,))
        thread.start()
        thread.join()
        return 1


class Task:
    def __init__(self):
        self.commandName = "SetTask"
        self.inputFormat = '{"Task","When"}'

    def process(self, obj):
        print("task", obj)
        self.fileWrite(obj['Task'], obj['When'])
        return 1

    def fileWrite(self, task, day):
        with open('static/todo.txt', 'a') as f:
            size = os.stat('static/todo.txt').st_size
            if size == 0:
                f.write(task+':'+day)
            else:
                f.write("\n"+task+':'+day)


class AI:
    
    def __init__(self, api_key_1=None, api_key_2=None, pluginArray=[]):
        
                if api_key_1 == None or api_key_2 == None:
                    exit()
                
                self.oled=display.Display()
                self.stopEvent=threading.Event()
                self.startDisplay("start")
                openai.api_key = api_key_1
                self.api_key_1=api_key_1
                self.api_key_2=api_key_2

                self.aiInstructions = '''The user will provide a phrase, and  check if it is a command or not. If it is a supported command response format:{}.
        If it is not a supported command,response format:{}.
        The supported commands={}  inputs required={}.
        Dont add Response or AI in the staring of response
                '''
                
                inst1 = '''{"positive":<response if task can be done or is  executed correctly>,"negative":<response if  not executed>, "command_name": <camel case name of the command>,
        "inputs":<inputs that the command might require from the phrase>}'''

                inst2 = '''{"response":"Not a valid command","command_name:"NotACommand"}'''

                self.aiStory = '''
                The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and sarcastic.Every response ends with movement control ,and an emotion command sepearted by & (movement:forward,backward,rotate right,rotate left,emotion:happy,sad,angry,serious,laugh,think), the bot uses this to express it's emotions For example(Thank you&rotate right&happy,alaram set&forward,backward&happy).The assistant was created by Avanish,Monish,Ramesh and Dhruva. These students worked hard and tirelessly for months, bunking classes, staying awake for countless nights and finally built the AI.
        Human: Hello, who are you?
        AI: I am an AI created by OpenAI. How can I help you today?&rotate right&happy
        Human: tell me a joke
        AI:Why did the chicken cross the playground?& &serious
        To get to the other slide!&rotate left&laugh
        Human: very nice
        AI:Thank you!&rotate right&happy
        Human: i am sad
        AI:I'm sorry to hear that. Is there anything I can do to help?&rotate left&serious
        Human:
                '''
                # self.file=open("out.txt","w")
                self.pluginsObject = []
                self.inputParams = {}
                self.commandName = []
                if len(pluginArray) != 0:
                    self.setUpPlugin(pluginArray)
                self.aiInstructions = self.aiInstructions.format(
                    inst1, inst2, self.commandName, self.inputParams)

                self.mic = pyaudio.PyAudio()
                self.stream = self.mic.open(
                    format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

                self.engine = tts.init()
                self.engine.setProperty('rate', 160)
                self.engine.setProperty('volume', 0.9)
                self.engine.setProperty('voice', 'english_rp+f4')
                
                self.motorControl=None
                self.motorDuration=2

                # self.test()
    def startDisplay(self,name):
        self.stopEvent.clear()
        self.x=threading.Thread(target=self.DisplayImage,args=(name,))
        self.x.setDaemon(True)
        self.x.start()

    def DisplayImage(self,name):
        while not self.stopEvent.is_set():
            self.oled.drawSavedImage(name) 
        return
    

    def changeImage(self,name):
        print("changing image to",name)
        self.stopEvent.set()
        self.x.join()
        self.startDisplay(name)


    def test(self):
        self.main("hello")
        n = input("What :")
        if n == 'y':
            self.test()
        pass

    def main(self,prompt=""):
        
        openai.api_key=self.api_key_1
        try:
            if prompt=="":
                prompt = self.SpeechTotextOffline()
                self.changeImage("processing")
                print("we entered")
                
            print(prompt)
            self.generateCommandResponse(prompt)

            return True
        except Exception as e:
            print("Error ",e)

            return False

    def stopSpeech(self):
        raise KeyboardInterrupt

    def setUpPlugin(self, pluginArray):
        for plugin in pluginArray:
            self.pluginsObject.append(plugin)
            self.commandName.append(plugin.commandName)
            self.inputParams[plugin.commandName]=plugin.inputFormat

        # self.aiInstructions=self.aiInstructions.format(self.commandName,self.inputParams)
    

    def setupMotionControl(self,motorObject):
        self.motionControl=motorObject


    def movement(self,what):
        if self.motorControl==None:
            print("Bot MotorControl is Absent")
            return

        thread=threading.Thread(self.motorControl.AIContorl,args=(what,self.motorDuration))
        thread.start()
        thread.join()

    def textToSpeech(self, text):
        if self.engine._inLoop:
            self.engine.endLoop()
        
        self.engine.say(text)
        self.engine.runAndWait()

    def generateNormalResponse(self,prompt):
        openai.api_key=self.api_key_2
        Modprompt=self.aiStory+prompt+'\n'+'AI:'
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=Modprompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response = response["choices"][0]["text"].split("&")
        print("Response1=",response)
        try:
            self.changeImage(response[-1])
        except:
            print("error")
        self.textToSpeech(response[0])
        
    def generateCommandResponse(self, prompt):

        Modprompt = self.aiInstructions+'\n'+prompt
        print("Mod prompt=",Modprompt)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=Modprompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response = response["choices"][0]["text"]
        print("Response=",response)
        self.interpretTheResponse(response,prompt)

    def interpretTheResponse(self, aiResponse,prompt):
        responseObject = eval(aiResponse)
        # self.file.write('\n'+responseObject)
        commandName = responseObject['command_name']

        if commandName == 'NotACommand':
            self.generateNormalResponse(prompt)

        elif commandName in self.commandName:
            index = self.commandName.index(commandName)
            status = self.pluginsObject[index].process(
                responseObject['inputs'])
            if status == 1:
                self.changeImage("think")
                self.textToSpeech(responseObject['positive'])
            else:
                self.changeImage("sad")
                self.textToSpeech(responseObject['negative'])
            #
        else:
            self.changeImage("sad")
            self.textToSpeech(responseObject['negative'])
            self.changeImage("start")
        self.changeImage("start")

    def SpeechTotextOffline(self):
        tempStream = self.stream
        tempStream.start_stream()
        while True:
            data = tempStream.read(4096,exception_on_overflow=0)
            if recognizer.AcceptWaveform(data):
                text = recognizer.Result()
                text = text[14:-3]
                print(text)
                if len(text)!=0:
                    return text


AIOBJ = AI(api_key_1="",
           api_key_2='', pluginArray=[Timer(), Task()])
