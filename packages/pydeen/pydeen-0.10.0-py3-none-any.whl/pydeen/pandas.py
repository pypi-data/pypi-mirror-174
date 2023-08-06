"""
This module contains functions for integrating the pandas library
"""


import pandas as pd
#from pandas import pd.DataFrame

from pydeen.menu import UserInput
from pydeen.types import Result, Factory, Base
from pydeen.utils import FileTransferUtil

class PandasResultDataframe(Result):
    
    MENU_PANDAS_DISPLAY         = "pandas_display"
    MENU_PANDAS_INFO            = "pandas_info"
    MENU_PANDAS_RESULT_NAME     = "pandas_result_name"
    MENU_PANDAS_SET_DESC        = "pandas_set_desc"
    MENU_PANDAS_HEAD_TAIL       = "pandas_head_tail"
    MENU_PANDAS_DESCRIBE        = "pandas_describe"
    MENU_PANDAS_DATATYPES       = "pandas_datatypes"
    MENU_PANDAS_VALUE_DIST      = "pandas_value_dist"
    MENU_PANDAS_SAVE_CSV        = "pandas_save_csv"
    MENU_PANDAS_SAVE_XLS        = "pandas_save_xls"
    MENU_PANDAS_SAVE_PICKLE     = "pandas_save_pickle"
    MENU_PANDAS_LOAD_CSV        = "pandas_load_csv"
    MENU_PANDAS_LOAD_PICKLE     = "pandas_load_pickle"
    MENU_PANDAS_LOAD_XLS        = "pandas_load_xls"
    MENU_PANDAS_DATAHUB_EXPORT  = "pandas_export_datahub"
    MENU_PANDAS_DATAHUB_IMPORT  = "pandas_import_datahub"



    def __init__(self, name:str, df:pd.DataFrame=None) -> None:
        super().__init__(df)
        self.type = "pydeen.PandasResultDataFrame"
        self.result_df:pd.DataFrame = df 
        self.result_name:str = name
        self.menu_title = "Pandas DataFrame - Menu"

    def get_dataframe(self) -> pd.DataFrame:
        return self.result_df
        
    def get_description(self) -> str:
        if self.result_name != None:
            super_desc = super().get_description()
            if super_desc == None:
                return f"{self.result_name}"
            else:
                return f"{self.result_name} {super_desc}"    
        else:
            return super().get_description()

    def get_default_filename(self, default:str=None) -> str:
        result = self.result_name
        if result == None or result == "":
            result = default
        if result == None or result == "":
            result = "DataFrame"
        return result.replace("/", "x")

    def get_columns(self) -> list:
        try:
            return self.result_df.columns.tolist()
        except Exception as exc:
            self.trace(f"Error occured while determing columns of DataFrame: {type(exc)} - {exc}")
            return super().get_columns()

    def is_empty(self) -> bool:
        try:
            if type(self.result_df) == pd.DataFrame:
                return self.result_df.empty
            else:
                return True
        except Exception as exc:
            print("Error: ",type(exc), exc)
            return True

    def menu_get_entries(self, prefilled: dict = None) -> dict:
        entries = Base.menu_get_entries(self,prefilled)
        try:
            if type(self.result_df) == pd.DataFrame:
                entries[PandasResultDataframe.MENU_PANDAS_RESULT_NAME] = f"Rename dataframe ({self.result_name})"
                entries[PandasResultDataframe.MENU_PANDAS_SET_DESC] = f"Set description dataframe ({super().get_description()})"
                entries[PandasResultDataframe.MENU_PANDAS_DISPLAY] = "Display dataframe"
                entries[PandasResultDataframe.MENU_PANDAS_INFO] = "Display dataframe info"

                if not self.is_empty():
                    entries[PandasResultDataframe.MENU_PANDAS_HEAD_TAIL] = "Display dataframe head/tail"
                    entries[PandasResultDataframe.MENU_PANDAS_DESCRIBE] = "Describe dataframe"
                    entries[PandasResultDataframe.MENU_PANDAS_DATATYPES] = "Display dataframe types"
                    entries[PandasResultDataframe.MENU_PANDAS_VALUE_DIST] = "Show value distribution of column"
                    entries[PandasResultDataframe.MENU_PANDAS_SAVE_CSV] = "Save dataframe to csv file"
                    entries[PandasResultDataframe.MENU_PANDAS_SAVE_XLS] = "Save dataFrame to excel file"
                    entries[PandasResultDataframe.MENU_PANDAS_SAVE_PICKLE] = "Save dataframe to pickle file"
                    entries[PandasResultDataframe.MENU_PANDAS_DATAHUB_EXPORT] = "Export to Datahub"
            else:
                entries[PandasResultDataframe.MENU_PANDAS_LOAD_CSV] = "Load csv file"
                entries[PandasResultDataframe.MENU_PANDAS_LOAD_XLS] = "Load from dataframe excel file"
                entries[PandasResultDataframe.MENU_PANDAS_LOAD_PICKLE] = "Load from dataframe pickle file"
                entries[PandasResultDataframe.MENU_PANDAS_DATAHUB_EXPORT] = "Import from Datahub"
        except Exception as exc:
            self.error(f"errors occured in pandas df menu {exc}")
        
        return entries

    def menu_process_selection(self, selected: str, text: str = None):
        if selected == PandasResultDataframe.MENU_PANDAS_DISPLAY:
            print(self.result_df)
        elif selected == PandasResultDataframe.MENU_PANDAS_RESULT_NAME:
            new_name = UserInput("Enter new name for dataframe", self.result_name).get_input(empty_allowed=True)
            if new_name != None and len(new_name) > 0 and self.result_name != new_name:
                self.result_name = new_name
                print(f"dataframe renamed to {new_name}")
        elif selected == PandasResultDataframe.MENU_PANDAS_SET_DESC:
            new_desc = UserInput("Enter new description for dataframe", super().get_description()).get_input(empty_allowed=True)
            if new_desc != None and len(new_desc) > 0:
                self.set_description(new_desc)
                print(f"dataframe description set to {new_desc}")
        elif selected == PandasResultDataframe.MENU_PANDAS_INFO:
            print(self.result_df.info())
        elif selected == PandasResultDataframe.MENU_PANDAS_HEAD_TAIL:
            print(self.result_df.head())
            print(self.result_df.tail())
        elif selected == PandasResultDataframe.MENU_PANDAS_DESCRIBE:
            print(self.result_df.describe())
        elif selected == PandasResultDataframe.MENU_PANDAS_DATATYPES:
            print(self.result_df.dtypes)
        elif selected == PandasResultDataframe.MENU_PANDAS_VALUE_DIST:
            columns = self.get_columns()
            selected = UserInput("Select column").get_selection_from_list("Show value distribution for dataframe column", columns)
            if selected != None:
                print(f"values of column {selected}:")
                print(self.result_df[selected].value_counts())   
        elif selected == PandasResultDataframe.MENU_PANDAS_SAVE_CSV:
            result_name = self.get_default_filename()
            filename = FileTransferUtil().enter_filename_to_save("Save current dataframe to csv", result_name, "csv", use_datetime_prefix=True)
            if filename != None:
                self.result_df.to_csv(filename, sep="\t", index=False)
                print(f"dataframe saved to csv file {filename}")
        elif selected == PandasResultDataframe.MENU_PANDAS_SAVE_XLS:
            result_name = self.get_default_filename()
            filename = FileTransferUtil().enter_filename_to_save("Save current dataframe to excel", result_name, "xlsx", use_datetime_prefix=True)
            if filename != None:
                self.result_df.to_excel(filename, sheet_name='pydeen_dataframe', header=True, index = False)
                print(f"dataframe saved to excel file {filename}")
        elif selected == PandasResultDataframe.MENU_PANDAS_SAVE_PICKLE:
            result_name = self.get_default_filename("dataframe_pickle")                
            filename = FileTransferUtil().enter_filename_to_save("Save current dataframe as pickle file", result_name, "pkl", use_datetime_prefix=True)
            if filename != None:
                print(f"Start save dataframe pickle file as {filename}...", self.result_df, type(self.result_df))    
                self.result_df.to_pickle(filename)
                print(f"dataframe pickle file saved as {filename}")    
        
        elif selected == PandasResultDataframe.MENU_PANDAS_LOAD_PICKLE:                
            result_name = self.get_default_filename()
            filename = FileTransferUtil().enter_filename_to_load("Load dataframe from pickle file", name=result_name, extension="pkl")
            if filename != None:
                new_df = pd.read_pickle(filename)
                if type(new_df) != pd.DataFrame:
                    print("Loading pandas pickle file failed or cancelled")
                else:
                    self.result_df = new_df
                    print(f"dataframe pickle file loaded from {filename}")    
        elif selected == PandasResultDataframe.MENU_PANDAS_LOAD_CSV:                
            result_name = self.get_default_filename()
            filename = FileTransferUtil().enter_filename_to_load("Load dataframe from csv file", name=result_name, extension="csv")
            if filename != None:
                new_df = pd.read_csv(filename, sep="\t")
                if type(new_df) != pd.DataFrame:
                    print("Loading csv file into pandas dataframe failed or cancelled")
                else:
                    self.result_df = new_df
                    print(f"dataframe loaded from csv file {filename}")    

        elif selected == PandasResultDataframe.MENU_PANDAS_LOAD_XLS:                
            result_name = self.get_default_filename()
            filename = FileTransferUtil().enter_filename_to_load("Load dataframe from excel file", name=result_name, extension="xlsx")
            if filename != None:
                new_df = pd.read_excel(filename)
                if type(new_df) != pd.DataFrame:
                    print("Loading excel file into pandas dataframe failed or cancelled")
                else:
                    self.result_df = new_df
                    print(f"dataframe loaded from excel file {filename}")    
        elif selected == PandasResultDataframe.MENU_PANDAS_DATAHUB_EXPORT:
                if Factory.get_datahub().register_object_with_userinput(self) == True:
                    print("Pandas dataframe result exported to datahub.")
                else:
                    print("Pandas dataframe result not exported to datahub.")        
        elif selected == PandasResultDataframe.MENU_PANDAS_DATAHUB_IMPORT:
                try:
                    dh = Factory.get_datahub()
                    df_key = dh.menu_select_key("Select dataframe result object", PandasResultDataframe)
                    if df_key != None and df_key != "":
                        dh_object = dh.get_object(df_key)
                        self.result_df = PandasResultDataframe.get_pd.DataFrame(dh_object)
                        if self.result_df != None:
                            print("Pandas dataframe loaded from datahub.")
                            print(self.result_df.info())
                        else:
                            print("Pandas dataframe not loaded from datahub.")        
                except Exception as exc:
                    print(f"Loading from datahub failed: {type(exc)} - {exc}")    

        else:    
            return super().menu_process_selection(selected, text)    
