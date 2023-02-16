def check_offer_legal(sender, receiver, offers):
    open_offers = [o.offer_id for o in offers if not o.closed and sender.id_in_group == o.sender.id_in_group and receiver.id_in_group == o.receiver.id_in_group]
    if len(open_offers) > 0 or sender.agreed or receiver.agreed:
        return False
    else:
        return True


def check_acceptance_legal(offer):
    return not offer.sender.agreed and not offer.receiver.agreed and not offer.closed


def get_available_players(player, offers):
    exchange_agreed = [p.id_in_group for p in player.get_others_in_subsession() if p.agreed]
    offer_pending = [o.receiver.id_in_group for o in offers if o.sender.id_in_group is player.id_in_group and not o.closed]
    return [i for i in range(1, 7) if i not in exchange_agreed and i not in offer_pending and i is not player.id_in_group]


def all_agreed(player):
    exchange_agreed = [p.id_in_group for p in player.get_others_in_subsession() if not p.agreed]
    if len(exchange_agreed) == 0:
        return True
    else:
        return False


def get_sent_offers(player, offers):
    #print(offers)
    #print([[o.offer_id, o.receiver.id_in_group, o.offer, o.demand] for o in offers if o.sender.id_in_group is player.id_in_group and not o.closed])
    return [[o.offer_id, o.receiver.id_in_group, o.offer, o.demand] for o in offers if o.sender.id_in_group is player.id_in_group and not o.closed]


def get_open_offers(player, offers):
    #print(offers)
    #print([[o.offer_id, o.sender.id_in_group, o.offer, o.demand] for o in offers if o.receiver.id_in_group is player.id_in_group and not o.closed])
    return [[o.offer_id, o.sender.id_in_group, o.offer, o.demand] for o in offers if o.receiver.id_in_group is player.id_in_group and not o.closed]