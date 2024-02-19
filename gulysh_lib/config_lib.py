import yaml
class Config():
    def __init__(self, config_file) -> None:
        self.config_file = config_file
        self.config = self.load()
        self.config_scheme = {}

    def load(self):
        """
        ## Загрузка конфига из файла
        """
        with open(self.config_file) as f:
            return yaml.safe_load(f)
         
    def reload(self):
        """
        Обновление конфига за счёт реинициализации объекта конфига
        """
        self.__init__()

    def dump(self):
        """
        Запись конфига назад в файл и обновление
        """
        with open(self.config_file) as f:
            yaml.safe_dump(f)
        self.reload()

    def change_value(self, config_path, value):
        # Признаю решение не сверх гениальным, но зато правльным.___.
        """
        Обновление значений конфига с последующим дампом и обновлением
        """
        config_path = value
        self.dump()
