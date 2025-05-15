# tkinter_sqlite_app

This project is a simple Tkinter application that integrates with an SQLite3 database to manage tasks. It provides a user-friendly interface for creating, updating, and viewing tasks.

## Project Structure

```
tkinter_sqlite_app
├── src
│   ├── main.py                # Entry point of the application
│   ├── controllers
│   │   └── controlador_tareas.py  # Manages application logic and interactions with the database
│   ├── models
│   │   └── database.py        # Handles SQLite3 database operations
│   └── views
│       └── tareas_view.py     # Defines the user interface for task management
├── requirements.txt           # Lists project dependencies
└── README.md                  # Documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd tkinter_sqlite_app
   ```

2. **Install dependencies**:
   It is recommended to use a virtual environment. You can create one using:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
   Then install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

This will launch the Tkinter application where you can manage your tasks.

## Features

- Create new tasks
- Update existing tasks
- View all tasks
- Simple and intuitive user interface

## License

This project is licensed under the MIT License.