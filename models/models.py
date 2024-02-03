class Instrument:
    
    def __init__(self, name, price, shortForm, symbol=None):
        """All instrument types (fund, currency etc.) will inherited from this class
        
        Parameters
        ----------
        name : str
            Name of the Instrument.
        price : float
           current price of the instrument in cents.
        shortForm : str
            3 letters short form of the instrument name
        symbol : str, optional
            symbol of the instrument
        
        """
        self.name = name
        self.currentPrice = price
        self.shortForm = shortForm
        self.symbol = symbol
    
class Fund(Instrument):
    
    fundId = 0 #id of the fund will be incremented by 1 on each fund creation
    fundList = list() # each created fund will be appended to the fundList()

    def __init__(self, name, price, shortForm, category, subCategory, organisation, symbol=None):
        super().__init__(name, price, shortForm, symbol)
        """Investment funds are modeled here. Inherited from Instrument Class.
        Parameters
        ----------
        name : str
            Name of the Instrument.
        price : float
           current price of the instrument in cents.
        shortForm : str
            3 letters short form of the instrument name
        category : str
            General Category of the investment fund
        subCategory : str
            Sub-Category of the investment fund
        organisation : str
            Owner of the fund
        symbol : str, optional
            symbol of the instrument
        
        """
        Fund.fundId += 1
        self.category = category
        self.subCategory = subCategory
        self.organisation = organisation
        self.id = Fund.fundId
        self.priceHistory = dict()
        Fund.fundList.append(self)

    def __str__(self):
        return f'Fund ID: {self.id} Name: {self.name} Current Price: {self.rate/100} Symbol: {self.symbol}'
    
    def __repr__(self):
        return f'Currency(\'{self.name}\', \'{self.code}\', {str(self.rate/100)})'
class Currency(Instrument):
    id = 0
    currencyList = list()

    def __init__(self, name, shortForm, price, symbol = None):
        """ Models currencies.
        Parameters
        ----------
        name : str
            Name of the Currency.
        code : str
            3 letters code of the currency.
        tl_rate : float
            Exchange rate to Turkish Lira (in cents)
        symbol : str, optional
            symbol of the Currency
        """
        super().__init__(name, price, shortForm, symbol)
        Currency.id += 1
        self.name = name
        self.code = shortForm
        self.rate = price
        self.symbol = symbol
        self.id = Currency.id
        Currency.currencyList.append(self)
    
    def __str__(self):
        return f'Currrency ID: {self.id} Name: {self.name} Current Rate: {self.rate/100} Symbol: {self.symbol}'
    
    def __repr__(self):
        return f'Currency(\'{self.name}\', \'{self.code}\', {str(self.rate/100)})'
    
    def initializeCurrencies():
        usDollars = Currency("US Dollar", "USD", 3049.07, "$")
        euro = Currency("Euro", "EUR", 3294.97, "€")
        tl = Currency("Turkish Lira", "TLR", 100.0, "₺")


