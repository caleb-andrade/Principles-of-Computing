"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

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
    scores = {}
    for num in hand:
        if not scores.has_key(num):
            scores[num] = num
        else:
            scores[num] += num
    num = scores.keys()[0]
    for key in scores:
        if scores[key] > scores[num]:
            num = key        
    return scores[num]

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = [1 + idx for idx in range(num_die_sides)]
    temp = gen_all_sequences(outcomes, num_free_dice)
#    print '\nheld dice: ', held_dice
#    print 'endings to add: ', temp
    hands = []
    for item in temp:
#        print 'ending: ', item
        hands.append(tuple(sorted(held_dice + item)))
#    print '\nhands: ', hands
    score_sum = 0.0
    for hand in hands:
#        print '\nhand: ', hand
        score_sum += score(hand) 
#        print 'score: ', score(hand)
#        print 'accumulated score: ', score_sum
#    print '\nscore_sum / len(hands): ', score_sum, '/', len(hands)
#    print
    return score_sum / len(hands)

#print expected_value((1,), 6, 0)

def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    power_set = set([()])
    outcomes = [num for num in range(len(hand))]
    for length in range(len(hand)+1):
        ans = set([()])
        for dummy_idx in range(length):
            temp = set()
            for seq in ans:
                for item in outcomes:
                    if item not in seq:
                        new_seq = list(seq)
                        new_seq.append(item)
                        subset = tuple(sorted(new_seq))
                        temp.add(subset)
            ans = temp
        power_set.update(list(ans))
    
    tuples = set()
    for subset in power_set:
        temp = []
        for dummy_i in range(len(subset)):
            temp.append(hand[subset[dummy_i]])
        tuples.add(tuple(sorted(temp)))
#        print '\ntuple: ', tuple(sorted(temp))
            
    return tuples

#print gen_all_holds((1,))

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
#    print '\nCalculating all possible holds'
    hands = gen_all_holds(hand)
#    print '\nHands: ', hands
    max_exp = 0
    max_hand = ()
    for item in hands:
#        print 'Calculating expected value for hand: ', item
        exp = expected_value(item, num_die_sides, len(hand)-len(item)) 
#        print 'Expected value: ', exp        
        if exp > max_exp:
            max_hand = item
            max_exp = exp
            
    return (max_exp, max_hand)

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score

#print strategy((1,), 6)
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



