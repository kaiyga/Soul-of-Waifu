
# Файл реализующий класс пользователя, его интерфейсы и селекторы его интерфейсов. 
# Способы модификации класса интерфейса, деклариются каждым классом в отдельности. 
# Какие значения Конфига получает селектор 
# Какой тип данных получает интерфейс и Какой тип данных он возвращает

from .addon_lib import Interface_Collection


class DialogEntity():
    def __init__(self) -> None:
        self.entityname = ""
    
    def split_selector(self, key, module_list):
        for module in module_list.keys():
            if module == key:
                return module_list[module]
        print(f"Interface {key} not found, use standard inteface")
        return module_list[list(module_list.keys())[0]]

    def reload(self):
        self.__init__()

class User(Interface_Collection, DialogEntity):
    def __init__(self, config, addon_collection:Interface_Collection):
        super().__init__()
        self.user_input_interface= self.split_selector(config['user']['input_interface'], addon_collection.user_input_interface)
        self.user_translate_interface = self.split_selector(config['user']['translate_interface'], addon_collection.user_translate_interface)
    

    def reload(self, config, addon_collection:Interface_Collection):
        self.__init__(config, addon_collection)


class AI(Interface_Collection, DialogEntity):
    def __init__(self, config, addon_collection:Interface_Collection) -> None:
        super().__init__()
        self.ai_chat_interface = self.split_selector(config['ai']['chat_interface'], addon_collection.ai_chat_interface) 
        self.ai_translate_interface= self.split_selector(config['ai']['translate_interface'], addon_collection.ai_translate_interface)
        self.ai_voice_interface = self.split_selector(config['ai']['voice_interface'], addon_collection.ai_voice_interface)

    def reload(self, config, addon_collection:Interface_Collection):
        self.__init__(config, addon_collection)

