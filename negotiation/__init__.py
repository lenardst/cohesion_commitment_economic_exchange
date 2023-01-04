from otree.api import *
from negotiation.reputation import Reputation


doc = """Negotiation between players"""


class C(BaseConstants):
    NAME_IN_URL = 'negotiation'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 30
    REPUTATION_SYSTEM = True

pass


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    pass


class Player(BasePlayer):
    agreed = models.BooleanField(initial=False)
    exchange_partner = models.IntegerField()
    send = models.IntegerField()
    receive = models.IntegerField()
    deviation = models.IntegerField(min=-3)
    deviation_partner = models.IntegerField()
    round_net = models.IntegerField()
    pass

# EXTRA MODEL


class Offer(ExtraModel):
    offer_id = models.IntegerField()
    sender = models.Link(Player)
    receiver = models.Link(Player)
    group = models.Link(Group)
    offer = models.IntegerField()
    demand = models.IntegerField()
    accepted = models.BooleanField()
    declined = models.BooleanField()
    closed = models.BooleanField(initial=False)


# PAGES


class Negotiation(Page):
    # form_model = 'player'
    # form_fields = ['exchange_partner', 'send', 'receive']
    # timeout_seconds = 180

    @staticmethod
    def vars_for_template(player: Player):
        reputation_list = []
        for p in player.get_others_in_subsession():
            deviations = [i.deviation for i in p.in_previous_rounds() if C.REPUTATION_SYSTEM or i.exchange_partner is player.id_in_group]
            reputation_list.append(Reputation(p.id_in_group, deviations))
        return dict(
            reputation_list=reputation_list
        )

    @staticmethod
    def live_method(player, data):  # Data is a list of values. First value specifies the type of action
        print(str(player.id_in_group) + ',' + str(data))
        if data[0] == 'O':  # O for create offer
            offer = Offer.create(offer_id=len(Offer.filter())+1, sender=player, receiver=player.group.get_player_by_id(int(data[1])),
                                 group=player.group, offer=int(data[2]), demand=int(data[3]))
            print(['O', offer.offer_id, offer.sender.id_in_group, offer.demand, offer.offer])
            return{offer.receiver.id_in_group: ['O', offer.offer_id, offer.sender.id_in_group, offer.demand, offer.offer]}
        else:
            if data[0] == 'D':  # D for decline
                offer = Offer.filter(receiver=player, offer_id=data[1])[0]
                offer.accepted = False
                offer.declined = True
                offer.closed = True
            else:
                if data[0] == 'A':  # A for accept
                    offer = Offer.filter(group=player.group, receiver=player, offer_id=data[1])[0]
                    offer.receiver.agreed = True
                    offer.sender.agreed = True
                    offer.accepted = True
                    offer.declined = False
                    offer.sender.send = offer.offer
                    offer.sender.receive = offer.demand
                    offer.receiver.send = offer.demand
                    offer.receiver.receive = offer.offer
                    offer.receiver.exchange_partner = offer.sender.id_in_group
                    offer.sender.exchange_partner = offer.receiver.id_in_group
                    # Close all offers where exchange partners are involved
                    closing_offers = [o for o in Offer.filter(group=player.group) if (o.receiver == offer.receiver or
                                      o.receiver == offer.sender or o.sender == offer.sender or o.sender == offer.receiver)
                                      and o.closed==False]
                    for o in closing_offers:
                        o.closed = True
                    closing_offers_id = [o.offer_id for o in closing_offers]
                    available_players = len([p.id_in_group for p in player.get_others_in_subsession() if p.agreed is False])
                    other_players = [i for i in [1, 2, 3, 4, 5, 6] if i != offer.receiver.id_in_group and i != offer.sender.id_in_group]
                    if available_players==0:
                        return{0: ['N']}
                    else:
                        return{other_players[0]: ['C', closing_offers_id, [offer.sender.id_in_group, offer.receiver.id_in_group]],
                               other_players[1]: ['C', closing_offers_id, [offer.sender.id_in_group, offer.receiver.id_in_group]],
                               other_players[2]: ['C', closing_offers_id, [offer.sender.id_in_group, offer.receiver.id_in_group]],
                               other_players[3]: ['C', closing_offers_id, [offer.sender.id_in_group, offer.receiver.id_in_group]],
                               offer.sender.id_in_group: ['A', offer.receiver.id_in_group, offer.offer, offer.demand],
                               offer.receiver.id_in_group: ['A', offer.sender.id_in_group, offer.demand, offer.offer]}

    @staticmethod
    def js_vars(player):
        return dict(
            available_players=[p.id_in_group for p in player.get_others_in_subsession()],
        )

    pass


class WaitForExchange(WaitPage):
    pass


class Deviation(Page):
    form_model = 'player'
    form_fields = ['deviation']

    @staticmethod
    def js_vars(player):
        return dict(
            slider_min=max(player.send - 3, 0),
            slider_max=player.send + 3,
            slider_middle=player.send
        )
    pass


class WaitAfterExchange(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        for p in group.get_players():
            p.deviation_partner = p.group.get_player_by_id(p.exchange_partner).deviation
    pass


page_sequence = [Negotiation, WaitForExchange, Deviation, WaitAfterExchange]
