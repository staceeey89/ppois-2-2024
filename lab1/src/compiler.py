from .source_code import SourceCode
from .machine_code import MachineCode
from .programming_language import ProgrammingLanguage
from .lexical_analyzer import LexicalAnalyzer
from .syntax_analyzer import SyntaxAnalyzer
from .optimizer import Optimizer


class Compiler:
    def __init__(self):
        self.source_code: str = ""
        self.machine_code: str = ""
        self.error: str = "Нет ошибок компиляции"
        self.optimize_code: str = ""

    def __str__(self):
        return f"\nSource code:\n{self.source_code}\nOptimize code: {self.optimize_code}\nMachine code: {self.machine_code}\n{self.error}"

    def compile_the_project(self,source_code: SourceCode,programming_language: ProgrammingLanguage,operators: dict):
        self.source_code = source_code.get_source_code()
        lexical_analyzer = LexicalAnalyzer()
        lexical_analyzer.convert_to_tokens(source_code)
        if lexical_analyzer.error:
            self.error = lexical_analyzer.error
            return
        syntax_analyzer = SyntaxAnalyzer()
        syntax_analyzer.set_operator_and_data_type(operators)
        error = syntax_analyzer.check_source_code(programming_language,lexical_analyzer.tokens)
        if error:
            self.error = error
            return
        optimizer = Optimizer()
        optimizer.optimize_source_code(syntax_analyzer)
        self.optimize_code = optimizer.result_code
        machine_code = MachineCode()
        machine_code.translate_to_machine_code(optimizer)
        self.machine_code = machine_code.get_machine_code()
