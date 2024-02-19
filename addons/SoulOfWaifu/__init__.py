
from gulysh_lib.menu_lib import Config
from gulysh_lib.addon_lib import AddonTemplate

class SoulOfWaifu(AddonTemplate):
    def __init__(self) -> None:
        super().__init__()
        self.addon_path = "./addons/content/"
    
    def pre_init(self):
        pass

    def init_interfaces(self):
        @self.add_Interface("Keybord Input", "uii")
        def keybord_input() -> str:
            return str(input("You # "))
        
        @self.add_Interface("Translate OFF", "uti")
        def translate(text:str, targetlang:str="") -> str:
            return text
        
        @self.add_Interface("AI OFF", "aci")
        def empety_text_of_answer(text:str) -> str:
            return "RUNTIME IS WORK. PLS ENABLE MODULE OF YOUR AI CHAT FOR GETTING CHAT"


        @self.add_Interface("Translate OFF", "ati")
        def translate(text:str, targetlang:str="") -> str:
            return text


        @self.add_Interface("Print text", "avi")
        def print_text(text:str) -> str:
            print("SoulOfWaifu # ", text)


def load_addon():
    return SoulOfWaifu()


