import os
import asyncio

os.system(f"pip install -r {__path__[0]}/req.txt")


from gulysh_lib.menu_lib import Config, Settings_Menu
from gulysh_lib.addon_lib import AddonTemplate


from gpytranslate import Translator


class GoogleTranslater_Addon(AddonTemplate):
    def __init__(self) -> None:
        self.t = Translator()

        super().__init__()

    def init_interfaces(self): 
        self = self

        def translate(text="", targetlang="en")-> str:
            translation = asyncio.run(self.t.translate(text, targetlang=targetlang))
            return translation.text           

        @self.add_Interface("GoogleTranslater", "uti")
        def translater(text, targetlang)->str:
            return translate(text, targetlang)

        @self.add_Interface("GoogleTranslater", "ati")
        def translater(text, targetlang)-> str:            
            return translate(text, targetlang)


def load_addon():
    return GoogleTranslater_Addon()