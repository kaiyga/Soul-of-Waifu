import os
import sys
import importlib
import importlib.util

def load_addons(addon_dir="addons"):
    addons_list = [addon for addon in os.listdir(addon_dir) if os.path.isdir(os.path.join(addon_dir, addon))]
    addons = []
    for addon in addons_list:
        try:
            spec = importlib.util.spec_from_file_location(addon, f"./addons/{addon}/__init__.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            addon_obj = module.load_addon()
            if addon_obj.check_load():
                addons.append(addon_obj)
            print(f"Addon {addon} is loaded")
        except Exception as e:
            print(f"Addon Ignored: {addon} has not be loaded!")
            print(f"\nError in module: {addon}:\n{e}\n\n============================\n")
      
    return addons


class Interface_Collection():
    def __init__(self) -> None:
        self.user_input_interface = {}
        self.user_translate_interface = {}

        self.ai_chat_interface = {}
        self.ai_translate_interface = {}
        self.ai_voice_interface = {}
        self.settings_menus= {}


class AddonCollection(Interface_Collection):
    def __init__(self) -> None:
        super().__init__()
        addons = load_addons()

        for addon in addons: self.user_input_interface.update(addon.user_input_interface)
        for addon in addons: self.user_translate_interface.update(addon.user_translate_interface)
        for addon in addons: self.ai_chat_interface.update(addon.ai_chat_interface) 
        for addon in addons: self.ai_translate_interface.update(addon.ai_translate_interface)
        for addon in addons: self.ai_voice_interface.update(addon.ai_voice_interface)
        for addon in addons: self.settings_menus.update(addon.settings_menus)

        
class AddonTemplate(Interface_Collection):
    """
    Addon template for inheritance
    """
    def __init__(self) -> None:
        self.pre_init()
        super().__init__()
        self.init_interfaces()

    def pre_init(self):
        """
        Check and init addon dependence 
        """
        pass

    def init_interfaces(self):
        """
        Init interfaces
        """
        pass

    def check_load(self):
        return True
    
    def reload(self):
        self.__init__()


    def add_Interface(self, interface_name:str="", interface_type:str=""):
        """
        Add Interface to list

        ### Use exemple
        ```py
        @self.addInterface("Inteface_name", "uii")
        keybord_uii() -> str:
            return input("Write to Neuro: ") 
        ```
        """
        def decorator(meth):
            def wrapper():
                module = {interface_name: meth}
                match interface_type:
                    case "user_input_interface" | "uii":
                        self.user_input_interface.update(module)
                    case "user_translate_interface" | "uti":
                        self.user_translate_interface.update(module)
                    
                    case "ai_chat_interface" | "aci":
                        self.ai_chat_interface.update(module)
                    case "ai_translate_interface" | "ati":
                        self.ai_translate_interface.update(module)
                    case "ai_voice_interface" | "avi":
                        self.ai_voice_interface.update(module)
                    case "settings_menu" | "stm":
                        self.settings_menus.update(module)   
            wrapper()
        return decorator
    





