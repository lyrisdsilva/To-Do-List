import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os
import json
from datetime import datetime

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")
        master.geometry("500x700")
        master.resizable(False, False)
        master.configure(bg="#1E1E1E")  # Background color

        self.tasks = []  # To store tasks as dictionaries: {'text': str, 'completed': bool, 'priority': str}
        self.tasks_file = os.path.join(os.path.dirname(__file__), "tasks.json")
        self.priority_var = tk.StringVar(value="Medium")

        # Load decorative images
        self.load_images()

        # --- Header ---
        header_frame = tk.Frame(master, bg="#F3CFEB", height=60)
        header_frame.pack(fill="x", padx=0, pady=(0, 0), side="top")
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="TO - DO LIST",
            font=("Arial", 20, "bold"),
            bg="#252526",
            fg="#E5E5E5"
        )
        title_label.pack(pady=12)

        # Bottom border for header
        header_border = tk.Frame(master, bg="black", height=3)
        header_border.pack(fill="x", padx=0, pady=(0, 10))

        # --- Statistics Section ---
        stats_frame = tk.Frame(master, bg="#7974DD")
        stats_frame.pack(pady=(5, 0), padx=20, fill="x")

        self.stats_label = tk.Label(
            stats_frame,
            text="Total: 0 | Pending: 0 | Completed: 0",
            font=("Arial", 10),
            bg="#2D2D30",
            fg="#A0A0A0"
        )
        self.stats_label.pack()

        # --- Input Section with tulips positioned above ---
        input_container = tk.Frame(master, bg="#2D2D30", height=55)
        input_container.pack(pady=10, padx=20, fill="x")
        input_container.pack_propagate(False)

        # #E5E5E5 input box with purple border
        input_box = tk.Frame(input_container, bg="#202124", height=80)
        input_box.place(x=0, y=0, relwidth=1.0)

        self.task_entry = tk.Entry(
            input_box,
            font=("Arial", 14),
            relief="flat",
            borderwidth=0,
            bg="#202124",
            fg="#E5E5E5",
            highlightthickness=0
        )
        self.task_entry.pack(fill="both", padx=(80, 15), pady=15, ipady=5)
        self.task_entry.bind('<Return>', lambda _: self.add_task())  # Enter key support

        # --- Priority Selection ---
        priority_frame = tk.Frame(master, bg="#1E1E1E")
        priority_frame.pack(pady=5)

        tk.Label(priority_frame, text="Priority:", bg="#1E1E1E", fg="#E5E5E5", font=("Arial", 10)).pack(side="left", padx=5)
        tk.Label()

        priorities = ["High", "Medium", "Low"]
        for priority in priorities:
            rb = tk.Radiobutton(
                priority_frame,
                text=priority,
                variable=self.priority_var,
                value=priority,
                bg="#1E1E1E",
                fg="#E5E5E5",
                selectcolor="#4743AA",
                font=("Arial", 9),
                activebackground="#1E1E1E",
                activeforeground="#E5E5E5"
            )
            rb.pack(side="left", padx=3)

        # --- Add Task Button ---
        if hasattr(self, 'button_image'):
            self.add_button = tk.Button(
                master,
                text="Add Task",
                command=self.add_task,
                font=("Arial", 13, "bold"),
                fg="#4743AA",
                image=self.button_image,
                compound="center",
                cursor="hand2",
                borderwidth=0,
                relief="flat",
                bg="#7974DD",
                activebackground="#7974DD",
                highlightthickness=0
            )
        else:
            self.add_button = tk.Button(
                master,
                text="Add Task",
                command=self.add_task,
                font=("Arial", 13, "bold"),
                bg="#F3CFEB",
                fg="#4743AA",
                relief="flat",
                cursor="hand2",
                padx=25,
                pady=10,
                borderwidth=0
            )
        self.add_button.pack(pady=5)

        # --- Tasks Section (Purple box with TASKS header and list) ---
        tasks_container = tk.Frame(master, bg="#8C88E9")
        tasks_container.pack(pady=10, padx=20, fill="both", expand=True)

        # TASKS header inside the box
        tasks_label = tk.Label(
            tasks_container,
            text="TASKS",
            font=("Arial", 14, "bold"),
            bg="#8C88E9",
            fg="#E5E5E5",
            pady=10
        )
        tasks_label.pack(fill="x")

        # Listbox with butterfly - both inside the purple box
        list_inner_frame = tk.Frame(tasks_container, bg="#8C88E9")
        list_inner_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.task_listbox = tk.Listbox(
            list_inner_frame,
            font=("Arial", 14, "normal"),
            bg="#a0caf0",
            fg="#E5E5E5",
            selectbackground="#2a6fad",
            selectforeground="#E5E5E5",
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        self.task_listbox.pack(side="left", fill="both", expand=True, padx=(20, 0), ipady=8)
        self.task_listbox.bind('<Double-Button-1>', self.edit_task)  # Double-click to edit
        self.task_listbox.bind('<space>', self.toggle_complete)  # Space to toggle

        # Butterfly image on the right inside the purple box
        if hasattr(self, 'butterfly_image'):
            butterfly_label = tk.Label(list_inner_frame, image=self.butterfly_image, bg="#8C88E9")
            butterfly_label.pack(side="right", padx=5, anchor="s")

        # --- Button Container ---
        button_container = tk.Frame(master, bg="#7974DD")
        button_container.pack(pady=5)

        # --- Complete/Uncomplete Button ---
        if hasattr(self, 'button_image'):
            self.complete_button = tk.Button(
                button_container,
                text="Complete",
                command=self.toggle_complete,
                font=("Arial", 11, "bold"),
                fg="#4743AA",
                image=self.button_image,
                compound="center",
                cursor="hand2",
                relief="flat",
                bg="#7974DD",
                activebackground="#7974DD",
                borderwidth=0,
                highlightthickness=0
            )
        else:
            self.complete_button = tk.Button(
                button_container,
                text="Complete",
                command=self.toggle_complete,
                font=("Arial", 11, "bold"),
                bg="#F3CFEB",
                fg="#4743AA",
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=8,
                borderwidth=0
            )
        self.complete_button.pack(side="left", padx=5)

        # --- Delete Button ---
        if hasattr(self, 'button_image'):
            self.delete_button = tk.Button(
                button_container,
                text="Delete",
                command=self.delete_task,
                font=("Arial", 11, "bold"),
                fg="#4743AA",
                image=self.button_image,
                compound="center",
                cursor="hand2",
                relief="flat",
                bg="#7974DD",
                activebackground="#7974DD",
                borderwidth=0,
                highlightthickness=0
            )
        else:
            self.delete_button = tk.Button(
                button_container,
                text="Delete",
                command=self.delete_task,
                font=("Arial", 11, "bold"),
                bg="#F3CFEB",
                fg="#4743AA",
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=8,
                borderwidth=0
            )
        self.delete_button.pack(side="left", padx=5)

        # --- Clear Completed Button ---
        if hasattr(self, 'button_image'):
            self.clear_button = tk.Button(
                button_container,
                text="Clear Done",
                command=self.clear_completed,
                font=("Arial", 11, "bold"),
                fg="#4743AA",
                image=self.button_image,
                compound="center",
                cursor="hand2",
                relief="flat",
                bg="#7974DD",
                activebackground="#7974DD",
                borderwidth=0,
                highlightthickness=0
            )
        else:
            self.clear_button = tk.Button(
                button_container,
                text="Clear Done",
                command=self.clear_completed,
                font=("Arial", 11, "bold"),
                bg="#F3CFEB",
                fg="#4743AA",
                relief="flat",
                cursor="hand2",
                padx=20,
                pady=8,
                borderwidth=0
            )
        self.clear_button.pack(side="left", padx=5)

        instructions = tk.Label(
            master,
            text="Double-click to edit | Space/Click Complete | Select to Delete",
            font=("Arial", 8),
            bg="#7974DD",
            fg="#E5E5E5"
        )
        instructions.pack(pady=(5, 10))

        # Load tasks from file on startup
        self.load_tasks()

    def load_images(self):
        """Load decorative images (tulips and butterfly)"""
        try:
            image_dir = os.path.join(os.path.dirname(__file__), "images")

            # Load tulips image
            tulips_path = os.path.join(image_dir, "tulips.png")
            if os.path.exists(tulips_path):
                tulips_img = Image.open(tulips_path)
                tulips_img = tulips_img.resize((60, 60), Image.Resampling.LANCZOS)
                self.tulips_image = ImageTk.PhotoImage(tulips_img)

            # Load butterfly image
            butterfly_path = os.path.join(image_dir, "butterfly.png")
            if os.path.exists(butterfly_path):
                butterfly_img = Image.open(butterfly_path)
                butterfly_img = butterfly_img.resize((100, 100), Image.Resampling.LANCZOS)
                self.butterfly_image = ImageTk.PhotoImage(butterfly_img)

            # Load button image
            button_path = os.path.join(image_dir, "buttons.png")
            if os.path.exists(button_path):
                button_img = Image.open(button_path)
                button_img = button_img.resize((150, 50), Image.Resampling.LANCZOS)
                self.button_image = ImageTk.PhotoImage(button_img)
        except Exception as e:
            print(f"Could not load images: {e}")
            # App will work without images

    def get_priority_symbol(self, priority):
        """Get symbol for priority level"""
        symbols = {"High": "⚠", "Medium": "●", "Low": "○"}
        return symbols.get(priority, "●")

    def format_task_display(self, task):
        """Format task for display in listbox"""
        checkbox = "☑" if task['completed'] else "☐"
        priority_symbol = self.get_priority_symbol(task['priority'])
        text = task['text']

        if task['completed']:
            return f"{checkbox} {priority_symbol} {text} ✓"
        else:
            return f"{checkbox} {priority_symbol} {text}"

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {
                'text': task_text,
                'completed': False,
                'priority': self.priority_var.get(),
                'created': datetime.now().isoformat()
            }
            self.tasks.append(task)
            self.refresh_listbox()
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
            self.update_stats()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def toggle_complete(self, event=None):
        """Toggle task completion status"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            # Find the actual task index (accounting for spacing)
            task_index = self.get_task_index_from_listbox(selected_index)

            if task_index is not None:
                self.tasks[task_index]['completed'] = not self.tasks[task_index]['completed']
                self.refresh_listbox()
                self.save_tasks()
                self.update_stats()
        except IndexError:
            if not event:  # Only show warning if triggered by button, not keyboard
                messagebox.showwarning("Warning", "Please select a task to mark as complete.")

    def edit_task(self, _event=None):
        """Edit selected task"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_index = self.get_task_index_from_listbox(selected_index)

            if task_index is not None:
                current_text = self.tasks[task_index]['text']
                new_text = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=current_text)

                if new_text and new_text.strip():
                    self.tasks[task_index]['text'] = new_text.strip()
                    self.refresh_listbox()
                    self.save_tasks()
        except IndexError:
            pass

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_index = self.get_task_index_from_listbox(selected_index)

            if task_index is not None:
                self.tasks.pop(task_index)
                self.refresh_listbox()
                self.save_tasks()
                self.update_stats()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def clear_completed(self):
        """Remove all completed tasks"""
        completed_count = sum(1 for task in self.tasks if task['completed'])

        if completed_count == 0:
            messagebox.showinfo("Info", "No completed tasks to clear.")
            return

        if messagebox.askyesno("Confirm", f"Delete {completed_count} completed task(s)?"):
            self.tasks = [task for task in self.tasks if not task['completed']]
            self.refresh_listbox()
            self.save_tasks()
            self.update_stats()

    def get_task_index_from_listbox(self, listbox_index):
        """Convert listbox index to actual task index (accounting for spacing lines)"""
        task_count = 0
        for i in range(listbox_index + 1):
            item = self.task_listbox.get(i)
            if item.strip():  # Not a spacing line
                if i == listbox_index:
                    return task_count
                task_count += 1
        return None

    def refresh_listbox(self):
        """Refresh the listbox display"""
        self.task_listbox.delete(0, tk.END)

        for i, task in enumerate(self.tasks):
            if i > 0:
                self.task_listbox.insert(tk.END, "")  # Spacing line

            display_text = self.format_task_display(task)
            self.task_listbox.insert(tk.END, display_text)

    def update_stats(self):
        """Update statistics display"""
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task['completed'])
        pending = total - completed

        self.stats_label.config(text=f"Total: {total} | Pending: {pending} | Completed: {completed}")

    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file, 'r') as f:
                    self.tasks = json.load(f)
                self.refresh_listbox()
                self.update_stats()
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
