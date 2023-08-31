from schedule import every, repeat, run_pending
import time
import threading
import requests
from bs4 import BeautifulSoup
from footyWatcher.models import Competition
from django.shortcuts import get_object_or_404

URL = "https://soccerlive.app/"
COMPETITION_TYPE= "div"
COMPETITION_CLASS= "top-tournament"
COMPETITION_TITLE_TYPE= "span"
COMPETITION_TITLE_CLASS= "league-name"

class CheckJob(threading.Thread):
    def run(cls):
        while True:
            run_pending()
            time.sleep(1)
    
@repeat(every(30).minutes)
def update_games():
    print("Starting job to update games")
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    competitions_elements = soup.find_all(COMPETITION_TYPE, class_=COMPETITION_CLASS)
    for competion in competitions_elements:
        handle_competition(competion)
        print()

def handle_competition(competition_element):
    competition_name_element = competition_element.find(COMPETITION_TITLE_TYPE, class_=COMPETITION_TITLE_CLASS)
    if(competition_name_element != None):
        competition_name = competition_name_element.text.strip()
        try:
            competition = Competition.objects.get(name=competition_name)
            print("Found competition")
        except Competition.DoesNotExist:
            competition = Competition(name= competition_name_element.text.strip())
            competition.save()
            print("Created competition")
        print(competition)

def start():
    update_games()
    CheckJob().start()