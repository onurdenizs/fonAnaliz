class Instrument:
    
    def __init__(self, name,  shortForm, symbol=None):
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
        
        self.shortForm = shortForm
        self.symbol = symbol
    
class Fund(Instrument):
    
    fundId = 0 #id of the fund will be incremented by 1 on each fund creation
    fundList = list() # each created fund will be appended to the fundList()

    def __init__(self, name, price, shortForm, category, subCategory, organisation, symbol=None):
        super().__init__(name,  shortForm, symbol)
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
        self.price = price
        self.category = category
        self.subCategory = subCategory
        self.organisation = organisation
        self.id = Fund.fundId
        self.priceHistory = dict()
        Fund.fundList.append(self)

    def __str__(self):
        return f'Fund ID: {self.id} Name: {self.name} Fund Category: {self.category} Managing Organisation: {self.organisation} Current Price: {self.currentPrice/100} Symbol: {self.symbol}'
    
    def __repr__(self):
        return f'Fund(\'{self.name}\', {self.currentPrice/100}, \'{self.shortForm}\', \'{self.category}\', \'{self.subCategory}\', \'{self.organisation}\')'
    
    def initializeFunds():
        """Initializes FOLLOWING 9 Portfolio Funds: MAC, AFA, YAS, YBE, TKF, AFV, YKT, YAY, YZG"""
        MAC = Fund("Marmara Capıtal Portföy Hisse Senedi (TL) Fonu (Hisse Senedi Yoğun Fon)", 47, "MAC", "Hisse Senedi Fonları", "", "Marmara Capital Portföy")
        AFA = Fund("Ak Portföy Amerika Yabancı Hisse Senedi Fonu", 51, "AFA", "Hisse Senedi Fonları", "", "Ak Portföy")
        YAS = Fund("Yapı Kredi Portföy Koç Holding İştirak ve Hisse Senedi Fonu (Hisse Senedi Yoğun Fon)", 1107, "YAS", "Hisse Senedi Fonları", "", "Yapı Kredi Portföy")
        YBE = Fund("YYapı Kredi Portföy Eurobond (Dolar) Borçlanma Araçları Fonu", 93, "YBE", "Borçlanma Araçları Fonları", "", "Yapı Kredi Portföy")
        TKF = Fund("Tacirler Portföy Hisse Senedi Fonu (Hisse Senedi Yoğun Fon)", 3710, "TKF", "Hisse Senedi Fonları", "", "Tacirler Portföy")
        AFV = Fund("Ak Portföy Avrupa Yabancı Hisse Senedi Fonu", 27, "AFV", "Hisse Senedi Fonları", "", "Ak Portföy")
        YKT = Fund("Yapı Kredi Portföy Altın Fonu", 28, "YKT", "Kıymetli Madenler Fonları", "", "Yapı Kredi Portföy")
        YAY = Fund("Yapı Kredi Portföy Yabancı Teknoloji Sektörü Hisse Senedi Fonu", 63143, "YAY", "Hisse Senedi Fonları", "", "Yapı Kredi Portföy")
        YZG = Fund("Yapı Kredi Portföy Gümüş Fon Sepeti Fonu", 320, "YZG", "Fon Sepeti Fonları", "", "Yapı Kredi Portföy")

class Currency(Instrument):
    id = 0
    currencyList = list()

    def __init__(self, name, shortForm, buyingPrice, sellingPrice, symbol = None):
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
        super().__init__(name, shortForm, symbol = "",  buyingPrice = None, sellingPrice = None)
        Currency.id += 1
        self.name = name
        self.buyingPrice = buyingPrice
        self.sellingPrice = sellingPrice
        self.code = shortForm
        self.symbol = symbol
        self.valueHistory = dict()
        self.id = Currency.id
        Currency.currencyList.append(self)
    def initializeCurrencyTypes():
        pass
    
    def __str__(self):
        return f'Currrency ID: {self.id} Name: {self.name} Current Rate: {self.rate/100} Symbol: {self.symbol}'
    
    def __repr__(self):
        return f'Currency(\'{self.name}\', \'{self.code}\', {str(self.rate/100)})'
    
    def initializeCurrencies():
        """Intializes USD, Euro and Turkish Lira Currency Types"""
        usDollars = Currency("US Dollar", "USD", 3049.07, "$")
        euro = Currency("Euro", "EUR", 3294.97, "€")
        tl = Currency("Turkish Lira", "TLR", 100.0, "₺")

class Portfolio:
    id = 0
    portfolioList = list()

    def __init__(self, name):
        """This class will Simulate Portfolios where all the investment
        instruments are hold
        Parameters
        ----------
        name : str
            Name of the Portfolio.
        """
        Portfolio.id += 1
        self.name = name
        self.instrumentList = list()
        self.valueHistory = list()
        self.currentValue = 0
        self.valueHistory = dict()


