import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess

# speech engine initialization
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
activationWord = "monday"
browser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
webbrowser.register('browser', None, webbrowser.BackgroundBrowser(browser_path))
# speaker
def speaker(text, rate = 120):
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()
# speech recognizer
def parse_command():
    listener = sr.Recognizer()
    print('loading...')

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input = listener.listen(source)

    try:
        print('recognizing speech...')
        query = listener.recognize_google(input, language = "en_gb")
        print(f'the input speech was {query}')
    except Exception as exception:
        print("I did not catch that")
        print(exception)
        return None
    return query
# send message via WhatsApp
def sendmsg(text, person):
    import pywhatkit
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute + 2
    if person == 'one':
        phone_number = '+77714643646'
        pywhatkit.sendwhatmsg(phone_number, text,hour, minute,15, True, 5)
    elif person == 'five':
        phone_number = '+77028590056'
        pywhatkit.sendwhatmsg(phone_number, text,hour, minute,15, True, 5)
# wisher in beginning
def wisher():
    hour = datetime.datetime.now().hour
    if hour >= 5 and hour < 12:
        speaker('Good morning, sir')
    elif hour >= 12 and hour < 17:
        speaker('Good afternoon, sir')
    elif hour >= 17 and hour < 23:
        speaker('Good evening, sir')
    else:
        speaker('Good night, sir') 
# main function
wisher()
while True:
    query = parse_command().lower().split()
    print(query)
    if query[0] == activationWord:
        query.pop(0)
        # repeating words
        if query[0] == 'say':
            if ' hello' in query:
                speaker('Greetings, my lord!')
            else:
                query.pop(0)
                text = ' '.join(query)
                speaker(text)
        # opening the web browser
        if query[0] == 'go' and query[1] == 'to':
            speaker("Opening...")
            query.pop(0)
            query.pop(0)
            if query[0] == 'browser':
                query.pop(0)
                text = ' '.join(query)
                webbrowser.get('browser').open_new(text)
        if query[0] == 'send' and query[1] == 'message':
            speaker('Sending...')
            query.pop(0)
            query.pop(0)
            query.pop(0)
            person = query[0]
            query.pop(0)
            text = ' '.join(query)
            sendmsg(text, person)
    if query[0] == "stop":
        break
