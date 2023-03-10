from stats_api.models import Player


def calculater_player_score(player: Player, saves, passes, complete_passes, dribbles, blocks, interceptions, key_passes,
                            shots_on_target, chances_missed, post_hits, goals, own_goals, assists, yellow_cards,
                            red_cards):
    score = 5
    if player.post == 'GK':
        score += (saves * 0.2) + (complete_passes * 0.03) - ((passes - complete_passes) * 0.08) + (
                dribbles * 0.15) + (interceptions * 0.3) + (key_passes * 0.5) + (shots_on_target * 0.25) - (
                         chances_missed * 0.1) + (post_hits * 0.3) + (goals * 2.5) - (own_goals * 1) + (
                         assists * 1.8) - (yellow_cards * 0.4) - (red_cards * 1)
        if score > 10:
            return 10
        elif score < 0:
            return 0
        else:
            return score
    elif player.post == 'LB' or player.post == 'RB':
        score += (blocks * 0.2) + (complete_passes * 0.015) - ((passes - complete_passes) * 0.06) + (
                dribbles * 0.09) + (interceptions * 0.2) + (key_passes * 0.25) + (shots_on_target * 0.18) - (
                         chances_missed * 0.18) + (post_hits * 0.15) + (goals * 1.5) - (own_goals * 1) + (
                         assists * 1.3) - (yellow_cards * 0.4) - (red_cards * 1)
        if score > 10:
            return 10
        elif score < 0:
            return 0
        else:
            return score
    elif player.post == 'CB':
        score += (blocks * 0.15) + (complete_passes * 0.015) - ((passes - complete_passes) * 0.06) + (
                dribbles * 0.12) + (interceptions * 0.18) + (key_passes * 0.35) + (shots_on_target * 0.2) - (
                         chances_missed * 0.13) + (post_hits * 0.22) + (goals * 1.8) - (own_goals * 1) + (
                         assists * 1.3) - (yellow_cards * 0.4) - (red_cards * 1)
        if score > 10:
            return 10
        elif score < 0:
            return 0
        else:
            return score
    elif player.post == 'CDM':
        score += (blocks * 0.15) + (complete_passes * 0.013) - ((passes - complete_passes) * 0.05) + (
                dribbles * 0.12) + (interceptions * 0.15) + (key_passes * 0.30) + (shots_on_target * 0.18) - (
                         chances_missed * 0.13) + (post_hits * 0.2) + (goals * 1.7) - (own_goals * 1) + (
                         assists * 1.3) - (yellow_cards * 0.4) - (red_cards * 1)
        if score > 10:
            return 10
        elif score < 0:
            return 0
        else:
            return score
    elif player.post == 'CM' or player.post == 'RM' or player.post == 'LM':
        score = score + ((blocks * 0.2) + (complete_passes * 0.01) - ((passes - complete_passes) * 0.03) + (
                dribbles * 0.10) + (interceptions * 0.18) + (key_passes * 0.25) + (shots_on_target * 0.15) - (
                                 chances_missed * 0.15) + (post_hits * 0.18) + (goals * 1.6) - (own_goals * 1) + (
                                 assists * 1.3) - (yellow_cards * 0.4) - (red_cards * 1))
        if score > 10:
            return 10
        elif score < 0:
            return 0
        else:
            return score
    elif player.post == 'LW' or player.post == 'RW':
        score += (blocks * 0.22) + (complete_passes * 0.011) - ((passes - complete_passes) * 0.03) + (
                dribbles * 0.09) + (interceptions * 0.17) + (key_passes * 0.24) + (shots_on_target * 0.15) - (
                         chances_missed * 0.17) + (post_hits * 0.14) + (goals * 1.4) - (own_goals * 1) + (
                         assists * 1.3) - (yellow_cards * 0.4) - (red_cards * 1)
        if score > 10:
            return 10
        elif score < 0:
            return 0
        else:
            return score
    elif player.post == 'ST':
        score += (blocks * 0.24) + (complete_passes * 0.011) - ((passes - complete_passes) * 0.03) + (
                dribbles * 0.1) + (interceptions * 0.18) + (key_passes * 0.27) + (shots_on_target * 0.1) - (
                         chances_missed * 0.25) + (post_hits * 0.1) + (goals * 1.3) - (own_goals * 1) + (
                         assists * 1.3) - (yellow_cards * 0.4) - (red_cards * 1)
        if score > 10:
            return 10
        elif score < 0:
            return 0
        else:
            return score
    else:
        return 0
