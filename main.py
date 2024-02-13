import sys

from data import readPortfolio
from features.Tcmb import *

myTcmb = Tcmb(apiKey="xyh5URAL0e")
myTcmb.update_evds_data()
