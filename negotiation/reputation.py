from statistics import mean


class Reputation:
    def __init__(self, player_id, reputation_list):
        self.player_id = player_id
        self.reputation_list = list(filter(None, reputation_list))
        if len(self.reputation_list) == 0:
            self.reputation_mean = 0
        else:
            self.reputation_mean = mean(self.reputation_list)
