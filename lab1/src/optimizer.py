from .syntax_analyzer import SyntaxAnalyzer


class Optimizer:
    def __init__(self):
        self.result_code: str = ""

    def __str__(self):
        return self.result_code

    def optimize_source_code(self, syntax_analyzer: SyntaxAnalyzer):
        lines = syntax_analyzer.lines
        for line in lines:
            for token in line:
                self.result_code += token
                if syntax_analyzer.token_and_type[token] == "dataType":
                    self.result_code += " "
            if len(line) == 2:
                buffer_value = line[1]
                del lines[self.__find_next_buffer_value_entry(lines, buffer_value)]
            self.result_code += ";"

    def __find_next_buffer_value_entry(self, lines: list, value: str):
        for index,line in enumerate(lines,0):
            if len(line) > 2 and line[0] == value:
                for token_index, token in enumerate(line, 0):
                    if token_index > 0:
                        self.result_code += token
                return index