from statistics import mean


class Reputation:
    def __init__(self, player_id, reputation_list):
        self.player_id = player_id
        self.reputation_list = list(filter(None, reputation_list))
        if len(self.reputation_list) == 0:
            self.reputation_mean = 0
        else:
            self.reputation_mean = mean(self.reputation_list)


class ExchangeRound:
    def __init__(self, round, partner, amount_agreed_receive, amount_received, amount_agreed_sent, amount_sent):
        self.round = round
        self.partner = partner
        self.amount_agreed_receive = amount_agreed_receive
        self.amount_received = amount_agreed_receive + amount_received
        self.amount_agreed_sent = amount_agreed_sent
        self.amount_sent = amount_agreed_sent + amount_sent
