from .programming_language import ProgrammingLanguage
from .source_code import SourceCode

VARIABLE = "variable"


class SyntaxAnalyzer:
    def __init__(self):
        self.operator_dictionary = {}
        self.token_and_type = {}
        self.end_of_line = []
        self.tokens = []
        self.lines = []

    def set_operator_and_data_type(self, operator: str, data_types: list):
        self.operator_dictionary[operator] = data_types

    def set_operator_and_data_type(self, dictionary: dict):
        self.operator_dictionary.update(dictionary)

    def check_source_code(self, programming_language: ProgrammingLanguage, tokens: list):
        self.__set_operator_type(programming_language, tokens)
        self.__change_token_data_type(tokens)
        self.__split_into_line(tokens)
        error = self.__set_variable_type()
        if error:
            return f"{error}"
        error = self.__check_unknown_variables()
        if error:
            return f"{error}"
        error = self.__check_operands()
        if error:
            return f"{error}"

    def __check_operands(self):
        for line_index,line in enumerate(self.lines,1):
            for index, token in enumerate(line, 1):
                if self.token_and_type[token] == "operator":
                    if self.token_and_type[line[index - 2]] == self.token_and_type[line[index]]:
                        if self.__check_acceptable_data_types(self.token_and_type[line[index]],token):
                            continue
                        else:
                            return f"В строке {line_index} нельзя выполнить операцию с этими типами данных"
                    return f"В строке {line_index} учавствуют операнды разных типов данных"
    def __check_acceptable_data_types(self,dataType: str,token: str) -> bool:
        for type in self.operator_dictionary[token]:
            if type == dataType:
                return True
        return False
    def __check_unknown_variables(self):
        for index, line in enumerate(self.lines, 1):
            for token in line:
                if self.token_and_type[token] == VARIABLE:
                    return f"Ошибка в строке {index}"

    def __set_variable_type(self):
        for line_index, line in enumerate(self.lines, 1):
            data_type = VARIABLE
            next = 0
            for index, token in enumerate(line, 1):
                if index == next:
                    if self.token_and_type[token] == VARIABLE:
                        self.token_and_type[token] = data_type
                    else:
                        return f"Ошибка в строке {line_index}"
                if self.token_and_type[token] == "dataType":
                    data_type = token
                    next = index + 1

    def __split_into_line(self, tokens: list):
        line_elements = []
        for index, token in enumerate(tokens, 1):
            if self.__check_last_token_of_line(index):
                line_elements.append(token[:-1])
                copied_line_elements = line_elements[:]
                self.lines.append(copied_line_elements)
                line_elements.clear()
            else:
                line_elements.append(token)

    def __check_last_token_of_line(self, index: int):
        for position in self.end_of_line:
            if index == position:
                return True
        return False

    def get_info(self):
        print(f"{self.token_and_type}")
        print(f"{self.end_of_line}")
        print(f"{self.lines}")
        print(f"{self.operator_dictionary}")

    def __change_token_data_type(self, tokens: list):
        for token in tokens:
            if token[-1] == ";":
                token = token[:-1]
            if token[0].isdigit():
                if self.__check_numeric_variable(token):
                    self.token_and_type[token] = "float"
                else:
                    self.token_and_type[token] = "int"
            if token[0] == "\"":
                self.token_and_type[token] = "string"

    def __check_numeric_variable(self, token: str):
        for char in token:
            if char == '.':
                return True
        return False

    def __set_operator_type(self, programming_language: ProgrammingLanguage, tokens: list):
        self.tokens = tokens
        for index, token in enumerate(tokens, 1):
            if self.__is_it_last_of_string(token):
                self.end_of_line.append(index)
                token = token[:-1]
            if token == "":
                continue
            if self.__is_it_reserved_word(token, programming_language):
                self.token_and_type[token] = programming_language.get_key_word_list().get(token)
            elif self.__is_it_operator(token):
                self.token_and_type[token] = "operator"
            else:
                self.token_and_type[token] = VARIABLE

    def __is_it_operator(self, token: str) -> bool:
        value = self.operator_dictionary.get(token)
        if value is not None:
            return True
        else:
            return False

    def __is_it_reserved_word(self, token: str, programming_language: ProgrammingLanguage) -> bool:
        value = programming_language.get_key_word_list().get(token)
        if value is not None:
            return True
        else:
            return False

    def __is_it_last_of_string(self, token: str) -> bool:
        for char in token:
            if char == ';':
                return True
        return False
