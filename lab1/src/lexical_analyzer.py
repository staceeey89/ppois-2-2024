from .source_code import SourceCode
class LexicalAnalyzer:
    def __init__(self):
        self.tokens = [str]
        self.error = ""
        self.forbidden_characters = ['@','#','$','%','^','&','*','!','~','/',':','?']


    def convert_to_tokens(self, source_code: SourceCode):
        self.tokens = []
        self.tokens = source_code.get_source_code().split()
        error: str = self.__check_correct_token_form()
        if error:
            self.error = error

    def __check_correct_token_form(self):
        for token in self.tokens:
            error: str
            if token[0].isdigit():
                error = self.__check_digital_token(token)
            else:
                error = self.__check_string_token(token)
            if error:
                return error
            error = self.__check_forbidden_characters(token)
            if error:
                return error

    def __check_forbidden_characters(self,token:str):
        if token == "*" or token == "/":
            return
        for char1 in token:
            for char2 in self.forbidden_characters:
                if char1 == char2:
                    return f"Неверный ввод токена: {token}"
    def __check_string_token(self,token: str):
        counter = 0
        for char in token:
            if char == '.':
                counter += 1
            if counter > 1:
                return f"Неверный ввод токена: {token}"
    def __check_digital_token(self,token: str):
        counter = 0
        for char in token:
            if char == ';':
                continue
            if char.isdigit() or char == '.':
                if char == '.':
                    counter += 1
                if char == '.' and counter > 1:
                    return f"Неверный ввод токена: {token}"
            else:
                return f"Неверный ввод токена: {token}"
    def get_list_of_tokens(self) -> list:
        if self.error:
            return self.error
        else:
            return self.tokens
