from data import readPortfolio
import sys

sys.path.insert(0, r'C:\Users\onurd\OneDrive\Masaüstü\PhD\codingPractices\fonAnaliz\tests\models')
from models.models import Currency

Currency.initializeCurrencies()
sys.stdout.reconfigure(encoding='utf-8')

class InitialTests:
    def test_initialization():
        for curr in Currency.currencyList:
            print(curr)
            print(repr(curr))

            
InitialTests.test_initialization()