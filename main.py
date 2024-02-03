from data import readPortfolio
import sys

sys.path.insert(0, r'C:\Users\onurd\OneDrive\Masaüstü\PhD\codingPractices\fonAnaliz\tests\models')
from models.models import Currency, Fund

Currency.initializeCurrencies()
Fund.initializeFunds()
sys.stdout.reconfigure(encoding='utf-8')

class InitialTests:
    def test_initialization():
        print("\n-----------------------------")
        print("Printing Currency List:")
        print("-----------------------------")
        for curr in Currency.currencyList:
            print(curr)
            
        print("\n-----------------------------")
        print("Printing Fund List:")
        print("-----------------------------")

        for fund in Fund.fundList:
            print(fund)
        
    
    

InitialTests.test_initialization()