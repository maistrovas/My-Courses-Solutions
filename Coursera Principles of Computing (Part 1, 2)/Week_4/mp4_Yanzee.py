"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""
#import codeskulptor
#codeskulptor.set_timeout(20)
import math
def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    distinct_hand = set()
    for cube in hand:
        distinct_hand.add(cube)
    result = []
    summ = 0
    for cube in distinct_hand:
        summ = 0
        for other_cube in hand:
            if cube == other_cube:
                summ += other_cube  
        result.append(summ)
    return max(result)
        
def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    die_sides = set()
    for _ in range(1, num_die_sides + 1):
        die_sides.add(_)
            # generate all posible permutation(eolls) of dice that steel ib the game
    future_possible_seq = gen_all_sequences(die_sides, num_free_dice)
    future_possible_seq = tuple(future_possible_seq)
            # generate scores of  all posible permutation
            # of roll + cubes that in hand result.
    full_possible_score = []
    for seq in future_possible_seq:
        full_possible_score.append(score(held_dice + seq))
    
    exp_val = float(sum(full_possible_score)) / len(full_possible_score)
    return exp_val

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand (sorted tuple)

    Returns a set of tuples, where each tuple is dice to hold
    """

    answer = [[]]
    for entery in hand:
        answer.extend([subset + [entery] for subset in answer])
    subsets = set()
    for elem in answer:
        subsets.add(tuple(elem))
    return subsets

#print gen_all_holds((1,2,3,4))

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    exp_hold_values = {}
    all_holds = tuple(gen_all_holds(hand))
    for hold in all_holds:
        num_free_dice = list(hand)
        for _ in hold:
            num_free_dice.remove(_)
        print num_free_dice
        value = expected_value(hold, num_die_sides, len(num_free_dice))   
        exp_hold_values[hold] = value
    best_value = max(exp_hold_values.values())
    for hold in exp_hold_values:
        if exp_hold_values[hold] == best_value:
            best_hold = hold
            break
    return (best_value, best_hold)

#print strategy((1,), 6)
def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
run_example()
print expected_value((1,2), 4,3)

# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)

    
