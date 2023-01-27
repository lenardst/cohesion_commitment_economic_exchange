from otree.api import *

import settings
from negotiation.reputation import DisplayPlayer
import random


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
    gift_remaining = models.CurrencyField(initial=0)
    gift_received = models.CurrencyField(initial=0)

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
    body_text = "Please wait until the other participants have sent their gifts and completed the survey."
    pass


class GiftGiving(Page):
    form_model = 'player'
    form_fields = ['gift1', 'gift2', 'gift3', 'gift4', 'gift5', 'gift6']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_players=[DisplayPlayer(p.id_in_group, player.participant.player_colors[player.participant.player_order.index(p.id_in_group)]) for p in player.get_others_in_subsession()],
            exchange_partners=[e.partner.number for e in player.participant.exchange_list]
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            other_players=[p.id_in_group for p in player.get_others_in_subsession()]
        )

    def before_next_page(player: Player, timeout_happened):
        player_to_gift = random.choice(player.participant.player_order)
        player_gift = [player.gift1, player.gift2, player.gift3, player.gift4, player.gift5, player.gift6][
            player_to_gift]
        player.gift_remaining = C.GIFT - player_gift
        player.payoff += player.gift_remaining
        other = player.group.get_player_by_id(player_to_gift)
        other.gift_received += player_gift * C.GIFT_FACTOR
        other.payoff += other.gift_received

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
            other_players=[DisplayPlayer(p.id_in_group, player.participant.player_colors[player.participant.player_order.index(p.id_in_group)]) for p in player.get_others_in_subsession()],
            exchange_partners=[e.partner.number for e in player.participant.exchange_list]
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            other_players=[p.id_in_group for p in player.get_others_in_subsession()]
        )

    pass


class Results(Page):
    def vars_for_template(player: Player):
        return dict(
            participation_fee=cu(settings.SESSION_CONFIG_DEFAULTS['participation_fee']),
            trade_earnings=player.participant.payoff-player.gift_remaining-player.gift_received,
            gift_remaining=player.gift_remaining,
            gift_received=player.gift_received,
            total=player.participant.payoff+settings.SESSION_CONFIG_DEFAULTS['participation_fee']
        )

    pass


page_sequence = [GiftGiving, Questionaire, ResultsWaitPage, Results]
