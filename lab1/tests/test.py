from src.source_code import SourceCode
from src.person import Programmer, Person
from src.programming_language import ProgrammingLanguage
from src.compiler import Compiler
from src.optimizer import Optimizer
from src.syntax_analyzer import SyntaxAnalyzer
from src.lexical_analyzer import LexicalAnalyzer
from src.machine_code import MachineCode
import unittest

class TestPerson(unittest.TestCase):
    def test_get_person_info(self):
        person = Person("Steve Jobs", 25)
        info = person.get_person_info()
        self.assertEqual(info, "Steve Jobs \nAge: 25")

class TestProgrammer(unittest.TestCase):
    def test_set_personal_data(self):
        programmer = Programmer()
        programmer.set_personal_data("Yurhilevich Eugene", 30, 5)
        self.assertEqual(programmer.full_name, "Yurhilevich Eugene")
        self.assertEqual(programmer.age, 30)
        self.assertEqual(programmer.experience, 5)

    def test_write_source_code(self):
        programmer = Programmer()
        programmer.write_source_code("py", "print('Hello')", "Python code")
        self.assertEqual(programmer.source_code.file_extension, "py")
        self.assertEqual(programmer.source_code.get_source_code(), "print('Hello')")
        self.assertEqual(programmer.source_code.description, "Python code")

class TestLexicalAnalyzer(unittest.TestCase):
    def test_correct_token_form(self):
        source_code = SourceCode("int x = 10;")
        lexical_analyzer = LexicalAnalyzer()
        lexical_analyzer.convert_to_tokens(source_code)
        self.assertEqual(lexical_analyzer.error, "")

    def test_forbidden_characters(self):
        source_code = SourceCode("x @= 5;")
        lexical_analyzer = LexicalAnalyzer()
        lexical_analyzer.convert_to_tokens(source_code)
        self.assertNotEqual(lexical_analyzer.error, "")

class TestProgrammingLanguage(unittest.TestCase):
    def setUp(self):
        self.language = ProgrammingLanguage("Python", "py", {"if": "conditional", "for": "loop"})

    def test_str_method(self):
        self.assertEqual(str(self.language), "Language: Python\nFile extension: .py")

    def test_add_new_key_words_list(self):
        key_word_list = {"while": "loop", "def": "function"}
        self.language.add_new_key_words(key_word_list)
        self.assertEqual(self.language.get_key_word_list(), {"if": "conditional", "for": "loop", "while": "loop", "def": "function"})

    def test_get_key_word_list(self):
        key_word_list = self.language.get_key_word_list()
        self.assertIsInstance(key_word_list, dict)

class TestSourceCode(unittest.TestCase):
    def test_change_source_code(self):
        source_code = SourceCode("print('Hello, World!')", "Sample code")
        new_source_code = "print('Updated code')"
        source_code.change_source_code(new_source_code)
        self.assertEqual(source_code.get_source_code(), new_source_code)

    def test_get_source_code(self):
        source_code = SourceCode("print('Hello, World!')", "Sample code")
        expected_source_code = "print('Hello, World!')"
        self.assertEqual(source_code.get_source_code(), expected_source_code)

    def test_str_representation(self):
        source_code = SourceCode("print('Hello, World!')", "Sample code")
        expected_str = "Sample code \nprint('Hello, World!')"
        self.assertEqual(str(source_code), expected_str)

class TestSyntaxAnalyzer(unittest.TestCase):
    def test_check_source_code_valid(self):
        programmer = Programmer()
        programmer.set_personal_data("Yurhilevich Eugene Vitalievich", 18, 2)
        str1 = "int a = 15; int b; b = a + 23; int c; c = a + b; cout << a + b;"
        str2 = "Этот код складывается два числа по условию, а=15, б=а+23. И выводит результат а+б на экран"
        programmer.write_source_code("cpp", str1, str2)
        dct = {"int": "dataType", "float": "dataType", "return": "singleOperator", "string": "dataType", "cout": "singleOperator", "<<": "singleOperator"}
        lang = ProgrammingLanguage("C++", "cpp", dct)
        lexycal_analyzer = LexicalAnalyzer()
        lexycal_analyzer.convert_to_tokens(programmer.get_source_code())
        dct2 = {"+": ["int", "float", "string"], "-": ["int", "float"], "=": ["int", "float", "string"],
                "*": ["int", "float"], "/": ["int", "float"]}
        syntax_analyzer = SyntaxAnalyzer()
        syntax_analyzer.set_operator_and_data_type(dct2)
        error = syntax_analyzer.check_source_code(lang, lexycal_analyzer.tokens)
        self.assertEqual(error, None)

class TestCompiler(unittest.TestCase):
    def test_compile_the_project(self):
        programmer = Programmer()
        programmer.set_personal_data("Yurhilevich Eugene Vitalievich", 18, 2)
        str1 = "int a = 15; int b; b = a + 23; int c; c = a + b; cout << a + b;"
        str2 = "Этот код складывается два числа по условию, а=15, б=а+23. И выводит результат а+б на экран"
        programmer.write_source_code("cpp", str1, str2)
        dct = {"int": "dataType", "float": "dataType", "return": "singleOperator", "string": "dataType",
               "cout": "singleOperator", "<<": "singleOperator"}
        language = ProgrammingLanguage("C++", "cpp", dct)
        dct2 = {"+": ["int", "float", "string"], "-": ["int", "float"], "=": ["int", "float", "string"],
                "*": ["int", "float"], "/": ["int", "float"]}
        compiler = Compiler()
        compiler.compile_the_project(programmer.get_source_code(), language, dct2)
        self.assertEqual(compiler.optimize_code, "int a=15;int b=a+23;int c=a+b;cout<<a+b;")
        self.assertEqual(compiler.error, "Нет ошибок компиляции")

class TestMachineCode(unittest.TestCase):
    def test_translate_to_machine_code(self):
        optimizer = Optimizer()
        optimizer.result_code = "a+b"
        machine_code = MachineCode()
        machine_code.translate_to_machine_code(optimizer)
        self.assertEqual(machine_code.get_machine_code(),"011000010010101101100010")

if __name__ == '__main__':
    unittest.main()
