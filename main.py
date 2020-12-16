from bs4 import BeautifulSoup
from speech_recognition import UnknownValueError
import datetime
import requests
import re
import webbrowser
import argparse
import os
import aiml
from getvoice import mic_input
import say

def corona_updates(audio):

    audio = audio

    url = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(url)

    page = response.content
    soup = BeautifulSoup(page, 'lxml')

    totalCases = soup.findAll('div', attrs={'class': 'maincounter-number'})
    totalActiveClosed = soup.findAll('div', attrs={'class': 'number-table-main'})
    total_cases = []
    total_active_closed = []
    for total in totalCases:
        total_cases.append(total.find('span').text)
    for active_closed in totalActiveClosed:
        total_active_closed.append(active_closed.text.strip())

    world_total = 'Total Coronavirus Cases: ' + total_cases[0]
    world_deaths = 'Total Deaths: ' + total_cases[1]
    world_recovered = 'Total Recovered: ' + total_cases[2]
    world_active = 'Total Active Cases: ' + total_active_closed[0]
    world_closed = 'Total Closed Cases: ' + total_active_closed[1]

    info = 'For more information visit: ' + 'https://www.worldometers.info/coronavirus/#countries'

    if 'world' in audio:
        print('WORLD UPDATES: ')
        print(world_total)
        print(world_deaths)
        print(world_recovered)
        print(world_active)
        print(world_closed)
        print(info)

        say.speak('WORLD UPDATES')
        say.speak(world_total)
        say.speak(world_deaths)
        say.speak(world_recovered)
        say.speak(world_active)
        say.speak(world_closed)
        say.speak('For more information visit: worldometers.info')

    else:
        country = audio

        url = 'https://www.worldometers.info/coronavirus/country/' + country.lower() + '/'
        response = requests.get(url)

        page = response.content
        soup = BeautifulSoup(page, 'lxml')

        totalcases = soup.findAll('div', attrs={'class': 'maincounter-number'})
        total_cases = []
        for total in totalcases:
            total_cases.append(total.find('span').text)

        total = 'Total Coronavirus Cases: ' + total_cases[0]
        deaths = 'Total Deaths: ' + total_cases[1]
        recovered = 'Total Recovered: ' + total_cases[2]

        info = 'For more information visit: ' + url

        updates = country + ' Updates: '

        print(updates.upper())
        print(total)
        print(deaths)
        print(recovered)
        print(info)

        say.speak(updates)
        say.speak(total)
        say.speak(deaths)
        say.speak(recovered)
        say.speak('For more information visit: worldometers.info')

def scrape_news():
    url = 'https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en '
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.findAll('h3', attrs = {'class':'ipQwMb ekueJc RD0gLb'})
    for n in news:
        print(n.text)
        print('\n')
        say.speak(n.text)
    print('For more information visit: ', url)
    say.speak('For more information visit google news')

def welcome():
    hour = int(datetime.datetime.now().hour)
    print('CORVUS ASSISTANT 101')
    if hour >= 0 and hour < 12:
        say.speak('Good Morning !')

    elif hour >= 12 and hour < 18:
        say.speak('Good Afternoon!')

    else:
        say.speak('Good Evening!')

    say.speak('Im here to provide you with essential info about Corona Virus or COVID-19. Here you can request information about the contagion, symptoms, prevention, risks, and case statistics across the world.')
    assistant_name = ("Corvus 101")
    say.speak(assistant_name)
    say.speak('How may I help you sir?')

mode = "voice"

def get_arguments():
    parser = argparse.ArgumentParser()
    optional = parser.add_argument_group('params')
    optional.add_argument('-t', '--text', action='store_true', required=False,
                          help='Enable text mode')
    arguments = parser.parse_args()
    return arguments

def task(audio):
    BRAIN_FILE = "brain.dump"
    kernel = aiml.Kernel()
    if os.path.exists(BRAIN_FILE):
        print("Loading from brain file: " + BRAIN_FILE)
        kernel.loadBrain(BRAIN_FILE)
    else:
        print("Parsing aiml files")
        kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
        # print("Saving brain file: " + BRAIN_FILE)
        # kernel.saveBrain(BRAIN_FILE) #save the brain_file as brain.dump
    ai_speech = kernel.respond(audio)
    print('..\n', ai_speech)
    say.speak(ai_speech)
    if 'covid' in audio:
        print('..')
        words = audio.split(' ')
        try:
            corona_updates(words[-1])
        except IndexError:
            not_found = 'I cant find any results with '+ words[-1]+'. Please check if you spelled it correctly.'
            print(not_found)
            say.speak(not_found)
            pass

    elif 'news' in audio:
        print('..')
        scrape_news()

    elif 'where is' in audio:
        print('..')
        words = audio.split('where is')
        link = str(words[-1])
        link = re.sub(' ', '', link)
        say.speak('Locating')
        say.speak(link)
        print('Locating ' + words[-1])
        link = f'https://www.google.co.in/maps/place/{link}'
        print(link)
        webbrowser.open(link)

def audio_string():
    global mode
    args = get_arguments()
    if (args.text):
        mode = "text"
        audio = input("Corvus Assistant : ").lower()
    else:
        audio = mic_input.get_audio().lower()
    task(audio)

def start_listening():
    try:
        audio_string()
    except UnknownValueError:
        print('Unknown Value Error')

def keep_listening():
    welcome()
    while True:
        try:
            audio_string()
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            break
        except UnknownValueError:
            print('Unknown Value Error')

if __name__ == "__main__":
    keep_listening()