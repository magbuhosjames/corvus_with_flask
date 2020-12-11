from getvoice import getvoice
import say
import gettingtime
import os
import webbrowser
from speech_recognition import UnknownValueError
import threading
import requests
from bs4 import BeautifulSoup
import re

def corona_updates(said):

    said = said

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

    if 'world' in said:
        print('World Updates: ')
        print(world_total)
        print(world_deaths)
        print(world_recovered)
        print(world_active)
        print(world_closed)
        print(info)

        say.say('World Updates')
        say.say(world_total)
        say.say(world_deaths)
        say.say(world_recovered)
        say.say(world_active)
        say.say(world_closed)
        say.say('For more information visit: worldometers.info')

    else:
        country = said

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

        say.say(updates)
        say.say(total)
        say.say(deaths)
        say.say(recovered)
        say.say('For more information visit: worldometers.info')

def scrape_news():
    url = 'https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en '
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.findAll('h3', attrs = {'class':'ipQwMb ekueJc RD0gLb'})
    for n in news:
        print(n.text)
        print('\n')
        say.say(n.text)
    print('For more information visit: ', url)
    say.say('For more information visit google news')

def listen_for_flask():
    said = getvoice.getvoice()

    try:
        try:
            with open("listening", "r") as a:
                if a.read() == "true":
                    action = threading.Thread(target=corona_updates, args=[said])
                    action.start()
        except FileNotFoundError as e:
            action = threading.Thread(target=corona_updates, args=[said])
            action.start()
    except UnknownValueError:
        print("Unknown Value Error")
   

def start_listening():
    try:
        getvoice.getvoice()
    except UnknownValueError:
        print("Unknown Value Error")

def keep_listening():
    while True:
        said = getvoice.getvoice()
        if 'covid' in said:
            print('..')
            words = said.split(' ')
            corona_updates(words[-1])

        elif 'coronavirus' in said:
            ncov = 'A novel coronavirus is a new coronavirus that has not been previously identified. The virus causing coronavirus disease 2019 (COVID-19), is not the same as the coronaviruses that commonly circulate among humans and cause mild illness, like the common cold.'
            print(ncov)
            say.say(ncov)

        elif 'news' in said:
            print('..')
            scrape_news()

        elif 'where is' in said:
            print('..')
            words = said.split('where is')
            link = str(words[-1])
            link = re.sub(' ', '', link)
            say.say('Locating')
            say.say(link)
            print('Locating ' + words[-1])
            link = f'https://www.google.co.in/maps/place/{link}'
            print(link)
            webbrowser.open(link)

        elif 'who are you' in said:
            say.say("Hello I am Corvus 101, I am built to provide information about Coronavirus.")

        elif 'time' in said:
            hours, minutes = gettingtime.time()
            say.say("The time is " + hours + " " + minutes)

        elif 'date' in said:
            date, month = gettingtime.date()
            say.say("the date is " + date + " of " + month)

        elif 'search' in said:
            search_for = said.split("search ")[1]
            if search_for[:3] == "for":
                search_for = search_for.replace("for", "", 1)

            search_for = quote(search_for)
            if "google" in said:
                search_for = search_for.replace("in%20google%20", "", 1)
                search_for = search_for.replace("google%20", "", 1)
                if search_for.startswith("for%20"):
                    search_for = search_for.replace("for%20", "", 1)
                os.system("start https://www.google.com/search?q=" + search_for)


if __name__ == "__main__":
    keep_listening()