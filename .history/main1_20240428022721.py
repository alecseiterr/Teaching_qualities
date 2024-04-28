from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QTableView, QLabel
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPixmap
import sys
import asyncio
from data import process_feedback_table
from model import process_with_llm, data_new


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор файла и обработка")

        self.button = QPushButton("Выбрать файл XLSX")
        self.button.clicked.connect(self.open_dialog)

        self.hourlyButton = QPushButton("Показать график среднеи плотность сообщений по часам")
        self.hourlyButton.clicked.connect(lambda: self.display_image('hourly_plot.png'))

        self.tonButton = QPushButton("Показать график частоты эмоционального тона (1) по часам суток")
        self.tonButton.clicked.connect(lambda: self.display_image('ton_plot.png'))

        self.problemButton = QPushButton("Показать график ежедневного количества проблем и уроков.")
        self.problemButton.clicked.connect(lambda: self.display_image('problem_plot.png'))

        self.tableView = QTableView(self)
        self.imageLabel = QLabel(self)
        self.imageLabel.setScaledContents(True)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.tableView)
        layout.addWidget(self.hourlyButton)
        layout.addWidget(self.tonButton)
        layout.addWidget(self.problemButton)
        layout.addWidget(self.imageLabel)

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
        self.display_data(processed_df)

    def display_data(self, df):
        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(df.columns)

        for index, row in df.iterrows():
            items = [QStandardItem(str(value)) for value in row]
            model.appendRow(items)

        self.tableView.setModel(model)

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.imageLabel.setPixmap(pixmap)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())