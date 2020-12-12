from getvoice import getvoice
import say
import getdatetime
import webbrowser
import datetime
from speech_recognition import UnknownValueError
import requests
from bs4 import BeautifulSoup
import re
import argparse

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
        print('World Updates: ')
        print(world_total)
        print(world_deaths)
        print(world_recovered)
        print(world_active)
        print(world_closed)
        print(info)

        say.speak('World Updates')
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

        print(updates)
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

def task():
    global mode
    args = get_arguments()
    welcome()
    while True:
        if (args.text):
            mode = "text"
            audio = input("Corvus Assistant : ")
        else:
            audio = getvoice.get_audio().lower()
        if 'covid' in audio:
            print('..')
            words = audio.split(' ')
            corona_updates(words[-1])

        elif 'coronavirus' in audio:
            ncov = 'A novel coronavirus is a new coronavirus that has not been previously identified. The virus causing coronavirus disease 2019 (COVID-19), is not the same as the coronaviruses that commonly circulate among humans and cause mild illness, like the common cold.'
            print('..')
            print(ncov)
            say.speak(ncov)

        elif 'virus spread' in audio:
            vspread = 'The virus that causes COVID-19 most commonly spreads between people who are in close contact with one another .within about 6 feet, or 2 arm lengths. \n It spreads through respiratory droplets or small particles, such as those in aerosols, produced when an infected person coughs, sneezes, sings, talks, or breathes. \n These particles can be inhaled into the nose, mouth, airways, and lungs and cause infection. This is thought to be the main way the virus spreads. \n Droplets can also land on surfaces and objects and be transferred by touch. A person may get COVID-19 by touching the surface or object that has the virus on it and then touching their own mouth, nose, or eyes. Spread from touching surfaces is not thought to be the main way the virus spreads. \nIt is possible that COVID-19 may spread through the droplets and airborne particles that are formed when a person who has COVID-19 coughs, sneezes, sings, talks, or breathes. There is growing evidence that droplets and airborne particles can remain suspended in the air and be breathed in by others, and travel distances beyond 6 feet (for example, during choir practice, in restaurants, or in fitness classes). In general, indoor environments without good ventilation increase this risk.'
            print('..')
            print(vspread)
            say.speak(vspread)

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

        elif 'who are you' in audio:
            corvus = 'Hello I am Corvus 101, I am built to provide information about Coronavirus.'
            print('..')
            print(corvus)
            say.speak(corvus)

        elif 'time' in audio:
            print('..')
            hours, minutes = getdatetime.time()
            time = 'The time is ' + hours + ' ' + minutes
            print(time)
            say.speak(time)

        elif 'date' in audio:
            print('..')
            date, month = getdatetime.date()
            datenow = 'The date is ' + date + ' of ' + month
            print(datenow)
            say.speak(datenow)

def start_listening():
    try:
        task()
    except UnknownValueError:
        print('Unknown Value Error')

def keep_listening():
    while True:
        try:
            task()
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            break
        except UnknownValueError:
            print('Unknown Value Error')

if __name__ == "__main__":
    keep_listening()