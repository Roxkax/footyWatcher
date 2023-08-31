from django.db import models

# Create your models here.

class Competition(models.Model):
    name = models.CharField(max_length=200)
    

class Game(models.Model):
    home_team = models.CharField(max_length=200)
    away_team = models.CharField(max_length=200)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    start_date = models.DateTimeField("start_date")


class GameUrl(models.Model):
    url = models.CharField(max_length=500)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
