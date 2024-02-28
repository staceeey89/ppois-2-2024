class SourceCode:
    def __init__(self,source_code: str = "",descriprion: str = ""):
        self.__source_code = source_code
        self.description = descriprion
        self.file_extension = ""

    def __str__(self):
        description: str = self.description
        source_code: str = self.__source_code
        return f"{description} \n{source_code}"

    def change_source_code(self,source_code: str):
        self.__source_code = source_code

    def get_source_code(self) -> str:
        return self.__source_code
