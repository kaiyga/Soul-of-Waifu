import os

os.system(f"pip install -r {__path__[0]}/req.txt")

from gulysh_lib.menu_lib import Config, Settings_Menu
from gulysh_lib.addon_lib import AddonTemplate

from elevenlabs import generate, set_api_key, play, get_api_key

class ElevenLabs_Config(Config):
    def __init__(self, config_file) -> None:
        try: super().__init__(config_file)
        except:
            self.config_scheme= {"api":{ "api_key": "", "voice": "Nicole"}}
            self.dump(self.config_scheme)

class ElevenLabs_Addon(AddonTemplate):
    def __init__(self) -> None:
        super().__init__()
        
        self.config = ElevenLabs_Config(f"{__path__[0]}/config.yml")
        try: self.voice = self.config.config['api']['voice']; print(f"ElevenLabs Voice set {self.voice}")
        except: self.voice =  "Nicole"; print("ERROR: ElevenLabs Voice not found: Use Nicole voice")

        try: set_api_key(self.config.config['api']['api_key']); print("ElevenLabs API Key set")
        except: set_api_key(None); print("ERROR: ElevenLabs API Key set error")
        
       
    def init_interfaces(self): 
        self = self

        @self.add_Interface("ElevenLabs", "stm")
        def start_settings():
            self.ElevenLabs_Settings(self.config, self).start()
        

        @self.add_Interface("ElevenLabs Voice", "avi")
        def eleven_labs_voice(text=""):
            
            print(f"Soul Of Waifu # {text}")

            if get_api_key() == "":
                self.go_to_settings()
            
            try: 
                audio = generate(text = text, voice = self.voice, model = "eleven_multilingual_v2",)
                play(audio)
            except Exception as e:
                print(f"ERROR: Pls check ElevenLabs Configuration \n\n{e}")
                
    def go_to_settings(self):
        st = self.ElevenLabs_Settings(self.config, self)
        st.clear_console(); print(st.color.wrap("ERROR: Change Elevenlabs API key!", str(st.color.BOLD + st.color.RED)))
        st.start(clear=False)
        

    class ElevenLabs_Settings(Settings_Menu):
        def __init__(self, config: Config, Elevenlabs_Module_obj) -> None:
            self.obj = Elevenlabs_Module_obj
            super().__init__(config, Elevenlabs_Module_obj)
   
          
            
        def init_fields(self):
            self = self
            self.add_settings_write_point("API KEY", self.obj, "api.api_key" )
            self.add_settings_write_point("Voice", self.obj, "api.voice")


def load_addon():
    return ElevenLabs_Addon()