
import operator
import random
import ast
class dice:
    def __init__(self):
        self.eye = random.randint(1,6)

    def roll(self):
        self.eye = random.randint(1,6)

class cup:
    def __init__(self, no_dice):
        self.dice_list = []

        for i in range(no_dice):
            self.dice_list.append(dice())

    def remove_dice(self):
        self.dice_list.pop()

    def roll(self):
        for i in self.dice_list:
            i.roll()



class player:
    def __init__(self, start_no_dice):
        self.number_of_dice = start_no_dice
        self.cup = cup(start_no_dice)

    def remove_dice(self):
        self.number_of_dice -= 1
        self.cup.remove_dice()

    def roll(self):
        self.cup.roll()

    def decision(self, last_call, Q, no_dice_in_game):
        if sum(v for k,v in Q[no_dice_in_game][last_call].items()) == 0:
            return random.choice([k for k, v in Q[no_dice_in_game][last_call].items()])
        else:
            return max(Q[no_dice_in_game][last_call].items(), key=operator.itemgetter(1))[0]

    def get_eyes(self):
        dice_eyes = []
        for d in self.cup.dice_list:
            dice_eyes.append(d.eye)
        return dice_eyes

def call_bluff_success(last_call, players):
    dice_res = [d for p in players for d in p.get_eyes()]

    digit_called = last_call[1]
    if dice_res.count(digit_called) >= last_call[0]:
        return True
    else:
        return False

def get_reward(last_state, action, players):
    if action == 'call_bluff':
        if call_bluff_success(last_state, players):
            return 20
        else:
            return -50
    else:
        return 1

# Set up q_matrix
def get_all_alternatives(no_dice_in_game):
    alternatives = []
    for nd in range(no_dice_in_game):
        for dn in range(1, 7):
            alternatives.append((nd+1, dn))
    return alternatives

def get_all_possible_alternatives(no_dice_in_game):
    Q = {}
    for state_1 in get_all_alternatives(no_dice_in_game):
        multiplier_1, digit_1 = state_1
        Q_inner = {}
        for state_2 in get_all_alternatives(no_dice_in_game):
            multiplier_2, digit_2 = state_2
            if multiplier_2 > multiplier_1 or (multiplier_2 == multiplier_1 and digit_2 > digit_1):
                Q_inner[state_2] = 0
        Q_inner['call_bluff'] = 0
        Q[state_1] = Q_inner
    return Q

def get_all_possible_states_for_different_dice(dice_tots):
    Q = {}
    for d in dice_tots:
        Q[d] = get_all_possible_alternatives(d)
        Q[d]['call_bluff'] = {'call':0, 'bluff':0}
    return Q


Q = get_all_possible_states_for_different_dice([20,16,12,8,7,6,5,4,3,2])





# Hyperparameters
alpha = 0.1
gamma = 0.6
players = [player(4) for x in range(5)]


for epoch in range(100000):
    no_dice_in_game = 20
    i=0
    last_state = (random.randint(1,3), random.randint(1,6))

    #while all([p.number_of_dice > 0 for p in players]):

    while(last_state != 'call_bluff'):
        current_player = players[i % len(players)]
        current_state = current_player.decision(last_state, Q, no_dice_in_game)

        # Reward from last step
        last_reward = get_reward(last_state, current_state, players)

        # All remove dice except loser
        # if last_reward < 0:
        #     loser_idx = (i-1) % len(players)
        # else:
        #     loser_idx = i%len(players)
        #
        # for idx, pl in enumerate(players):
        #     if idx != loser_idx:
        #         pl.remove_dice()


        Q[no_dice_in_game][last_state][current_state] = (1-alpha) * Q[no_dice_in_game][last_state][current_state] + \
                                alpha * (last_reward + gamma * max(Q[no_dice_in_game][current_state].values()))

        last_state = current_state
        i+=1

#
# [print(k, sum(v.values())) for k,v in Q[20].items()]
#
#
#
# # Play
# no_dice_in_game = 20
# players = [cup(4) for x in range(5)]
# i = 0
# last_state = (random.randint(1, 3), random.randint(1, 6))
#
#
# while (last_state != 'call_bluff'):
#     player = players[i % len(players)]
#     if i%len(players) == 1:
#         current_state = ast.literal_eval(input('What is your move?'))
#     else:
#         current_state = player.decision(last_state, Q, no_dice_in_game)
#     print('from ',last_state, ' to ', current_state)
#
#     # Reward from last step
#     last_reward = get_reward(last_state, current_state, players)
#     print('player',i-1, ' got:', last_reward)
#     last_state = current_state
#     i += 1
