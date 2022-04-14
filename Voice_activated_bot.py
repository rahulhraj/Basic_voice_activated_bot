#importing required modules
import os
import pyttsx3
import speech_recognition as sr
import webbrowser
from datetime import date
from num2words import num2words
import urllib
import urllib.request
import pandas as pd
import sys



d=date.today()
mydict={"opera":r"C:\Users\hp\AppData\Local\Programs\Opera GX\launcher.exe","github":r"C:\Users\hp\AppData\Local\GitHubDesktop\GitHubDesktop.exe"}
websites=pd.read_csv("Web_Scrapped_websites.csv", encoding='latin-1')
websites['name']=websites['Website'].str.extract(r'(?<=\.)(\w*)(?=\.)')
list1=websites['name'].tolist()


#Creating class
class voiceactivation:
    #Method to take voice commands as input
    def connect(self):
5        try:
            urllib.request.urlopen('http://google.com')
            return True
        except:
            return False
        
    def takeCommands(self):
        #Using Recognizer and Microphone Method for input voice
        #commands
        r=sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            print('Listening')
            r.pause_threshold=0.5
            r.energy_threshold=10000
            audio=r.listen(source)
            #voice input is identified
            try:
                print("Recognizing...")
                Query=r.recognize_google(audio,language='en-in').lower()
                print("The query is printed= ",Query)
                return Query
            except Exception as e:
                print(e)
                print("Please say that again")
                self.Speak("Please say that again")
                return self.takeCommands()
        
    #method for voice output
    def Speak(self,audio):
        engine=pyttsx3.init('sapi5')
        voices=engine.getProperty('voices')
        engine.setProperty('voice',voices[1].id)
        engine.setProperty("rate",175)
        engine.say(audio)
        engine.runAndWait()

    def OpenApp(self,x):
        self.x=x
        os.startfile(mydict[self.x])
    def Diary(self):    
        f=open("{}{}{}.txt".format(num2words(d.day),num2words(d.month),num2words(d.year)),"w")
        f.write("file has been created")
        f.close()
    #method to self shut down system
    def quitSelf(self):
        self.Speak("Are you sure you want to switch of the computer?")
        take=self.takeCommands()
        choice=take
        if "yes" in choice:
            print("Shutting down...")
            self.Speak("Shutting down the computer")
            os.system("shutdown /s /t 30")
        if "no" in choice:
            print("Confirmed")
            self.Speak("Confirmed")

if __name__=='__main__':
    Maam=voiceactivation()
    connect_status=Maam.connect()
    if connect_status==False:
        print("SYSTEM OFFLINE! Please reconnect and restart")
        Maam.Speak("Your system is offline. Please reconnect and restart.")
        sys.exit()
    print("How can I help you?")
    Maam.Speak("How can I help you?")
    text = Maam.takeCommands()
    if "open" in text:
        if "diary" in text:
            Maam.Diary()
        elif text.split("open")[-1].replace(" ","") in mydict.keys():
            Maam.Speak("Opening")
            Maam.OpenApp(text.split("open")[-1].replace(" ",""))        
        elif text.split("open")[-1].replace(" ","") in list1:
            Maam.Speak("Opening")
            n = list1.index(text.split("open")[-1].replace(" ",""))
            webbrowser.open_new(websites['Website'][n])
        else:
            Maam.Speak("Here's what I found on the web.")
            url='http://www.google.com/search?q='
            text=text.split("open")[-1].replace(" ","+")
            final_url=url+text
            webbrowser.open_new(final_url)
    elif "shut down" in text:
        Maam.quitSelf()
    else:
        Maam.Speak("Here are some search results")
        url='http://www.google.com/search?q='
        text=text.split("open")[-1].replace(" ","+")
        final_url=url+text
        webbrowser.open_new(final_url)
