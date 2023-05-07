from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QPoint
from recorder import record_audio, stop_recording
from totext import transcribe_audio
from response import generate_response
from PyQt5.QtCore import Qt, QModelIndex, QAbstractListModel, QSize, QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListView, QPushButton, QLabel, QLineEdit, QStyledItemDelegate
from PyQt5.QtGui import QFontMetrics, QRegion


class UserMessageItem(QWidget):
    def __init__(self, message):
        super().__init__()
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.RichText)
        self.label.setFixedWidth(190)
        self.label.setStyleSheet("""
            QLabel {
                background-color: white;
                color: black;
                padding: 8px;
                border-radius: 8px;
            }
        """)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        self.setLayout(layout)

class AssistantMessageItem(QWidget):
    def __init__(self, message):
        super().__init__()
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.RichText)
        self.label.setFixedWidth(190)
        self.label.setStyleSheet("""
            QLabel {
                background-color: #0099FF;
                color: white;
                padding: 8px;
                border-radius: 8px;
            }
        """)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addStretch()
        self.setLayout(layout)




class MessageDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        is_user = index.data(Qt.UserRole)
        message = index.data(Qt.UserRole + 1)

        painter.save()

        if is_user:
            message_widget = UserMessageItem(message)
        else:
            message_widget = AssistantMessageItem(message)

        message_widget.resize(option.rect.size())

        painter.translate(option.rect.topLeft())
        message_widget.render(painter, QPoint(), QRegion(), QWidget.DrawChildren)

        painter.restore()

    def sizeHint(self, option, index):
        message = index.data(Qt.UserRole + 1)
        font_metrics = QFontMetrics(option.font)
        return QSize(200, font_metrics.boundingRect(QRect(0, 0, 190, 2000), Qt.TextWordWrap, message).height())
class MessageItem(QWidget):
    def __init__(self, message):
        super().__init__()

        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.RichText)
        self.label.setFixedWidth(190)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)

class AudioRecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio and Text Assistant")
        self.resize(700, 500)
        self.setMinimumSize(700, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.conversation_view = QListView()
        self.conversation_view.setItemDelegate(MessageDelegate(self))
        self.conversation_model = ConversationModel()
        self.conversation_view.setModel(self.conversation_model)
        layout.addWidget(self.conversation_view)

        input_layout = QHBoxLayout()
        layout.addLayout(input_layout)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type your message here")
        self.text_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.text_input)

        self.send_button = QPushButton("Send", clicked=self.send_message)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0099FF;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #007FD0;
            }
            QPushButton:pressed {
                background-color: #0066A1;
            }
        """)
        input_layout.addWidget(self.send_button)

        self.record_button = QPushButton("Start Recording", clicked=self.toggle_recording)
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #0099FF;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #007FD0;
            }
            QPushButton:pressed {
                background-color: #0066A1;
            }
        """)
        layout.addWidget(self.record_button)

        self.recording_label = QLabel("Recording...")
        self.recording_label.setVisible(False)
        layout.addWidget(self.recording_label)

        self.is_recording = False
        self.frames = None

    def toggle_recording(self):
        if not self.is_recording:
            self.frames = record_audio()
            self.record_button.setText("Stop Recording")
            self.recording_label.setVisible(True)
        else:
            stop_recording(self.frames)
            self.record_button.setText("Start Recording")
            self.recording_label.setVisible(False)
            transcribed_text = transcribe_audio('output.wav')
            self.add_message(transcribed_text, "user")  # Add role here

            gpt_response = generate_response(transcribed_text)
            self.add_message(gpt_response, "assistant")  # Add role here

        self.is_recording = not self.is_recording


    def send_message(self):
        user_message = self.text_input.text()
        if not user_message.strip():
            return

        self.add_message(user_message, "user")
        self.text_input.clear()

        assistant_response = generate_response(user_message)
        self.add_message(assistant_response, "assistant")

    def add_message(self, message, role):
        item = {"text": message, "is_user": role == "user"}
        self.conversation_model.addData(item)
        self.conversation_view.scrollToBottom()


class ConversationModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.messages)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.messages):
            return None

        message = self.messages[index.row()]

        if role == Qt.DisplayRole:
            return message["text"]
        elif role == Qt.UserRole:
            return message["is_user"]
        elif role == Qt.UserRole + 1:
            return message["text"]

        return None

    def addData(self, value):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.messages.append(value)
        self.endInsertRows()



class MessageDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        is_user = index.data(Qt.UserRole)
        message = index.data(Qt.UserRole + 1)

        painter.save()

        if is_user:
            message_widget = UserMessageItem(message)
        else:
            message_widget = AssistantMessageItem(message)

        message_widget.resize(option.rect.size())

        painter.translate(option.rect.topLeft())
        message_widget.render(painter, QPoint(), QRegion(), QWidget.DrawChildren)

        painter.restore()

    def sizeHint(self, option, index):
        message = index.data(Qt.UserRole + 1)
        font_metrics = QFontMetrics(option.font)
        padding = 10
        return QSize(200, font_metrics.boundingRect(QRect(0, 0, 190, 2000), Qt.TextWordWrap, message).height())



if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = AudioRecorderApp()
    window.show()

    sys.exit(app.exec_())
