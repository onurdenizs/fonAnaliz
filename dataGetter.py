import pandas as pd
from evds import evdsAPI 
from functools import total_ordering
import os
from features.Tcmb import *



class DataGetter:
    """this class establishes connections between local data files and EVDS online database systems
    """
    def initalizeDataSerie(TcmbObject):
        """
        """
        currentPath = os.getcwd()
        
        initialDataSerieCodeList = pd.read_csv(currentPath + "\initialSeries.txt",sep=";",dtype=str)
        codeList = initialDataSerieCodeList["SERIE_CODE"].to_list()

        
        for code in codeList:
            dataFilePath = currentPath+ "\\"+code+".txt"
            if os.path.isfile(dataFilePath):
                    print(code+".txt already exist, skipped")
            else:
                data = DataSerie.get_data_from_evds_with_dataSerie_code(TcmbObject.apiKey,code)
                if data.empty == False:
                    
                    data.to_csv(dataFilePath, sep=";")
        print("Series initialization Completed")
myTcmb = Tcmb(apiKey="xyh5URAL0e") 
DataGetter.initalizeDataSerie(myTcmb)     

        

