from django.db import models
from django.contrib.auth.models import User
from channels import Group
import json
from datetime import datetime

# Create your models here.
class Game(models.Model):
    creator = models.ForeignKey(User, related_name='creator')
    opponent = models.ForeignKey(User, related_name='opponent',null=True, blank=True)
    winner = models.ForeignKey(User, related_name='winner',null=True, blank=True)
    cols = models.IntegerField(default=6)
    rows = models.IntegerField(default=6)
    current_turn = models.ForeignKey(User, related_name='current_turn')
    completed = models.DateTimeField(null=True, blank=True)
    created =  models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'game -{0}'.format(self.pk)
    
    @staticmethod
    def get_available_games():
        return Game.objects.filter(opponent=None, )
    
    @staticmethod
    def created_count(user):
        return Game.objects.filter(creator=user).count()

    @staticmethod
    def get_games_for_player(user):
        from django.db.models import Q
        return Game.objects.filter(Q(opponent=user)|Q(creator=user))

    @staticmethod
    def get_by_id(id):
        try:
            return Game.objects.get(pk=id)
        except Game.DoesNotExist:
            pass

    @staticmethod
    def create_new(user):
        new_game = Game(creator=user, current_turn=user)
        new_game.save()
        for row in range(new_game.rows):
            for col in range(new_game.cols):
                  new_square = GameSquare(game=new_game,row=row,col=col)
                  new_square.save()
        new_game.add_log('Game created on {0}'.format(new_game.creator.username))
        return new_game

    def add_log(self, text, user=None):
        entry = GameLog(game=self, text=text, player=user).save()
        return entry

    def get_all_game_squares(self):
        return GameSquare.objects.filter(game=self)

    def get_game_square(row,col):
        try:
            return GameSquare.objects.get(game=self,col=col,row=row)
        except GameSquare.DoesNotExist:
            return None

    def get_square_by_coords(self, coords):
        try:
            square=GameSquare.objects.get(row=coords[1],col=coords[0],game=self)
            return square
        except GameSquare.DoesNotExist:
            reurn None

   def get_game_log(self):
        return GameLog.objects.filter(game=self)

   def send_game_update(self):
        


