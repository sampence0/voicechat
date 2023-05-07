
import openai
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication
from window import AudioRecorderApp
import sys
load_dotenv()

print(f"API Key: {openai.api_key}")


def get_stylesheet():
    return """
    QWidget {
        background-color: #292929;
        color: #ffffff;
        font: 12pt 'Arial';
    }

    QTextEdit {
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #444444;
    }

    QPushButton {
        background-color: #3a8bff;
        color: #ffffff;
        border: none;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
    }

    QPushButton:hover {
        background-color: #2e71d9;
    }

    QPushButton:pressed {
        background-color: #2977c9;
    }
    """



def main():
    app = QApplication(sys.argv)

    main_window = AudioRecorderApp()
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
