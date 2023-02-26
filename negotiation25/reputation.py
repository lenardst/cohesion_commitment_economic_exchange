from statistics import mean


class Reputation:
    def __init__(self, player, reputation_list):
        self.player = player
        self.reputation_list = [ReputationItem(i[0], i[1]) for i in reputation_list]
        if len(self.reputation_list) == 0:
            self.reputation_mean = 0
        else:
            self.reputation_mean = round(mean([i[0] for i in reputation_list]), 2)


class ReputationItem:
    def __init__(self, deviation, color):
        self.deviation = deviation
        self.color = color


class ExchangeRound:
    def __init__(self, round, player, amount_agreed_receive, amount_received, amount_agreed_sent, amount_sent):
        self.round = round
        self.partner = player
        self.amount_agreed_receive = amount_agreed_receive
        self.amount_received = amount_agreed_receive + amount_received
        self.amount_agreed_sent = amount_agreed_sent
        self.amount_sent = amount_agreed_sent + amount_sent


class DisplayPlayer:
    def __init__(self, number, label):
        self.number = number
        self.label = label

