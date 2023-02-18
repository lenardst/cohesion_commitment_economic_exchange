from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'instruction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(label='I confirm that I have signed the consent form.', choices=[[1, 'Yes']])
    pass
