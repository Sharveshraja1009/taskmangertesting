import unittest
from unittest.mock import patch
from tkinter import Tk
from task_manager_gui import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = TaskManager(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('tkinter.simpledialog.askstring', return_value="Edited Task")
    def test_add_and_edit_task(self, mock_input):
        # Add a task
        self.app.task_input.insert(0, "Test Task")
        self.app.due_date_input.insert(0, "2024-08-30")
        self.app.add_task()

        # Verify the task was added
        self.assertEqual(len(self.app.tasks), 1)
        self.assertEqual(self.app.tasks[0]["text"], "Test Task")
        self.assertEqual(self.app.tasks[0]["due_date"], "2024-08-30")
        self.assertEqual(self.app.tasks[0]["priority"], "Low")
        self.assertFalse(self.app.tasks[0]["completed"])

        # Simulate editing the task
        self.app.task_listbox.selection_set(0)
        self.app.edit_task()

        # Verify the task was edited
        self.assertEqual(self.app.tasks[0]["text"], "Edited Task")

    def test_remove_task(self):
        # Add a task to be removed
        self.app.task_input.insert(0, "Task to be removed")
        self.app.add_task()

        # Verify the task was added
        self.assertEqual(len(self.app.tasks), 1)

        # Simulate selecting and removing the task
        self.app.task_listbox.selection_set(0)
        self.app.remove_task()

        # Verify the task was removed
        self.assertEqual(len(self.app.tasks), 0)

    def test_filter_tasks(self):
        # Add multiple tasks with different priorities
        tasks = [("Task 1", "2024-08-30", "High"), ("Task 2", "2024-09-01", "Medium"), ("Task 3", "", "Low")]
        for text, due_date, priority in tasks:
            self.app.task_input.insert(0, text)
            self.app.due_date_input.insert(0, due_date)
            self.app.priority_var.set(priority)
            self.app.add_task()

        # Apply different filters and check the results
        self.app.filter_var.set("High")
        self.app.filter_tasks()
        self.assertEqual(len(self.app.get_filtered_tasks()), 1)

        self.app.filter_var.set("Medium")
        self.app.filter_tasks()
        self.assertEqual(len(self.app.get_filtered_tasks()), 1)

        self.app.filter_var.set("Low")
        self.app.filter_tasks()
        self.assertEqual(len(self.app.get_filtered_tasks()), 1)

        self.app.filter_var.set("All")
        self.app.filter_tasks()
        self.assertEqual(len(self.app.get_filtered_tasks()), 3)

if __name__ == '__main__':
    unittest.main()
