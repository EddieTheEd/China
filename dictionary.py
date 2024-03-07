import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, QShortcut, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon, QKeySequence
import PyQt5.QtCore as QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from dragonmapper.transcriptions import numbered_to_accented
from dragonmapper.hanzi import to_pinyin

import subprocess


def modify(total):
    new = []
    for result in total.split("\n"):
        first_space_index = result.find(' ')
        if first_space_index != -1:
            result = result[first_space_index + 1:]        
        start_index = result.find('[')
        end_index = result.find(']')
        
        first_part = result[:start_index].strip()
        middle_part = result[start_index+1:end_index].strip()
        last_part = result[end_index+1:].strip()

        middle_part = numbered_to_accented(middle_part)

        result_list = [first_part, middle_part, last_part]
        new.append(' '.join(result_list))

    return '\n'.join(new)


class ChineseTextSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("CEDICT Search")

        font = self.font()
        font.setPointSize(20)
        self.setFont(font)

        
        
        self.label = QLabel("Enter Chinese or English text:")
        self.entry = QLineEdit()
        self.label.setFont(font)
        self.entry.setFont(font)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_chinese)
        self.search_button.setFont(font)
        
        self.copy_button = QPushButton("Copy Result")
        self.copy_button.clicked.connect(self.copy_result)
        self.copy_button.setFont(font)

        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.search_button)
        self.buttons.addWidget(self.copy_button)
        
        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.result_label.setFont(font)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.result_label)

        self.shortcuts_button = QPushButton("Shortcuts")
        self.shortcuts_button.clicked.connect(self.shortcuts)
        self.shortcuts_button.setFont(font)
        
        # Create QWebEngineView instance
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QtCore.QUrl("https://www.writeinput.com/?lang=en"))  # Example URL

        # Wrap QWebEngineView in a QWidget
        web_view_widget = QWidget()
        web_view_layout = QVBoxLayout(web_view_widget)
        web_view_layout.addWidget(self.web_view)
        
        # Adjust layout to include QWebEngineView
        main_layout = QHBoxLayout()
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.label)
        left_layout.addWidget(self.entry)
        left_layout.addLayout(self.buttons)
        left_layout.addWidget(scroll_area)
        left_layout.addWidget(self.shortcuts_button)
        
        main_layout.addLayout(left_layout)
        main_layout.addWidget(web_view_widget)  # Add the QWidget containing QWebEngineView to the right
        main_layout.setStretchFactor(left_layout,   65)
        main_layout.setStretchFactor(web_view_widget,   35)
        
        self.setLayout(main_layout)

        self.resize(1200, 500)  # Adjust window size to accommodate QWebEngineView

        self.setWindowIcon(QIcon(os.path.join(os.path.expanduser('~'), 'Documents/ghp/China/stardict.svg')))

        self.entry.returnPressed.connect(self.search_chinese)

        shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        shortcut.activated.connect(self.close)
        
    def search_chinese(self):
        chinese_text = self.entry.text()
        if not chinese_text:
            self.result_label.setText("Please enter text to search.")
            return
        
        try:
            result = subprocess.check_output(['grep', '-E', '-i', chinese_text, os.path.join(os.path.expanduser('~'), 'Documents/ghp/China/scripts/cedict_ts.u8')], universal_newlines=True)
            answer = modify(result)
            self.result_label.setText(answer)
        except subprocess.CalledProcessError as e:
            self.result_label.setText("No matching results found.")
    
    def copy_result(self):
        result_text = self.result_label.text()
        if result_text:
            QApplication.clipboard().setText(result_text)
        else:
            QMessageBox.warning(self, "Empty Result", "No result to copy.")

    def shortcuts(self):
        QMessageBox.information(self, "Shortcuts", "Ctrl-W - Close\nEnter - Search")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChineseTextSearch()
    window.show()
    sys.exit(app.exec_())
