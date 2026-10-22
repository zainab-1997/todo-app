# 📝 Todo App

A clean, simple task manager web app built with **Python**, **Streamlit** and **SQLite**.

## Features

- Add tasks with a title, due date and priority (High / Medium / Low)
- Edit a task's title, due date or priority
- Mark tasks as completed (shown with strikethrough)
- Delete tasks safely using soft-delete (archiving), so data is never lost
- Input validation: empty titles and past due dates are rejected
- Tasks sorted by due date, with a color-coded priority bar
- Custom, clean UI styling

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| Language | Python |
| Database | SQLite |

## Project Structure

```
todo-app/
├── app.py           # Streamlit user interface
├── database.py      # SQLite data layer (create, read, update, archive)
└── requirements.txt # Dependencies
```

## Getting Started

```bash
git clone https://github.com/zainab-1997/todo-app.git
cd todo-app
pip install -r requirements.txt
streamlit run app.py
```

The database file (`tasks.db`) is created automatically on first run.

## What I Practiced

- Separating the UI layer from the data layer
- CRUD operations with parameterized SQL queries
- Form handling and session state in Streamlit
- Soft-delete pattern for data safety

## Author

**Zainab Al-Iqabi** · [GitHub](https://github.com/zainab-1997) · [LinkedIn](https://www.linkedin.com/in/zainab-al-iqabi-7098692a4/)
