import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess
import selenium
import sqlite3

import time
from telegram import init_telegram
from telegram import send_msg
from telegram import read_new_msg

from youtube import init_youtube
from youtube import search_video

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
        print(f'the input speech was: {query}')
    except Exception as exception:
        print("I did not catch that")
        print(exception)
        return None
    return query

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

def people_exist():
    conn = sqlite3.connect('./Contacts/people_data.db')
    c = conn.cursor()
    
    # check if table exists
    c.execute(" SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='people' ")
    if c.fetchone()[0] == 0:
        # creating new table, since table 'people' doesn't exist
        c.execute("""CREATE TABLE people (
        person_id text,
        phone_number text,
        first_name text,
        last_name text,
        birthday text,
        relation text,
        telegram_url text)
        """)
        conn.commit()
    c.close()
    conn.close()

def update_person():
    people_exist()
    conn = sqlite3.connect('./Contacts/people_data.db')
    c = conn.cursor()
    speaker('Enter the person id you want to update')
    res = 1
    while res == 1:
        person_id = input('Person_id:')
        res = check_in_db(person_id, 'person_id')
        if res == 1:
            speaker('Such person does not exist. Do you want to stop? Say Yes or No')
            answer = parse_command().lower()
            if answer == 'yes':
                res = None
                break
            else:
                speaker('Please, enter the correct person id')
    if person_id == None:
        return
    while True:
        speaker('Which column do you want to update?Please, enter this column')
        column_name = input("Enter the column's name here:")
        speaker('Enter the value')
        value = input("Enter the value here:")
        c.execute(f"""
                    UPDATE people
                    SET {column_name} = ?
                    WHERE person_id = ?
                    """, (value, person_id))
        conn.commit()
        speaker('Is that all?Enter Yes or No')
        answer = input('Answer:').lower()
        if answer == 'yes':
            break
    c.close()
    conn.close()

def delete_from_contacts():
    people_exist()
    conn = sqlite3.connect('./Contacts/people_data.db', timeout = 40)
    c = conn.cursor()
    speaker('Please, enter the id of the person you want to remove from your contacts')
    
    # check if the person exists in the table
    res = 1
    while res == 1:
        person_id = input('Please, enter the person_id:')
        person_id = person_id.lower()
        res = check_in_db(person_id, 'person_id')
        if res == 1:
            speaker('This person does not exist')
            speaker('Do you want to stop? Say yes or no')
            answer = parse_command()
            answer = answer.lower()
            if answer == 'yes':
                person_id = None
                break
            else:
                speaker('Enter another person')
    
    # deleting from contacts
    if person_id == None:
        return
    c.execute("""
            DELETE FROM people WHERE person_id = ?
                """, (person_id,))
    conn.commit()
    c.close()
    conn.close()

def add_to_contacts():
    people_exist()
    conn = sqlite3.connect('./Contacts/people_data.db')
    c = conn.cursor()
    speaker('Please, enter the following data')
        
    # entering person_id
    res = 0
    while res == 0:
        person_id = input('Please, enter the person_id, but in the form of text:')
        person_id = person_id.lower()
        res = check_in_db(person_id, 'person_id')
        if res == 0:
            speaker('This data is already in the table')
                
    # entering phone_number
    res = 0
    while res == 0:
        phone_number = input('Please, enter the phone number:')
        res = check_in_db(phone_number, 'phone_number')
        if res == 0:
            speaker('This data is already in the table')
                
    # entering first_name, last_name,birthday, relation
    first_name = input('Please, enter the first name:')
    last_name = input('Please, enter the last name:')
    birthday = input('Please, enter the date  of the birthday(dd-mm-yyyy):')
    relation = input('Please, enter the relation of this person to you:')
    url = input('Please, enter the url of the person from telegram:')
        
    # inserting values into the table 'people'
    data = (person_id, phone_number, first_name, last_name,birthday, relation, url)
    c.execute("INSERT INTO people VALUES(?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    c.close()
    conn.close()

# function for checking if the data exists in db 'contacts.db'
def check_in_db(data, column_name):
    conn = sqlite3.connect('./Contacts/people_data.db')
    c = conn.cursor()
    c.execute(f"SELECT COUNT({column_name}) FROM people WHERE {column_name} = ?", (data,))
    res = c.fetchone()[0]
    if res == 0:
        c.close()
        conn.close()
        return 1
    else:
        c.close()
        conn.close()
        return 0

wisher()
while True:
    calling = parse_command()
    calling = calling.lower()
    if calling == activationWord:
        wisher()
        speaker('How can I help you?')
        order = parse_command().lower()
        if 'manage contacts' in order:
            while True:
                speaker('What is next?')
                order = parse_command().lower()
                if 'add to contacts' in order:
                    add_to_contacts()
                elif 'delete from contacts' in order:
                    delete_from_contacts()
                elif 'update the contact' in order:
                    update_person()
                speaker('Exit a database?')
                if answer == 'yes':
                    speaker('Sure')
                    break
        elif 'telegram' in order:
            speaker('opening Telegram...')
            driver = init_telegram()
            speaker('Log in to the telegram, please')
            time.sleep(20)
            while True:
                speaker('What is next?')
                t_order = parse_command().lower()
                if 'send message' in t_order:
                    speaker('Enter the following data:')
                    url = input('To whom?:')
                    message = input('The content of the message:')
                    send_msg(driver, url, message)
                elif 'read message' in t_order:
                    speaker('wait a second')
                    url = input('From whom?:')
                    read_new_msg(driver, url)

                speaker('Do you want to continue the session?')
                answer = parse_command().lower()
                if answer == 'no':
                    speaker('Exitting telegram')
                    driver.close()
                    break
        elif 'youtube' in order:
            speaker('Opening youtube')
            driver = init_youtube()
            while True:
                speaker('What is next?')
                t_yt = parse_command().lower()
                if 'search' in t_yt:
                    speaker('What should I search?')
                    name = parse_command().lower()
                    search_video(name, driver)
        speaker('Do you want to continue the session?')
        answer = parse_command().lower()
        if answer == 'no':
            speaker('Have a good time!')
            break
        else:
            continue