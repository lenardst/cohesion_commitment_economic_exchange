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

    close1 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                 choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                          [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                          [6, 'very close']])
    close2 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                 choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                          [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                          [6, 'very close']])
    close3 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                 choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                          [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                          [6, 'very close']])
    close4 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                 choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                          [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                          [6, 'very close']])
    close5 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                 choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                          [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                          [6, 'very close']])
    close6 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                 choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                          [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                          [6, 'very close']])

    cohesive1 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    cohesive2 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    cohesive3 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    cohesive4 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    cohesive5 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    cohesive6 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])

    team1 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                         [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                         [6, 'very close']])
    team2 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                         [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                         [6, 'very close']])
    team3 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                         [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                         [6, 'very close']])
    team4 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                         [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                         [6, 'very close']])
    team5 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                         [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                         [6, 'very close']])
    team6 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                         [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                         [6, 'very close']])

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

    @staticmethod
    def get_form_fields(player: Player):
        form_fields = ['close1', 'cohesive1', 'team1', 'close2', 'cohesive2', 'team2',
                   'close3', 'cohesive3', 'team3', 'close4', 'cohesive4', 'team4',
                   'close5', 'cohesive5', 'team5', 'close6', 'cohesive6', 'team6']
        form_fields.pop(player.id_in_group*3-3)
        form_fields.pop(player.id_in_group * 3 - 3)
        form_fields.pop(player.id_in_group * 3 - 3)
        return form_fields

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_players=[p.id_in_group for p in player.get_others_in_subsession()],
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            other_players=[p.id_in_group for p in player.get_others_in_subsession()]
        )

    pass


class Results(Page):
    pass


page_sequence = [GiftGiving, Questionaire, Results]
