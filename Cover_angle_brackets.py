from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QTextEdit
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.lineEdit_Top = QTextEdit()
        self.lineEdit_Top.setPlaceholderText("Введите здесь текст")
        self.layout.addWidget(self.lineEdit_Top)

        self.lineEdit_Bottom = QTextEdit()
        self.lineEdit_Bottom.setPlaceholderText("А здесь не вводите")
        self.layout.addWidget(self.lineEdit_Bottom)

        self.button = QPushButton('convert')
        # Подключаем сигнал нажатия кнопки к слоту
        self.button.clicked.connect(self.copy_text)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    # Определяем слот - функцию, которая будет вызываться при нажатии кнопки
    def copy_text(self):
        text = self.lineEdit_Top.toPlainText()
        new_text = ''
        for char in text:
            print(char)
            if char == '<':
                new_text += '&lt;'
            elif char == '>':
                new_text += '&gt;'
            elif char == '{':
                new_text += '&#123;'
            elif char == '}':
                new_text += '&#125;'
            else:
                new_text += char
        self.lineEdit_Bottom.setPlainText(new_text)


# замени < на &lt;
# замени > на &gt;

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
