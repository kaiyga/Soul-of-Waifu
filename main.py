#from gulysh_lib import *

import sys
import os
from asyncio import run
sys.dont_write_bytecode = True



from gulysh_lib.config_lib import Config
from gulysh_lib.addon_lib import AddonCollection 
from gulysh_lib.menu_lib import Config, Menu, Settings_Menu
from gulysh_lib.user_lib import DialogEntity, AI, User
dbg = False

addon_collection = AddonCollection()
settings_config = Config("./configs/config.yml")

ai:AI = AI(settings_config.config, addon_collection)        
user:User = User(settings_config.config, addon_collection)

class Main_Menu(Menu):
    def __init__(self) -> None:
        self.lang = Config(str("configs/lang" + f"/{settings_config.config['lang']['file']}")).config
        super().__init__(dbg)
        
    def init_fields(self):
        self = self

        @self.add_fieldFunc(self.lang["main_menu_selector"]["start_runtime"])
        def start_runtime():
            self.clear_console()
            print("Print 'quit' for exit")
            while True:
                try:
                    inpt = user.user_input_interface()
                    if inpt == "quit": return
                    ai.ai_voice_interface(ai.ai_translate_interface(ai.ai_chat_interface(user.user_translate_interface(inpt, "en")), settings_config.config['lang']['file'].split(".")[0]))
                except: print('')
        @self.add_fieldFunc(self.lang["main_menu_selector"]["settings"])
        def start_settings():
            Settings_Menu_Runtime(settings_config).start()

        @self.add_fieldFunc(self.lang['interfaces_settings']['addon_settings'])
        def addons_settings():
            Addon_Settings_Menu(settings_config).start()
            
        @self.add_fieldFunc(self.lang["main_menu_selector"]["stop"])
        def stop():
            sys.exit()



main_menu = Main_Menu()


class Settings_Menu_Runtime(Settings_Menu):
    def __init__(self, config: Config) -> None:
        self.lang = Config(str("configs/lang" + f"/{settings_config.config['lang']['file']}")).config
        super().__init__(config, DialogEntity())
        self.debug=dbg
    

    def init_fields(self):
        settings_menu_lang = self.lang['interfaces_settings']

        self.add_field("Quit", None)
        self.add_settings_point(settings_menu_lang['input_interface'], user, "user.input_interface", addon_collection.user_input_interface)
        self.add_settings_point(settings_menu_lang['user_translate_interface'], user, "user.translate_interface", addon_collection.user_translate_interface)
        
        self.add_settings_point(settings_menu_lang['chat_interface'], ai, "ai.chat_interface", addon_collection.ai_chat_interface)
        self.add_settings_point(settings_menu_lang['ai_translate_interface'], ai, "ai.translate_interface", addon_collection.ai_translate_interface)
        self.add_settings_point(settings_menu_lang['voice_interface'], ai, "ai.voice_interface", addon_collection.ai_voice_interface)

        self.lang_selectinon_init()


    def lang_selectinon_init(self):
        
        lang_files = os.listdir("configs/lang/")
        lang_list= {}
        for langs in lang_files: lang_list.update({langs: f"configs/lang/{langs}"})

        self.add_settings_point(self.lang['interfaces_settings']['lang'], user, "lang.file", lang_list)


    def add_settings_point(self, field_name="", obj=None, config_path="ai.chat_interface", module_list={}):
        cfp = config_path.split(".")
        return super().add_settings_point(field_name, obj, config_path, module_list, self.lang[f"{cfp[0]}_selectors"][cfp[1]])
    
    def reload_conf(self, obj):
        settings_config.dump()
        
        main_menu.__init__()

        obj.reload(settings_config.config, addon_collection)
        self.__init__(self.config)
    

class Addon_Settings_Menu(Settings_Menu):
    def __init__(self, config: Config) -> None:
        self.lang = Config(str("configs/lang" + f"/{settings_config.config['lang']['file']}")).config
        super().__init__(config, DialogEntity())
    
    def init_fields(self):
        self.add_field("Quit", None)
        self.menu_fields.update(addon_collection.settings_menus)
        @self.add_fieldFunc("Download addon")
        def download_addon():
            while True:
                try: link = input(self.lang['addon_settings']['addon_download'])
                except: print("Not valid")

                try: os.system(f"cd addons; git clone {link} ; cd .." )
                except: print("Download Error. Check README")

                addon_collection.__init__()                
                print("Complete!")

                break
            
main_menu.start()
