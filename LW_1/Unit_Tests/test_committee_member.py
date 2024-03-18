from CommitteeMember import CommitteeMember
import unittest

class TestCommitteeMember(unittest.TestCase):
    def setUp(self):
        self.member = CommitteeMember("Иванов Иван", "БГУИР")
        self.member1 = CommitteeMember("Иванов Иван", "Комитет A")
        self.member2 = CommitteeMember("Петров Петр", "Комитет B")
        self.member1.assign_task("Написать отчет")

    def test_getters(self):
        self.assertEqual(self.member.get_tasks(), [])
        self.assertEqual(self.member.get_priority_map(), {})
        self.assertEqual(self.member.get_deadlines(), {})

    def test_assign_task(self):
        self.member.assign_task("Написать отчет", priority="высокий", deadline="31.12.2023")
        self.assertIn("Написать отчет", self.member.get_tasks())

    def test_complete_task(self):
        self.member.assign_task("Написать отчет")
        self.member.complete_task("Написать отчет")
        self.assertNotIn("Написать отчет", self.member.get_tasks())

    def test_delegate_task_valid(self):
        self.member1.delegate_task("Написать отчет", self.member2)
        self.assertNotIn("Написать отчет", self.member1.get_tasks())
        self.assertIn("Написать отчет", self.member2.get_tasks())

    def test_generate_task_report(self):
        self.member.assign_task("Задача 4", priority="высокий", deadline="Сегодня")
        self.member.assign_task("Задача 5", priority="средний", deadline="Завтра")
        self.member.assign_task("Задача 6", priority="низкий")
        self.member.complete_task("Задача 4")
        report = self.member.generate_task_report()
        self.assertIn("Задача 5", report)
        self.assertIn("Задача 6", report)

    def test_review_paper(self):
        paper = "Статья"
        self.member.review_paper(paper)

    def test_vote(self):
        decision = "Да"
        self.member.vote(decision)

    def test_organize_meeting(self):
        meeting_time = "Завтра в 15:00"
        self.member.organize_meeting(meeting_time)

    def test_send_reminder(self):
        reminder = "Не забудьте про встречу завтра."
        self.member.send_reminder(reminder)


if __name__ == '__main__':
    unittest.main()