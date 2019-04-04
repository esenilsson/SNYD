
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
            print('Zeroes for all', last_call)
            return random.choice([k for k, v in q_matrix[last_call].items() if possible[k]])
        else:
            print('Taking max')
            [v for k,v in q_matrix[last_call].items() if possible[k]]

            return max(q_matrix[last_call].items(), key=operator.itemgetter(1))[0]



def make_call(decision, last_call):
    print(decision, last_call)
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



players = [cup(4) for x in range(5)]
no_dice_in_game = 20
decisions = []
calls = []
last_decision = (1,1)

# Hyperparameters
alpha = 0.1
gamma = 0.6

for epoch in range(100):
    for i in range(100):
        player = players[i%len(players)]
        decision = player.decision(last_call, Q, no_dice_in_game)

        decisions.append(decision)
        if decision == 'call_bluff':
            # Here i need to assess whether it was a positive reward or negative
            if call_bluff_success(last_call, players):
                Q[last_call][decision] = (1 - alpha) * Q[last_call][decision] + alpha * (1)
            else:
                Q[last_call][decision] = (1 - alpha) * Q[last_call][decision] + alpha * (-1)
            break

        call = make_call(decision, last_call)
        calls.append(call)


        # If not call_bluff then it means that previous call was success
        # Q(state, action) = (1-alpha) * q(state, action) + alpha*(reward + sigma*max (Q(next_state, all_actions)))
        Q[last_call][decision] = (1-alpha) * Q[last_call][decision] + alpha * (1 + gamma * max(Q[call].values()))

        # Update Q
        last_decision = decision
        last_call = call













# What are states
- Number of dice in game
- Last call

# Actions
- Call bluff
- New call
    - Increase one mulitplier
    - Increase number
    - Other???
    - Play safe, only what you have


# Reward is dependent on next players choice
- if they make new call, then +1
- if they call bluff:
    - if current_player did not meet



