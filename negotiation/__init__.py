from otree.api import *
from negotiation.reputation import Reputation, ExchangeRound, DisplayPlayer
from negotiation.offer_queries import get_open_offers, get_sent_offers, get_available_players, all_agreed, \
    check_offer_legal, check_acceptance_legal
import random
import numpy

doc = """Negotiation between players"""


class C(BaseConstants):
    NAME_IN_URL = 'negotiation'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 2  # numpy.random.binomial(10, 0.5) + 20 + 1
    PAY_TRADED_UNIT = cu(0.03)
    PAY_BUDGET_UNIT = cu(0.01)
    UNIT_BUDGET = 15
    DEVIATION = 5
    PLAYER_COLORS = ['GREEN', 'BLUE', 'ORANGE', 'PURPLE', 'RED']
    QUESTION1 = 'If you agree to a trade that you receive 10 units, is it guaranteed that you will receive at least 10 units?'
    QUESTION2 = 'If you accept an offer, another participant can still accept an offer of yours in the same round?'
    QUESTION3 = 'Assume you agreed with another participant to send 10 units. If you now decide to send 9 instead of 10 units, how many other participants will learn about your decision?'


pass


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    number_exchanges = models.IntegerField(initial=0)
    pass


class Player(BasePlayer):
    agreed = models.BooleanField(initial=False)
    exchange_partner = models.IntegerField()
    send = models.IntegerField()
    receive = models.IntegerField()
    deviation = models.IntegerField(min=-C.DEVIATION, max=C.DEVIATION, initial=0)
    deviation_partner = models.IntegerField()
    reason_no_exchange = models.IntegerField(choices=[
        [1, 'I did not want to trade'],
        [2, 'I could not trade with the preferred participant(s).'],
        [3, 'I ran out of time.'],
        [4, 'I was inattentive.']], initial=0, label='Why did you not agree on a trade in the past negotiation?')
    quiz1 = models.BooleanField(label=C.QUESTION1, choices=[[True, 'Yes'], [False, 'No']])
    quiz2 = models.BooleanField(label=C.QUESTION2, choices=[[True, 'Yes'], [False, 'No']])
    quiz3 = models.IntegerField(label=C.QUESTION3)
    exchange_number = models.IntegerField()
    color_order = models.StringField()
    player_order = models.StringField()

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

class FirstWaitPage(WaitPage):
    body_text = "Please wait until the other participants in your session have arrived and signed the consent form."
    wait_for_all_groups = True

    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def after_all_players_arrive(subsession):
        for player in subsession.get_players():
            player.participant.player_order = [p.id_in_group for p in player.get_others_in_group()].copy()
            random.shuffle(player.participant.player_order)
            player.participant.player_colors = C.PLAYER_COLORS.copy()
            random.shuffle(player.participant.player_colors)
            player.color_order = str(player.participant.player_colors)
            player.player_order = str(player.participant.player_order)
        subsession.group_randomly(fixed_id_in_group=True)

    pass


class Game_Instruction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        reputation_list = []
        own_deviations = [[i.deviation, return_color(player, i.exchange_partner)] for i in player.in_previous_rounds()
                          if i.round_number != 1 and i.agreed]
        reputation_list.append(Reputation(DisplayPlayer(0, 'YOU'), own_deviations))
        for i in range(5):
            deviations = [[i.deviation, return_color(player, i.exchange_partner)] for i in
                          player.group.get_player_by_id(player.participant.player_order[i]).in_previous_rounds() if
                          i.agreed and
                          (player.session.config['rs'] or i.field_maybe_none('exchange_partner') is player.id_in_group)
                          and i.round_number != 1]
            reputation_list.append(
                Reputation(DisplayPlayer(player.participant.player_order[i], player.participant.player_colors[i]),
                           deviations))
        return dict(
            reputation_list=reputation_list,
            pay_traded_unit=C.PAY_TRADED_UNIT,
            pay_budget_unit=C.PAY_BUDGET_UNIT,
            rs=player.session.config['rs']
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            pay_traded_unit=C.PAY_TRADED_UNIT,
            pay_budget_unit=C.PAY_BUDGET_UNIT,
            player_colors=player.participant.player_colors,
            player_order=player.participant.player_order,
            unit_budget=C.UNIT_BUDGET
        )


class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2', 'quiz3']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Answers(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            rs=player.session.config['rs']
        )


class Negotiation(Page):
    # form_model = 'player'
    # form_fields = ['exchange_partner', 'send', 'receive']
    timer_text = 'Time left to negotiate:'

    @staticmethod
    def get_timeout_seconds(player):
        if player.round_number == 1:
            return 300
        else:
            return 120

    @staticmethod
    def vars_for_template(player: Player):
        reputation_list = []
        own_deviations = [[i.deviation, return_color(player, i.exchange_partner)] for i in player.in_previous_rounds()
                          if i.round_number != 1 and i.agreed]
        reputation_list.append(Reputation(DisplayPlayer(0, 'YOU'), own_deviations))
        for i in range(5):
            deviations = [[i.deviation, return_color(player, i.exchange_partner)] for i in
                          player.group.get_player_by_id(player.participant.player_order[i]).in_previous_rounds() if
                          i.agreed and
                          (player.session.config['rs'] or i.field_maybe_none('exchange_partner') is player.id_in_group)
                          and i.round_number != 1]
            reputation_list.append(
                Reputation(DisplayPlayer(player.participant.player_order[i], player.participant.player_colors[i]),
                           deviations))
        return dict(
            reputation_list=reputation_list,
            pay_traded_unit=C.PAY_TRADED_UNIT,
            pay_budget_unit=C.PAY_BUDGET_UNIT,
        )

    @staticmethod
    def js_vars(player: Player):
        return dict(
            pay_traded_unit=C.PAY_TRADED_UNIT,
            pay_budget_unit=C.PAY_BUDGET_UNIT,
            player_colors=player.participant.player_colors,
            player_order=player.participant.player_order,
            unit_budget=C.UNIT_BUDGET
        )

    @staticmethod
    def live_method(player, data):  # Data is a list of values. First value specifies the type of action
        # print(str(player.id_in_group) + ',' + str(data))
        if data[0] == 'O':  # O for create offer
            receiver = player.group.get_player_by_id(int(data[1]))
            offers = Offer.filter(group=player.group)
            if check_offer_legal(player, receiver, offers):
                offer = Offer.create(offer_id=len(Offer.filter()) + 1, sender=player, receiver=receiver,
                                     group=player.group, offer=int(data[2]), demand=int(data[3]))
                # print(['O', offer.offer_id, offer.sender.id_in_group, offer.demand, offer.offer])
                offers = Offer.filter(group=player.group)
                return {offer.receiver.id_in_group: ['R', get_available_players(offer.receiver, offers),
                                                     get_sent_offers(offer.receiver, offers),
                                                     get_open_offers(offer.receiver, offers)],
                        offer.sender.id_in_group: ['R', get_available_players(offer.sender, offers),
                                                   get_sent_offers(offer.sender, offers),
                                                   get_open_offers(offer.sender, offers)]}
            else:
                return {player.id_in_group: ['E',
                                             'This offer is not allowed because you sent it to a participant who '
                                             'agreed on a trade already or one of the offers you sent this '
                                             'participant is still pending. Please continue the negotiating.']}
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
                        player.group.number_exchanges += 1
                        offer.sender.exchange_number = player.group.number_exchanges
                        offer.receiver.exchange_number = player.group.number_exchanges
                        # Close all offers where exchange partners are involved
                        closing_offers = [o for o in Offer.filter(group=player.group) if
                                          (o.receiver == offer.receiver or
                                           o.receiver == offer.sender or o.sender == offer.sender or o.sender == offer.receiver)
                                          and o.closed == False]
                        for o in closing_offers:
                            o.closed = True
                        other_players = [p for p in offer.receiver.get_others_in_group() if
                                         p.id_in_group is not offer.sender.id_in_group]
                        if all_agreed(player):
                            return {0: ['N']}
                        else:
                            offers = Offer.filter(group=player.group)
                            return {other_players[0].id_in_group: ['R', get_available_players(other_players[0], offers),
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
                                    offer.sender.id_in_group: ['A', offer.receiver.id_in_group, offer.offer,
                                                               offer.demand],
                                    offer.receiver.id_in_group: ['A', offer.sender.id_in_group, offer.demand,
                                                                 offer.offer]}
                    else:
                        return {player.id_in_group: ['E',
                                                     'You accepted an offer that was closed by the sender by '
                                                     'accepting another offer. Please continue negotiating.']}
                else:
                    if data[0] == 'R':
                        offers = Offer.filter(group=player.group)
                        if player.agreed:
                            return {player.id_in_group: ['A', player.exchange_partner, player.send, player.receive]}
                        else:
                            return {player.id_in_group: ['R', get_available_players(player, offers),
                                                         get_sent_offers(player, offers),
                                                         get_open_offers(player, offers)]}

    pass


class WaitForInstructions(WaitPage):
    body_text = "Please wait until the other participants have read the instructions, and answered the questions."

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class WaitForExchange(WaitPage):
    body_text = "Please wait until the other participants are ready for the next round."
    pass


class Deviation(Page):
    form_model = 'player'
    form_fields = ['deviation']

    @staticmethod
    def is_displayed(player):
        return player.agreed

    @staticmethod
    def js_vars(player):
        return dict(
            slider_min=max(player.send - C.DEVIATION, 0),
            slider_max=player.send + C.DEVIATION,
            slider_middle=player.send,
            pay_traded_unit=C.PAY_TRADED_UNIT,
            pay_budget_unit=C.PAY_BUDGET_UNIT
        )

    def vars_for_template(player: Player):
        return dict(
            exchange_partner=player.participant.player_colors[
                player.participant.player_order.index(player.exchange_partner)],
            slider_min=max(player.send - C.DEVIATION, 0),
            slider_max=player.send + C.DEVIATION,
            slider_middle=player.send
        )

    pass


class NoExchangePage(Page):
    def is_displayed(player):
        return not player.agreed

    form_model = 'player'
    form_fields = ['reason_no_exchange']

    pass


class WaitAfterExchange(WaitPage):
    body_text = "Please wait until the other participants have completed their trades."

    @staticmethod
    def after_all_players_arrive(group):
        for p in group.get_players():
            if p.agreed:
                p.deviation_partner = p.group.get_player_by_id(p.exchange_partner).deviation
                p.payoff = (p.receive + p.deviation_partner) * C.PAY_TRADED_UNIT + (
                        C.UNIT_BUDGET + C.DEVIATION - p.send - p.deviation) * C.PAY_BUDGET_UNIT
            else:
                p.payoff = (C.UNIT_BUDGET + C.DEVIATION) * C.PAY_BUDGET_UNIT

    pass


class Result(Page):
    def before_next_page(player: Player, timeout_happened):
        if player.round_number == 1:
            player.participant.exchange_list = []
        else:
            if player.agreed:
                player.participant.exchange_list.append(
                    ExchangeRound(player.round_number, DisplayPlayer(player.exchange_partner,
                                                                     player.participant.player_colors[
                                                                         player.participant.player_order.index(
                                                                             player.exchange_partner)]), player.receive,
                                  player.deviation_partner,
                                  player.send, player.deviation))
            else:
                player.participant.exchange_list.append(
                    ExchangeRound(player.round_number, DisplayPlayer("", "No trade"), "", "", "", ""))

    @staticmethod
    def vars_for_template(player: Player):
        if player.agreed:
            return dict(
                net_receive=player.receive + player.deviation_partner,
                points_form_partner=(player.receive + player.deviation_partner) * C.PAY_TRADED_UNIT,
                remaining_budget=C.UNIT_BUDGET + C.DEVIATION - player.send - player.deviation,
                remaining_budget_pay=(C.UNIT_BUDGET + C.DEVIATION - player.send - player.deviation) * C.PAY_BUDGET_UNIT,
                abs_deviation_partner=abs(player.deviation_partner),
                exchange_partner=player.participant.player_colors[
                    player.participant.player_order.index(player.exchange_partner)]
            )
        else:
            return dict(
                net_receive=0,
                points_form_partner=0,
            )

    pass


class EndPracticeRound(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

    def before_next_page(player: Player, timeout_happened):
        player.payoff = 0
        player.participant.payoff = 0

    def vars_for_template(player: Player):
        if player.agreed:
            exchange_partner = player.participant.player_colors[
                player.participant.player_order.index(player.exchange_partner)]
        else:
            exchange_partner = 0
        return dict(
            rs=player.session.config['rs'],
            exchange_partner=exchange_partner
        )


page_sequence = [FirstWaitPage, Game_Instruction, Quiz, Answers, WaitForInstructions, WaitForExchange, Negotiation,
                 Deviation,
                 NoExchangePage, WaitAfterExchange, Result, EndPracticeRound]


#### Helper functions
def return_color(player, id):
    if player.id_in_group == id:
        return 'BLACK'
    else:
        return player.participant.player_colors[player.participant.player_order.index(id)]
