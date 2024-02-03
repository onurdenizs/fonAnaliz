import pandas as pd
def readPortfolio():
    df = pd.read_csv(r'C:\Users\onurd\OneDrive\Masaüstü\PhD\codingPractices\fonAnaliz\data\portfolio.txt', sep=";")

    print(df) 