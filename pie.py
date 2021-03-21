#
# Attempts to calculate price of utility for two players
#

benefit_A = int(input("Benefit to player A: "))
benefit_B = int(input("Benefit to player B: "))
cost_of_utility= int(input("Utility cost: "))

#
# If the party would pay on its own, then it pays
# half-a-pie less than that amount. Otherwise,
# it pays half-a-pie less than its gross benefit
#
def player_act_solo(benefit):
    if cost_of_utility > benefit:
        return False
    else:
        return True

#
# Pie = what two parties can get if working together vs
# what they can achieve if acting on their own.
#
# (benefit_together_a + benefit_together_b) - (benefit_on_own_a + benefit_on_own_b) = pie
#
# If cost of utility is > than benefit for one of the parties,
# it does NOT mean than pie suddenly disappears.
#
def pie():
    if player_act_solo(benefit_A) and player_act_solo(benefit_B):
        benefit_own = (benefit_A - cost_of_utility) + (benefit_B - cost_of_utility)
        print(1)

    elif player_act_solo(benefit_A) and not player_act_solo(benefit_B):
        benefit_own = benefit_A - cost_of_utility
        print(2)

    elif player_act_solo(benefit_B) and not player_act_solo(benefit_A):
        benefit_own = benefit_B - cost_of_utility
        print(3)

    else:
        raise RuntimeError("Check the input...")

    benefit_together = (benefit_A + benefit_B) - cost_of_utility
    pie = benefit_together - benefit_own
    print("Value on their own: %s" % (benefit_own))
    print("Value on together: %s" % (benefit_together))
    print("Pie: %s" % (pie))

pie()
#  print("\nPlayer A should pay %s\nPlayer B should pay %s" % (str(pie_A), str(pie_B)))
