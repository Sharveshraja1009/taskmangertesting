import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Task Manager")

        self.tasks = []

        self.filter_var = tk.StringVar()
        self.filter_var.set("All")

        self.create_widgets()

    def create_widgets(self):
        # Filter section
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        filter_label = tk.Label(filter_frame, text="Filter by priority:")
        filter_label.pack(side=tk.LEFT)

        filter_options = ["All", "High", "Medium", "Low"]
        filter_menu = tk.OptionMenu(filter_frame, self.filter_var, *filter_options, command=self.filter_tasks)
        filter_menu.pack(side=tk.LEFT, padx=5)

        # Input fields
        self.task_input = tk.Entry(self.root, width=40)
        self.task_input.pack(pady=5)

        self.due_date_input = tk.Entry(self.root, width=20)
        self.due_date_input.pack(pady=5)
        self.due_date_input.insert(0, "YYYY-MM-DD")

        self.priority_var = tk.StringVar()
        self.priority_var.set("Low")
        priority_options = ["Low", "Medium", "High"]
        priority_menu = tk.OptionMenu(self.root, self.priority_var, *priority_options)
        priority_menu.pack(pady=5)

        add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        add_button.pack(pady=10)

        # Task list
        self.task_listbox = tk.Listbox(self.root, width=70, height=15)
        self.task_listbox.pack(pady=20)

        self.task_listbox.bind('<Double-Button-1>', self.toggle_completion)

        # Buttons
        edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        edit_button.pack(side=tk.LEFT, padx=10)

        remove_button = tk.Button(self.root, text="Remove Task", command=self.remove_task)
        remove_button.pack(side=tk.LEFT, padx=10)

    def add_task(self):
        task_text = self.task_input.get().strip()
        due_date = self.due_date_input.get().strip()
        priority = self.priority_var.get()

        if not task_text:
            messagebox.showwarning("Input Error", "Please enter a task.")
            return

        if due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showwarning("Date Error", "Please enter a valid date in YYYY-MM-DD format.")
                return

        task_info = {
            "text": task_text,
            "due_date": due_date,
            "priority": priority,
            "completed": False
        }
        self.tasks.append(task_info)
        self.task_input.delete(0, tk.END)
        self.due_date_input.delete(0, tk.END)
        self.due_date_input.insert(0, "YYYY-MM-DD")
        self.priority_var.set("Low")

        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        filtered_tasks = self.get_filtered_tasks()

        for task in filtered_tasks:
            task_str = self.format_task_string(task)
            self.task_listbox.insert(tk.END, task_str)

    def get_filtered_tasks(self):
        filter_value = self.filter_var.get()
        if filter_value == "All":
            return self.tasks
        return [task for task in self.tasks if task["priority"] == filter_value]

    def format_task_string(self, task):
        status = "(Completed)" if task["completed"] else ""
        due_date_str = f"Due: {task['due_date']}" if task['due_date'] else ""
        return f"{task['text']} {due_date_str} - Priority: {task['priority']} {status}"

    def toggle_completion(self, event):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            return

        task = self.tasks[selected_index[0]]
        task["completed"] = not task["completed"]
        self.refresh_task_list()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            return

        task = self.tasks[selected_index[0]]
        new_task_text = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=task["text"])

        if new_task_text and new_task_text.strip():
            task["text"] = new_task_text.strip()
            self.refresh_task_list()

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            return

        del self.tasks[selected_index[0]]
        self.refresh_task_list()

    def filter_tasks(self, *args):
        self.refresh_task_list()


if __name__ == "__main__":
    root = tk.Tk()
    task_manager = TaskManager(root)
    root.mainloop()
