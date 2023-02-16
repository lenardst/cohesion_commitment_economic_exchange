from otree.api import *

import settings
from negotiation.reputation import DisplayPlayer
import random, copy


class C(BaseConstants):
    NAME_IN_URL = 'scmeasure'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    GIFT = cu(1)
    GIFT_FACTOR = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gift1 = models.CurrencyField(initial=0, min=0, max=10)
    gift2 = models.CurrencyField(initial=0, min=0, max=10)
    gift3 = models.CurrencyField(initial=0, min=0, max=10)
    gift4 = models.CurrencyField(initial=0, min=0, max=10)
    gift5 = models.CurrencyField(initial=0, min=0, max=10)
    gift6 = models.CurrencyField(initial=0, min=0, max=10)
    trading_earnings = models.CurrencyField(initial=0)
    gift_remaining = models.CurrencyField(initial=0)
    gift_received = models.CurrencyField(initial=0)
    player_to_gift = models.IntegerField()
    player_send_gift = models.IntegerField()

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
    partners1 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    partners2 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    partners3 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    partners4 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    partners5 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    partners6 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                    choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                             [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                             [6, 'very close']])
    harmonious1 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                      choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                               [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                               [6, 'very close']])
    harmonious2 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                      choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                               [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                               [6, 'very close']])
    harmonious3 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                      choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                               [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                               [6, 'very close']])
    harmonious4 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                      choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                               [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                               [6, 'very close']])
    harmonious5 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                      choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                               [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                               [6, 'very close']])
    harmonious6 = models.IntegerField(widget=widgets.RadioSelectHorizontal,
                                      choices=[[0, 'very distant'], [1, 'distant'], [2, 'rather distant'],
                                               [3, 'neither close nor distant'], [4, 'rather close'], [5, 'close'],
                                               [6, 'very close']])
    age = models.IntegerField(label='Please enter your age.')
    sex = models.IntegerField(label='Please chose the gender you identify with.',
                              choices=[[0, 'female'], [1, 'male'], [2, 'Else or prefer not to say.']])
    major = models.StringField(label='Please enter your main field of studies.')
    pass


# Pages


class ResultsWaitPage(WaitPage):
    body_text = "Please wait until the other participants have sent their gifts."

    def after_all_players_arrive(group: Group):
        for p in group.get_players():
            p.trading_earnings = p.participant.payoff
        set_players = [2, 3, 4, 5, 6, 1]
        for p in group.get_players():
            p.player_to_gift = set_players[p.id_in_group-1]
            player_gift = [p.gift1, p.gift2, p.gift3, p.gift4, p.gift5, p.gift6][
                p.player_to_gift - 1]
            p.gift_remaining = C.GIFT - player_gift
            p.participant.payoff += p.gift_remaining
            other = p.group.get_player_by_id(p.player_to_gift)
            other.player_send_gift = p.id_in_group
            other.gift_received += player_gift * C.GIFT_FACTOR
            other.participant.payoff += other.gift_received
        for p in group.get_players():
            p.participant.payoff = round(p.participant.payoff * 2) / 2


class GiftGiving(Page):
    form_model = 'player'
    form_fields = ['gift1', 'gift2', 'gift3', 'gift4', 'gift5', 'gift6']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_players=[DisplayPlayer(p.id_in_group, player.participant.player_colors[
                player.participant.player_order.index(p.id_in_group)]) for p in player.get_others_in_subsession()],
            exchange_partners=[e.partner.number for e in player.participant.exchange_list]
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
        form_fields = ['close1', 'cohesive1', 'team1', 'partners1', 'harmonious1', 'close2', 'cohesive2', 'team2',
                       'partners2', 'harmonious2',
                       'close3', 'cohesive3', 'team3', 'partners3', 'harmonious3', 'close4', 'cohesive4', 'team4',
                       'partners4', 'harmonious4',
                       'close5', 'cohesive5', 'team5', 'partners5', 'harmonious5', 'close6', 'cohesive6', 'team6',
                       'partners6', 'harmonious6']
        form_fields.pop(player.id_in_group * 5 - 5)
        form_fields.pop(player.id_in_group * 5 - 5)
        form_fields.pop(player.id_in_group * 5 - 5)
        form_fields.pop(player.id_in_group * 5 - 5)
        form_fields.pop(player.id_in_group * 5 - 5)
        return form_fields

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_players=[DisplayPlayer(p.id_in_group, player.participant.player_colors[
                player.participant.player_order.index(p.id_in_group)]) for p in player.get_others_in_subsession()],
            exchange_partners=[e.partner.number for e in player.participant.exchange_list]
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            other_players=[p.id_in_group for p in player.get_others_in_subsession()]
        )

    pass


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'sex', 'major']

    pass


class Results(Page):
    def vars_for_template(player: Player):
        return dict(
            trade_earnings=player.trading_earnings,
            gift_remaining=player.gift_remaining,
            gift_received=player.gift_received,
            total=player.participant.payoff,
            player_to_gift=player.participant.player_colors[player.participant.player_order.index(player.player_to_gift)],
            gift=C.GIFT-player.gift_remaining,
            player_send_gift=player.participant.player_colors[player.participant.player_order.index(player.player_send_gift)],
        )
    pass


page_sequence = [GiftGiving, ResultsWaitPage, Questionaire, Demographics, Results]
