from io import BytesIO
import board
import digitalio
from PIL import Image,ImageDraw,ImageSequence
import adafruit_ssd1306 as ada
import time 
import threading
import os
import pickle
i2c=board.I2C()
class Display:

	def __init__(self,width=128,height=64,border=5,resetPin=digitalio.DigitalInOut(board.D4),addr=0x3c,i2c=None,gifFolder="./oled/gif"):
		if not i2c:
			i2c=board.I2C()
		self.gifFolder=gifFolder
		self.oled=ada.SSD1306_I2C(width,height,i2c,addr=addr,reset=resetPin)
		self.flag=True
		self.width=width
		self.height=height
		self.border=border
		self.setupGIF()
	def setupGIF(self):
		if os.path.exists(self.gifFolder+"/GIFS"):
			with open(self.gifFolder+"/GIFS","rb") as file:
					data=pickle.load(file)
					self.gifs=data
			print(self.gifs)
		else:
			gifs={}
			for file in os.listdir(self.gifFolder):
				if file.endswith(".gif"):
					lis=[]
					with Image.open(self.gifFolder+"/"+file) as im:
						iter=ImageSequence.Iterator(im)
						for frame in iter:
							buf=BytesIO()
							frame.save(buf,format="png")
							buf.seek(0)
							im=Image.open(buf)
							im=im.resize((self.width,self.height),Image.ANTIALIAS).convert('1')
							lis.append(im)
					gifs[file[:-4]]=lis
			with open(self.gifFolder+"/GIFS","wb") as file:
				pickle.dump(gifs,file)
			self.gifs=gifs
		
	def clear(self):
		self.oled.fill(1)
		self.oled.show()
	def drawImage(self,file):
		lis=[]
		try:
			with Image.open(file) as im:
				iter=ImageSequence.Iterator(im)
				for frame in iter:
					buf=BytesIO()
					frame.save(buf,format="png")
					buf.seek(0)
					im=Image.open(buf)
					im=im.resize((self.width,self.height),Image.ANTIALIAS).convert('1')
					lis.append(im)
					self.oled.image(im)
					self.oled.show()
			i=0
			while i<=len(lis):
				self.oled.image(lis[i])
				self.oled.show()
				i+=1
				if i==len(lis):
					i=0
		except Exception as e:
			print(e)
			return ("Error")
	def drawSavedImage(self,file):
		
	
		if file in self.gifs:
			lis=self.gifs[file]
			
			i=0
			while i<len(lis):
				self.oled.image(lis[i])
				self.oled.show()
				i+=1
				
		else:
			return ("Error")

