import random

roles_4 = ["OG", "OO", "CG", "CO"]  # For 4 players (2v2 Debate)
roles_8 = ["PM", "LO", "DPM", "DLO", "MG", "MO", "GW", "OW"]  # For 8 players (BP Debate)

def assign_roles(players):
    if len(players) == 4:
        random.shuffle(roles_4)  # Randomly assign roles for 4 players
        return dict(zip(players, roles_4))
    elif len(players) == 8:
        random.shuffle(roles_8)  # Randomly assign roles for 8 players
        return dict(zip(players, roles_8))

