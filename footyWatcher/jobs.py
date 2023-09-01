from schedule import every, repeat, run_pending
import time
import threading
import requests
from bs4 import BeautifulSoup
from footyWatcher.models import Competition
from django.shortcuts import get_object_or_404

URL = "https://soccerlive.app/"
COMPETITION_TYPE = "div"
COMPETITION_CLASS = "top-tournament"
COMPETITION_TITLE_TYPE = "span"
COMPETITION_TITLE_CLASS = "league-name"
GAME_LINK_TYPE = "a"
GAME_LINK_CLASS = "competition"

TEAMS_TYPE = "span"
HOME_TEAM_CLASS = "competition-cell-side1"
AWAY_TEAM_CLASS = "competition-cell-side2"


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
    competition_name_element = competition_element.find(
        COMPETITION_TITLE_TYPE, class_=COMPETITION_TITLE_CLASS
    )
    if competition_name_element != None:
        competition_name = competition_name_element.text.strip()
        try:
            competition = Competition.objects.get(name=competition_name)
            print(f"Found competition {competition.name}")
        except Competition.DoesNotExist:
            competition = Competition(name=competition_name_element.text.strip())
            competition.save()
            print(f"Created competition {competition.name}")
    for game in competition_element.find(GAME_LINK_TYPE, class_=GAME_LINK_CLASS):
        print(game)
        # handle_game(game, competition)


def handle_game(game, competition):
    home_team_element = game.find(TEAMS_TYPE, class_=HOME_TEAM_CLASS)
    print(home_team_element)
    away_team_element = game.find(TEAMS_TYPE, class_=AWAY_TEAM_CLASS)
    print(away_team_element)


def start():
    update_games()
    CheckJob().start()
