
def get_modifier(ability_score):
    # given an ability score, return the associated modifier
    return int(round(0.5*ability_score-5.25))

def avg_dice(dice):
    # returns avg of rolls given a D&D-style dice string - like '3d6+5', etc.
    dice,  add  = dice.split('+')
    rolls, size = map(float, dice.lower().split('d'))
    return int(round(rolls*(size/2.))) + int(add)

class Character(object):
    #def __init__(self, strength, dexterity, AC):
    def __init__(self, AC):
        #self.str = strength
        #self.dex = dexterity
        self.AC  = AC

class Weapon(object):
    def __init__(self, char, bab_dmg_pairs, dmg_dice, crit_range, crit_mult):  
        # bab_dmg_pairs should be [(bab, dmg_mult), ...]
        self.babs       = bab_dmg_pairs
        self.dmg_dice   = dmg_dice
        self.crit_range = crit_range # assumed to be lowest non-crit roll...
        self.crit_mult  = crit_mult
        self.dmg        = self.get_damage()
        self.crit_dmg   = self.get_crit_damage()

    def get_damage(self, ):
        return avg_dice(self.dmg_dice)

    def get_crit_damage(self, ):
        return self.crit_mult*self.get_damage()

    def get_hit_chances(self, enemy):
        # get chances to hit without critting
        hit_chances = []
        for bab,mult in self.babs:
            # figure out what would need to roll
            to_hit = enemy.AC - bab
            # figure out probability of rolling that or more
            hit_chance = max(0., min(1., 1.-(to_hit/float(self.crit_range))))
            hit_chances.append((hit_chance, mult))
        return hit_chances

    def get_crit_chances(self, enemy):
        # get chances to hit with critting
        crit_chances = []
        hit_chances = self.get_hit_chances(enemy)
        for i,(bab,mult) in enumerate(self.babs):
            to_hit = enemy.AC - bab
            chances = 1
            hits    = 1 # also account for natural 20
            # not guaranteed hit if not natural 20
            for roll in range(self.crit_range+1, 20):
                # i blame this on tiredness
                if roll >= to_hit: hits += 1
                chances += 1
            crit_chance = (float(hits)/chances) * (20-self.crit_range)/20.
            # just threat - need to roll again to hit!
            # should use current attack's bab, right?
            hit_chance,_ = hit_chances[i]
            crit_chance *= hit_chance
            crit_chances.append((crit_chance, mult))
        return crit_chances

    def get_DPR(self, enemy):
        # (hit chance without crit x hit damage) + (crit chance x crit damage)
        hit_chances  = self.get_hit_chances(enemy)
        crit_chances = self.get_crit_chances(enemy)
        dmg = 0
        for i in range(len(hit_chances)):
            hit_ch,  hit_mult  = hit_chances[i]
            crit_ch, crit_mult = crit_chances[i]
            dmg += self.dmg*hit_ch*hit_mult + self.crit_dmg*crit_ch*crit_mult
        return dmg
            
if __name__=='__main__':
    # calculate DPR in closed form way
    plain = Character(0)
    enemy = Character(21)
    #sword = Weapon(plain, [(12,1),(7,1)], '1d8+0', 17, 2)
    # NOTE: manyshot slightly high because only crits once
    # vanilla bow
    bow    = Weapon(plain, [(10,1),(5,1)], '2d4+0', 19, 3)
    # bow w/ rapid, manyshot
    bowrm  = Weapon(plain, [(8,2),(8,1),(3,1)], '2d4+0', 19, 3)
    # bow w/ deadly aim, manyshot
    bowdm  = Weapon(plain, [(8,2),(3,1)], '2d4+4', 19, 3)
    # bow w/ deadly aim, rapid shot
    bowdr  = Weapon(plain, [(6,1),(6,1),(1,1)], '2d4+4', 19, 3)
    # bow w/ deadly aim, manyshot, rapid shot
    bowdmr = Weapon(plain, [(6,2),(6,1),(1,1)], '2d4+4', 19, 3)
    # bow w/ precise shot, imp precise shot, deadly aim
    #bowpid = Weapon(plain, [(8,2),(8,1),(3,1)], '2d4+0', 19, 3)
    print 'bow:\t',bow.get_DPR(enemy)
    print 'bowrm:\t',bowrm.get_DPR(enemy)
    print 'bowdm:\t',bowdm.get_DPR(enemy)
    print 'bowdr:\t',bowdr.get_DPR(enemy)
    print 'bowdmr:\t',bowdmr.get_DPR(enemy)
    #print 'bowpid:\t',bowpid.get_DPR(enemy)
    
