from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
import sqlite3
import sys

# Создание базы данных или подключение к существующей
c = sqlite3.connect('security.db')
cur = c.cursor()

# Создание таблицы для сотрудников
cur.execute("""CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_name TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    pass_number TEXT UNIQUE NOT NULL)""")

# Создание таблицы для гостей
cur.execute("""CREATE TABLE IF NOT EXISTS guests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_name TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    pass_number TEXT UNIQUE NOT NULL)""")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Перевалочный пункт')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label_employee = QLabel('Рабочий:')
        self.layout.addWidget(self.label_employee)

        self.form_employee = QFormLayout()
        self.layout.addLayout(self.form_employee)

        self.last_name_employee = QLineEdit()
        self.form_employee.addRow('Фамилия:', self.last_name_employee)

        self.first_name_employee = QLineEdit()
        self.form_employee.addRow('Имя:', self.first_name_employee)

        self.pass_number_employee = QLineEdit()
        self.form_employee.addRow('Номер пропуска:', self.pass_number_employee)

        self.button_employee = QPushButton('Добавить сотрудника')
        self.button_employee.clicked.connect(self.add_employee)
        self.layout.addWidget(self.button_employee)

        self.label_guest = QLabel('Гость:')
        self.layout.addWidget(self.label_guest)

        self.form_guest = QFormLayout()
        self.layout.addLayout(self.form_guest)

        self.last_name_guest = QLineEdit()
        self.form_guest.addRow('Фамилия:', self.last_name_guest)

        self.first_name_guest = QLineEdit()
        self.form_guest.addRow('Имя:', self.first_name_guest)

        self.pass_number_guest = QLineEdit()
        self.form_guest.addRow('Номер пропуска:', self.pass_number_guest)

        self.label_entry_time = QLineEdit()
        self.form_guest.addRow("Время входа:",self.label_entry_time)

        self.skoka_entry_time = QLineEdit()
        self.form_guest.addRow("Время выхода:", self.skoka_entry_time)

        self.button_guest = QPushButton('Добавить гостя')
        self.button_guest.clicked.connect(self.add_guest)
        self.layout.addWidget(self.button_guest)



    def add_employee(self):
        last_name = self.last_name_employee.text()
        first_name = self.first_name_employee.text()
        pass_number = self.pass_number_employee.text()

        if last_name.isdigit() or first_name.isdigit():
            QMessageBox.critical(self, 'Ошибка', 'Фамилия и имя не должны содержать цифры')
            return

        try:
            cur.execute("INSERT INTO employees (last_name, first_name, pass_number) VALUES (?, ?, ?)", (last_name, first_name, pass_number,))
            c.commit()
            QMessageBox.information(self, 'Успех', 'Рабочий успешно добавлен')
            self.last_name_employee.clear()
            self.first_name_employee.clear()
            self.pass_number_employee.clear()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, 'Ошибка', 'Такой номер пропуска уже существует')
        if not last_name or not first_name or pass_number:
            QMessageBox.critical(self, 'Ошибка', 'Все поля должны быть заполнены')

    def add_guest(self):
        last_name = self.last_name_guest.text()
        first_name = self.first_name_guest.text()
        pass_number = self.pass_number_guest.text()
        label_entry_time = self.label_entry_time.text()
        skoka_entry_time = self.skoka_entry_time.text()

        if last_name.isdigit() or first_name.isdigit():
            QMessageBox.critical(self, 'Ошибка', 'Фамилия и имя не должны содержать цифры')
            return

        try:
            cur.execute("INSERT INTO guests (last_name, first_name, pass_number) VALUES (?, ?, ?)", (last_name, first_name, pass_number))
            c.commit()
            QMessageBox.information(self, 'Успех', 'Гость успешно добавлен')
            self.last_name_employee.clear()
            self.first_name_employee.clear()
            self.pass_number_employee.clear()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, 'Ошибка', 'Такой номер пропуска уже существует')
        if not label_entry_time.isdigit() or not skoka_entry_time.isdigit():
            QMessageBox.critical(self, 'Ошибка', 'Время не может содержать буквы')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
  8====D
