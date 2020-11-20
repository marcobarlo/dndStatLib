import numpy as np
import matplotlib.pyplot as plt
import os
import discord
from dotenv import load_dotenv
import random


class DiceRoll:
    nDice = 0
    diceType = 0
    modifier = 0
    distribution = 0
    rollValues = 0
    cdf = 0
    mean = 0
    variance = 0
    min = 0
    max = 0

    def __init__(self, nDice=0, diceType=0, modifier=0):
        """ nDice is the number of dices to roll, diceType is the number of faces of the dice, modifier is the
        overall modifier to the score of the dice """
        if nDice != 0:
            self.nDice = [nDice]
            self.diceType = [diceType]
            self.modifier = modifier
            # compute the probability distribution of the roll
            distr = np.ones(diceType) / diceType
            unif = distr
            for i in range(1, nDice):
                distr = np.convolve(distr, unif)
            self.distribution = distr
            # compute the range values of the roll
            self.rollValues = np.arange(nDice, nDice * diceType + 1) + modifier
            # compute cdf
            self.cdf = np.cumsum(distr)
            # compute mean
            self.mean = np.dot(distr, self.rollValues)
            # compute variance
            self.variance = np.dot(distr, (self.rollValues - self.mean) ** 2)
            # compute max min
            self.max = nDice * diceType + modifier
            self.min = nDice + modifier

    def getModifier(self):
        return self.modifier

    def getDiceNumber(self):
        return self.nDice

    def getDiceType(self):
        return self.diceType

    def getDistribution(self):
        """gets the distribution function for the roll, use getRollValues to get the scores these distribution are
        paired with """
        return self.distribution

    def getRollValues(self):
        """gets the range of the possible scores for the roll, if you want to get the probability of every score use
        getDistribution, the values returned are paired with the rollValues vector """
        return self.getRollValues

    def getCdf(self):
        """gets the cumulative distribution function"""
        return self.cdf

    def getPercentile(self, score):
        """gets the percentile of the score for a roll, i.e. get the probability for a roll to be less or equal than
        the score"""
        if score > self.max:
            return 1
        elif score < self.min:
            return 0
        else:
            return self.cdf[score - self.min]

    def getMean(self):
        return self.mean

    def getVariance(self):
        return self.variance

    def roll(self):
        result = 0
        for j in range(len(self.nDice)):
            for i in range(self.nDice[j]):
                result += np.random.randint(1, self.diceType[j] + 1)
            result += self.modifier
        return result

    def plotDensity(self, show=True):
        x = np.random.randint(0, 10)
        plt.plot(self.rollValues, self.distribution, 'o-')
        # plt.stem(self.rollValues,self.distribution,'C'+str(x)+'-', 'C'+str(x)+'o' )
        if show:
            plt.show()

    def plotCdf(self, show=True):
        num = np.random.randint(0, 10)
        y = self.cdf
        x = self.rollValues
        # plt.stem(x,y,'C'+str(num)+'-', 'C'+str(num)+'o')
        plt.plot(x, y, 'o-')
        if show:
            plt.show()

    def probHigherOrEqualThan(self, value):
        if value > self.max:
            return 0
        elif value < self.min:
            return 1
        else:
            return 1 - self.cdf[value - self.min - 1]

    def compare(self, anotherRoll):
        return 0

    def __add__(self, anotherRoll):
        # check anotherRoll type
        roll = DiceRoll()
        distr = np.convolve(self.distribution, anotherRoll.distribution)
        roll.distribution = distr
        roll.max = self.max + anotherRoll.max + roll.modifier
        roll.min = self.min + anotherRoll.min
        roll.nDice = self.nDice + anotherRoll.nDice
        roll.diceType = self.diceType + anotherRoll.diceType
        roll.modifier = self.modifier + anotherRoll.modifier
        roll.rollValues = np.arange(roll.min, self.max + anotherRoll.max + 1)
        roll.cdf = np.cumsum(distr)
        roll.mean = np.dot(distr, roll.rollValues)
        roll.variance = np.dot(distr, (roll.rollValues - roll.mean) ** 2)
        return roll

    def printStats(self):
        print('Max: ' + str(self.max) + ' Min: ' + str(self.min) + ' Variance: ' + str(self.variance) + ' Mean: ' + str(
            self.mean))


class Roll20(DiceRoll):
    def __init__(self, modifier=0):
        super().__init__(1, 20, modifier)

    def probHit(self, ac):
        return super().probHigherOrEqualThan(ac)

    def probPassDC(self, dc):
        return super().probHigherOrEqualThan(dc)


def probHit(modifier, ac):
    r = Roll20(modifier)
    return r.probHit(ac)


def probPassDC(modifier, dc):
    r = Roll20(modifier)
    return r.probPassDC(dc)


def plotDensityList(inputl):
    strings = []
    for elem in inputl:
        strings.append('%d d%d +%d' % (elem.nDice, elem.diceType, elem.modifier))
        elem.plotDensity(False)
    plt.legend(strings)
    plt.show()


def main():
    # list = []
    # roll = DiceRoll(1, 10, 1)
    # list.append(roll)
    # roll = DiceRoll(1, 12)
    # list.append(roll)
    # roll = DiceRoll(2, 6)
    # list.append(roll)
    # plotDensityList(list)
    # distr = np.ones(8) / 8
    # unif = distr
    # unif2 = np.ones(4) / 4
    # distr = np.convolve(unif2, unif)
    # # distr= np.cumsum(distr)
    # rollValues = np.arange(2, 13)
    # plt.plot(rollValues, distr, 'o-')
    # plt.legend(['1d10+1', '1d12', '2d6', '1d8+1d4'])
    # plt.show()
    roll1 = DiceRoll(1, 8, 3)
    roll2 = DiceRoll(1, 4)
    rolls = roll1 + roll2
    for i in range(10):
        print(roll1.roll())
    # rolls.plotDensity()
    for i in range(10):
        print(rolls.roll())
    rolls.printStats()
    #start_bot
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

    client = discord.Client()

    @client.event
    async def on_ready():
        guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
        guild = discord.utils.get(client.guilds, name=GUILD)
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

    @client.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord server!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        brooklyn_99_quotes = ['I\'m the human form of the 💯 emoji.','Bingpot!',('Cool. Cool cool cool cool cool cool cool, ''no doubt no doubt no doubt no doubt.'),]

        if message.content == '99!':
            response = random.choice(brooklyn_99_quotes)
            await message.channel.send(response)
    client.run(TOKEN)

if __name__ == '__main__':
    main()
