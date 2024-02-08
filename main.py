from data import readPortfolio
import sys
from features.Tcmb import *

sys.path.insert(0, r'C:\Users\onurd\OneDrive\Masaüstü\PhD\codingPractices\fonAnaliz\tests\models')
from models.models import Currency, Fund



myTcmb = Tcmb(apiKey="xyh5URAL0e")
myTcmb.update_evds_data()

