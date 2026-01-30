import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import json
from datetime import datetime


class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")
        master.geometry("500x700")
        master.resizable(False, False)
        master.configure(bg="#F5F2EE")

        self.tasks = []
        self.tasks_file = os.path.join(os.path.dirname(__file__), "tasks.json")
        self.priority_var = tk.StringVar(value="Medium")

        # ---------- HEADER ----------
        header_frame = tk.Frame(master, bg="#E8E2DC", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="TO - DO LIST",
            font=("Arial", 20, "bold"),
            bg="#E8E2DC",
            fg="#3E3A37"
        ).pack(pady=12)

        tk.Frame(master, bg="#DED6CE", height=2).pack(fill="x", pady=(0, 10))

        # ---------- STATS ----------
        stats_frame = tk.Frame(master, bg="#DED6CE")
        stats_frame.pack(padx=20, fill="x")

        self.stats_label = tk.Label(
            stats_frame,
            text="Total: 0 | Pending: 0 | Completed: 0",
            font=("Arial", 10),
            bg="#DED6CE",
            fg="#6E6761"
        )
        self.stats_label.pack(pady=5)

        # ---------- INPUT ----------
        input_container = tk.Frame(master, bg="#DED6CE")
        input_container.pack(padx=20, pady=10, fill="x")

        self.task_entry = tk.Entry(
            input_container,
            font=("Arial", 14),
            bg="#F0ECE8",
            fg="#3E3A37",
            insertbackground="#3E3A37",
            relief="flat"
        )
        self.task_entry.pack(fill="x", padx=10, pady=10)
        self.task_entry.bind("<Return>", lambda _: self.add_task())

        # ---------- PRIORITY ----------
        priority_frame = tk.Frame(master, bg="#F5F2EE")
        priority_frame.pack(pady=5)

        tk.Label(
            priority_frame,
            text="Priority:",
            bg="#F5F2EE",
            fg="#3E3A37"
        ).pack(side="left", padx=5)

        for priority in ["High", "Medium", "Low"]:
            tk.Radiobutton(
                priority_frame,
                text=priority,
                variable=self.priority_var,
                value=priority,
                bg="#F5F2EE",
                fg="#3E3A37",
                selectcolor="#F0ECE8",
                activebackground="#F5F2EE",
                activeforeground="#3E3A37"
            ).pack(side="left", padx=3)

        # ---------- ADD BUTTON ----------
        self.add_button = self.rounded_button(
            master, "Add Task", self.add_task, width=180, height=44, radius=16
        )
        self.add_button.pack(pady=12)

        # ---------- TASKS ----------
        tasks_container = tk.Frame(master, bg="#DED6CE")
        tasks_container.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(
            tasks_container,
            text="TASKS",
            font=("Arial", 14, "bold"),
            bg="#DED6CE",
            fg="#3E3A37"
        ).pack(pady=10)

        # 🔹 Bigger font = bigger checkbox
        self.task_listbox = tk.Listbox(
            tasks_container,
            font=("Arial", 16),
            bg="#F0ECE8",
            fg="#3E3A37",
            selectbackground="#CBBFB5",
            selectforeground="#3E3A37",
            relief="flat",
            highlightthickness=0
        )
        self.task_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.task_listbox.bind("<Double-Button-1>", self.edit_task)
        self.task_listbox.bind("<space>", self.toggle_complete)

        # ---------- ACTION BUTTONS ----------
        button_container = tk.Frame(master, bg="#F5F2EE")
        button_container.pack(pady=10)

        self.complete_button = self.rounded_button(
            button_container, "Complete", self.toggle_complete
        )
        self.delete_button = self.rounded_button(
            button_container, "Delete", self.delete_task
        )
        self.clear_button = self.rounded_button(
            button_container, "Clear Done", self.clear_completed, width=150
        )

        self.complete_button.pack(side="left", padx=6)
        self.delete_button.pack(side="left", padx=6)
        self.clear_button.pack(side="left", padx=6)

        tk.Label(
            master,
            text="Double-click to edit | Space to complete | Select to delete",
            font=("Arial", 8),
            bg="#F5F2EE",
            fg="#6E6761"
        ).pack(pady=(5, 10))

        self.load_tasks()

    # ---------- ROUNDED BUTTON ----------
    def rounded_button(self, parent, text, command, width=120, height=36, radius=14):
        canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg=parent["bg"],
            highlightthickness=0
        )

        fill = "#B8A89A"
        hover = "#A9998C"
        text_color = "#3E3A37"

        x0, y0, x1, y1 = 2, 2, width - 2, height - 2

        items = [
            canvas.create_arc(x0, y0, x0 + radius*2, y0 + radius*2, start=90, extent=90, fill=fill, outline=fill),
            canvas.create_arc(x1 - radius*2, y0, x1, y0 + radius*2, start=0, extent=90, fill=fill, outline=fill),
            canvas.create_arc(x0, y1 - radius*2, x0 + radius*2, y1, start=180, extent=90, fill=fill, outline=fill),
            canvas.create_arc(x1 - radius*2, y1 - radius*2, x1, y1, start=270, extent=90, fill=fill, outline=fill),
            canvas.create_rectangle(x0 + radius, y0, x1 - radius, y1, fill=fill, outline=fill),
            canvas.create_rectangle(x0, y0 + radius, x1, y1 - radius, fill=fill, outline=fill)
        ]

        text_id = canvas.create_text(
            width // 2,
            height // 2,
            text=text,
            fill=text_color,
            font=("Arial", 11, "bold")
        )

        def recolor(color):
            for item in items:
                canvas.itemconfig(item, fill=color, outline=color)

        canvas.bind("<Enter>", lambda e: recolor(hover))
        canvas.bind("<Leave>", lambda e: recolor(fill))
        canvas.bind("<Button-1>", lambda e: command())
        canvas.tag_bind(text_id, "<Button-1>", lambda e: command())

        return canvas

    # ---------- TASK LOGIC ----------
    def get_priority_symbol(self, priority):
        return {"High": "⚠", "Medium": "●", "Low": "○"}.get(priority, "●")

    def format_task_display(self, task):
        # 🔹 Bigger, cleaner checkbox symbols
        checkbox = "■" if task["completed"] else "□"
        symbol = self.get_priority_symbol(task["priority"])
        return f"{checkbox} {symbol} {task['text']}"

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter a task.")
            return

        self.tasks.append({
            "text": text,
            "completed": False,
            "priority": self.priority_var.get(),
            "created": datetime.now().isoformat()
        })

        self.task_entry.delete(0, tk.END)
        self.refresh_listbox()
        self.save_tasks()
        self.update_stats()

    def toggle_complete(self, event=None):
        try:
            i = self.task_listbox.curselection()[0]
            self.tasks[i]["completed"] = not self.tasks[i]["completed"]
            self.refresh_listbox()
            self.save_tasks()
            self.update_stats()
        except IndexError:
            pass

    def edit_task(self, event=None):
        try:
            i = self.task_listbox.curselection()[0]
            new_text = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=self.tasks[i]["text"])
            if new_text:
                self.tasks[i]["text"] = new_text.strip()
                self.refresh_listbox()
                self.save_tasks()
        except IndexError:
            pass

    def delete_task(self):
        try:
            i = self.task_listbox.curselection()[0]
            self.tasks.pop(i)
            self.refresh_listbox()
            self.save_tasks()
            self.update_stats()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def clear_completed(self):
        self.tasks = [t for t in self.tasks if not t["completed"]]
        self.refresh_listbox()
        self.save_tasks()
        self.update_stats()

    # ---------- DATA ----------
    def refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, self.format_task_display(task))

    def update_stats(self):
        total = len(self.tasks)
        completed = sum(t["completed"] for t in self.tasks)
        self.stats_label.config(
            text=f"Total: {total} | Pending: {total - completed} | Completed: {completed}"
        )

    def save_tasks(self):
        with open(self.tasks_file, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as f:
                self.tasks = json.load(f)
            self.refresh_listbox()
            self.update_stats()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
