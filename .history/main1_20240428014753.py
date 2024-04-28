from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QTableView, QLabel
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPixmap
import sys
import pandas as pd
import asyncio
from data import process_feedback_table
from model import process_with_llm, data_new


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор файла и обработка")

        self.button = QPushButton("Выбрать файл XLSX")
        self.button.clicked.connect(self.open_dialog)

        self.tableView = QTableView(self)  # Виджет таблицы для отображения данных
        self.imageLabel = QLabel(self)  # QLabel для отображения изображения
        self.imageLabel.setScaledContents(True)  # Масштабирование изображения по размеру QLabel

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        layout.addWidget(self.imageLabel)  # Добавляем QLabel в layout

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_dialog(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Выберите файл xlsx", "", "XLSX files (*.xlsx)")
        if filepath:
            asyncio.run(self.process_file(filepath))

    async def process_file(self, filepath):
        processed = process_feedback_table(filepath)
        processed_df = data_new(processed)
        self.display_data(processed_df)  # Отображаем DataFrame в QTableView
        self.display_image('hourly_plot.png')  # Путь к вашему сохраненному файлу с графиком

    def display_data(self, df):
        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(df.columns)

        for index, row in df.iterrows():
            items = [QStandardItem(str(value)) for value in row]
            model.appendRow(items)

        self.tableView.setModel(model)

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.imageLabel.setPixmap(pixmap)  # Загрузка и отображение графика

def process_feedback_table(file_path):
    df = pd.read_excel(file_path)
    return df  # Возвращение обработанного DataFrame

def data_new(df):
    # Процессируем данные если нужно
    return df  # Возвращаем изменённый DataFrame

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())