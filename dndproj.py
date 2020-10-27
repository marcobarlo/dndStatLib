import numpy as np;
import matplotlib.pyplot as plt;
    
class DiceRoll:
    def __init__(self, nDice, diceType, modifier=0):
        #nDice is the number of dices to roll, diceType is the number of faces of the dice, modifier is the overall modifier to the score of the dice
        self.nDice= nDice
        self.diceType=diceType
        self.modifier=modifier
        #compute the probability distribution of the roll
        distr=np.ones(diceType)/diceType
        unif=distr
        for i in range(1,nDice):
            distr=np.convolve(distr,unif)
        self.distribution= distr
        #compute the range values of the roll
        self.rollValues= np.arange(nDice,nDice*diceType+1)+modifier
        #compute cdf
        self.cdf=np.cumsum(distr)
        #compute mean
        self.mean= np.dot(distr, self.rollValues)
        #compute variance
        self.variance= np.dot(distr, (self.rollValues - self.mean)**2)
        #compute max min
        self.max = nDice*diceType + modifier
        self.min = nDice + modifier

    def getModifier(self):
        return self.modifier
    def getDiceNumber(self):
        return self.nDice
    def getDiceType(self):
        return self.diceType
    def getDistribution(self):
        #gets the distribution function for the roll, use getRollValues to get the scores these distribution are paired with
        return self.distribution
    def getRollValues(self):
        #gets the range of the possible scores for the roll, if you want to get the probability of every score use getDistribution, the values returned are paired with the rollValues vector
        return self.getRollValues
    def plotCdf(self,show=True):
        num = np.random.randint(0,10)
        y=self.cdf
        x=self.rollValues
        plt.stem(x,y,'C'+str(num)+'-', 'C'+str(num)+'o') 
        if(show==True):
            plt.show()
    def getCdf(self):
        #gets the cumulative distribution function
        return self.cdf
    def getPercentile(self,score):
        #gets the percentile of the score for a roll, i.e. get the probability for a roll to be less or equal than the score
        if(score> self.max):
            return 1;
        elif(score < self.min):
            return 0;
        else:
            return self.cdf[score- self.nDice]     
    def plotDensity(self,show=True):	
        x = np.random.randint(0,10)
        plt.stem(self.rollValues,self.distribution,'C'+str(x)+'-', 'C'+str(x)+'o' )
        if(show==True):
            plt.show()
    def getMean(self):
        return self.mean
    def getVariance(self):
        return self.variance
    def roll(self):
        result=0
        for i in range(self.nDice):
            result+= np.randint(1, self.diceType+1)
        result+= self.modifier
        return result
    def probHigherOrEqualThan(self,value):
        if(value>self.max):
            return 0
        elif(value<self.min):
            return 1
        else:
            return (1-self.cdf[value -self.nDice - self.modifier -1])
    def compare(anotherRoll):
        return 0

class Roll20(DiceRoll):
    def __init__(self,modifier=0):
        super().__init__(1,20,modifier)
    def probHit(self,ac):
        return super().probHigherOrEqualThan(ac)
    def probPassDC(self,dc):
        return super().probHigherOrEqualThan(dc)

def probHit(modifier,ac):
    r = Roll20(modifier)
    return r.probHit(ac)
def probPassDC(modifier,dc):
    r = Roll20(modifier)
    return r.probPassDC(dc)
def plotDensityList(inputl):
    strings=[]	
    for elem in inputl:
        strings.append('%d d%d +%d' % (elem.nDice,elem.diceType, elem.modifier))
        elem.plotDensity(False)
    plt.legend(strings)
    plt.show()

#roll = DiceRoll(8,6)
#print(roll.getPercentile(28))
#print(probHit(10,22))
#roll.plotCdf()
#roll.plotDensity()
list=[]
roll= DiceRoll(5,4)
roll2= DiceRoll(2,3,4)
roll3= DiceRoll(7,4)
roll4= DiceRoll(2,3,9)
list.append(roll)
list.append(roll2)
list.append(roll4)
list.append(roll3)
plotDensityList(list)