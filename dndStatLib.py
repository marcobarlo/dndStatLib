import numpy as np;
import matplotlib.pyplot as plt;

def plotDensityList(input):
    strings=[]	
    for elem in input:
        strings.append('%d d%d' % (elem.getDiceNumber,elem.getDiceType))
        elem.plotDensity(False)
    plt.legend(strings)
    plt.show()
    
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
        y=self.cdf
        x=self.rollValues
        plt.stem(x,y,'C0-', 'C0o') 
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
        plt.stem(self.rollValues,self.distribution,'C0-')
        if(show==True):
            plt.show()
    def getMean(self):
        return self.mean
    def getVariance(self):
        return self.variance
    def roll(self):
        return 0
    def passDCprob(self,dc):
        if(dc>self.max):
            return 0;
        else:
            return (1-self.cdf[dc -self.nDice-1])
    
roll = DiceRoll(8,6)
print(roll.getPercentile(28))
print(roll.passDCprob(48))
roll.plotCdf()
roll.plotDensity()