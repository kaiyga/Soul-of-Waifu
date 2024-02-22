import os 
import asyncio

os.system(f"pip install -r {__path__[0]}/req.txt")


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
        
        self.config = CharacterAI_Config(f"{__path__[0]}/config.yml")

        # Login in ChrAI

        try: self.cAI_client = PyAsyncCAI(self.config.config['api']['api_key']); print("Client Succses")
        except: self.cAI_client = None
    
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

            if self.cAI_client == None: return "Pls configure module: Character AI : Self.Client Error"
            if self.chat == None: return "Pls configure module: Character AI: Self.Chat Error" 

            async def c(self, text=text):
                async with self.cAI_client.connect() as chat2:
                    data = await chat2.send_message( self.cAI_character, self.chat['chats'][0]['chat_id'], text, self.author)
                    return data['turn']['candidates'][0]['raw_content']
            return asyncio.run(c(self, text))


    async def getCAIChat(self):
        return await self.cAI_client.chat2.get_chat(self.cAI_character)
    
    def get_character_id(self):
        return self.config.config['character_list']['list'][ self.config.config['api']['character'] ] 
        


    class CharacterAI_Settings(Settings_Menu):
        def __init__(self, config: Config, chrAI_Module_obj) -> None:
            self.obj = chrAI_Module_obj
            super().__init__(config, chrAI_Module_obj)
          
            
        def init_fields(self):
            self = self
    
            self.add_settings_write_point("API KEY", self.obj, "api.api_key" )
            self.add_settings_point("Character", self.obj, "api.character", self.config.config['character_list']['list'])
            @self.add_fieldFunc("Add Character")
            def add_character():
                print("Write 'quit' for exit")
                chr_name = input("Character Name: ")
                if chr_name == "quit" : return
                chr_id = input("Character ID: ")
                if chr_name == "quit" : return

                self.config.config['character_list']['list'][chr_name] = chr_id
                self.reload_conf(self.obj)

            @self.add_fieldFunc("Delete Character")
            def delete_character():
                i=0
                chr_list =self.config.config['character_list']['list']
                chr_name = self.selector("Delete Character: ", chr_list, 0)
                if chr_name == None: return
                
                self.config.config['character_list']['list'].pop(chr_name)
                self.reload_conf(self.obj)
                return
#                    except: "Value not found. Try again"
                    


def load_addon():
    return CharacterAI_Addon()
