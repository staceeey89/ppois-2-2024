import unittest
import main


class TestPassword(unittest.TestCase):
    def setUp(self):
        self.OS = main.OperatingSystem("Olegux")

    def test_set_correct_password(self):
        self.OS.set_password('1234')
        self.assertEqual(self.OS.password, '1234')


class TestNetwork(unittest.TestCase):
    def setUp(self):
        self.OS = main.OperatingSystem("Olegux")
        self.linked_os = main.OperatingSystem("OS1")
        self.OS.form_network(self.linked_os)
        self.linked_os.form_network(self.OS)

    def test_connecting(self):
        self.assertIn(self.linked_os, self.OS.network_protocol.osc)
        self.assertIn(self.OS, self.linked_os.network_protocol.osc)

    def test_send_message(self):
        self.OS.send("hello", self.linked_os.name)
        self.assertEqual(self.linked_os.kernel.signal.content, "hello")
        self.assertEqual(self.OS.kernel.signal.content, "Accepted!")


class TestFileSystemAndDriver(unittest.TestCase):
    def setUp(self):
        self.OS = main.OperatingSystem("Olegux")
        self.file = self.OS.create_file('file.txt', "Hello world!")
        self.OS.install_driver("GPU")

    def test_creation_file(self):
        self.assertIn(self.file, self.OS.file_system.files)

    def test_deleting_file(self):
        self.OS.delete_file('file.txt')
        self.assertNotIn(self.file, self.OS.file_system.files)

    def test_viewing_content(self):
        self.assertEqual(self.OS.view_content('file.txt'), 'Hello world!')

    def test_installing_driver(self):
        self.assertTrue(self.OS.check_driver('GPU'))


class TestProcesses(unittest.TestCase):
    def setUp(self):
        self.OS = main.OperatingSystem("Olegux")
        self.OS.start()
        self.process = self.OS.fork(50)

    def test_creation_process(self):
        self.assertIn(self.process, self.OS.kernel.processes)

    def test_deleting_process(self):
        self.OS.terminate_process('2')
        self.assertNotIn(self.process, self.OS.kernel.processes)


if __name__ == '__main__':
    unittest.main()
