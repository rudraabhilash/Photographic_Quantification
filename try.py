# print("Hello!")

# -Name(), size, price


# sum (pricei * sizei)/sum(sizei )


# def update(name, size, price)
# def getavgprice(name): -> ave price of that name
class Stockstat:

    def __init__(self):
        self.name = ''
        self.size = 0
        self.price = 0
        self.stockdict = {}
        self.sizelot = {}
    def update(self, name, size,price):
        self.name = name
        self.size = size
        self.price = price
        cum = 0
        if self.name in self.stockdict:
            cum += self.stockdict[self.name] + size*price
            self.sizelot[self.name] = self.sizelot[self.name]+self.size 
        else:
            self.stockdict[self.name] = size*price 
            self.sizelot[self.name] = size 
    def getavgprice(self, name):
        if name in self.stockdict:
            return self.stockdict[name]/self.sizelot[name]
        else:
            print('ticker do not exist yet')



data = [
    ('RIL', 100, 10 ),
    ('RIL', 100, 10 ),
    ('RIL', 100, 10 ),
]

while(1): #we are receiving stream
    Stockstat = Stockstat()
    stockstat.update('RIL', 100, 10)
    avg = stockstat.getavgprice('RIL')
    print('Avg price = ', avg)