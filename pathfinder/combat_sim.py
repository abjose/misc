import random

"""
Simulate combat between two medium-sized combatants in Pathfinder 3.75.
All attacks are full-round.

Notes
-maybe randomly generate enemy stats in certain range?
-probably shouldn't simulate movement? do ranged and melee separately, and
 just give avg. DPR for two modes
"""

def get_modifier(ability_score):
    # given an ability score, return the associated modifier
    return int(round(0.5*ability_score-5.25))

def roll(dice, allow_zero=False):
    # returns sum of rolls given a D&D-style dice string - like '3d6', etc.
    rolls, size = map(int, dice.lower().split('d'))
    return sum([random.randint(1-allow_zero,size) for _ in range(rolls)])

class Character(object):
    def __init__(self, bab, strength, dexterity, AC):
        self.bab = bab
        self.strength = strength
        self.dex = dexterity
        self.AC  = AC
        
    def make_attack(self, enemy, weapon, modifier):
        # make attack(s)
        dmg = 0
        for b in self.bab:
            base_roll = roll('1d20')
            attack_roll = base_roll + b + modifier
            if base_roll == 20:
                dmg += self.critical_hit(weapon)
            elif attack_roll > enemy.AC:
                if attack_roll in weapon.crit_range:
                    dmg += self.critical_hit(weapon)
                else:
                    dmg += self.hit(weapon)
        return dmg

    def hit(self, weapon):
        # assumes should always apply strength modifier
        return weapon.deal_damage() + get_modifier(self.strength)
        
    def critical_hit(self, weapon):
        return sum([self.hit(weapon) for _ in range(weapon.crit_mult)])
                
    def make_melee_attack(self, enemy, weapon):
        #bab + Strength modifier
        return self.make_attack(enemy, weapon, get_modifier(self.strength))

    def make_ranged_attack(self, enemy, weapon):
        # tries to attack given enemy with given weapon; returns damage dealt
        # assumes target is in range
        return self.make_attack(enemy, weapon, get_modifier(self.dex))

    def randomize(self, bab_range, str_range, dex_range, AC_range):
        # randomize own stats within given ranges
        self.bab = [random.choice(bab_range)]
        self.strength = random.choice(str_range)
        self.dex = random.choice(dex_range)
        self.AC  = random.choice(AC_range)

class Weapon(object):
    def __init__(self, dmg_dice, dmg_bonus, crit_range, crit_mult):
        self.dmg_dice = dmg_dice
        self.crit_range = crit_range
        self.crit_mult  = crit_mult

    def deal_damage(self, ):
        return roll(self.dmg_dice)

if __name__=="__main__":
    me = Character([7,2], 20, 17, 25)
    char_manyshot_rapid = Character([7,7,7,2], 20, 12, 25)
    enemy = Character([0],0,0,0)
    bab_range = range(1)
    str_range = range(1)
    dex_range = range(1)
    AC_range  = range(15,26)
    longbow  = Weapon('1d8', 0, [20],         3)
    falchion = Weapon('2d4', 0, range(18,21), 2)

    rounds = 10000
    ranged_dmg = 0
    melee_dmg = 0
    for i in range(rounds):
        enemy.randomize(bab_range, str_range, dex_range, AC_range)
        ranged_dmg += char_manyshot_rapid.make_ranged_attack(enemy, longbow)
        #melee_dmg  += me.make_melee_attack(enemy,  falchion)

    print 'ranged avg:\t', ranged_dmg/float(rounds)
    print 'melee  avg:\t', melee_dmg/float(rounds)

    # normal  :      9.8  ranged, 11.5 melee
    # many/rap:      18.5 ranged
    # many/rap/dead: 
