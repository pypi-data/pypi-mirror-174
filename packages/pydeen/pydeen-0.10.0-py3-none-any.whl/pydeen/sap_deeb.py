"""
    SAP NetWeaver ABAP features based on abapGit Addon DEEB
"""

from re import S
import numpy
import pandas as pd 
import json

from pydeen.types import Backend, Factory, Result
from pydeen.http import HTTPConnector
from pydeen.menu import  UserInput
from pydeen.sap_abap import SAPAbapHttpBackend
from pydeen.pandas import PandasResultDataframe
from pydeen.exits import MenuExit, MenuExitCallback
#from pandas import DataFrame
#from datetime import datetime, timedelta, timezone


class SAPAbapDeebResult(Result):
    def __init__(self, result, metainfo=None) -> None:
        super().__init__(result)
        self.type = "pydeen.SAPAbapDeebResult"
        self.metainfo = metainfo


class SAPAbapDeebConnector(HTTPConnector, MenuExitCallback):
    
    # static constants
    MENU_PING               = "ping"
    MENU_SEARCH_TABLE       = "search_table"
    MENU_SEARCH_VIEW        = "search_view"
    MENU_SEARCH_CDS         = "search_cds"
    MENU_SQL_SELECT         = "sql_select"
    MENU_RESULT_RAW         = "result_raw"
    MENU_RESULT_MENU        = "result_menu"
    MENU_RESULT_PANDAS      = "result_pandas"
    MENU_PANDAS_MENU        = "pandas_menu"
    MENU_PANDAS_TEMPLATE    = "pandas_create_template"
    MENU_PANDAS_EXPORT_ZTAB = "pandas_export_ztab"
    MENU_PANDAS_IMPORT      = "pandas_import"
    MENU_DATAHUB_MENU       = "datahub_menu"
    MENU_DATAHUB_IMPORT     = "datahub_import"
    MENU_RESET              = "reset"
    
    SAP_INVALID_FIELD_NAMES = ["KEY", "COUNT"] 
    SAP_FIELDNAME_MAX_LEN   = 30

    def __init__(self, backend:Backend=None, url_or_endpoint:str=""):
        url = url_or_endpoint
        if url == None or len(url) == 0:
            url = '/sap/bc/bsp/sap/zdeeb_ws'
            
        super().__init__(backend, url)
        self.type = "pydeen.SAPAbapDeebConnector"
        self.menu_result:Result   = None
        self.menu_title = "SAP ABAP DEEB Connector - Menu"
        self.menu_result_pd:PandasResultDataframe = None
        self.max_rec = 10000
        self.last_input = None
        
    def get_sap_fieldname(self, column_name:str) -> str:
        """generates a SAP fieldname from given column name. CamelCase will be transformed to typical sap name convention

        :param column_name: a colum name like MyColumnName
        :type column_name: str
        :return: a field name for SAP usage
        :rtype: str
        """
        result = ""
        last_char_lower = False
        for char in column_name:
            upper_char = char.upper()
            if upper_char == char:
                char_is_lower = False
            else:
                char_is_lower = True

            if last_char_lower == True and char_is_lower == False:
                result += "_"

            result += upper_char
            last_char_lower = char_is_lower
        
        result = result.replace("__", "_")
        
        # find invalid key names
        if result in SAPAbapDeebConnector.SAP_INVALID_FIELD_NAMES:
            old_result = result
            result = f"REC_{result}"
            self.trace(f"Invalid SAP fieldname found '{old_result}'. Modified to '{result}'.")
            
        
        # shorten long fieldnames delete chars
        DELETE_CHARS = "AEIOU"
        if len(result) > SAPAbapDeebConnector.SAP_FIELDNAME_MAX_LEN:
            old_result = result
            for char_del in DELETE_CHARS:
                result = result.replace(char_del,"")
            if old_result != result:
                self.trace(f"SAP fieldname too long '{old_result}'. Delete some characters to '{result}'.")

        # split and keep only first chars
        if len(result) > SAPAbapDeebConnector.SAP_FIELDNAME_MAX_LEN:
            old_result = result
            splitted = result.split('_')
            result =  ""
            for part in splitted:
                if len(result) > 0:
                    result = result + "_"
                
                if len(part) > 3:
                    result = result + part[:3]
                else:
                    result = result + part
            if old_result != result:
                self.trace(f"SAP fieldname too long '{old_result}'. Shorten parts to '{result}'.")

        # last try - shorten to 30 and accept duplicates
        if len(result) > SAPAbapDeebConnector.SAP_FIELDNAME_MAX_LEN:
            old_result = result
            result = result[:SAPAbapDeebConnector.SAP_FIELDNAME_MAX_LEN]
            if old_result != result:
                self.trace(f"SAP fieldname too long '{old_result}'. Shortened to '{result}'. Check for duplicates")

        return result    

    def get_df_result_as_list_of_dict(self, result_df:PandasResultDataframe, map_fieldname_to_sap:bool=True) -> list:
        # prepare access
        result = []
        df = result_df.get_dataframe()
        cols = result_df.get_columns()

        # prepare mapping
        cols_map = {}
        for col in cols:
            col_mapped = col
            if map_fieldname_to_sap:
                col_mapped = self.get_sap_fieldname(col)
            cols_map[col] = col_mapped    

        # loop rows
        for i in range(len(df)):
            record = {}
            for col in cols:
                value_raw = df[col].loc[i]
                key   = cols_map[col]
                
                value_type = type(value_raw)
                if value_type == numpy.int64:
                    value = int(value_raw)
                elif value_type == numpy.float64:
                    value = float(value_raw)
                elif value_type == numpy.bool_:
                    value = bool(numpy)        
                else:                    
                    value = value_raw

                #print(value_type, value_raw)

                record[key] = value
            result.append(record)

        return result

    def get_table_template_from_pandas_df(self, tabname:str, df:pd.DataFrame, label:str=None, 
        key_count:int=1,  min_char_len_if_empty:int=10, dec_length:int=23, decimals:int=3, 
        enhancementCategory:str="#NOT_EXTENSIBLE", tableCategory:str="#TRANSPARENT", deliveryClass:str="#A", dataMaintenance:str="#ALLOWED", 
        with_client_key:bool=True, with_timestamp_key:bool=False, skip_unnamed:bool=True) -> str:

        # prepare columns
        cols = df.columns.values.tolist()
        cols_list = []
        
        for col in cols:
            if col == "Unnamed" and skip_unnamed:
                continue

            col_max_len = 0
            col_type = df.dtypes[col].__repr__() #columns[col].to_native_types()
            if col_type.find("'O'") >= 0:
                try:
                    col_max_len = df[col].astype(str).str.len().max()           
                except Exception as exc:                    
                    print(f"Error processing column {col} ({df[col].object_d}): {type(exc)} - {exc}")
                    col_max_len = 0

                if col_max_len == 0:
                    col_max_len = min_char_len_if_empty
                
                if col_max_len > 1333:
                    col_type_abap = f"abap.string(0)"
                else:    
                    col_type_abap = f"abap.char({col_max_len})"
            else:
                col_type_abap = f"abap.dec({dec_length},{decimals})"    

            col_tupel = (col, self.get_sap_fieldname(col), col_type, col_max_len, col_type_abap)
            cols_list.append(col_tupel)

        if label == None:
            tab_label = "table template generated by PyDEEN"
        else:
            tab_label = label


        # table header
        result = ""
        result += f"@EndUserText.label : '{tab_label}'\n"
        result += f"@AbapCatalog.enhancementCategory : {enhancementCategory}\n"
        result += f"@AbapCatalog.tableCategory : {tableCategory}\n"
        result += f"@AbapCatalog.deliveryClass : {deliveryClass}\n"
        result += f"@AbapCatalog.dataMaintenance : {dataMaintenance}\n"        

        # table start and keys
        result += f"define table {tabname} " + "{\n"
        
        if with_client_key:
            result += f"  key CLIENT : abap.clnt not null;\n"
        if with_timestamp_key:
            result += "  key TIMESTAMP : timestampl not null;\n"

        col_index = 0
        for col_tupel in cols_list:
            if col_index < key_count:
                key_include = "key "
            else:
                key_include = ""

            result += f"  {key_include}{col_tupel[1]} : {col_tupel[4]};\n"
            col_index += 1
            
        result += "}"
        return result

    def menu_action_reset(self):
        self.menu_result = None
        self.menu_result_pd = None
        print("Menu context cleared.")

    def menu_action_ping(self):
        
        success, response, http_code = self.ping()

        if success == True:
            print(response)
        else:
            print(f"Ping failed: http code {http_code} - {response}")    


    def menu_action_search_table(self):
        input = UserInput("Enter Wildcard for table (use '*')", self.last_input).get_input(empty_allowed=True)
        if input == None:
            return

        result = self.search_tables(input)
        if result == None or len(result) == 0:
            print("No results")
        else:
            count = len(result)
            print(f"{count} tables found.")
            for record in result:
                #print(f"{record[0]} - {record[1]} ({record[2]})")
                print(record)

    def menu_action_search_cds(self):
        input = UserInput("Enter Wildcard for cds (use '*')", self.last_input).get_input(empty_allowed=True)
        if input == None:
            return

        result = self.search_cds_view(input)
        if result == None or len(result) == 0:
            print("No results")
        else:
            count = len(result)
            print(f"{count} cds views found.")
            for record in result:
                #print(f"{record[0]} - {record[1]} ({record[2]})")
                print(record)

    def menu_action_sql_select(self):
        input = UserInput("Enter SQL Statement", self.last_input).get_input(empty_allowed=True)
        if input == None:
            return

        self.menu_result = None
        self.last_input = input

        success, response, http_code = self.execute_sql(input)
        if success == True:
            #result = json.loads(response)
            #self.menu_result = SAPAbapDeebResult(result)
            self.menu_result = self.sql_response_to_result(response)
            count = self.menu_result.get_count()
            cols  = self.menu_result.get_columns()
            print(f"SQL select finished: {count} records in {len(cols)} columns")
            print(cols)
        else:
            print(f"SQL select failed: http code {http_code} - {response}")   

    def menu_action_generate_sap_template(self, result_df:PandasResultDataframe) -> bool:
        # enter table name
        table_name = UserInput("Enter a name for the Z-Table", "ZMYTABLE").get_input()
        if table_name == None:
            return True

        # Default Options
        #if UserInput("Open extended options").get_input_yes_no(False) == True:
        #    print("extended Option not implemented yet")

        # generate    
        tab_template = self.get_table_template_from_pandas_df(table_name, PandasResultDataframe.get_dataframe(result_df))
        if tab_template != None:
            print(f"\n\nUse this as eclipse table template:\n\n{tab_template}")
            return True
        else:
            return False

    def exit_menu_get_entries_top(self, exit, owner) -> dict:
        result = {}
        if type(owner) == PandasResultDataframe:
            result[SAPAbapDeebConnector.MENU_PANDAS_TEMPLATE] = "Generate SAP table template"
            return result
        else:
            return super().exit_menu_get_entries_top(exit, owner)
    
    def exit_menu_get_entries_bottom(self, exit, owner) -> dict:
        result = {}        
        if type(owner) == PandasResultDataframe:
            result[SAPAbapDeebConnector.MENU_PANDAS_EXPORT_ZTAB] = "Export to SAP Backend as Z-Table"
            return result
        else:
            return super().exit_menu_get_entries_top(exit, owner)

    def menu_get_entries(self, prefilled: dict = None) -> dict:
        entries = super().menu_get_entries(prefilled)

        entries[SAPAbapDeebConnector.MENU_PING] = "Ping ABAP Backend DEEB Service"
        entries[SAPAbapDeebConnector.MENU_SEARCH_TABLE] = "Search table"
        entries[SAPAbapDeebConnector.MENU_SEARCH_CDS] = "Search cds view"
        entries[SAPAbapDeebConnector.MENU_SQL_SELECT] = "Excecute SQL Select Statement"

        if self.menu_result != None:
            entries[SAPAbapDeebConnector.MENU_RESULT_MENU] = f"Open menu for current result"
            
        if type(self.menu_result_pd) == PandasResultDataframe:
            entries[SAPAbapDeebConnector.MENU_PANDAS_MENU] = f"Open menu for pandas dataframe"
        else:
            if self.menu_result != None:
                entries[SAPAbapDeebConnector.MENU_RESULT_PANDAS] = f"Get current result as pandas dataframe"

        if type(self.menu_result_pd) != PandasResultDataframe:
            if Factory.get_datahub().get_count(PandasResultDataframe) > 0:
                entries[SAPAbapDeebConnector.MENU_DATAHUB_IMPORT] = "Import pandas dataframe from Datahub"
            else:
                entries[SAPAbapDeebConnector.MENU_PANDAS_IMPORT] = "Import pandas dataframe"
 
        if Factory.get_datahub().get_count() > 0:
            entries[SAPAbapDeebConnector.MENU_DATAHUB_MENU] = "Open Datahub menu"


        entries[SAPAbapDeebConnector.MENU_RESET] = "Reset menu context"

        return entries

    def execute_table_update(self, tabname:str, data, with_timestamp:bool=False, delete:bool=True, interactive:bool=True, timestamp=None, all_namespaces:bool=False):
                    # prepare payload
                    data_lin = len(data)
                    data_str = json.dumps(data) 
                    data_len = len(data_str) / 1024

                    payload = {
                        'table' : tabname.upper(),
                        'data' : data_str,
                        'with_timestamp' : with_timestamp,
                        'timestamp' : timestamp,
                        'delete' : delete,
                        'all_namespaces' : all_namespaces
                    }

                    # status
                    if interactive:
                        if data_lin > 1000 or data_len > 1000:
                            print("You will transfer a large amount of data to the SAP backend. Please be patient.")
                        print(f"Sending data with {data_lin} lines and {data_len:.2f} KByte to SAP backend...")

                    # call deeb api table update
                    success, response, http_code = self.execute_request(payload, "table_update")
                    if interactive:                    
                        if success:
                            print(f"Success: {response}")
                        else:
                            print(f"Error: {http_code} - {response}")                    
                    
                    return success, response, http_code

    def exit_menu_process_selection(self, exit, owner, selected: str, text: str = None) -> bool:
        
        if isinstance(owner, PandasResultDataframe):
            if selected == SAPAbapDeebConnector.MENU_PANDAS_TEMPLATE:
                self.menu_action_generate_sap_template(owner)
                return True
            elif selected == SAPAbapDeebConnector.MENU_PANDAS_EXPORT_ZTAB:
                tab_name = UserInput("Enter table name").get_input(empty_allowed=True)
                if tab_name != None and tab_name != "":
                    print("Preparing data...")
                    data = self.get_df_result_as_list_of_dict(self.menu_result_pd)
                    success = self.execute_table_update(tab_name, data, interactive=True)
                return True 
        else:    
            return super().exit_menu_process_selection(exit, owner, selected, text)


    def menu_process_selection(self, selected: str, text: str = None):
        try:
            if selected == SAPAbapDeebConnector.MENU_RESULT_MENU:
                self.menu_result.menu()
            elif selected == SAPAbapDeebConnector.MENU_RESULT_PANDAS:
                df:pd.DataFrame = self.menu_result.get_result_as_pandas_df()
                self.menu_result_pd = PandasResultDataframe(name=self.menu_result.result_name, df=df)
                print(df)    
            elif selected == SAPAbapDeebConnector.MENU_PANDAS_MENU:
                self.menu_result_pd.menu(menu_exit=self)
            elif selected == SAPAbapDeebConnector.MENU_RESET:
                self.menu_action_reset()
            elif selected == SAPAbapDeebConnector.MENU_PING:
                self.menu_action_ping()    
            elif selected == SAPAbapDeebConnector.MENU_SEARCH_TABLE:
                self.menu_action_search_table()
            elif selected == SAPAbapDeebConnector.MENU_SEARCH_CDS:
                self.menu_action_search_cds()
            elif selected == SAPAbapDeebConnector.MENU_SQL_SELECT:
                self.menu_action_sql_select()    
            elif selected == SAPAbapDeebConnector.MENU_DATAHUB_MENU:
                Factory.get_datahub().menu() 
            elif selected == SAPAbapDeebConnector.MENU_DATAHUB_IMPORT:
                dh_key = Factory.get_datahub().menu_select_key("Enter the key for pandas dataframe object", PandasResultDataframe)        
                if dh_key != None:
                    object = Factory.get_datahub().get_object(dh_key)
                    if object != None:
                        self.menu_result_pd = object
                        print("Panadas dataframe object imported.")
                        print(self.menu_result_pd.get_dataframe())

            elif selected == SAPAbapDeebConnector.MENU_PANDAS_IMPORT:
                df_import = PandasResultDataframe(name="dataframe")
                df_import.menu()
                if not df_import .is_empty():
                    self.menu_result_pd = df_import
                    print("Imported:\n", self.menu_result_pd)
            else:
                return super().menu_process_selection(selected, text)
        except Exception as exc:
            print("Errors occured:", type(exc), exc)


    def ping(self):
        # build a new request
        request = self.create_request()        
        # prepare params
        params = {}

        client  = self.backend.get_client()
        if client != None:
            params[SAPAbapHttpBackend.HTTP_PARAM_SAPCLIENT] = client

        # call sap service api
        self.trace("Call sap for DEEB Ping")
        http_code = request.get(f"{self.endpoint}/ping", params)
        response = request.get_response_text()
        if http_code < 200 or http_code > 299:
            self.trace(f"invalid answer - return code {http_code}") 
            return False, response, http_code
        else:
            self.trace("Ping OK")
            return True, response, http_code            
               
    def sql_response_to_result(self, response: str) -> Result:
        try:
            result = json.loads(response)
            return SAPAbapDeebResult(result)
        except Exception as exc:
            self.error(f"Errors occured while convert sql response to Result: {type(exc)} - {exc}")
            return None   
    
    def execute_sql(self, sql:str, max_rec:int=0):
        # build a new request
        request = self.create_request()        
        
        payload = {}
        payload["SQL"] = sql 
        
        max_records = max_rec
        if max_records <= 0:
            max_records = self.max_rec

        if max_records > 0:
            payload["MAX_RECORDS"] = max_records
        
        # prepare params
        params = {}
        client  = self.backend.get_client()
        if client != None:
            params[SAPAbapHttpBackend.HTTP_PARAM_SAPCLIENT] = client

        # call sap service api
        self.trace("Call sap for DEEB SQL Select")
        
        http_code = request.post(json.dumps(payload), f"{self.endpoint}/sql_select", params)
        response = request.get_response_text()
        if http_code < 200 or http_code > 299:
            self.trace(f"invalid answer - return code {http_code}") 
            return False, response, http_code
        else:
            self.trace("SQL Select OK")
            return True, response, http_code   

    def execute_request(self, payload:dict, deeb_service:str, params:dict=None):
        # build a new request
        request = self.create_request()        
        
        # prepare params
        req_params = {}
        client  = self.backend.get_client()
        if client != None:
            req_params[SAPAbapHttpBackend.HTTP_PARAM_SAPCLIENT] = client
        if params != None:
            req_params.update(params)    

        # call sap service api
        self.trace(f"Call sap for deeb request service {deeb_service}")
        
        http_code = request.post(json.dumps(payload), f"{self.endpoint}/{deeb_service}", req_params)
        response = request.get_response_text()
        if http_code < 200 or http_code > 299:
            self.trace(f"deeb service {deeb_service} - invalid answer - return code {http_code}") 
            return False, response, http_code
        else:
            self.trace(f"deeb request {deeb_service} OK")
            return True, response, http_code   

    def search_tables(self, wildcard:str) -> list:
        try:
            if wildcard == None:
                return None
            search_str = wildcard.replace("*", "%")

            #sql_request = f"SELECT m~tabname as table_name, t~ddtext  as description, t~DDLANGUAGE as language FROM dd02l AS m LEFT OUTER JOIN dd02t AS t ON m~tabname = t~tabname and m~as4local = t~as4local and m~as4vers = t~as4vers WHERE m~tabname LIKE '{search_str}' OR t~ddtext LIKE '{search_str}' ORDER BY m~tabname"
            sql_request = f"SELECT tabname as table_name FROM dd02l where tabname like '{search_str}' order by tabname"

            success, sql_response, http_code = self.execute_sql(sql_request, self.max_rec)
            if success == False:
                return None

            result = []    
            if sql_response != None:
                json_result = json.loads(sql_response)
                for line in json_result:
                    table = line["TABLE_NAME"]
                    table = table.replace("\\/", "/")
                    result.append(table)

            return result
        except Exception as exc:
            self.error(f"Error while selecting tables with wildcard {wildcard}: {type(exc)} - {exc}")
            return None    

    def search_cds_view(self, wildcard:str) -> list:
        try:
            if wildcard == None:
                return None
            search_str = wildcard.replace("*", "%")

            #sql_request = f"SELECT m~tabname as table_name, t~ddtext  as description, t~DDLANGUAGE as language FROM dd02l AS m LEFT OUTER JOIN dd02t AS t ON m~tabname = t~tabname and m~as4local = t~as4local and m~as4vers = t~as4vers WHERE m~tabname LIKE '{search_str}' OR t~ddtext LIKE '{search_str}' ORDER BY m~tabname"
            sql_request = f"SELECT OBJ_NAME as CDS_NAME FROM TADIR where PGMID = 'R3TR' and OBJECT = 'DDLS' and OBJ_NAME like '{search_str}' order by OBJ_NAME"

            success, sql_response, http_code = self.execute_sql(sql_request, self.max_rec)
            if success == False:
                return None

            result = []    
            if sql_response != None:
                json_result = json.loads(sql_response)
                for line in json_result:
                    table = line["CDS_NAME"]
                    table = table.replace("\\/", "/")
                    result.append(table)

            return result
        except Exception as exc:
            self.error(f"Error while selecting cds views with wildcard {wildcard}: {type(exc)} - {exc}")
            return None    


    def get_current_result(self) -> Result:
        return self.menu_result

    def get_current_result_as_pandas_df(self) -> Result:
        try:
            return self.menu_result.get_result_as_pandas_df()
        except:
            return None    
