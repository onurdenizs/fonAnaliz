import pandas as pd
from evds import evdsAPI 
from functools import total_ordering
import os

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
        
    def write_data_into_excel_file(fileName, sheetNameList, dataList, writingMode = "w"):
        """Writes list of data into excel sheets with given sheet names list
        Parameters
        ----------
        fileName : str
            filename without extension
        sheetsheetNameListName : list of str
            name of the sheet to write on in the excel file
        dataList : list of pandas.dataFrame
            data to be written on excel file
        writingMode : str
            default is 'w' for write mode, can be set equal to 'a' for append mode
        Returns
        -------
        
        """
        if len(dataList) == len(sheetNameList):
            for i in range (0,len(dataList)):
                if os.path.exists(fileName+".xlsx"):
                    with pd.ExcelWriter(fileName+".xlsx", mode='a', engine="openpyxl", if_sheet_exists="overlay") as writer:
                        dataList[i].to_excel(writer, sheet_name=sheetNameList[i])  
                else:
                    with pd.ExcelWriter(fileName+".xlsx") as writer:
                        dataList[i].to_excel(writer, sheet_name=sheetNameList[i])
        else:
            raise Exception("Element numbers in sheetNamesList and dataList should be equal!")

    
   
    def update_evds_data(apiKey):
        """Updates the excel file and sheets of the excel file according to the current EVDS data
        Parameters
        ----------
        apiKey : str
            Personal Api Key
        
        Returns
        -------

        """
        
        categoryData, columnLabelList = Category.get_category_infos_from_evds("xyh5URAL0e")
        groupData, columnLabelList2 = DataGroup.get_dataGroup_infos_from_evds("xyh5URAL0e") 
        serieData, columnLabelList3 = DataSerie.turn_csv_to_dataSeries_dataframe("Series.txt")
        myCategoryList = Category.return_dataFrame_into_category_list(categoryData,columnLabelList[0], columnLabelList[1], columnLabelList[2])
        myDataGroupList = DataGroup.return_dataFrame_into_dataGroup_list(groupData, columnLabelList2[0], columnLabelList2[1], columnLabelList2[2], columnLabelList2[3], columnLabelList2[4], columnLabelList2[5], columnLabelList2[6], columnLabelList2[7])
        updatedCategoryData = DataGroup.match_dataGroupList_items_with_Categories(myDataGroupList, categoryData)
        dataList = [updatedCategoryData, groupData, serieData]
        sheets = ["Categories", "Data Groups", "Data Series"]
        Tcmb.write_data_into_excel_file("EVDS", sheets, dataList)
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
    def return_category_list_into_dataFrame(categoryList):
        """Turns given list of category object into a dataFrame with columns (CATEGORY_ID, TOPIC_TITLE_ENG, TOPIC_TITLE_TR)
        
        Parameters
        ----------
        categoryList : list()
            list of Categories

        Returns
        -------
        data : pandas.dataFrame
            dataFrame with columns (CATEGORY_ID, TOPIC_TITLE_ENG, TOPIC_TITLE_TR)
        """
        idList = list()
        topicEng = list()
        topicTr = list()
        for category in categoryList:
            idList.append(category.id)
            topicEng.append(category.englishTitle)
            topicTr.append(category.turkishTitle)
        dict = {'CATEGORY_ID': idList, 'TOPIC_TITLE_ENG': topicEng, 'TOPIC_TITLE_TR': topicTr} 
        data = pd.DataFrame(dict)
        return data

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
        
    def format_dataGroup_dataFrame(data):
        """Formats given dataFrame of DataGroup infos in order it to have compatible Category ids' with Category class objects.
        
        Problem: when you get the DataGroup Info from EVDS as .csv file it returns category id's as "1" and not "1.0"
        But when you get the Category Info from EVDS category ids' come as "1.0, 2.0 etc"
        In order to get standard category ids with both classes this method does following steps:
        
        1.1) loops through data and checks each row of 'CATEGORY_ID' column if it contains '.'
        1.2) if not adds '.0' at the end of the CATEGORY_ID string
        """
        for i in range(0,len(data)):
            
            if "." not in data.loc[i, "CATEGORY_ID"]: #step 1.1

                dataString = data.loc[i, "CATEGORY_ID"] + ".0" 
                
                data.loc[i, "CATEGORY_ID"] = dataString #step 1.2
                   
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
        data = pd.read_csv("https://evds2.tcmb.gov.tr/service/evds/datagroups/key="+apiKey+"&mode=0&code=0&type=csv",dtype=str)
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
    
    def create_unnamed_categories_for_given_data_groups(categoryIdsToCreate):
        """Takes a list of categoryIds to create new Categories for this ids.
        Parameters
        ----------
        categoryIdsToCreate : list()
            list of Category ids to be created
        
        Returns
        ----------
        categotyList : list()
            list of newly created categories 
        """
        categotyList = list()
        for categoryId in categoryIdsToCreate:
            categotyList.append(Category(categoryId))
        return categotyList
    
    def match_dataGroupList_items_with_Categories(dataGroupList, categoryDataFrame):
        """Takes a list which contains DataGroup objects and adds each DataGroup object in the list
        to the object's category.dataGroupList
        Parameters
        ----------
        dataGroupList : list()
            list to be searched for categories and matched
        categoryDataFrame : pandas.dataFrame
            data frame of Category infos from EVDS
        
        Note: 

        categoryDataFrame variable will be updated just in case if you get a new category id  when you request Data Group info from EVDS.
        Reason: (08.Feb.2024) when you request all the Data Groups from EVDS as . csv file you get category id = 0 for some Data Groups.
        But when you request all the Category infos from EVDS as .csv you don't get any category with id = 0. But the data in category id is important. 
        So this category with id = 0 or any category which is not in the EVDS category list are created with this function.
        """
        categoryIdsToCreate = list()
        
        for grp in dataGroupList:
            cat, index = Category.get_category_by_id_in_a_list(grp.categoryId, Category.categoryList)
            if cat is not None:
                cat.dataGroupList.append(grp)
            else:
                foundCategory = grp.categoryId.replace(".0","")
                if foundCategory not in categoryIdsToCreate:
                    categoryIdsToCreate.append(foundCategory)
        categoryList = list()
        if len(categoryIdsToCreate) > 0:
            categoryList = DataGroup.create_unnamed_categories_for_given_data_groups(categoryIdsToCreate)
            newlyCreatedCategoryDataFrame = Category.return_category_list_into_dataFrame(categoryList)
            #print(newlyCreatedCategoryDataFrame["CATEGORY_ID"])
            data = pd.concat([newlyCreatedCategoryDataFrame, categoryDataFrame], ignore_index=True)
            columnList = list(categoryDataFrame.columns)
            
            return data
        else:
            return categoryDataFrame
            
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
         
         self.code = code
         self.dataGroupCode = dataGroupCode
         self.titleTr = titleTr
         self.titleEng = titleEng
         self.frqStr = frqStr
         self.aggMethod = aggMethod
         self.startDate = startDate
         self.endDate = endDate
         

    def get_dataSerie_infos_of_dataGroup(apiKey, dataGroupCode):
        """Gets Data Serie infos of given Data Group Code.
        Parameters
        ----------
        apiKey : str
            Personal Api Key
        dataGroupCode : str 
            unique Code of the data group that being interested 
            for example if you want to get all data series for data group cold "Gold Prices (Averaged) - Free Market (TRY) /Archive)", 
            then dataGroupCode should be given as 'bie_mkaltytl'
            
        
        Returns
        -------
        data : pandas.DataFrame
            dataFrame includes all the data Serie infos of related Data Group
        columnLabelList : list()
            list of the column labels
        """ 
        try:
            data = pd.read_csv("https://evds2.tcmb.gov.tr/service/evds/serieList/key="+apiKey+"&type=csv&code="+dataGroupCode)
        except pd.errors.EmptyDataError:
            data = "No DATA"
        return data
         
    def get_dataSerie_infos_from_evds(apiKey, dataGroupList, dropLabels = True):
        """Gets infos of all the Data Series listed in EVDS
        Parameters
        ----------
        apiKey : str
            Personal Api Key
        dataGroupList : list()
            List that counatains all the unique Data group codes in EVDS database
        dropLabels : boolean
            Not mandatory. Default value is True.
            drops following columns from the data recieved from EVDS:
            ["DEFAULT_AGG_METHOD_STR", "TAG", "TAG_ENG", "DATASOURCE", "DATASOURCE_ENG", "METADATA_LINK", "METADATA_LINK_ENG", "REV_POL_LINK", "REV_POL_LINK_ENG", "APP_CHA_LINK", "APP_CHA_LINK_ENG"]
        Returns
        -------
        data : pandas.DataFrame
            dataFrame includes all the dat Serie infos in EVDS
        """
        headerWriting = True
        dataList = list()
        fileName = "Series.txt"
        
        listFileName = "seriesList.txt"
        if os.path.exists(listFileName):
            f = open(listFileName, "r")
            serieReadLines = f.readlines()
            serieList = [line.rstrip() for line in serieReadLines]
            print("initially len serieList  = {0}".format(str(len(serieList))))
            f.close() 
        else:
            serieList = list()
        for group in dataGroupList:
            print("len serieList = {0}".format(str(len(serieList))))
            
            if group.code not in serieList:
                groupData = DataSerie.get_dataSerie_infos_of_dataGroup(apiKey, group.code)
                if not isinstance(groupData,str):
                    if dropLabels:
                        groupData = groupData.drop(["DEFAULT_AGG_METHOD_STR", "TAG", "TAG_ENG", "DATASOURCE", "DATASOURCE_ENG", "METADATA_LINK", "METADATA_LINK_ENG", "REV_POL_LINK", "REV_POL_LINK_ENG", "APP_CHA_LINK", "APP_CHA_LINK_ENG"],  axis= 'columns')
                    if os.path.exists(fileName):
                        headerWriting = False
                    groupData.to_csv(fileName, sep=';', header=headerWriting, index=False, mode='a', encoding='utf-8')
                    serieList.append(group.code)
                    f = open(listFileName, "a")
                    f.write(group.code+"\n")
                    f.close()
                    dataList.append(groupData)
        return dataList   
    def turn_csv_to_dataSeries_dataframe(filename): 
        data = pd.read_csv(filename, sep=";")
        columnLabelList = data.columns.values.tolist() 
        return data, columnLabelList
    def getDataSerie_with_code(dataSerieCode):
        """
        Gets a unique code to find the data Serie which this code belongs to
        for example if you want to Find the data serie called '(USD) US Dollar (Buying)' dataSerieCode should be: 'TP.DK.USD.A.YTL'
        Parameters
        ----------
        dataSerieCode : str
            unique data serie code (ex: TP.DK.USD.A.YTL)
        

        Returns
        -------
        dataSerie : DataSerie object
            if no data Serie object is found it returns none
        
        """
        data = pd.read_csv("Series.txt", sep=";")
        for i in range(0,len(data)):
            
            if data.loc[i,"SERIE_CODE"] == dataSerieCode:
                dataSerie = DataSerie(data.loc[i,"SERIE_CODE"],data.loc[i,"DATAGROUP_CODE"], data.loc[i,"SERIE_NAME"], data.loc[i,"SERIE_NAME_ENG"], data.loc[i,"FREQUENCY_STR"], data.loc[i,"DEFAULT_AGG_METHOD"], data.loc[i,"START_DATE"], data.loc[i,"END_DATE"])
                return dataSerie
           

    def get_data_from_evds_with_dataSerie_code(apiKey, dataSerieCode, startDay=None, startMonth=None, startYear=None, endDay=None, endMonth=None, endYear=None):
        """
        Gets a DataSerie object, and returns it's data as pandas.Dataframe object between given start date and end date.
        Parameters
        ----------
        apiKey : str
            Personal Api Key
        dataSerieCode : str
            unique code of Data Serie interested
        startDay : str
            day
        startMonth : str
            month
        startYear : str
            year
        endDay : str
            day
        endMonth : str
            month
        endYear : str
            year

        Returns
        -------
        data : pandas.DataFrame
        
        """
        dataSerie = DataSerie.getDataSerie_with_code(dataSerieCode)
        
        if dataSerie != None:
        
            if startDay == None:
                startDay = dataSerie.startDate[0:2]
            elif len(startDay) == 1:
                startDay = "0"+ startDay
            if startMonth == None:
                startMonth = dataSerie.startDate[3:5]
            elif len(startMonth) == 1:
                startMonth = "0" + startMonth
            if startYear == None:
                startYear = dataSerie.startDate[6:10]
            if endDay == None:
                endDay = dataSerie.endDate[0:2]
            elif len(endDay) == 1:
                endDay = "0"+ endDay
            if endMonth == None:
                endMonth = dataSerie.endDate[3:5]
            elif len(endMonth) == 1:
                endMonth = "0" + endMonth
            if endYear == None:
                endYear = dataSerie.endDate[6:10]
                
            sDate = startDay + "-" + startMonth + "-" + startYear
            eDate = endDay + "-" + endMonth + "-" + endYear
            evds = evdsAPI(apiKey) 
            data = evds.get_data([dataSerie.code], startdate=sDate, enddate=eDate)  
            return data
        else:
            return None
