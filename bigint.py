

# bit of code for maintaining arbitrarily large integers as lists of digits
# was done in pseudocode as an interview question, so pretty minimal right now

# TODO:
# - allow signs
# - allow floats
# - allow math

class BigInt:

    def __init__(self, num):
        # Takes number as string. Why not maintain as string?
        # int() will take care of some bad inputs...want to handle locally?
        self.val = [int(n) for n in num]
        self.verify_val()
        self.clean_val()

    def __str__(self):
        return ("").join([str(i) for i in self.val])

    def __cmp__(self, other):
        # return -1 if self<other, 0 if self==other, positive if self>other
        pass
        
    def verify_val(self):
        # verify that val looks like a number
        pass

    def clean_val(self):
        # call various functions to clean up val
        self.strip_leading_zeros()

    def strip_leading_zeros(self):
        for i in range(1,len(self.val)):
            if self.val[i] != 0:
                if self.val[i-1] == 0:
                    # if (zero, nonzero), cut and break
                    self.val = self.val[i:]
                # break either way - because have (nonzero, nonzero) otherwise
                return
            # otherwise val[i] == 0, so continue
        # if get here, then we had a string of all 0s, so...clear everything?
        self.val = [0]
                
    def find_interior_negatives(self):
        # check to see if anything but the leading digit is negative
        pass




if __name__=="__main__":
    # run some tests
    n = BigInt("1234567890")
    print n

    # really big number
    n = BigInt("49681726398471239847687623478612374691872356791293847619283747")
    print n

    # make sure leading 0s get killed
    n = BigInt("000000000000100")
    print n

    # what happens if only 0?
    n = BigInt("000000000")
    print n
