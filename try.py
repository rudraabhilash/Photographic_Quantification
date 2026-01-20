# print("Hello!")

# -Name(), size, price


# sum (pricei * sizei)/sum(sizei )


# def update(name, size, price)
# def getavgprice(name): -> ave price of that name
class vwap:
	def __init__(self):
		Self.sumPriceSize = {}
		Self.sumSize = {}
	def update(self, name, price, size):
		if name not in self.sumPriceSize:
            self.sumPriceSize[name] = 0
            self.sumSize[name] = 0
        self.sumPriceSize[name] += price * size
        self.sumSize[name] += size
    def getavgprice(self, name):
        if name not in self.sumPriceSize:
            return None
        return self.sumPriceSize[name]/self.sumSize[name]


        
