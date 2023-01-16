from otree.api import *
from negotiation.reputation import Reputation
from negotiation.offer_queries import get_open_offers, get_sent_offers, get_available_players, all_agreed, check_offer_legal, check_acceptance_legal


doc = """Negotiation between players"""


class C(BaseConstants):
    NAME_IN_URL = 'negotiation'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 4
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
            receiver = player.group.get_player_by_id(int(data[1]))
            offers = Offer.filter(group=player.group)
            if check_offer_legal(player, receiver, offers):
                offer = Offer.create(offer_id=len(Offer.filter())+1, sender=player, receiver=receiver,
                                     group=player.group, offer=int(data[2]), demand=int(data[3]))
                print(['O', offer.offer_id, offer.sender.id_in_group, offer.demand, offer.offer])
                offers = Offer.filter(group=player.group)
                return{offer.receiver.id_in_group: ['R', get_available_players(offer.receiver, offers), get_sent_offers(offer.receiver, offers), get_open_offers(offer.receiver, offers)],
                       offer.sender.id_in_group: ['R', get_available_players(offer.sender, offers), get_sent_offers(offer.sender, offers), get_open_offers(offer.sender, offers)]}
            else:
                return{player.id_in_group: ['E', 'This offer is not allowed because you sent it to a participant how agreed on an exchange already or one of the offers you sent this participant is still pending.']}
        else:
            if data[0] == 'D':  # D for decline
                offer = Offer.filter(receiver=player, offer_id=data[1])[0]
                offer.accepted = False
                offer.declined = True
                offer.closed = True
                offers = Offer.filter(group=player.group)
                return {offer.receiver.id_in_group: ['R', get_available_players(offer.receiver, offers),
                                                     get_sent_offers(offer.receiver, offers),
                                                     get_open_offers(offer.receiver, offers)],
                        offer.sender.id_in_group: ['R', get_available_players(offer.sender, offers),
                                                   get_sent_offers(offer.sender, offers),
                                                   get_open_offers(offer.sender, offers)]}
            else:
                if data[0] == 'A':  # A for accept
                    offer = Offer.filter(group=player.group, receiver=player, offer_id=data[1])[0]
                    if check_acceptance_legal(offer):
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
                        other_players = [p for p in offer.receiver.get_others_in_subsession() if p.id_in_group is not offer.sender.id_in_group]
                        if all_agreed(player):
                            return{0: ['N']}
                        else:
                            offers = Offer.filter(group=player.group)
                            return{other_players[0].id_in_group: ['R', get_available_players(other_players[0], offers),
                                                         get_sent_offers(other_players[0], offers),
                                                         get_open_offers(other_players[0], offers)],
                                   other_players[1].id_in_group: ['R', get_available_players(other_players[1], offers),
                                                         get_sent_offers(other_players[1], offers),
                                                         get_open_offers(other_players[1], offers)],
                                   other_players[2].id_in_group: ['R', get_available_players(other_players[2], offers),
                                                         get_sent_offers(other_players[2], offers),
                                                         get_open_offers(other_players[2], offers)],
                                   other_players[3].id_in_group: ['R', get_available_players(other_players[3], offers),
                                                         get_sent_offers(other_players[3], offers),
                                                         get_open_offers(other_players[3], offers)],
                                   offer.sender.id_in_group: ['A', offer.receiver.id_in_group, offer.offer, offer.demand],
                                   offer.receiver.id_in_group: ['A', offer.sender.id_in_group, offer.demand, offer.offer]}
                    else:
                        return{player.id_in_group: ['E', 'You accepted an offer that was closed by the sender by accepting another offer.']}
                else:
                    if data[0] == 'R':
                        offers = Offer.filter(group=player.group)
                        if player.agreed:
                            return{player.id_in_group: ['A', player.exchange_partner, player.send, player.receive]}
                        else:
                            return{player.id_in_group: ['R', get_available_players(player, offers),
                                                         get_sent_offers(player, offers),
                                                         get_open_offers(player, offers)]}
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
            slider_max=min(player.send + 3, 20),
            slider_middle=player.send
        )
    pass


class WaitAfterExchange(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        for p in group.get_players():
            p.deviation_partner = p.group.get_player_by_id(p.exchange_partner).deviation
    pass

class Result(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            net_receive=player.receive - player.deviation_partner,
            points_form_partner=(player.receive - player.deviation_partner)*2,
            points=(player.receive + player.deviation_partner)*2 + 20 - (player.send + player.deviation),
            remaining_budget=20 - (player.send + player.deviation)
        )
    pass


page_sequence = [Negotiation, WaitForExchange, Deviation, WaitAfterExchange, Result]
