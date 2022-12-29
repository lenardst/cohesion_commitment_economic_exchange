from otree.api import *


doc = """Negotiation between players"""


class C(BaseConstants):
    NAME_IN_URL = 'negotiation'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 30

pass


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    pass


class Player(BasePlayer):
    exchange_partner = models.IntegerField()
    send = models.IntegerField()
    receive = models.IntegerField()
    deviation = models.IntegerField()
    deviation_partner = models.IntegerField()
    round_net = models.IntegerField()
    pass

# PAGES


class Negotiation(Page):
    form_model = 'player'
    form_fields = ['exchange_partner', 'send', 'receive']
    # timeout_seconds = 180

    @staticmethod
    def live_method(player, data):
        return{int(data[0]): [player.id_in_group, data[1], data[2]]}

    pass


class WaitForExchange(WaitPage):
    pass


class Deviation(Page):
    form_model = 'player'
    form_fields = ['deviation']
    pass


class WaitAfterExchange(WaitPage):
    pass


page_sequence = [Negotiation, WaitForExchange, Deviation, WaitAfterExchange]
