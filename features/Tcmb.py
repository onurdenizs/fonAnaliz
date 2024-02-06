import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from evds import evdsAPI 
from functools import total_ordering
pd.options.mode.copy_on_write = True

class Tcmb:
    def __init__(self, apiKey, categoryList = list()) -> None:
        """Class to serve as the main object in order to retrieve data from Turkish Republic Central Bank (TCMB)
        When a Tcmb object is created, 1 empty lists are created automatically as instance properties:
        categoryList
        Parameters
        ----------
        apiKey : str
            your Personal Api Key

        Note
        ----
            In order to get your personal api key you need to register TCMB's electronic data distrubiton system (EVDS)
            here is the link -> : https://evds2.tcmb.gov.tr/index.php?/evds/login

        Than:
        1) Login to the system
        2) Go to your profile Page
        3) Below the Update Profile box Find the -API Key- button and click on it
        4) Copy your personal API key and use it as the input argument when you instantiate a TCMB object

        """
        self.apiKey = apiKey
        self.categoryList = categoryList
        
        
    
    def getDataGroupInfo(self):
        """Returns all the info related to TCMB EVDS data Groups. These are the Data you can get from EVDS""" 
        data = pd.read_csv("https://evds2.tcmb.gov.tr/service/evds/datagroups/key="+self.apiKey+"&mode=0&type=csv")

        
         
        #print(ana_veri.head(20))
        
        #for i in range(0,len(ana_veri)):
        #    print("Index : "+str(i)+" " +str(ana_veri["DATAGROUP_NAME_ENG"].iloc[i]))
        return data
    def getDataNames(self):
        """Gets name of each Data Groups in TCMB EVDS"""
        ana_veri = self.getDataGroupInfo()
        groupNamesEng = ana_veri.columns
        return groupNamesEng
@total_ordering
class Category:
    """Data categories of EVDS data. EVDS data has a 3 level hierchical data architecture. 
        Categories are the top of the Hierarch level. Hierchical order can be summerised as follow:
        ----------------------------->
        Category (1)
            DaraGroup (X)
                DataSerie (A)
                DataSerie (B)
            DataGroup (Y)
                DataSerie (C)
                DataSerie (D)
                DataSerie (E)
                DataSerie (F)
        Category (2)
            .
            .
            .
        ----------------------------->
        Each category may have several Data Groups but a Data Group can be belong to only one Category.
        Similarly each Data Group can have multiple Data Series, but a Data Serie can only be belong to only one DataGroup.

        each EVDS data category has following 3 properties: 
        1) CATEGORY_ID (ex: 1.0)
        2) TOPIC_TITLE_ENG (ex: MARKET DATA (CBRT)) 
        3) TOPIC_TITLE_TR (ex: PİYASA VERİLERİ (TCMB))
    """
    categoryList = list()
    def __init__(self, evdsCategoryId, topicEng = None , topicTur = None) -> None:
        """Gets -CATEGORY_ID-, -TOPIC_TITLE_ENG-, -TOPIC_TITLE_TR-  parameters and creates a Category object
        Parameters
        ----------
        evdsCategoryId : str
            id of the data category in EVDS database (dataFrame column name = CATEGORY_ID)
        topicEng : str
            Title of the data category in EVDS database in English Language (dataFrame column name = TOPIC_TITLE_ENG)   
        topicTur : str
            Title of the data category in EVDS database in Turkish Language (dataFrame column name = TOPIC_TITLE_ENG)    
        
        Returns
        -------
        
        """
        if isinstance(evdsCategoryId, str) == False:
            evdsCategoryId = str(evdsCategoryId)
        
        self.dataGroupList = list()
        self.id = evdsCategoryId
        if topicEng is None:
            topicEng = "No Name CategoryID: " + self.id
        if topicTur is None:
            topicTur = "İsimsiz Kategori Id No: " + self.id
        self.englishTitle = topicEng
        self.turkishTitle = topicTur
        Category.categoryList.append(self)
    
    def __lt__(self, other): 
        return self.id<other.id 
  
    def __eq__(self, other): 
        return self.id == other.id 
  
    def __le__(self, other): 
        return self.id<= other.id 
      
    def __ge__(self, other): 
        return self.id>= other.id 
          
    def __ne__(self, other): 
        return self.id != other.id
    
    def get_category_infos_from_evds(apiKey):
        """Gets -CATEGORY_ID-, -TOPIC_TITLE_ENG-, -TOPIC_TITLE_TR-  infos of all the Categories listed in EVDS
        Parameters
        ----------
        apiKey : str
            Personal Api Key
        
        Returns
        -------
        data : pandas.DataFrame
            dataFrame includes all the topic titles in EVDS
        columnLabelList : list()
            list of the column labels
        """
        data = pd.read_csv("https://evds2.tcmb.gov.tr/service/evds/categories/key="+apiKey+"&type=csv")
        columnLabelList = data.columns.values.tolist()
        return data, columnLabelList
    def return_dataFrame_into_category_list(categoriesDataFrame, idColumnName, engTitleColumnName, turTitleColumnName):
        """Turns given dataFrame object which hold the data categories information(CATEGORY_ID, TOPIC_TITLE_ENG, TOPIC_TITLE_TR)
        into a list with categories
        
        Parameters
        ----------
        categoriesDataFrame : pandas.dataFrame
            dataFrame which holds category information
        idColumnName : str
            column name which holds category ID info
        engTitleColumnName : str
            column name which holds english title info
        turTitleColumnName : str
            column name which holds turkish title ID info
        
        Returns
        -------
        categoryList : list()
            list of created categories
        """
        categoryList = list()
        
        for i in range(0,len(categoriesDataFrame)):
            newCategory = Category(str(categoriesDataFrame[idColumnName].iloc[i]), str(categoriesDataFrame[engTitleColumnName].iloc[i]), str(categoriesDataFrame[turTitleColumnName].iloc[i]))
            categoryList.append(newCategory)

        return categoryList
    def get_category_by_id_in_a_list(evdsCategoryId, dataList):
        """Takes an id as string searches the category with that id and returns the found category if any.
        
        Parameters
        ----------
        evdsCategoryId : str
            id of the data category in EVDS database (dataFrame column name = CATEGORY_ID)
        categoryList : list()
            list that is searched to find the category
        
        Returns
        -------
        cat : Category() or None
            if category for the given id is found, returns that Category object
            else returns None
        index : int
            index of the found cat in the list
        """
        cat = None
        index = None
        for i in range(0,len(dataList)):
            if dataList[i].id == evdsCategoryId:
                cat = dataList[i]
                
                index = i
                break
        return cat, index
    def create_categories_from_id_list(categoryIdList):
        """Creates categories with the each category Id in the given list"""
class DataGroup:
    """Data Groups of each of EVDS data Category. Data Group is a sub-level of a Category. Data Group also 
       acts as the container of Data Series. Each Data Group belongs to a single category, and each Data Group can have
       more than one Data Serie. each Data Group has a unique property called data group code 
       (ex: 'Open Market Repo and Reverse Repo Transactions' Data Group's unique code is: 'bie_pyrepo')
        Data Greoup properties are:
        1) CATEGORY_ID (ex: 1.0)
        2) DATAGROUP_CODE (ex: bie_pyrepo)
        3) DATAGROUP_NAME (ex: Açık Piyasa Repo ve Ters Repo İşlemleri) 
        4) DATAGROUP_NAME_ENG (ex: Open Market Repo and Reverse Repo Transactions)
        5) FREQUENCY_STR (ex: AYLIK)
        6) FREQUENCY (ex: 9.0)
        7) START_DATE (ex: 01-05-1989 day-month-year)
        8) END_DATE (ex: 01-08-2020 day-month-year)
    """
    dataGroupList = list()
    def __init__(self, evdsCategoryId, code, nameTr, nameEng, frqStr, frq, startDate, endDate):
        """Gets 7 mandatory parameters for a DataGroup object and creates a DataGroup object
        Parameters
        ----------
        evdsCategoryId : str
            id of the data category in EVDS database (dataFrame column name = CATEGORY_ID)
        code : str
            Data Group code (evdsDataFrame[DATAGROUP_CODE])   
        nameTr : str
            Data Group Title in Turkish Langauge (evdsDataFrame[DATAGROUP_NAME]) 
        nameEng : str
            Data Group Title in English Langauge (evdsDataFrame[DATAGROUP_NAME_ENG]) 
        frqStr : str
            Data frequency in string (evdsDataFrame[FREQUENCY_STR]) 
        frq : str
            Data frequnecy in str(float) (evdsDataFrame[FREQUENCY]) 
        startDate : str
            Data Group start date in str(float) (evdsDataFrame[START_DATE])
        endDate : str
            Data Group end date in str(float) (evdsDataFrame[END_DATE])
        
        
        Returns
        -------
        
        """
        self.categoryId = evdsCategoryId
        self.code = code
        self.nameTr = nameTr
        self.nameEng = nameEng
        self.frqStr = frqStr
        self.frq = frq
        self.startDate = startDate
        self.endDate = endDate
        self.dataSerieList = list()
        DataGroup.dataGroupList.append(self)
    def get_category_of_dataGroup(self):
        pass
    
    def format_dataGroup_dataFrame(data):
        """formats given dataFrame of DataGroup infos in order it to have compatible Category ids' with Category class objects.
        
        Problem: when you get the DataGroup Info from EVDS as .csv file it returns category id's as "1" and not "1.0"
        But when you get the Category Info from EVDS category ids' come as "1.0, 2.0 etc"
        In order to get standard category ids with both classes this method does following steps:
        1) changes dataFrame's CATEGORY_ID columns data type to string
        2.1) loops through data and checks each row of 'CATEGORY_ID' column if it contains '.'
        2.2) if not adds '.0' at the end of the CATEGORY_ID string
        """
        
        data.loc[:, ["CATEGORY_ID"]] = data.loc[:, ["CATEGORY_ID"]].astype(str) #Step 1
        for i in range(0,len(data)):
            
            if "." not in data.loc[i, "CATEGORY_ID"]: #step 2.1

                dataString = data.loc[i, "CATEGORY_ID"] + ".0" 
                
                data.loc[i, "CATEGORY_ID"] = dataString #step 2.2
                
                             
    def get_dataGroup_infos_from_evds(apiKey, dropLabels = True):
        """Gets infos of all the Data Groups listed in EVDS
        Parameters
        ----------
        apiKey : str
            Personal Api Key
        dropLabels : Boolean (default value = True)
            
        
        Returns
        -------
        data : pandas.DataFrame
            dataFrame includes all the dataGroup infos in EVDS
        columnLabelList : list()
            list of the column labels
        """
        

        
        data = pd.read_csv("https://evds2.tcmb.gov.tr/service/evds/datagroups/key="+apiKey+"&mode=0&code=0&type=csv")
        if dropLabels:
            labelsToDrop = ["DATASOURCE", "DATASOURCE_ENG", "METADATA_LINK", "METADATA_LINK_ENG", "REV_POL_LINK", "REV_POL_LINK_ENG", "APP_CHA_LINK", "APP_CHA_LINK_ENG"]
            data = data.drop(labelsToDrop,  axis= 'columns')
        DataGroup.format_dataGroup_dataFrame(data)                    
        columnLabelList = data.columns.values.tolist() 
        return data, columnLabelList
    def return_dataFrame_into_dataGroup_list(dataGroupDataFrame, catIdColumnLabel, nameEngColumnLabel, endDateColumnLabel, startDateColumnLabel, nameTrColumnLabel, codeColumnLabel, frqColumnLabel, frqStrColumnLabel):
        
        """Turns given dataFrame object which hold the dataGroup information into a list with dataGroups
        
        Parameters
        ----------
        dataGroupDataFrame : pandas.dataFrame
            dataFrame which holds dataGroup information
        catIdColumnLabel : str
            column name which holds category ID info
        nameEngColumnLabel : str
            column name which holds english title info
        endDateColumnLabel : str
            column name which holds end date Info
        startDateColumnLabel : str
            column name which holds start date Info
        nameTrColumnLabel : str
            column name which holds Turkish title info
        codeColumnLabel : str
            column name which holds code Info
        frqColumnLabel : str
            column name which holds frequency Info
        frqStrColumnLabel : str
            column name which holds frequency string Info
        
        Returns
        -------
        dataGroupList : list()
            list of created dataGroups
        """
        dataGroupList = list()
        
        for i in range(0,len(dataGroupDataFrame)):
            newDataGroup= DataGroup(str(dataGroupDataFrame[catIdColumnLabel].iloc[i]), str(dataGroupDataFrame[codeColumnLabel].iloc[i]), str(dataGroupDataFrame[nameTrColumnLabel].iloc[i]), str(dataGroupDataFrame[nameEngColumnLabel].iloc[i]), str(dataGroupDataFrame[frqStrColumnLabel].iloc[i]), str(dataGroupDataFrame[frqColumnLabel].iloc[i]), str(dataGroupDataFrame[startDateColumnLabel].iloc[i]), str(dataGroupDataFrame[endDateColumnLabel].iloc[i]))
            dataGroupList.append(newDataGroup)

        return dataGroupList
    def get_data_groups_by_categoryId(evdsCategoryId, dataGroupList):
        """returns list of DataGroup objects which belong to the Category given by the evdsCategoryId.
        Parameters
        ----------
        evdsCategoryId : str(should be formatted like this"1.0")
            category ID to be searched
        dataGroupList : list()
            list which contains DataGroup objects
        Returns
        -------
        foundDataGorups : list()
            list of found dataGroups which belong to the Category interested
        """
        foundDataGorups = list()
        for grp in dataGroupList:
            if grp.categoryId == evdsCategoryId:
                foundDataGorups.append(grp)
        return foundDataGorups
    
    def match_dataGroupList_items_with_Categories(dataGroupList):
        """Takes a list which contains DataGroup objects and adds each DataGroup object in the list
        to the object's category.dataGroupList
        Parameters
        ----------
        dataGroupList : list()
            list to be searched for categories and matched
        """
        categoryIdsToCreate = list()
        zeroCategoryCounter= 0
        #print(len(Category.categoryList))
        #print(len(Category.categoryList[5].dataGroupList))
        

        for grp in dataGroupList:
            
            cat, index = Category.get_category_by_id_in_a_list(grp.categoryId, Category.categoryList)
            if grp.categoryId == "0.0":
                zeroCategoryCounter += 1
            if cat is not None:
                #print(index)
                #print(cat.turkishTitle)
                #print(Category.categoryList[index].turkishTitle)
                
                #print("Append yapmadan önce bu Category {0} length'i {1}".format(cat.turkishTitle, str(len(cat.dataGroupList))))
                cat.dataGroupList.append(grp)
                #Category.categoryList[index].dataGroupList.append(grp)
                #print("Append yaptıktan sonra bu Category {0} length'i {1}".format(cat.turkishTitle, str(len(cat.dataGroupList))))
            else:
                if grp.categoryId not in categoryIdsToCreate:
                    categoryIdsToCreate.append(grp.categoryId)
        for categoryId in categoryIdsToCreate:
            newCat = Category(categoryId)
        #print(len(Category.categoryList))
        #f or category in Category.categoryList:
        #    print(category.turkishTitle)
        #    print(len(category.dataGroupList))

        
    
class DataSerie:
    """DataSerie is the sub-category of a DataGroup. For each DataGroup there can be several DataSeries. 
    Each data serie has a unique code. For example: 'TP.MK.CUM.YTL' is the unique code of the data serie Cumhuriyet Gold Selling Price (TRY/Number) (Archive)
    DataSeries are the conatiners of actual data.
    
    Following are the most important properties of a DataSerie: 
    1) SERIE_CODE (ex: TP.MK.CUM.YTL)
    2) DATAGROUP_CODE (ex: bie_mkaltytl)
    3) SERIE_NAME (ex: Cumhuriyet Altını Satış Fiyatı (TL/Adet) (Arşiv))
    4) SERIE_NAME_ENG (ex: Cumhuriyet Gold Selling Price (TRY/Number) (Archive))
    5) FREQUENCY_STR (ex: AYLIK)
    6) DEFAULT_AGG_METHOD (ex: ORTALAMA)
    7) START_DATE (ex: 01-12-1950)
    8) END_DATE (ex: 01-10-2023)
    """
    id = 0
    def __init__(self, code, dataGroupCode, titleTr, titleEng, frqStr, aggMethod, startDate, endDate ) -> None:
         """Gets 8 mandatory parameters for a DataSerie object and creates a DataSerie object.
        
        Parameters
        ----------
        code : str
            unique code of the DataSerie itself (evdsDataFrame[SERIE_CODE])
        dataGroupCode : str
            unique code of the DataGroup which this DataSerie object belongs to (evdsDataFrame[DATAGROUP_CODE])   
        titleTr : str
            Data Serie Title in Turkish Langauge (evdsDataFrame[SERIE_NAME]) 
        titleEng : str
            Data Serie Title in English Langauge (evdsDataFrame[SERIE_NAME_ENG]) 
        frqStr : str
            Data frequency in string (evdsDataFrame[FREQUENCY_STR]) 
        aggMethod : str
            Data Serie aggregation method (evdsDataFrame[DEFAULT_AGG_METHOD]) 
        startDate : str
            Data Serie start date in str(float) (evdsDataFrame[START_DATE])
        endDate : str
            Data Serie end date in str(float) (evdsDataFrame[END_DATE])
       
        Returns
        -------
        
        """
         DataSerie.id += 1
         self.code = code
         self.dataGroupCode = dataGroupCode
         self.titleTr = titleTr
         self.titleEng = titleEng
         self.frqStr = frqStr
         self.aggMethod = aggMethod
         self.startDate = startDate
         self.endDate = endDate
         self.id = DataSerie.id
         
         
    def get_dataSerie_infos_from_evds(apiKey, dropLabels = True):
        pass    
a = Tcmb(apiKey="xyh5URAL0e")
data, columnLabelList = Category.get_category_infos_from_evds("xyh5URAL0e")
data2, columnLabelList2 = DataGroup.get_dataGroup_infos_from_evds("xyh5URAL0e") 
#print(data2["CATEGORY_ID"].iloc[-1])
#print(columnLabelList2)
#for col in data.columns:
#    print(col)




evds = evdsAPI('xyh5URAL0e') 
dat2 = evds.get_data(['TP.DK.USD.A.YTL','TP.MK.CUM.YTL'], startdate="01-01-2017", enddate="31-12-2018")  
cat = evds.main_categories
myCategoryList = Category.return_dataFrame_into_category_list(data,columnLabelList[0], columnLabelList[1], columnLabelList[2])
myDataGroupList = DataGroup.return_dataFrame_into_dataGroup_list(data2, columnLabelList2[0], columnLabelList2[1], columnLabelList2[2], columnLabelList2[3], columnLabelList2[4], columnLabelList2[5], columnLabelList2[6], columnLabelList2[7])
DataGroup.match_dataGroupList_items_with_Categories(myDataGroupList)

#anyCat = Category.get_category_by_id_in_a_list("2.0")
#print(anyCat.turkishTitle)
#print(len(myCategoyList[0].dataGroupList))
#print(myDataGroupList[1].categoryId)
#print(cat.head(5))


