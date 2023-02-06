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
    sex = models.IntegerField(label='Please chose the gender you identify with.', choices=[[0, 'female'], [1, 'male'], [2, 'Else or prefer not to say.']])
    major = models.IntegerField(label='Please chose your main field of studies or the one that is closest.', choices=
                                    [[2, 'Accountancy'],
                                     [3, 'Accountancy HBO [higher vocational]'],
                                     [4, 'Anthropology'],
                                     [5, 'Archaeology'],
                                     [6, 'Art and Economics HBO [higher vocational]'],
                                     [7, 'Arts'],
                                     [8, 'Astronomics'],
                                     [9, 'Biochemistry'],
                                     [10, 'Bioinformatics'],
                                     [11, 'Biology'],
                                     [12, 'Business Administration'],
                                     [13, 'Chemistry'],
                                     [14, 'Cognitive Artificial Intelligence'],
                                     [15, 'Commercial Economy HBO [higher vocational]'],
                                     [16, 'Commercial Information Technology'],
                                     [17, 'Communication [&amp; Media Design] HBO [higher vocational]'],
                                     [18, 'Communication Management HBO [higher vocational]'],
                                     [19, 'Communication science'],
                                     [20, 'Computer Science'],
                                     [21, 'Dentistry'],
                                     [22, 'Dutch Language and Culture'],
                                     [23, 'Economic mathematics'],
                                     [24, 'Economics'],
                                     [25, 'Educational science'],
                                     [26, 'Engineering'],
                                     [27, 'English Language and Literature Studies [Britain/America]'],
                                     [28, 'Environmental Sciences'],
                                     [29, 'Facility Management HBO [higher vocational]'],
                                     [30, 'Financial Services Management HBO [higher vocational]'],
                                     [31, 'General social sciences'],
                                     [32, 'Geography'],
                                     [33, 'Geology'],
                                     [34, 'German Language and Literature Studies'],
                                     [35, 'Health Sciences'],
                                     [36, 'History'],
                                     [37, 'History of art'],
                                     [38, 'Humanistics'],
                                     [39, 'Indogerman Languages'],
                                     [40, 'Integral Safety HBO [higher vocational]'],
                                     [41, 'International Communication and Media HBO [higher vocational]'],
                                     [42, 'International Marketing Management HBO [higher vocational]'],
                                     [43, 'Journalism HBO [higher vocational]'],
                                     [44, 'Language and Culture studies'],
                                     [45, 'Law'],
                                     [46, 'Law HBO [higher vocational]'],
                                     [47, 'Mathematics'],
                                     [48, 'Media Management HBO [higher vocational]'],
                                     [49, 'Media science'],
                                     [50, 'Medical technology'],
                                     [51, 'Medicine'],
                                     [52, 'Musicology'],
                                     [53, 'Nature science and innovation management'],
                                     [54, 'Neuroscience'],
                                     [55, 'Nutrition science'],
                                     [56, 'Optometry HBO [higher vocational]'],
                                     [57, 'Orthoptics HBO [higher vocational]'],
                                     [58, 'PABO HBO [higher vocational]'],
                                     [59, 'Pedagogics'],
                                     [60, 'Personnel and Labour HBO [higher vocational]'],
                                     [61, 'Pharmaceutics'],
                                     [62, 'Philology'],
                                     [63, 'Philosophy'],
                                     [64, 'Physics'],
                                     [65, 'Physiotherapy HBO [higher vocational]'],
                                     [66, 'Policy and management studies'],
                                     [67, 'Political Science'],
                                     [68, 'Prehistory and early history'],
                                     [69, 'Psychology'],
                                     [70, 'Public Administration'],
                                     [71, 'Roman Languages and Literature Studies'],
                                     [72, 'Slavic Languages and Literature'],
                                  [73, 'None of the above']])
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
        form_fields = ['close1', 'cohesive1', 'team1',  'partners1', 'harmonious1', 'close2', 'cohesive2', 'team2', 'partners2', 'harmonious2',
                       'close3', 'cohesive3', 'team3',  'partners3', 'harmonious3', 'close4', 'cohesive4', 'team4', 'partners4',  'harmonious4',
                       'close5', 'cohesive5', 'team5', 'partners5', 'harmonious5', 'close6', 'cohesive6', 'team6', 'partners6', 'harmonious6']
        form_fields.pop(player.id_in_group*3-3)
        form_fields.pop(player.id_in_group * 3 - 3)
        form_fields.pop(player.id_in_group * 3 - 3)
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


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'sex', 'major']

    pass


class Results(Page):
    def before_next_page(player: Player, timeout_happened):
            player.payoff = round(player.payoff,1)

    def vars_for_template(player: Player):
        return dict(
            trade_earnings=player.participant.payoff-player.gift_remaining-player.gift_received,
            gift_remaining=player.gift_remaining,
            gift_received=player.gift_received,
            total=player.participant.payoff,
        )

    pass


page_sequence = [GiftGiving, Questionaire, Demographics, ResultsWaitPage, Results]
