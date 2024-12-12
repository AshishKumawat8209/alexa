from django.shortcuts import render
from django.http import HttpResponse
from django import forms

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

def home(request):
    
    if request.method == 'POST':
        if 'btn1' in request.POST:

            r = sr.Recognizer()
            engin = pyttsx3.init()
            voices = engin.getProperty('voices')
            engin.setProperty('voice', voices[1].id)

            newRate = engin.getProperty('rate')
            newRate = newRate-20
            engin.setProperty('rate',newRate)

            engin.say("Jay shree raaam! this is alexa, how can i help you dude.")
            engin.runAndWait()

            def talk(text):
                engin.say(text)
                engin.runAndWait()

            def take_command():
                command = ''
                try:
                    with sr.Microphone() as source:
                        audio = r.listen(source)
                        command = r.recognize_google(audio)
                        command = command.lower()
                        if 'alexa' in command:
                            command = command.replace('alexa','')
                            return command
                        elif command == '':
                            return ''
                        else:
                            talk("call me alexa")
                            return take_command()
                except:
                    pass
                return command

            def run_alexa():
                command = take_command()
                if command == '':
                    talk("alexa didn't listen anything")
                elif 'play' in command:
                    song = command.replace('play','')
                    talk("playing"+song)
                    pywhatkit.playonyt(song)
                elif 'search' in command :
                    srch = command.replace('search','')
                    talk("Searching"+srch)
                    pywhatkit.search(srch)
                elif 'time'  in command:
                    time = datetime.datetime.now().strftime('%I:%M %p')
                    talk('current time is '+time)
                elif 'who is' in command:
                    person = command.replace('who is', '')
                    info = wikipedia.summary(person,1)
                    talk(info)
                elif 'bye' in command:
                    talk('bye dude, nice too meet you ')
                    return
                else:
                    talk("sorry, i can't")
                talk("what's my next command dude.")
                run_alexa() 
            run_alexa()

    return render(request, "index.html")