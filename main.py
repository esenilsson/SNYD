
import operator
import random

class dice:
    def __init__(self):
        pass
    def roll(self):
        return random.randint(1,6)


class cup:
    def __init__(self, no_dice):
        self.dice_list = []

        for i in range(no_dice):
            self.dice_list.append(dice().roll())

    def remove_dice(self):
        self.dice_list.pop()

    def decision(self, last_call, q_matrix, no_dice_in_game):

        # Restrictions
        possible = {}
        multiplier, digit = last_call
        possible['up_mul'] = multiplier < no_dice_in_game
        possible['up_dig'] = (multiplier < no_dice_in_game) or (digit < 6)
        possible['up_safe'] = (multiplier < no_dice_in_game) or (digit < 6)
        possible['call_bluff'] = True

        if sum(v for k,v in q_matrix[last_call].items()) == 0:
            print(last_call, 'all zeroes')
            return random.choice([k for k, v in q_matrix[last_call].items() if possible[k]])
        else:
            #[v for k,v in q_matrix[last_call].items() if possible[k]]
            print(last_call, 'Take max')
            #print(max(q_matrix[last_call].items(), key=operator.itemgetter(1))[0])
            #print(q_matrix[last_call])
            return max(q_matrix[last_call].items(), key=operator.itemgetter(1))[0]



def make_call(decision, last_call, player):
    if decision == 'up_mul':
        multiplier = last_call[0]
        digit = last_call[1]
        return (multiplier +1, digit)
    elif decision == 'up_dig':
        multiplier = last_call[0]
        digit = last_call[1]

        if digit == 6:
            return (multiplier +1, 1)
        else:
            return (multiplier, digit + 1)
    elif decision == 'up_safe':
        multiplier = last_call[0]
        digit = last_call[1]
        player
        return (multiplier + 1, digit)


def call_bluff_success(last_call, players):
    dice_res = [d for p in players for d in p.dice_list]

    digit_called = last_call[1]
    if dice_res.count(digit_called) >= last_call[0]:
        return True
    else:
        return False


# Set up q_matrix
def all_alternatives(no_dice_in_game):
    alternatives = []
    for nd in range(no_dice_in_game):
        for dn in range(1, 7):
            alternatives.append((nd+1, dn))
    return alternatives



Q = {}
for alt in all_alternatives(20):
    Q[alt] = {'up_mul': 0, 'up_dig': 0, 'up_safe': 0, 'call_bluff': 0}



def get_reward(last_state, action, players):
    if action == 'call_bluff':
        if call_bluff_success(last_state, players):
            return 10
        else:
            return -5
    else:
        return 1



# Hyperparameters
alpha = 0.1
gamma = 0.6

for epoch in range(100000):
    no_dice_in_game = 20
    players = [cup(4) for x in range(5)]
    done = False
    i=0
    last_state = (random.randint(1,3), random.randint(1,6))
    last_action = 'up_dig'
    while(not done):
        player = players[i % len(players)]

        # State
        # Actions available
        # Player
        # Reward

        action = player.decision(last_state, Q, no_dice_in_game)
        state = make_call(action, last_state, player)

        # Reward from last step
        last_reward = get_reward(last_state, action, players)
        Q[last_state][last_action] = (1-alpha) * Q[last_state][last_action] + \
                                alpha * (last_reward + gamma * max(Q[last_state].values()))

        if action == 'call_bluff':
            done = True

        last_state = state
        last_action = action

        print(Q[(20,6)])
        i+=1



[print(k, sum(v.values())) for k,v in Q.items()]

player.decision()


