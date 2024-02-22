import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, QShortcut
from PyQt5.QtGui import QIcon, QKeySequence
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
        
        self.label = QLabel("Enter text:")
        self.entry = QLineEdit()
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_chinese)
        
        self.result_label = QLabel()
        self.result_label.setWordWrap(True)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.result_label)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.entry)
        layout.addWidget(self.search_button)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)

        self.resize(600, 400)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChineseTextSearch()
    window.show()
    sys.exit(app.exec_())
