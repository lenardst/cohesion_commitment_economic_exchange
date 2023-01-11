from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'scmeasure'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gift1 = models.IntegerField(initial=0, min=0, max=10)
    gift2 = models.IntegerField(initial=0, min=0, max=10)
    gift3 = models.IntegerField(initial=0, min=0, max=10)
    gift4 = models.IntegerField(initial=0, min=0, max=10)
    gift5 = models.IntegerField(initial=0, min=0, max=10)
    gift6 = models.IntegerField(initial=0, min=0, max=10)

    perception1 = models.IntegerField(initial=0)
    perception2 = models.IntegerField(initial=0)
    perception3 = models.IntegerField(initial=0)
    perception4 = models.IntegerField(initial=0)
    perception5 = models.IntegerField(initial=0)
    perception6 = models.IntegerField(initial=0)
    pass

# Pages


class ResultsWaitPage(WaitPage):
    pass


class GiftGiving(Page):
    form_model = 'player'
    form_fields = ['gift1', 'gift2', 'gift3', 'gift4', 'gift5', 'gift6']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_players=[p.id_in_group for p in player.get_others_in_subsession()]
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            other_players=[p.id_in_group for p in player.get_others_in_subsession()]
        )
    pass


class Questionaire(Page):
    form_model = 'player'
    form_fields = ['perception1', 'perception2', 'perception3', 'perception4', 'perception5', 'perception6']
    pass

class Results(Page):
    pass

page_sequence = [GiftGiving, Questionaire, Results]
