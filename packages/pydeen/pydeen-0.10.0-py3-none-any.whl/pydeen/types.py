"""
main types defintions and functionality for the framework
"""

from encodings import search_function
import json
import pandas as pd

from requests import Session

from pydeen.utils import CryptUtil, CryptEngine, FileTransferUtil
from pydeen.exits import MenuExit, MenuExitCallback
from pydeen.menu import  MenuSelection, MenuAction, UserInput
from pydeen.core import PyDEEN

class Base:
    """
        Abstract base class
    """

    BASE_PROP_TYPE = "type"
    BASE_PROP_PROP = "properties"
    BASE_PROP_KEY  = "key"
    BASE_PROP_DESCRIPTION = "description" 

    def __init__(self) -> None:
        self.type = "pydeen.Base"
        self._properties = {}
        self.debug = False
        self.interactive = False
        self.last_error = None
        self.menu_title:str="PyDEEN Menu"
        self.menu_exit:MenuExit = None

    def __repr__(self) -> str:
        return self.type

    def get_type(self) -> str:
        if self.type == None:
            return type(self)
        else:
            return self.type

    def trace(self, msg):
        if self.debug == True:
            print("DEBUG:", msg)
        
        try:
            PyDEEN.get_logger(self.get_type()).debug(msg)
        except Exception as exc:
            print(f"error while write to log: {type(exc)} - {exc}")    

    def info(self, msg):
        if self.debug == True or self.interactive == True:
            print("INFO:", msg)

        try:
            PyDEEN.get_logger(self.get_type()).info(msg)
        except Exception as exc:
            print(f"error while write to log: {type(exc)} - {exc}")    

    def warning(self, msg):
        if self.debug == True or self.interactive == True:
            print("WARNING:", msg)

        try:
            PyDEEN.get_logger(self.get_type()).warning(msg)
        except Exception as exc:
            print(f"error while write to log: {type(exc)} - {exc}")    

    def error(self, msg):
        if self.debug == True  or self.interactive == True:
            print("ERROR:", msg)

        self.last_error = msg    

        try:
            PyDEEN.get_logger(self.get_type()).error(msg)
        except Exception as exc:
            print(f"error while write to log: {type(exc)} - {exc}")    

    def get_last_error(self) -> str:
        return self.last_error

    def reset_last_error(self):
        self.last_error = None    
    
    def get_properties(self):
        return self._properties

    def set_property(self, name, value):
        if value == None or value == "":
            self._properties.pop(name, None)
        else:        
            self._properties[name] = value

    def get_property(self, name, default=None):
        if name in self._properties.keys():
            value = self._properties[name]
            value_type = type(value)
            if value_type == dict:
                engine_key = value[CryptEngine.PROP_ENGINE]
                engine = CryptUtil.get_engine(engine_key)        
                return engine.decode(value) 
            else:
                return value 
        else:
            return default

    def get_type(self) -> str:
        return self.type

    def get_key(self) -> str:
        return self.get_property(Base.BASE_PROP_KEY)

    def set_key(self, desc:str):
        self.set_property(Base.BASE_PROP_DESCRIPTION, desc)    

    def get_description(self) -> str:
        prop = self.get_property(Base.BASE_PROP_DESCRIPTION, None)
        return prop    


    def set_description(self, desc:str):
        self.set_property(Base.BASE_PROP_DESCRIPTION, desc)

    def get_config(self):
        return self._properties

    def get_config_file_name(self, filename) -> str:
        if filename.find(".") > 0:
            return filename
        else:
            return filename + "." + self.type + ".cfg"   

    def set_config(self, config):
        self._properties = config    

    def save_config(self, filename) -> bool:
        try:
            config = self.get_config()
            if config == None:
                return False

            with open(self.get_config_file_name(filename), "w") as file:
                file.write(json.dumps(config))
            return True         
        except Exception as exc:
            self.error(f"Error while saving config: {type(exc)} - {exc}")
            return False
        

    def load_config(self, filename) -> bool:    
        try:    
            json_string = ""
            with open(self.get_config_file_name(filename),"r") as file:
                for line in file:
                    if json_string == "":
                        json_string = line
                    else:    
                        json_string += "\n" + line
            
            json_obj = json.loads(json_string)
            return self.set_config(json_obj)
        except Exception as exc:
            self.error(f"Error while loading config: {type(exc)} - {exc}")
            return False


    def menu_get_title(self) -> str:
        if self.menu_title != None:
            return self.menu_title
        else:    
            return "PyDEEN Menu"

    def menu_get_entries(self, prefilled:dict=None) -> dict:
        """
        Creates a context oriented menu for 'menu()'
        """
        # prepare and prefill
        result = {}
        if prefilled != None:
            result.update(prefilled)
            self.trace("menu has prefilled entries")

        # check menu exit
        if self.menu_exit != None:
            if self.menu_exit.entries_top != None:
                result.update(self.menu_exit.entries_top)
                self.trace("Menu extended at top level by menuexit static")
            
            entries_top = self.menu_exit.callback.exit_menu_get_entries_top(self.menu_exit, self)
            if entries_top != None:
                result.update(entries_top)
                self.trace("Menu extended at top level by menuexit callback")
        # return
        return result            

    def menu_process_selection(self, selected:str, text:str=None) -> bool:
        """
        Processes the user input from 'menu()'
        """
#        if self.menu_exit != None:
#            if self.menu_exit.callback.exit_menu_process_selection(self, selected, text) == True:
#                return True
#            else:
        if text == None:
            print(f"Selected menu {selected} not handled")
        else:    
            print(f"Selected menu '{text}' (code:{selected}) not handled")
        return False    

    def menu(self, menu_exit:any=None):
        """
        This function created an individual menu for the context object.
        See function 'menu_get_entries' and 'menu_process_selection' too.
        """

        # prepare      
        title = self.menu_get_title()
        self.trace(f"Menu {title} entered")
        saved_interactive = self.interactive
        self.interactive = True
        
        self.menu_exit = None
        if isinstance(menu_exit, MenuExit):
            self.menu_exit = menu_exit
            self.trace(f"menuexit {menu_exit} detected")
        elif isinstance(menu_exit, MenuExitCallback):
            menu_exit_proxy = MenuExit(menu_exit) 
            self.menu_exit = menu_exit_proxy
            self.trace(f"menuexit callback {menu_exit} detected")

        # menu loop
        valid = True
        while valid == True:
            # build main menu    
            entries = self.menu_get_entries()

            # check menu exit
            if self.menu_exit != None:
                if self.menu_exit.entries_bottom != None:
                    entries.update(self.menu_exit.entries_bottom)
                    self.trace("menu extended at bottom by menuexit static")
                
                entries_bottom = self.menu_exit.callback.exit_menu_get_entries_bottom(menu_exit, self)    
                if entries_bottom != None:
                    entries.update(entries_bottom)
                    self.trace("menu extended at bottom by menuexit static")

            # check menu exists
            if entries == None or len(entries) == 0:
                print(f"This object has no menu {self}")
                return False

            # show menu            
            action = MenuSelection(title, entries, True, False).show_menu()
            if action.is_quit_entered():
                valid = False
            else:
                try:
                    selected = action.get_selection()
                    menu_text = entries[selected]
                    handled = False

                    if self.menu_exit != None and self.menu_exit.callback != None:
                        handled = self.menu_exit.callback.exit_menu_process_selection(menu_exit, self, selected, text=menu_text)
                    
                    if handled == True:
                        self.trace(f"selection {selected} was handled by menu_exit")
                    else:       
                        self.menu_process_selection(selected, menu_text)    
                except Exception as exc:
                    print("Errors occured:", type(exc), exc)
            
        # cleanup and exit
        self.interactive = saved_interactive
        self.menu_exit = None


class DataHub(Base):

    MENU_DISPLAY_LIST       = "display_list"
    MENU_CHANGE_DESCRIPTION = "change_description"
    MENU_DELETE_ALL         = "delete_all"
    MENU_DELETE_SINGLE      = "delete_single"
    MENU_OPEN_MENU          = "open_menu"

    def __init__(self, title:str=None) -> None:
        super().__init__()
        self.type = "pydeen.DataHub"
        self.menu_title = title
        self.hubdata:dict={}
        if title == None:
            self.menu_title = "PyDEEN DataHub - Menu"

    def is_key_available(self, key:str) -> bool:
        if key in self.hubdata:
            return True
        else:
            return False

    def register_object(self, key:str, object):
        self.hubdata[key] = object

    def unregister_object(self, key:str):
        del self.hubdata[key]

    def get_object(self, key:str):
        if self.is_key_available(key) == True:
            object = self.hubdata[key]
            return object
        else:
            return None

    def get_count(self, data_type:type=None) -> int:
        if data_type == None:
            count = len(self.hubdata.keys())
        else:
            count = 0
            for key in self.hubdata:
                object = self.hubdata[key]
                if isinstance(object, (data_type)) == True:
                    count += 1
        return count   

    def get_key_list(self, data_type:type=None) -> list:
        if data_type == None:
            return list(self.hubdata.keys())
        else:
            result = []
            for key in self.hubdata:
                object = self.hubdata[key]
                if isinstance(object, data_type) == True:
                    result.append(key)
            return result   

    def get_key_and_type_list(self, data_type:type=None) -> list:
        result = []
        for key in self.hubdata:
            object = self.hubdata[key]
            if data_type == None or isinstance(object, data_type) == True:
                entry = (key, type(object))
                result.append(entry)
        return result   

    def get_used_types_list(self) -> list:
        result = []
        for key in self.hubdata:
            object = self.hubdata[key]
            data_type = type(object)
            if not data_type in result:
                result.append(data_type)
        return result  

    def get_object_description(self, object, with_type:bool=False) -> str:
        if isinstance(object, Base):
            desc = object.get_description()
            if desc == None:
                desc = type(object)
            else:
                if with_type:    
                    desc = f"{desc} ({type(object)})"
        else:    
            desc = type(object)
        return desc    

    def menu_select_key(self, title:str=None, data_type:type=None) -> str:
        # check
        if self.get_count(data_type) == 0:
            return None
        
        # prepare title
        title_used = title
        if title_used == None:
            title_used = "Select datahub object"
        
        # get entries
        entries = {}
        for key in self.hubdata:
            object = self.hubdata[key]
            desc = self.get_object_description(object)
            entries[key] = f"{key} - {desc}"

        # open menu
        action = MenuSelection(title_used, entries, quit=False, cancel=True).show_menu()
        if action.is_cancel_entered():
            return None
        else:
            return action.get_selection()

    def register_object_with_userinput(self, object) -> bool:
        # enter key
        valid = False
        while valid == False:
            key_name = UserInput("Enter a key for Datahub").get_input(empty_allowed=True)
            if key_name == None or key_name == "":
                return False

            if self.is_key_available(key_name) == True:
                print(f"Key '{key_name}' is used already. Try again.")
            else:
                valid = True

        # register 
        self.register_object(key_name, object)
        return True



    def menu_get_entries(self, prefilled: dict = None) -> dict:
        entries = super().menu_get_entries(prefilled)
        count = self.get_count() 
        if count > 0:
            entries[DataHub.MENU_DISPLAY_LIST] = f"Display list of objects in datahub ({count})"
            entries[DataHub.MENU_CHANGE_DESCRIPTION] = f"Change object description"
            entries[DataHub.MENU_OPEN_MENU] = f"Open object menu"
            entries[DataHub.MENU_DELETE_SINGLE] = f"Delete single object"
            entries[DataHub.MENU_DELETE_ALL] = f"Delete all objects from datahub"
        
        return entries

    def menu_process_selection(self, selected: str, text: str = None):
        try:
            if selected == DataHub.MENU_DISPLAY_LIST:
                for key in self.hubdata:
                    object = self.hubdata[key]
                    desc   = self.get_object_description(object)
                    objtype = type(object)
                    print(f"{key} - {desc} ({objtype})")
            elif selected == DataHub.MENU_OPEN_MENU:
                selected = self.menu_select_key(title="Select object by key")
                if selected != None:
                    object = self.get_object(selected)
                    print(f"Open menu for: ", selected, object)
                    Base.menu(object)
            elif selected == DataHub.MENU_CHANGE_DESCRIPTION:
                selected = self.menu_select_key(title="Select object by key")
                if selected != None:
                    object = self.get_object(selected)
                    if isinstance(object, Base):
                        obj_desc = Base.get_description(object)
                        new_obj_desc = UserInput("Set description", obj_desc).get_input(empty_allowed=True)
                        if new_obj_desc != None and len(new_obj_desc) > 0:
                            Base.set_description(object, new_obj_desc)
                            print(f"New description set for object: {new_obj_desc}")
                    else:
                        print(f"selected object has an unsupported type: {type(object)}")

            elif selected == DataHub.MENU_DELETE_SINGLE:
                selected = self.menu_select_key(title="Select object by key")
                if selected != None:
                    self.unregister_object(selected)
                    print(f"object with key {selected} removed from datahub")    
            elif selected == DataHub.MENU_DELETE_ALL:
                self.hubdata={}
                print("datahub cleared.")
            else:    
                return super().menu_process_selection(selected, text)    
            return False
        except Exception as exc:
            print(f"Error: {type(exc)} - {exc}")
            return False


class Factory:
    PYDEEN_DATAHUB = DataHub("Central PyDEEN Datahub") 

    @classmethod
    def get_datahub(cls) -> DataHub:
        return cls.PYDEEN_DATAHUB


class Auth(Base):
    """
        abstract authentification
    """

    AUTH_TYPE_NONE  = "None"
    AUTH_TYPE_BASIC = "Basic"

    AUTH_PROP_TYPE = "type"
    AUTH_PROP_USER = "user"
    AUTH_PROP_PASS = "password"


    def __init__(self) -> None:
        Base.__init__(self)
        self.type = "pydeen.Auth"

    def get_config(self):
        return self._properties

    def init_from_config(self, type, config:dict) -> bool:
        # have to be redefined
        self._properties = {}
        return False

    def set_config(self, config:dict) -> bool:
        
        self._properties = {}
        if Auth.AUTH_PROP_TYPE in config.keys():
            type = config[Auth.AUTH_PROP_TYPE]
        else:
            type = Auth.AUTH_TYPE_NONE     
        
        return self.init_from_config(type, config)

    def get_auth_type(self) -> str:
        type = self.get_property(Auth.AUTH_PROP_TYPE)
        if type == None:
            type = Auth.AUTH_TYPE_NONE

    def get_auth_headers(self) -> dict:
        return None      

    def get_auth_for_request(self):
        return None

    def get_auth_for_requests_session(self) -> Session:
        return None


class Backend(Base):
    """
        abstract enterprise backend with properties
    """
    # static constants
    BACKEND_PROP_NAME       = "name"
    BACKEND_PROP_AUTH       = "auth"
    BACKEND_PROP_HOST       = "host"
    BACKEND_PROP_PROTOCOL   = "protocol"
    BACKEND_PROP_TENANT     = "tenant"
    BACKEND_PROP_PORT       = "port"
    BACKEND_PROP_PATH       = "path"
    BACKEND_PROP_URL        = "url"
    BACKEND_PROP_LANGUAGE   = "language"


    def __init__(self, name, auth:Auth=None) -> None:
        Base.__init__(self)
        self.name = name
        self.type = "pydeen.Backend"
        self.params = {}

        if auth == None:
            self._auth = Auth()
        else:
            self._auth = auth

    def get_name(self):
        return self.name
        
    def set_auth_info(self, auth:Auth):
        self._auth = auth

    def set_auth_basic(self, user, password):
        self._auth = Auth()
        self._auth.set_basic_auth(user, password)

    def get_auth_info(self) -> Auth:
        return self._auth

    def get_params(self):
        return self.params

    def is_auth_info_available(self) -> bool:
        """
            checks if an authorization information is given
        """
        if self._auth == None or self._auth.get_auth_type() == Auth.AUTH_TYPE_NONE:
            return False
        else:
            return True    

    def get_auth_for_request(self):
        return None    

    def set_connection(self, host, port="", protocol="", tenant="", path="", language=""):
        self.set_property(Backend.BACKEND_PROP_HOST, host)
        self.set_property(Backend.BACKEND_PROP_PORT, port)
        self.set_property(Backend.BACKEND_PROP_PROTOCOL, protocol)
        self.set_property(Backend.BACKEND_PROP_TENANT, tenant)
        self.set_property(Backend.BACKEND_PROP_PATH, path)
        self.set_property(Backend.BACKEND_PROP_LANGUAGE, language)

    def get_config(self):
        json_obj = {}
        json_obj[Backend.BASE_PROP_TYPE] = self.type
        json_obj[Backend.BASE_PROP_PROP] = self._properties
        json_obj[Backend.BACKEND_PROP_NAME] = self.name
        json_obj[Backend.BACKEND_PROP_AUTH] = self._auth.get_config()
        return json_obj

    def set_config(self, config) -> bool:

        # set main fields
        self.name = config[Backend.BACKEND_PROP_NAME]
        self.type = config[Backend.BASE_PROP_TYPE]
        self._properties = config[Backend.BASE_PROP_PROP]

        # check auth info
        self._auth = Auth()
        auth_config = config[Backend.BACKEND_PROP_AUTH]
        #print("Read AuthConfig", auth_config)
        if self._auth.set_config(auth_config) == False:
            print("no auth information available for backend")

        # result
        return True
    
    def get_url(self) -> str:
        return self.get_property(Backend.BACKEND_PROP_URL)
        
class Connector(Base):
    """
        abstract connector to an backend system
    """
    def __init__(self, backend) -> None:
        Base.__init__(self)
        self.type = "pydeen.Connector"
        self.backend = backend
        self.params = {}

    def __repr__(self) ->str:
        return f"{self.type} to {self.backend}"

    def get_backend(self) -> Backend:
        return self.backend

class EntityMetaInfo(Base):
    def __init__(self) -> None:
        super().__init__()
        self.type = "EntityMetaInfo"

    def get_columns(self) -> list:
        return None

class ResultSingle(Base):

    MENU_DISPLAY_RAW        = "result_display_raw"
    MENU_SAVE_RAW           = "result_save_raw"
    MENU_DISPLAY_COLS       = "result_display_cols"
    MENU_DATAHUB_EXPORT     = "export_datahub"

    def __init__(self, result, name:str=None) -> None:
        super().__init__()
        self.result = result 
        self.result_name:str =  name  
        self.type = "pydeen.ResultSingle"
        self.columns = None
        self.entityMetaInfo:EntityMetaInfo=None
        self.menu_title = "Single Result - Menu"

    def get_columns(self) -> list:
        # check metainfo
        result = None
        if self.entityMetaInfo != None:
            result = self.entityMetaInfo.get_columns()

        if result != None:
            return result
        
        # cols from data cached?
        if self.columns != None:
            return self.columns
        
        # check workaround
        if self.result == None or type(self.result) is not dict:
            return []
        else:
            self.columns = []
            for name in self.result:
                self.columns.append(name)
            return self.columns

    def menu_get_entries(self, prefilled: dict = None) -> dict:
        # check
        entries = super().menu_get_entries(prefilled)
        if self.result == None:
            return entries
        
        # prepare
        columns = self.get_columns()

        entries[ResultSingle.MENU_DISPLAY_RAW] = "Display raw data"
        entries[ResultSingle.MENU_SAVE_RAW] = "Save raw data"
        if columns != None and len(columns) > 0:
            entries[ResultSingle.MENU_DISPLAY_COLS] = "Display column names"
        
        entries[ResultSingle.MENU_DATAHUB_EXPORT] = "Export to Datahub"

        return entries

    def menu_process_selection(self, selected: str, text: str = None):
        try:
            if selected == ResultSingle.MENU_DISPLAY_RAW:
                print(self.result)
            elif selected == ResultSingle.MENU_SAVE_RAW:
                content = json.dumps(self.result)
                if self.result_name != None:
                    name = self.result_name
                else:
                    name = "result"    
                FileTransferUtil().enter_filename_and_save_text("Save single result as text", name, content, with_datetime_prefix=True, extension="txt")
            elif selected == ResultSingle.MENU_DISPLAY_COLS:
                columns = self.get_columns()
                print(f"columns: {len(columns)}")
                for col in columns:
                    print(col)
            elif selected == ResultSingle.MENU_DATAHUB_EXPORT:
                if Factory.get_datahub().register_object_with_userinput(self) == True:
                    print("Single Result exported to Datahub.")
                else:
                    print("Single Result not exported to Datahub.")
            else:
                return super().menu_process_selection(selected, text)
        except Exception as exc:
            print("Errors occured:", type(exc), exc)


class Result(Base):

    MENU_DISPLAY_RAW        = "result_display_raw"
    MENU_CHANGE_DESC        = "result_change_description"
    MENU_SAVE_RAW           = "result_save_raw"
    MENU_DISPLAY_COLS       = "result_display_cols"
    MENU_DATAHUB_EXPORT     = "export_datahub"

    def __init__(self, result, name:str=None) -> None:
        super().__init__()
        self.result = result 
        self.result_name:str =  name  
        self.type = "pydeen.Result"
        self.columns = None
        self.entityMetaInfo:EntityMetaInfo=None
        self.menu_title = "Result - Menu"

    def set_entity_metainfo(self, metainfo):
        self.entityMetaInfo = metainfo

    def get_name(self) -> str:
        if self.result_name != None:
            return self.result_name
        else:
            return "unknown"

    def set_name(self, name):
        self.result_name = name

    def get_result_raw(self):
        return self.result

    def is_list(self) -> bool:
        if self.result == None:
            return False

        if type(self.result) == "<class 'list'>":
            return True

    def is_list_of_dict(self) -> bool:
        if self.is_list() == False or self.is_empty() == True:
            return False
        if len(self.result) == 0:
            return False

        if type(self.result[0]) == "<class 'dict'>":
            return True

    def is_empty(self) -> bool:
        if self.result == None:
            return True

        if self.is_list() == True:
            if self.result.len() == 0:
                return True                    
        
        return False

    def get_columns(self) -> list:
        # check metainfo
        result = None
        if self.entityMetaInfo != None:
            result = self.entityMetaInfo.get_columns()

        if result != None:
            return result
        
        # cols from data cached?
        if self.columns != None:
            return self.columns
        
        # check workaround
        if self.is_list_of_dict() == False:
            return None
        else:
            result = []
            for name in self.result[0].keys():
                result.append(name)
        # workaround active
        self.columns = result
        return result             

    def get_count(self) -> int:        
        if self.result == None:
            return 0

        try:
            return len(self.result)
        except:
            print("ERROR COUNT")
            return 0    

    def get_result_as_pandas_df(self, type_mapping:bool=True, ignore_tech_cols:bool=True) -> pd.DataFrame:
        try:
            # check result
            if self.is_list_of_dict() == False:
                self.error("invalid result type to convert to pandas dataframe")
                return None
            
            # get result
            raw  = self.get_result_raw()
            cols = self.get_columns()
            if cols == None or len(cols) == 0 or raw == None or len(raw) == 0:
                self.error("invalid result data to convert to pandas dataframe")
                return None

            # filter columns
            use_cols = []
            for col in cols:
                if ignore_tech_cols == True and (col.find("__") == 0 or col.find("___") > 0):
                    continue
                use_cols.append(col)
            if len(use_cols) == 0:
                return  None

            # prepare pandas
            data = []
            for record in raw:
                entry = []
                for col in use_cols:
                    try:
                        raw_value = record[col]
                        value = self.convert_raw_value(col, raw_value)
                    except Exception as exc:
                        self.trace(f"column {col} not found in record: {exc} set empty value")
                        value = None 
                    entry.append(value)
                data.append(entry)    

            # create dataframe
            df = pd.DataFrame(data,columns=use_cols)
            return df
        except Exception as exc:
            print(f"Error while transforming result to pandas df: {type(exc)} - {exc}")

    def convert_raw_value(self, column, value):
        return value   


    def get_record_by_index(self, index:int) -> dict:
        """returns a record from result set as dict object

        :param index: index of the record, starting at 0
        :type index: int
        :return: record as dict object or None
        :rtype: dict
        """
        try:
            return self.result[index]
        except:
            return None        

    def get_record_text_preview(self, record:dict, separator:str="|", max_cols:int=5, max_len:int=50, cols_to_ignore:list=None) -> str:
        # check
        if record == None or type(record) != dict:
            return None
        # prepare
        result = None
        col_cnt = 0
        # loop columns
        for key in record:
            if cols_to_ignore != None and key in cols_to_ignore:
                continue
            
            value = None
            try:
                value = str(record[key])
                if value == None or len(value) > max_len:
                    continue
            except:
                continue
                        
            if result == None:
                result = value
            else:
                result = result + separator + value

            col_cnt += 1
            if col_cnt >= max_cols:
                break

        return result

    def menu_get_result_single(self) -> ResultSingle:
        # check
        result = None
        count = self.get_count()

        if count <= 0:
            self.trace("empty result")
            return None
        # only 1 record?
        elif count == 1:
            self.trace("only one record - return it without menu")
            result = ResultSingle(self.result[0], self.result_name)
        # > 1 record - enter menu
        else:    
            # build entries
            entries = {}
            index = 1
            for record in self.result:
                entries[str(index)] = f"{self.get_record_text_preview(record, max_cols=10)}"
                index += 1

            # show menu
            valid = True
            while valid == True:
                menu = MenuSelection(
                    "Select Record with index", entries, False, True)
                action = menu.show_menu()
                if action.is_cancel_entered() == True:
                    valid = False
                elif action.is_selected() == True:
                    index = int(action.get_selection())
                    record = self.result[index-1]
                    result = ResultSingle(record, self.result_name)
                    valid = False

        if result != None:    
            result.entityMetaInfo = self.entityMetaInfo
            result.debug = self.debug
            result.interactive = self.interactive
            result.set_property(Base.BASE_PROP_DESCRIPTION, self.get_record_text_preview(result.result, max_cols=10))
            return result
        else:
            return None

    def menu_get_entries(self, prefilled: dict = None) -> dict:
        # check
        entries = super().menu_get_entries(prefilled)
        if self.is_empty( ) == True:
            return entries
        
        # prepare
        count = self.get_count()
        columns = self.get_columns()

        entries[Result.MENU_CHANGE_DESC] = f"Change description ({self.get_description()})"
        entries[Result.MENU_DISPLAY_RAW] = "Display raw data"
        entries[Result.MENU_SAVE_RAW] = "Save raw data"
        if columns != None and len(columns) > 0:
            entries[Result.MENU_DISPLAY_COLS] = "Display column names"
        
        entries[Result.MENU_DATAHUB_EXPORT] = "Export to Datahub"
        
        self.trace(f"{count} menu entries created for {self}")
        return entries


    def menu_process_selection(self, selected: str, text: str = None):
        try:
            if selected == Result.MENU_DISPLAY_RAW:
                print(self.get_result_raw())
            elif selected == Result.MENU_CHANGE_DESC:
                new_desc = UserInput("Set description", self.get_description()).get_input(empty_allowed=True)
                if new_desc != None and len(new_desc) > 0:
                    self.set_description(new_desc)
                    print(f"Description set to {new_desc}")
            elif selected == Result.MENU_SAVE_RAW:
                content = json.dumps(self.result)
                if self.result_name != None:
                    name = self.result_name
                else:
                    name = "result"    
                FileTransferUtil().enter_filename_and_save_text("Save result as text", name, content, with_datetime_prefix=True, extension="txt")
            elif selected == Result.MENU_DISPLAY_COLS:
                columns = self.get_columns()
                print(f"columns: {len(columns)}")
                for col in columns:
                    print(col)
            elif selected == Result.MENU_DATAHUB_EXPORT:
                if Factory.get_datahub().register_object_with_userinput(self) == True:
                    print("Result exported to Datahub.")
                else:
                    print("Result not exported to Datahub.")
            else:
                return super().menu_process_selection(selected, text)
        except Exception as exc:
            print(f"Errors occured in menu {selected} processing:", type(exc), exc)


    def parse_json_result_record(self, record:dict, follow_sub_objects:bool=True, current_result:dict=None, current_prefix:str=None, ignore_key_prefix:str=None) -> dict:
        try:
            # check input
            if record == None or len(record.keys()) == 0:
                return None
            
            # prepare result
            if current_result == None:
                result = {}
            else:
                result = current_result

            # loop all attributes
            for key in record.keys():
                
                if ignore_key_prefix != None and key.find(ignore_key_prefix) == 0:
                    continue
                
                value = record[key]
                value_type = type(value)

                if current_prefix == None:    
                    name = key
                else:
                    name = f"{current_prefix}_{key}"

                if value_type == list:
                    self.trace(f"parse record: ignore list value for dkey {name}")
                elif value_type == dict:
                    if follow_sub_objects and len(value) > 0:
                        result = self.parse_json_result_record(value, follow_sub_objects=True, current_result=result, current_prefix=name)
                        if result == None:
                            self.error(f"error while parsing json object attribute with key {name}")
                            return None
                    else:
                        self.trace(f"parse record: ignore dict value for key {name}")
                else:
                    result[name] = value

            return result

        except Exception as exc:
            self.error(f"error while parsing json record: {type(exc)} - {exc}")
            return None

    def append_json_result_record(self, record:dict, follow_sub_objects:bool=True, ignore_key_prefix:str=None) -> bool:
        parsed_record = self.parse_json_result_record(record=record, follow_sub_objects=follow_sub_objects, ignore_key_prefix=ignore_key_prefix)
        if parsed_record == None or len(parsed_record) == 0:
            return False
        else:
            # append
            self.result.append(parsed_record)
            # learn columns
            if self.columns == None or len(self.columns) == 0:
                self.columns = list(parsed_record.keys())
                self.trace(f"columns learned from parsed record: {len(self.columns)} lines")
            else:
                for col in parsed_record.keys():
                    if not col in self.columns:
                        self.columns.append(col)
                        self.trace(f"column learned from parsed record: {col}")
            return True

class Request(Base):

    def __init__(self) -> None:
        super().__init__()
        self.result = None
        self.type = "pydeen.Request"

    def get_result(self) -> Result:
        return self.result


