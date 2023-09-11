from schedule import every, repeat, run_pending
import time
from django.utils import timezone
import threading
import requests
from bs4 import BeautifulSoup
from footyWatcher.models import Competition, Game

URL = "https://soccerlive.app/"
COMPETITION_TYPE = "div"
COMPETITION_CLASS = "top-tournament"
COMPETITION_TITLE_TYPE = "span"
COMPETITION_TITLE_CLASS = "league-name"
GAME_LINK_TYPE = "a"
GAME_LINK_CLASS = "competition"

TEAMS_TYPE = "span"
TEAM_NAME_CLASS = "name"
HOME_TEAM_CLASS = "competition-cell-side1"
AWAY_TEAM_CLASS = "competition-cell-side2"
GAME_TIME_CLASS = "competition-cell-score"
TIME_CLASS = "time"
TIME_VARIABLE = "datetime"
GAME_URL_VARIABLE = "href"


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
        print(competition.game_set.all())
        for game in competition_element.find_all(
            GAME_LINK_TYPE, class_=GAME_LINK_CLASS
        ):
            try:
                handle_game(game, competition)
            except:
                print("Could not create game")


def handle_game(game, competition):
    game_link = game["href"]
    game_home_team = (
        game.find(TEAMS_TYPE, class_=HOME_TEAM_CLASS)
        .find(TEAMS_TYPE, class_=TEAM_NAME_CLASS)
        .text.strip()
    )
    game_away_team = (
        game.find(TEAMS_TYPE, class_=AWAY_TEAM_CLASS)
        .find(TEAMS_TYPE, class_=TEAM_NAME_CLASS)
        .text.strip()
    )
    try:
        game = competition.game_set.filter(
            home_team=game_home_team, away_team=game_away_team
        ).get()
        print(f"Found game {game.home_team} vs {game.away_team}")
    except Game.DoesNotExist:
        game = competition.game_set.create(
            home_team=game_home_team,
            away_team=game_away_team,
            start_date=get_game_date(game),
        )


def get_game_date(game):
    game_start_date_element = game.find(TEAMS_TYPE, class_=GAME_TIME_CLASS)
    time_element = game_start_date_element.find(TIME_CLASS)
    if time_element != None:
        return time_element[TIME_VARIABLE]
    else:
        return timezone.now()


def start():
    update_games()
    CheckJob().start()
