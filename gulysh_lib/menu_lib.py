


import yaml
class Config():
    def __init__(self, config_file) -> None:
        self.config_file = config_file
        self.config = self.load()
        self.config_scheme = {}

    def load(self):
        """
        ## Load config from file
        """
        with open(self.config_file, "r",  encoding='utf-8') as f:
            return yaml.safe_load(f)
         
    def reload(self):
        """
        Reload and reinit config
        """
        self.__init__(self.config_file)

    def dump(self, config=None):
        """
        Write to config and reload 
        """
        with open(self.config_file, "w") as f:
            if config==None:
                yaml.safe_dump(self.config, f)
            else:
                yaml.safe_dump(config, f)
        self.reload()




class Menu():
    """
    Класс реализующий логику селектора
    """
    def __init__(self, config:Config, debug=False) -> None:
        self.debug = debug
        self.config = config
        self.menu_fields = {}
        self.init_fields()
    
    def start(self):
        while True:
            self.clear_console()
            i = self.selector("Change menu point: ", self.menu_fields)
            if i == "quit":
                return
            i()

    def init_fields(self):
        pass

    def add_field(self, field_name:str="", value=None):
        """
        Add func in menu_fields list
        """
        self.menu_fields.update({field_name: value})

    def add_fieldFunc(self, field_name:str=""):
        """
        Decorator! Add your fun in menu_fields list
        ```
        @self.add_fieldFunc
        def your_func:
            ...
        ```
        """
        def decorator(func):
            field = {field_name: func}
            def wrapper():
                self.menu_fields.update(field)
            wrapper()
        return decorator
    
    def selector(self, inpt_text:str="Change your ... : ", fields:dict={"field_description": "field_varible"}, value_index=1):
        """
        From list selector. Return value from collection 
        """
        while True:
            i=0
            text=""
            for field in fields.keys(): text+= str( f"[{i}]" + " | " + f"{field}\n"); i+=1
            text+=str("\n"+ inpt_text)
            try:
                varible = input(text)
                if varible == "q": return
                varible = int(varible)

                key = list(fields.keys())[varible]

                match value_index:
                    case 1:
                        return fields[key]
                    case 0:
                        return key
            except:
                print("Varible not found pls try again")
        
    def clear_console(self):
        if not(self.debug):
            import os
            os.system('cls' if os.name == 'nt' else 'clear')
  

class Settings_Menu(Menu):
    """
    Settings menu for your config!
    """
    def __init__(self, config: Config, obj) -> None:
        super().__init__(config)
        self.config = config
        self.add_field("Quit", "quit")

    def init_fields(self):
        ...

    def start(self):
        while True:
            self.clear_console()
            resp = self.selector("Change settings : ", self.menu_fields)
            if resp == "quit": return
            resp()

    def add_settings_point(self, field_name="", obj=None, config_path="ai.chat_interface", module_list=[], inpt_title="Change varible: ", no_reload=False):
        """
        Add settings from list selector point 
        """
        cfp, cfp_value = self.get_conf_path(config_path)
  
        @self.add_fieldFunc(f"{field_name} : {cfp_value}")
        def infield():
            self.config.config[cfp[0]][cfp[1]] = self.selector(inpt_title, module_list, 0)
            self.reload_conf(obj)

    def add_settings_write_point(self, field_name, obj=None, config_path="ai.chat_interface"):
        """
        Add writeble settings point 
        """
        cfp, cfp_value = self.get_conf_path(config_path)

        @self.add_fieldFunc(f"{field_name}")
        def infield():
            value = input(f"\n\nPrint 'q' to return\n\nOld value: {cfp_value}\nNew value: ")
            if value == "q": return

            self.config.config[cfp[0]][cfp[1]] =  value
            self.reload_conf(obj)



    def reload_conf(self, obj):
        
        self.config.dump()
        obj.reload()
        self.__init__(self.config, obj)

    def get_conf_path(self, config_path):
        cfp = config_path.split(".")

        try: cfp_value = self.config.config[cfp[0]][cfp[1]]
        except: cfp_value=None; print("Config Value is None!")
        
        return cfp, cfp_value
