import os 
import asyncio

os.system(os.path.normpath(f"pip install -r {__path__[0]}/req.txt"))


from gulysh_lib.menu_lib import Config, Settings_Menu
from gulysh_lib.addon_lib import AddonTemplate  

from characterai import PyAsyncCAI

class CharacterAI_Config(Config):
    def __init__(self, config_file) -> None:
        try: super().__init__(config_file)
        except:
            self.config_scheme= {"api":{ "api_key": "", "character": "Chraracter Assistent"}, "character_list": {"list": {"Chraracter Assistent" : "YntB_ZeqRq2l_aVf2gWDCZl4oBttQzDvhj9cXafWcF8"}}}
            self.dump(self.config_scheme)

class CharacterAI_Addon(AddonTemplate):
    def __init__(self) -> None:
        super().__init__()
        
        # Load Config 
        self.config = CharacterAI_Config(f"{__path__[0]}/config.yml")

        try: # Login in ChrAI
            self.cAI_client = PyAsyncCAI(self.config.config['api']['api_key'])
            print(asyncio.run(self.cAI_client.user.followers()))
            print("Client Succses")
        except: # Set None ChrAI
            self.cAI_client = None
    
        try: self.cAI_character = self.get_character_id()
        except Exception as e: self.cAI_client = None
        
        try: self.chat = asyncio.run(self.getCAIChat()); print("Chat get Succses")
        except Exception as e: self.chat = None; print(e)
            
        try: self.author = {'author_id': self.chat['chats'][0]['creator_id']}; print("Get Author Succses")
        except: self.author = None

    def init_interfaces(self):
        self=self

        # Add settings module 
        @self.add_Interface("Character AI", "stm")
        def start_menu():
            self.CharacterAI_Settings(self.config, self).start()

        # Add chat module
        @self.add_Interface("CharacterAI Chat", "aci")
        def character_ai_chat(text:str) -> str:

            if self.cAI_client == None: self.go_to_settings("\nCharecter AI API ERROR: Your API key is not valid.\n\nAdd valid API Key from https://beta.character.ai/profile?\nHow find API-key https://pycai.gitbook.io/welcome/api/values"); \
            print("CharacterAI - Addon: Sorry, you should have API. You can try again");\
            return None
            
            if self.chat == None: self.go_to_settings("Pls add/change valid character"); \
            print("CharacterAI - Addon: Sorry, you should have Character for dialog. You can try again");\
            return None

            
            async def c(self, text=text):
                async with self.cAI_client.connect() as chat2:
                    data = await chat2.send_message( self.cAI_character, self.chat['chats'][0]['chat_id'], text, self.author)
                    return data['turn']['candidates'][0]['raw_content']
            return asyncio.run(c(self, text))


    async def getCAIChat(self):
        return await self.cAI_client.chat2.get_chat(self.cAI_character)

    def get_character_id(self):
        return self.config.config['character_list']['list'][ self.config.config['api']['character'] ] 
        
    def go_to_settings(self, error):
        print("In go to settings")
        i = self.CharacterAI_Settings(self.config, self)
        i.clear_console(); 
        print(i.color.wrap(error, str(f"{i.color.BOLD} {i.color.RED}")))
        i.start(clear=False)


    class CharacterAI_Settings(Settings_Menu):
        def __init__(self, config: Config, chrAI_Module_obj, debug=False) -> None:
            super().__init__(config, chrAI_Module_obj, debug)
        

        def init_fields(self):
            self = self

            self.add_settings_write_point("API KEY", self.obj, "api.api_key" )
            
            self.add_settings_point("Character", self.obj, "api.character", self.config.config['character_list']['list'])

            @self.add_fieldFunc("Add Character")
            def add_character():
                try:
                    print("Write 'quit' for exit")
                    chr_name = input("Character Name: ")
                    if chr_name == "quit" : return
                    chr_id = input("Character ID: ")
                    if chr_name == "quit" : return

                    self.config.config['character_list']['list'][chr_name] = chr_id
                    self.reload_conf(self.obj)
                except: print("Write 'quit' to exit")
                
            @self.add_fieldFunc("Delete Character")
            def delete_character():
                try: 
                    i=0
                    chr_list =self.config.config['character_list']['list']
                    chr_name = self.selector("Delete Character: ", chr_list, 0)
                    if chr_name == None: return
                    
                    self.config.config['character_list']['list'].pop(chr_name)
                    self.reload_conf(self.obj)
                    return
                except: print("Write 'quit' to exit")    


def load_addon():
    return CharacterAI_Addon()
