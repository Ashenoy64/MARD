from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3 as tts
import threading
import time
import openai
import os

model = Model("vosk-model-en-in-0.5")
# wakeWordRecog=KaldiRecognizer(model,16000,'["mard","mard"]')
recognizer = KaldiRecognizer(model, 16000)

class Timer:
    def __init__(self):
        self.commandName = "SetTimer"
        self.inputFormat = '{<TimeInSeconds>}'

    def func(self,tsec):
        time.sleep(tsec)
        print("Time is Up")

    def process(self, inputObj):
        str_time = inputObj['TimeInSeconds']
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
        The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and sarcastic.The assistant was created by Avanish,Monish,Ramesh and Dhruva. These students worked hard and tirelessly for months, bunking classes, staying awake for countless nights and finally built the AI.
Human: Hello, who are you?
AI: I am an AI created by MONISH AVANISH DHRUVA ANF RAMESH, and my name is MARD . How can I help you today?{rotate right}
Human: tell me a joke
AI:Why did the chicken cross the playground?
To get to the other side!!
Human: very nice
AI:Thank you!
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
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        self.engine.setProperty('voice', 'english_rp+f4')

        # print(self.aiInstructions)

        # self.test()

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
        response = response["choices"][0]["text"]
        print("Response=",response)
        self.textToSpeech(response)
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
                self.textToSpeech(responseObject['positive'])
            else:
                self.textToSpeech(responseObject['negative'])
        else:
            self.textToSpeech(responseObject['negative'])

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
