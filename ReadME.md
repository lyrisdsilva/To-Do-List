# To-Do List App

A desktop to-do list application built with Python and Tkinter. This app lets you add, edit, complete, and delete tasks, with priority selection and persistent storage.

## Features

- Add, edit, and delete tasks
- Mark tasks as complete/incomplete
- Priority selection (High, Medium, Low)
- Task statistics: total, pending, completed
- Double-click to edit tasks
- Space or button to mark complete
- Delete and clear completed tasks
- Tasks saved to `tasks.json` for persistence
- Decorative images for enhanced UI (tulips, butterfly, buttons)

## Getting Started

1. Make sure Python 3 is installed.
2. Install required packages:
   ```bash
   pip install pillow
   ```
3. Place decorative images in the `images/` folder (optional).
4. Run the app:
   ```bash
   python to_do.py
   ```

## Usage

- Enter a task and click "Add Task".
- Select priority before adding.
- Double-click a task to edit.
- Select a task and click "Complete" or press Space to toggle completion.
- Select a task and click "Delete" to remove.
- Click "Clear Done" to remove all completed tasks.
- Tasks are saved automatically.