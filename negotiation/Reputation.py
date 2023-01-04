from statistics import mean


class Reputation:
    def __init__(self, player_id, reputation_list):
        self.player_id = player_id
        self.reputation_list = reputation_list
        self.reputation_mean = mean(reputation_list)
