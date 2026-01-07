HOST = "sql_host"
USER = "user"
PASSWORD = "sql_password"
HOTEL_ICON_PATH = "Icons/Hotel.svg"
SPINNER_PATH = "Icons/spinner.gif"
EYE_CLOSE_PATH = "Icons/Eye_close.svg"
EYE_OPEN_PATH = "Icons/Eye_open.svg"
MAXIMIZE_PATH = "Icons/maximize.svg"
MINIMIZE_PATH = "Icons/minimize.svg"
RESTORE_PATH = "Icons/restore.svg"
HOTEL_IMAGE_PATH = "Icons/hotel.png"
CLOSE_PATH = "Icons/close.png"

try:
    from pymysql.err import IntegrityError
    from PyQt6.QtGui import (
        QAction,
        QIcon,
        QFont,
        QPainter,
        QPainterPath,
        QColor,
        QMovie,
        QRegion,
    )
    from PyQt6.QtWidgets import (
        QApplication,
        QWidget,
        QGridLayout,
        QRadioButton,
        QButtonGroup,
        QPushButton,
        QLabel,
        QStackedLayout,
        QMainWindow,
        QTableWidget,
        QTableWidgetItem,
        QHBoxLayout,
        QDialog,
        QLineEdit,
        QDialogButtonBox,
        QMessageBox,
        QVBoxLayout,
        QSpinBox,
        QGroupBox,
        QFormLayout,
        QHeaderView,
        QSizePolicy,
        QToolButton,
        QScrollArea,
        QDateEdit,
        QAbstractItemView,
        QGraphicsDropShadowEffect,
        QProgressDialog,
        QFrame,
        QMenuBar,
        QStyle,
        QTimeEdit,
        QGraphicsOpacityEffect,
        QGraphicsBlurEffect,
        QStatusBar,
    )
    from PyQt6.QtCore import (
        QTimer,
        Qt,
        QDate,
        pyqtSignal,
        QThread,
        QRectF,
        QPropertyAnimation,
        QObject,
        QRunnable,
        QThreadPool,
        QTime,
        QEasingCurve,
        QSize,
        QPoint,
        QEvent,
    )
    import time, pymysql, sys, json, re, ast, pathlib, socket, ctypes.wintypes, threading, schedule
    from collections import defaultdict
    from datetime import datetime
    from PyQt6 import sip
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        Image,
    )
    from reportlab.lib.units import inch
except ModuleNotFoundError as e:
    print("Module not found", e.name)


def create_connection():
    co = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    with co.cursor() as cu:
        cu.execute("CREATE DATABASE IF NOT EXISTS hotel_management")
    co.commit()
    co.close()

    conn = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database="hotel_management",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    return conn


def setup_database():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
	CREATE TABLE IF NOT EXISTS hotel_details (
		hotel_id INT AUTO_INCREMENT PRIMARY KEY,
		hotel_name VARCHAR(50),
		place VARCHAR(100),
		pin_code INT,
		contact_hotel VARCHAR(50),
		username VARCHAR(50) UNIQUE,
		password VARCHAR(255),
		floor INT,
		room INT,
		room_no LONGTEXT,
		check_in TIME,
		check_out TIME
	)
	"""
    )
    cursor.execute(
        """
		CREATE TABLE IF NOT EXISTS room_types (
			id INT AUTO_INCREMENT PRIMARY KEY,
			hotel_id INT,
			room_type VARCHAR(30),
			total INT,
			room_no LONGTEXT,
			price FLOAT,
			FOREIGN KEY (hotel_id) REFERENCES hotel_details(hotel_id) ON DELETE CASCADE
		)
		"""
    )
    cursor.execute(
        """
			CREATE TABLE IF NOT EXISTS hotel_bookings (
			id INT AUTO_INCREMENT PRIMARY KEY,
			booking_id VARCHAR(15) NOT NULL UNIQUE,
			hotel_id INT NOT NULL,
			name VARCHAR(255) NOT NULL,
			room_no TEXT NOT NULL,
			room_type_id TEXT NOT NULL,
			date_from DATE NOT NULL,
			date_to DATE NOT NULL,
			phone VARCHAR(20),
			aadhar VARCHAR(20),
			age INT,
			email VARCHAR(50),
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (hotel_id) REFERENCES hotel_details(hotel_id)
		);
	"""
    )

    conn.commit()
    cursor.close()
    conn.close()


class RoundedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._mouse_pos = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()
            return
        if (
            event.modifiers() & Qt.KeyboardModifier.ControlModifier
            and event.key() == Qt.Key.Key_W
        ):
            event.ignore()
            return
        if (
            event.modifiers() & Qt.KeyboardModifier.MetaModifier
            and event.key() == Qt.Key.Key_W
        ):
            event.ignore()
            return
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._mouse_pos = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._mouse_pos:
            self.move(event.globalPosition().toPoint() - self._mouse_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._mouse_pos = None

    @staticmethod
    def show_about(parent=None):
        dialog = RoundedDialog(parent)
        dialog.setWindowTitle("About")
        dialog.resize(500, 300)

        dialog.setStyleSheet(
            """
			RoundedDialog {
				border: 2px solid #2E86C1;
				border-radius: 20px;
				background-color: #b3cde0; 
			}
		"""
        )

        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet(
            """
			background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
										stop:0 #357ABD, stop:1 #2E86C1);
			border-top-left-radius: 20px;
			border-top-right-radius: 20px;
		"""
        )
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        header_layout.setSpacing(10)

        icon_label = QLabel()
        icon_label.setPixmap(QIcon(HOTEL_ICON_PATH).pixmap(32, 32))
        header_layout.addWidget(icon_label)

        title_label = QLabel("About Hotel Management System")
        title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addWidget(header)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        content.setStyleSheet(
            """
			background-color: #e6f0fa;
			border-bottom-left-radius: 20px;
			border-bottom-right-radius: 20px;
		"""
        )

        label = QLabel(
            "<b>Hotel Management System</b><br><br>"
            "A sophisticated software solution designed to "
            "<b>streamline hotel operations</b>, optimize room reservations, "
            "automate billing, and enhance guest experience."
        )
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setStyleSheet("font-size: 14px; color: #2E86C1;")
        content_layout.addWidget(label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #ccc;")
        content_layout.addWidget(separator)

        close_btn = QPushButton("Close")
        close_btn.setFixedSize(100, 36)
        close_btn.setStyleSheet(
            """
			QPushButton {
				background-color: #2E86C1;
				color: white;
				font-size: 14px;
				border-radius: 12px;
				padding: 6px;
			}
			QPushButton:hover {
				background-color: #21618C;
			}
		"""
        )
        close_btn.setGraphicsEffect(
            QGraphicsDropShadowEffect(
                blurRadius=10, xOffset=0, yOffset=2, color=QColor(0, 0, 0, 60)
            )
        )
        close_btn.clicked.connect(dialog.accept)
        content_layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(content)
        dialog.exec()


class HotelIDialog(RoundedDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Hotel ID")
        self.setFixedSize(400, 250)

        self.bg_frame = QFrame()
        self.bg_frame.setStyleSheet(
            """
			QFrame {
				background-color: #ffffff;
				border-radius: 16px;
			}
		"""
        )

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.bg_frame.setGraphicsEffect(shadow)

        self.title = QLabel("Enter Hotel ID")
        self.title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("color: #2E86C1; margin-bottom: 15px;")

        self.close_btn = QPushButton("\u00d7")
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.setStyleSheet(
            """
			QPushButton {
				border: none;
				color: #666;
				font-size: 20px;
				font-weight: bold;
				border-radius: 14px;
				background-color: transparent;
			}
			QPushButton:hover { background-color: #EAECEE; }
		"""
        )
        self.close_btn.clicked.connect(self.reject)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        top_layout.addWidget(self.title)
        top_layout.addWidget(self.close_btn, alignment=Qt.AlignmentFlag.AlignTop)

        self.hotel_id_input = QLineEdit()
        self.hotel_id_input.setPlaceholderText("Hotel ID")
        self.hotel_id_input.setFont(QFont("Segoe UI", 12))
        self.hotel_id_input.setStyleSheet(
            """
			QLineEdit {
				border: 1px solid #c0c0c0;
				border-radius: 10px;
				padding: 6px 10px;
				height: 36px;
				background-color: #fdfdfd;
			}
			QLineEdit:focus {
				border: 1px solid #2E86C1;
				background-color: #ffffff;
			}
		"""
        )

        self.next_btn = QPushButton("Next")
        self.next_btn.setStyleSheet(
            """
			QPushButton {
				background-color: #2E86C1;
				color: white;
				border-radius: 8px;
				padding: 8px 20px;
				font-weight: bold;
			}
			QPushButton:hover {
				background-color: #21618C;
			}
		"""
        )
        self.next_btn.clicked.connect(self.verify_and_accept)
        self.hotel_id_input.returnPressed.connect(self.next_btn.click)

        inner_layout = QVBoxLayout(self.bg_frame)
        inner_layout.setContentsMargins(25, 25, 25, 25)
        inner_layout.setSpacing(15)
        inner_layout.addLayout(top_layout)
        inner_layout.addWidget(self.hotel_id_input)
        inner_layout.addWidget(self.next_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.addWidget(self.bg_frame)

    def get_hotel_id(self):
        return self.hotel_id_input.text().strip()

    def verify_and_accept(self):
        hotel_ID = self.get_hotel_id()

        if not hotel_ID:
            MessageBoxManager.warning(
                self, "Missing Hotel ID", "Please enter a valid Hotel ID."
            )
            return

        if not verify_hotel_id(hotel_ID):
            MessageBoxManager.warning(
                self, "Invalid Hotel ID", "Hotel ID not found in the system."
            )
            return

        self.accept()


def verify_hotel_id(hotel_ID: str) -> bool:
    conn = create_connection()
    if not conn:
        QMessageBox.critical(
            None, "Database Error", "Failed to connect to the database."
        )
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM hotel_details WHERE hotel_id = %s", (hotel_ID,))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        MessageBoxManager.warning(None, "DB ERROR", f"Failed to verify hotel ID: {e}")
        return False
    finally:
        conn.close()


def display_table_data(
    table: QTableWidget, data: list, columns: list, no_data_message="No data available"
):
    table.clearContents()
    table.setRowCount(0)
    table.setColumnCount(len(columns))
    table.setHorizontalHeaderLabels([col.replace("_", " ").title() for col in columns])

    if not data:
        table.setRowCount(1)
        table.setSpan(0, 0, 1, len(columns))
        item = QTableWidgetItem(no_data_message)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        table.setItem(0, 0, item)
        return

    table.setRowCount(len(data))
    for row_idx, row in enumerate(data):
        for col_idx, col_name in enumerate(columns):
            item = QTableWidgetItem(str(row.get(col_name, "")))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(row_idx, col_idx, item)


def scroll_bar():
    return """
		QScrollArea {
			border: none;
			background-color: #f9f9f9;
		}

		QScrollBar:vertical {
			width: 6px;
			background: #e0e0e0;
			border-radius: 3px;
		}
		QScrollBar::handle:vertical {
			background: #4A90E2;
			min-height: 20px;
			border-radius: 3px;
		}
		QScrollBar::handle:vertical:hover {
			width: 10px;
			background: #2C3E50;
			border-radius: 5px;
		}
		QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
			height: 0;
		}

		QScrollBar:horizontal {
			height: 6px;
			background: #e0e0e0;
			border-radius: 3px;
		}
		QScrollBar::handle:horizontal {
			background: #4A90E2;
			min-width: 20px;
			border-radius: 3px;
		}
		QScrollBar::handle:horizontal:hover {
			height: 10px;
			background: #2C3E50;
			border-radius: 5px;
		}
		QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
			width: 0;
		}
	"""


class BookingViewer(RoundedDialog):
    def __init__(self, hotel_id):
        super().__init__()
        self.setWindowTitle(f"Bookings for Hotel ID: {hotel_id}")
        self.resize(980, 550)
        self.hotel_id = hotel_id
        self.bookings = []
        self.bg_frame = QFrame()
        self.bg_frame.setStyleSheet(
            """
			QFrame {
				background-color: #ffffff;
				border-radius: 16px;
			}
		"""
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 70))
        self.bg_frame.setGraphicsEffect(shadow)
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Type here to filter...")
        self.filter_input.setFont(QFont("Segoe UI", 11))
        self.filter_input.setStyleSheet(
            """
			QLineEdit {
				border: 1px solid #c0c0c0;
				border-radius: 10px;
				padding: 6px 10px;
				height: 36px;
				background-color: #fdfdfd;
			}
			QLineEdit:focus {
				border: 1px solid #2E86C1;
				background-color: #ffffff;
			}
		"""
        )
        self.filter_input.textChanged.connect(self.filter_bookings)

        filter_label = QLabel("Search by Customer Name or Booking ID:")
        filter_label.setFont(QFont("Segoe UI", 11))

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_input)
        close_x = QPushButton("\u00d7")
        close_x.setFixedSize(28, 28)
        close_x.setStyleSheet(
            """
			QPushButton {
				border: none;
				color: #666;
				font-size: 20px;
				font-weight: bold;
				border-radius: 14px;
				background-color: transparent;
			}
			QPushButton:hover { background-color: #EAECEE; }
		"""
        )
        close_x.clicked.connect(self.reject)
        top_layout = QHBoxLayout()
        top_layout.addLayout(filter_layout)
        top_layout.addWidget(close_x, alignment=Qt.AlignmentFlag.AlignTop)
        self.table = QTableWidget()
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(
            """
			QScrollArea {
				border: none;
				background-color: #f9f9f9;
			}

			QScrollBar:vertical {
				width: 6px;
				background: #e0e0e0;
				border-radius: 3px;
			}
			QScrollBar::handle:vertical {
				background: #4A90E2;
				min-height: 20px;
				border-radius: 3px;
			}
			QScrollBar::handle:vertical:hover {
				width: 10px;
				background: #2C3E50;
				border-radius: 5px;
			}
			QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
				height: 0;
			}

			QScrollBar:horizontal {
				height: 6px;
				background: #e0e0e0;
				border-radius: 3px;
			}
			QScrollBar::handle:horizontal {
				background: #4A90E2;
				min-width: 20px;
				border-radius: 3px;
			}
			QScrollBar::handle:horizontal:hover {
				height: 10px;
				background: #2C3E50;
				border-radius: 5px;
			}
			QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
				width: 0;
			}

			QHeaderView::section {
				background-color: #B5E0EA;
				color: black;
				font-weight: bold;
				font-size: 14px;
				padding: 6px;
				border: none;
			}
		"""
        )
        inner_layout = QVBoxLayout(self.bg_frame)
        inner_layout.setContentsMargins(25, 25, 25, 25)
        inner_layout.setSpacing(15)
        inner_layout.addLayout(top_layout)
        inner_layout.addWidget(self.table)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.addWidget(self.bg_frame)
        self.load_bookings(hotel_id)

    def load_bookings(self, hotel_id):
        conn = create_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        cursor.execute(
            """
			SELECT booking_id, name, room_no, room_type_id, date_from, date_to, phone, aadhar, age
			FROM hotel_bookings
			WHERE hotel_id = %s 
			  AND date_to >= (CURDATE() - INTERVAL 1 DAY)
		""",
            (hotel_id,),
        )

        bookings = cursor.fetchall()

        cursor.execute(
            """
			SELECT id, room_type
			FROM room_types
			WHERE hotel_id = %s
		""",
            (hotel_id,),
        )
        room_types = cursor.fetchall()

        room_type_map = {str(r["id"]): r["room_type"] for r in room_types}

        for b in bookings:
            ids = b["room_type_id"].split(",")
            names = [room_type_map.get(i.strip(), f"Unknown({i})") for i in ids]
            b["room_type"] = ", ".join(names)

        self.bookings = bookings
        cursor.close()
        conn.close()
        self.display_bookings(self.bookings)

    def display_bookings(self, bookings):
        columns = [
            "booking_id",
            "name",
            "room_no",
            "room_type",
            "date_from",
            "date_to",
            "phone",
            "aadhar",
            "age",
        ]
        display_table_data(
            self.table, bookings, columns, no_data_message="No bookings available"
        )

    def filter_bookings(self, text):
        text = text.lower()
        filtered = [
            row
            for row in self.bookings
            if text in str(row["booking_id"]).lower()
            or text in str(row["name"]).lower()
        ]
        self.display_bookings(filtered)


class TableLoaderSignals(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)


class TableLoader(QRunnable):
    def __init__(self, fetch_fn):
        super().__init__()
        self.fetch_fn = fetch_fn
        self.signals = TableLoaderSignals()

    def run(self):
        try:
            data = self.fetch_fn()
            self.signals.finished.emit(data)
        except Exception as e:
            self.signals.error.emit(str(e))


class RoomLogWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, booking_manager, hotel_id):
        super().__init__()
        self.booking_manager = booking_manager
        self.hotel_id = hotel_id

    def run(self):
        try:
            self.booking_manager._setup_logging_table_for_hotel(self.hotel_id)

            self.finished.emit()
        except Exception as e:
            self.error.emit(f"{str(e)}")


class TimeWorker(QObject):
    time_signal = pyqtSignal(str)

    def __init__(self, interval_seconds=60):
        super().__init__()
        self.interval = interval_seconds
        self.running = True

    def run(self):
        while self.running:
            now = datetime.now().strftime("%A, %d %b %Y  %I:%M %p")
            self.time_signal.emit(now)
            for _ in range(self.interval * 2):
                if not self.running:
                    return
                time.sleep(0.5)

    def stop(self):
        self.running = False


class ConnectionMonitor(QObject):
    status_changed = pyqtSignal(bool)

    def __init__(self, interval=5):
        super().__init__()
        self.interval = interval
        self.running = True
        self.last_status = None

    def run(self):
        while self.running:
            connected = self.check_connection()
            if connected != self.last_status:
                self.last_status = connected
                self.status_changed.emit(connected)
            for _ in range(int(self.interval * 2)):
                if not self.running:
                    return
                time.sleep(0.5)

    def check_connection(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def stop(self):
        self.running = False


class DatabaseMonitor(QObject):
    status_changed = pyqtSignal(bool)

    def __init__(self, host, user, password, database, interval=10):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.interval = interval * 1000
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_connection)
        self._last_status = None
        self._running = True

    def run(self):
        self.check_connection()
        self.timer.start(self.interval)

    def stop(self):
        self._running = False
        self.timer.stop()

    def check_connection(self):
        if not self._running:
            return

        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                connect_timeout=2,
            )
            conn.close()
            status = True
        except Exception:
            status = False

        if status != self._last_status:
            self.status_changed.emit(status)
            self._last_status = status


user32 = ctypes.windll.user32

SW_MINIMIZE = 6
SW_RESTORE = 9
GWL_STYLE = -16
WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_VISIBLE = 0x10000000
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOZORDER = 0x0004
SWP_FRAMECHANGED = 0x0020
SW_MAXIMIZE = 3


class HomePage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)

        self.setStyleSheet(
            "background: transparent; margin: 0; padding: 0; border: none;"
        )

        self._is_maximized = False
        self._normal_geometry = self.geometry()
        self.loader = LoadingOverlay(self, gif_path=SPINNER_PATH)
        self._table_cache = {"management": None, "booking": None}
        self._last_update_time = None
        self.booking_manager = BookingDataManagement()
        self._drag_pos = QPoint()

        self.threadpool = QThreadPool()
        self.setWindowIcon(QIcon(HOTEL_ICON_PATH))

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(800, 600)
        self.setMinimumSize(self.sizeHint())
        self._mouse_pos = None
        self.selected_option = None
        self.next_page = None

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet(
            """
			background-color: #2E86C1;
			color: white;
			border-top-left-radius: 12px;
			border-top-right-radius: 12px;
		"""
        )

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        self.icon_label = QLabel()
        self.icon_label.setPixmap(QIcon(HOTEL_ICON_PATH).pixmap(28, 28))
        self.icon_label.setFixedSize(28, 28)
        title_layout.insertWidget(0, self.icon_label)
        if self.next_page:
            self.title_label = QLabel({self.next_page})
        else:
            self.title_label = QLabel("EasyStay")

        self.title_label.setStyleSheet(
            "font-weight: bold; font-size: 16px; color: white;"
        )
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        self.btn_min = QPushButton()
        self.btn_max = QPushButton()
        self.btn_close = QPushButton()
        for btn, icon in zip(
            (self.btn_min, self.btn_max, self.btn_close),
            (MINIMIZE_PATH, MAXIMIZE_PATH, "Icons/close.svg"),
        ):
            btn.setFixedSize(36, 36)
            btn.setIcon(QIcon(icon))
            btn.setStyleSheet(
                """
				QPushButton { background: transparent; border: none; }
				QPushButton:hover { background-color: rgba(255,255,255,0.2); border-radius: 6px; }
				QPushButton:pressed { background-color: rgba(255,255,255,0.1); border: none; }
			"""
            )
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
            title_layout.addWidget(btn)
        for btn in (self.btn_min, self.btn_max, self.btn_close):
            btn.setFixedSize(36, 36)
            btn.setStyleSheet(
                """
				QPushButton {
					background: transparent;
					border: none;
				}
				QPushButton:hover {
					background-color: rgba(255, 255, 255, 0.2);
					border-radius: 6px;
				}
				QPushButton:pressed {
					background-color: rgba(255, 255, 255, 0.1);
					border: none;
				}
				QPushButton:focus {
					outline: none;
					border: none;
				}
			"""
            )
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        title_layout.addWidget(self.btn_min)
        title_layout.addWidget(self.btn_max)
        title_layout.addWidget(self.btn_close)
        self.main_layout.addWidget(self.title_bar)

        self.menu_bar = QMenuBar()
        self.menu_bar.setStyleSheet(
            """
			QMenuBar {
				background-color: #dfe7ff;
				border-bottom: 2px solid #2E86C1;
				font-family: 'Segoe UI', 'Arial';
				font-size: 14px;
			}
			QMenuBar::item {
				spacing: 5px;
				padding: 6px 14px;
				color: #2E86C1;
				background: transparent;
				border-radius: 6px;
				font-weight: bold;
				transition: all 0.2s ease;
			}
			QMenuBar::item:selected {
				background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
												  stop:0 #4da6ff, stop:1 #2E86C1);
				color: white;
			}
			QMenu {
				background-color: #ffffff;
				border: 1px solid #ccc;

				border-top-left-radius: 0px;
				border-top-right-radius: 0px;
				border-bottom-left-radius: 15px;
				border-bottom-right-radius: 15px;

				padding: 10px;
				min-width: 200px;

				border-bottom: 1px solid #ccc;
				margin: 0px;
			}


			QMenu::item {
				padding: 8px 16px;
				border-radius: 12px;
				margin: 3px 3px;
				color: #2E86C1;
			}
			QMenu::item:selected {
				background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
												  stop:0 #4da6ff, stop:1 #2E86C1);
				color: white;
			}
		"""
        )
        self.main_layout.addWidget(self.menu_bar)

        self.pages_widget = QWidget()
        self.pages_layout = QStackedLayout()
        self.pages_widget.setLayout(self.pages_layout)
        self.main_layout.addWidget(self.pages_widget)

        self.page1 = QWidget()
        layout1 = QVBoxLayout(self.page1)
        layout1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout1.setSpacing(30)

        title_label = QLabel("Welcome to EasyStay")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2E86C1;")
        layout1.addWidget(title_label)

        card_widget = QWidget()
        card_layout = QVBoxLayout(card_widget)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)
        card_widget.setStyleSheet(
            """
			QWidget { background-color: #ffffff; border-radius: 15px; border: 1px solid #ccc; }
		"""
        )
        self.radio1 = QRadioButton("Management Portal")
        self.radio2 = QRadioButton("Booking Portal")
        for rb in (self.radio1, self.radio2):
            rb.setStyleSheet(
                """
				QRadioButton { font-size: 18px; padding: 12px; border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9; }
				QRadioButton::hover { background-color: #e8f0fe; border: 1px solid #2E86C1; }
				QRadioButton::indicator { width: 20px; height: 20px; }
			"""
            )
            card_layout.addWidget(rb)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setEnabled(False)
        self.submit_button.setFixedWidth(180)
        self.submit_button.setStyleSheet(
            """
			QPushButton { background-color: #2E86C1; color: white; font-size: 16px; border-radius: 10px; padding: 10px; }
			QPushButton:hover { background-color: #21618C; }
			QPushButton:disabled { background-color: #aaa; color: #eee; }
		"""
        )
        card_layout.addWidget(
            self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout1.addWidget(card_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.pages_layout.addWidget(self.page1)

        self.page2 = QWidget()
        layout2 = QVBoxLayout(self.page2)
        layout2.setContentsMargins(10, 10, 10, 10)
        layout2.setSpacing(10)
        self.filter_input_page2 = QLineEdit()
        self.filter_input_page2.setPlaceholderText("Filter by Hotel Name or Place")
        self.filter_input_page2.setStyleSheet(self._line_edit_style())
        self.filter_input_page2.textChanged.connect(self.refresh_hotel_list_page2)
        self.page2.layout().insertWidget(0, self.filter_input_page2)

        self.table = QTableWidget()
        self.table.setColumnCount(3)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(
            """
			QTableWidget {
				background-color: #f9f9f9;
				alternate-background-color: #e8f0fe;
				gridline-color: #ccc;
				font-size: 14px;
				border: 1px solid #ccc;
				border-top-left-radius: 0px;
				border-top-right-radius: 0px;
				border-bottom-left-radius: 15px;
				border-bottom-right-radius: 15px;
			}
			QHeaderView::section {
				background-color: #2E86C1;
				color: white;
				font-weight: bold;
				padding: 4px;
				border: none;
			}
			QTableWidget::item:selected {
				background-color: #21618C;
				color: white;
			}
		"""
        )
        self.table.cellClicked.connect(self.cell_clicked)
        layout2.addWidget(self.table)

        self.page2.setUpdatesEnabled(True)
        QApplication.processEvents()
        self.pages_layout.addWidget(self.page2)

        self.page3 = QWidget()
        layout3 = QVBoxLayout(self.page3)
        layout3.setContentsMargins(10, 10, 10, 10)
        layout3.setSpacing(10)
        self.filter_input_page3 = QLineEdit()
        self.filter_input_page3.setPlaceholderText("Filter by Hotel Name or Place")
        self.filter_input_page3.setStyleSheet(self._line_edit_style())
        self.filter_input_page3.textChanged.connect(self.refresh_hotel_list_page3)
        self.page3.layout().insertWidget(0, self.filter_input_page3)

        self.table1 = QTableWidget()
        self.table1.setColumnCount(4)

        self.table1.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table1.verticalHeader().setVisible(False)
        self.table1.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table1.setAlternatingRowColors(True)
        self.table1.setStyleSheet(self.table.styleSheet())
        self.table1.cellClicked.connect(self.cell_clicked_book)
        layout3.addWidget(self.table1)

        status_bar = QStatusBar()
        status_bar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        status_bar.setStyleSheet(
            """
					QStatusBar {
						background-color: #ffffff;
						color: #2b2b2b;
						border-top: 1px solid #dcdcdc;
						border-bottom-left-radius: 14px;
						border-bottom-right-radius: 14px;
						padding: 5px 10px;
					}
					QStatusBar::item {
						border: none;
					}
				"""
        )
        self.setStatusBar(status_bar)

        self.network_label = QLabel("Internet: Connected")
        self.network_label.setStyleSheet(
            """
					QLabel {
						color: #007acc; 
						font-weight: 500;
						font-size: 12px;
						padding: 0 6px;
					}
				"""
        )
        self.statusBar().addPermanentWidget(self.network_label)

        self.db_label = QLabel("\U0001f5c4\ufe0f Database: Connected")
        self.db_label.setStyleSheet(
            """
					QLabel {
						color: #007acc; 
						font-size: 12px;
						padding: 0 6px;
					}
				"""
        )
        self.statusBar().addPermanentWidget(self.db_label)
        self.time_label = QLabel("Wednesday, 29 Oct 2025 | 08:30 PM")
        self.time_label.setStyleSheet(
            """
									QLabel {
										color: #555555; 
										font-size: 12px;
										padding: 0 6px;
									}
								"""
        )
        self.statusBar().addPermanentWidget(self.time_label)

        self.start_time_thread()
        self.start_network_thread()
        self.start_db_thread()

        self.page3.setUpdatesEnabled(True)
        QApplication.processEvents()
        self.pages_layout.addWidget(self.page3)

        self.btn_close.clicked.connect(self.close)
        self.btn_min.clicked.connect(self.show_native_minimized)
        self.btn_max.clicked.connect(self.toggle_max_restore)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio1, 1)
        self.button_group.addButton(self.radio2, 2)
        self.button_group.buttonClicked.connect(self.on_radio_selected)

        self.submit_button.clicked.connect(self.start_page_change)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.pages_widget.setGraphicsEffect(shadow)

        self.toggle_menu_item = self.menu_bar.addMenu("&Toggle")
        self.action_menu_item = self.menu_bar.addMenu("&Actions")
        self.action2_menu_item = self.menu_bar.addMenu("&Actions")
        self.about_menu_item = self.menu_bar.addMenu("&Help")
        for menu in (
            self.toggle_menu_item,
            self.action_menu_item,
            self.action2_menu_item,
            self.about_menu_item,
        ):
            menu.setWindowFlags(
                Qt.WindowType.Popup
                | Qt.WindowType.FramelessWindowHint
                | Qt.WindowType.NoDropShadowWindowHint
            )
            menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            menu.setStyleSheet(
                """
				QMenu {
					background-color: #ffffff;
					border: 1px solid #ccc;
					border-top-left-radius: 0px;
					border-top-right-radius: 0px;
					border-bottom-left-radius: 15px;
					border-bottom-right-radius: 15px;
					padding: 10px;
					min-width: 200px;
					margin: 0px;
				}
				QMenu::item {
					padding: 8px 16px;
					border-radius: 10px;
					color: #2E86C1;
				}
				QMenu::item:selected {
					background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
													  stop:0 #4da6ff, stop:1 #2E86C1);
					color: white;
				}
			"""
            )
            menu.menuAction().setVisible(False)

        self.toggle_action = QAction(f"Go to {self.next_page}", self)
        self.home = QAction(f"Home Page", self)
        self.home.setShortcut("Alt+Home")
        self.toggle_menu_item.addActions((self.toggle_action, self.home))
        self.toggle_action.triggered.connect(self.start_page_change)
        self.home.triggered.connect(self.home_action)

        action_add = QAction("Add Hotel", self)
        search_add = QAction("Search Booking", self)
        search_add.triggered.connect(self.open_hotel1_dialog)
        search_add.setShortcut("Ctrl+F")
        action_add.setShortcut("Ctrl+N")
        self.action_menu_item.addAction(action_add)
        self.action_menu_item.addAction(search_add)
        action_add.triggered.connect(self.open_hotel_form_dialog)

        action_check_booking = QAction("Check Booking", self)
        action_check_booking.setShortcut("Ctrl+Shift+C")
        delete_booking = QAction("Cancel Booking", self)
        delete_booking.setShortcut("Ctrl+Delete")
        book_hotel = QAction("Book Hotel", self)
        book_hotel.setShortcut("Alt+H")
        self.action2_menu_item.addActions(
            (action_check_booking, delete_booking, book_hotel)
        )
        action_check_booking.triggered.connect(self.check_booking)
        delete_booking.triggered.connect(self.delete_booking)

        about_action = QAction("About", self)
        about_action.setShortcut("F1")
        self.about_menu_item.addAction(about_action)
        about_action.triggered.connect(self.show_about)
        book_hotel.triggered.connect(self.book_hotel_dialog)

        self.update_menu_label()
        self.refresh_hotel_table(table=0)
        self.refresh_hotel_table(table=1)
        self.setUpdatesEnabled(True)
        QApplication.processEvents()
        self.pages_layout.setCurrentWidget(self.page1)
        self.winId()
        QTimer.singleShot(100, lambda: self.enable_os_shortcuts())

        self.installEventFilter(self)

    def apply_rounded_corners(self):
        radius = 20
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, self.width(), self.height()), radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        radius = 20 if not self._is_maximized else 0
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        painter.fillPath(path, QColor("#f0f4ff"))

    def enable_os_shortcuts(self):
        try:
            hwnd = int(self.windowHandle().winId())
            style = user32.GetWindowLongW(hwnd, GWL_STYLE)
            WS_OVERLAPPEDWINDOW = 0x00CF0000
            WS_VISIBLE = 0x10000000
            style |= WS_OVERLAPPEDWINDOW | WS_VISIBLE
            user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            user32.SetWindowPos(
                hwnd,
                0,
                0,
                0,
                0,
                0,
                SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
            )
        except Exception as e:
            MessageBoxManager.info(None, "OS shortcut enable failed:", e)

    def _apply_native_style(self):
        win = self.windowHandle()
        if not win:
            raise RuntimeError("Window handle not created yet")

        hwnd = int(win.winId())
        style = user32.GetWindowLongW(hwnd, GWL_STYLE)
        style |= WS_OVERLAPPEDWINDOW | WS_VISIBLE
        user32.SetWindowLongW(hwnd, GWL_STYLE, style)

        user32.SetWindowPos(
            hwnd,
            0,
            0,
            0,
            0,
            0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED,
        )
        return hwnd

    def show_native_minimized(self):
        try:
            hwnd = self._apply_native_style()
            user32.ShowWindow(hwnd, SW_MINIMIZE)
        except Exception as e:
            MessageBoxManager.info(None, "Native minimize failed:", e)
            self.showMinimized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and not self._is_maximized:
            if self._drag_pos is not None:
                self.move(
                    self.pos() + (event.globalPosition().toPoint() - self._drag_pos)
                )
                self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F4 and (
            event.modifiers() & Qt.KeyboardModifier.AltModifier
        ):
            self.close()
        elif event.key() == Qt.Key.Key_M and (
            event.modifiers() & Qt.KeyboardModifier.AltModifier
        ):
            self.show_native_minimized()
        elif event.key() == Qt.Key.Key_F11:
            self.toggle_max_restore()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.WindowStateChange:
            QTimer.singleShot(50, self._on_window_state_changed)
        return super().eventFilter(obj, event)

    def _on_window_state_changed(self):
        if self._is_maximized:
            self.btn_max.setIcon(QIcon(RESTORE_PATH))
            self.title_bar.setStyleSheet(
                """
				background-color: #2E86C1;
				border-top-left-radius: 0px;
				border-top-right-radius: 0px;
			"""
            )
        else:
            self.btn_max.setIcon(QIcon(MAXIMIZE_PATH))
            self.title_bar.setStyleSheet(
                """
				background-color: #2E86C1;
				border-top-left-radius: 12px;
				border-top-right-radius: 12px;
			"""
            )
        self.title_bar.update()
        self.update()

    def home_action(self):
        loader = LoadingOverlay(self, gif_path=SPINNER_PATH, text="Loading...")
        loader.show_overlay()
        if hasattr(self, "button_group"):
            self.button_group.setExclusive(False)
        self.radio1.setAutoExclusive(False)
        self.radio2.setAutoExclusive(False)
        self.radio1.setChecked(False)
        self.radio2.setChecked(False)
        self.radio1.setAutoExclusive(True)
        self.radio2.setAutoExclusive(True)
        if hasattr(self, "button_group"):
            self.button_group.setExclusive(True)

        QApplication.processEvents()
        for menu in (
            self.toggle_menu_item,
            self.action_menu_item,
            self.action2_menu_item,
            self.about_menu_item,
        ):
            menu.menuAction().setVisible(False)
        self.pages_layout.setCurrentWidget(self.page1)
        loader.hide_overlay()

    def start_time_thread(self):
        self._time_thread = QThread()
        self._time_worker = TimeWorker(interval_seconds=30)
        self._time_worker.moveToThread(self._time_thread)
        self._time_thread.started.connect(self._time_worker.run)
        self._time_worker.time_signal.connect(self._update_time)
        self._time_thread.start()

    def _update_time(self, text):
        self.time_label.setText(text)

    def start_db_thread(self):
        self._db_thread = QThread()
        self._db_worker = DatabaseMonitor(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database="hotel_management",
            interval=10,
        )
        self._db_worker.moveToThread(self._db_thread)
        self._db_thread.started.connect(self._db_worker.run)
        self._db_worker.status_changed.connect(self._update_db_status)
        self._db_thread.start()

    def _update_db_status(self, connected: bool):
        if connected:
            self.db_label.setText("\U0001f5c4\ufe0f Database: Connected")
            self.db_label.setStyleSheet(
                "color: #007acc; font-weight: 500; font-size: 12px; padding: 0 6px;"
            )
        else:
            self.db_label.setText("\U0001f5c4\ufe0f Database: Disconnected")
            self.db_label.setStyleSheet(
                "color: #d32f2f; font-weight: 500; font-size: 12px; padding: 0 6px;"
            )

    @staticmethod
    def _line_edit_style():
        return """
				QLineEdit, QDateEdit {
					border: 1px solid #ccc;
					border-radius: 6px;
					padding: 6px 8px;
					height:28px;
					font-size: 14px;
				}
				QLineEdit:focus, QDateEdit:focus {
					border: 1px solid #2E86C1;
					background: #FDFEFE;
				}
			"""

    def start_network_thread(self):
        self._net_thread = QThread()
        self._net_worker = ConnectionMonitor(interval=5)
        self._net_worker.moveToThread(self._net_thread)
        self._net_thread.started.connect(self._net_worker.run)
        self._net_worker.status_changed.connect(self._update_network_status)
        self._net_thread.start()

    def _update_network_status(self, connected: bool):
        if connected:
            self.network_status = "Connected"
            self.network_label.setStyleSheet(
                "color: #007acc; font-size: 12px; padding: 0 6px;"
            )
        else:
            self.network_status = "Disconnected"
            self.network_label.setStyleSheet(
                "color: #ff6b6b; font-size: 12px; padding: 0 6px;"
            )

        self.network_label.setText(f"\U0001f310 Internet: {self.network_status}")

    def closeEvent(self, event):
        for attr in ["_time_worker", "_net_worker"]:
            if hasattr(self, attr):
                getattr(self, attr).stop()
        for attr in ["_time_thread", "_net_thread"]:
            if hasattr(self, attr):
                thread = getattr(self, attr)
                thread.quit()
                thread.wait(1500)
        if hasattr(self, "_db_worker"):
            self._db_worker.stop()
        if hasattr(self, "_db_thread"):
            self._db_thread.quit()
            self._db_thread.wait(1500)
        super().closeEvent(event)

    def populate_table(
        self,
        table: QTableWidget,
        data: list,
        columns: list,
        action_name: str = None,
        log_msg: str = None,
        no_data_message="No data available",
    ):
        table.setUpdatesEnabled(False)
        table.clearContents()
        table.setRowCount(0)
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(
            [col.replace("_", " ").title() for col in columns]
        )

        if action_name:
            self.booking_manager.log_action1(
                action_name, message=log_msg or f"Fetched {len(data)} rows for table"
            )

        if not data:
            table.setRowCount(1)
            table.setSpan(0, 0, 1, len(columns))
            item = QTableWidgetItem(no_data_message)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            table.setItem(0, 0, item)
            table.setUpdatesEnabled(True)
            return

        for row_idx, row in enumerate(data):
            table.insertRow(row_idx)
            for col_idx, col_name in enumerate(columns):
                value = row.get(col_name, "")
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row_idx, col_idx, item)

        table.setUpdatesEnabled(True)

    def _on_table_loaded(self, cache_key, data):
        self._table_cache[cache_key] = data

        if cache_key == "management":
            self.populate_table(
                self.table,
                data,
                ["hotel_id", "hotel_name", "place", "pin_code"],
                action_name="select_management_hotels",
                log_msg=f"Fetched {len(data)} management hotels",
            )
        elif cache_key == "booking":
            self.populate_table(
                self.table1,
                data,
                ["hotel_id", "hotel_name", "pin_code", "place"],
                action_name="select_booking_hotels",
                log_msg=f"Fetched {len(data)} booking hotels",
            )

    def refresh_all_tables(self, force=True):
        self.invalidate_cache()
        QTimer.singleShot(
            0, lambda: self.refresh_hotel_table(force=force, background=True, table=0)
        )
        QTimer.singleShot(
            0, lambda: self.refresh_hotel_table(force=force, background=True, table=1)
        )

    def invalidate_cache(self, table_key=None):
        if table_key:
            self._table_cache[table_key] = None
        else:
            self._table_cache = {"management": None, "booking": None}

    def book_hotel_dialog(self):
        MessageBoxManager.info(
            self,
            "<b>Book Hotel</b>",
            "Click on the <b>hotel</b> you want to <b>book</b>. "
            "If <b>rooms</b> appear <b>unavailable</b>, try adjusting the <b>Booked From</b> "
            "and <b>Booked To</b> dates to match your desired booking period.",
        )

    def toggle_max_restore(self):
        hwnd = int(self.winId())
        screen = QApplication.primaryScreen().availableGeometry()

        if self._is_maximized:

            user32.ShowWindow(hwnd, SW_RESTORE)
            self.setGeometry(self._normal_geometry)
            self.setMask(QRegion())
            self._is_maximized = False

            self.title_bar.setStyleSheet(
                """
				background-color: #2E86C1;
				border-top-left-radius: 12px;
				border-top-right-radius: 12px;
			"""
            )
            self.btn_max.setIcon(QIcon(MAXIMIZE_PATH))

            shadow = self.pages_widget.graphicsEffect()
            if isinstance(shadow, QGraphicsDropShadowEffect):
                shadow.setEnabled(True)

        else:

            self._normal_geometry = self.geometry()

            geo = QApplication.primaryScreen().availableGeometry()
            self.setGeometry(geo)

            self.setMask(QRegion())
            shadow = self.pages_widget.graphicsEffect()
            if isinstance(shadow, QGraphicsDropShadowEffect):
                shadow.setEnabled(False)

            self.title_bar.setStyleSheet(
                """
				background-color: #2E86C1;
				border-top-left-radius: 0px;
				border-top-right-radius: 0px;
			"""
            )
            self.btn_max.setIcon(QIcon(RESTORE_PATH))
            self._is_maximized = True

        self.update()
        self.repaint()

    @staticmethod
    def check_booking():
        a = BookInitialDialog(
            title_obj="Check Booking",
            placeholder="Enter your name or booking id...",
            btn_text="Check",
        )
        a.exec()

    @staticmethod
    def delete_booking():
        a = BookInitialDialog(
            title_obj="Cancel Booking",
            placeholder="Enter your name or booking id...",
            btn_text="Delete",
        )
        a.exec()

    def open_hotel1_dialog(self):

        hotel_dialog = HotelIDialog()
        if not hotel_dialog.exec():
            return

        hotel_ID = hotel_dialog.get_hotel_id()

        login_dialog = LoginDialog(hotel_ID)
        if not login_dialog.exec():
            MessageBoxManager.warning(self, "Login Failed", "Incorrect credentials!")
            return

        loader = LoadingOverlay(self, gif_path=SPINNER_PATH, text="Loading bookings...")
        loader.show_overlay()
        QApplication.processEvents()
        QTimer.singleShot(0, loader.hide_overlay)

        def run_show_bookings():
            self.show_bookings(hotel_ID)

        QTimer.singleShot(0, run_show_bookings)

    def get_filtered_hotels(self, page=2):
        if page == 2:
            text = self.filter_input_page2.text().strip().lower()
        else:
            text = self.filter_input_page3.text().strip().lower()

        conn = create_connection()
        cu = conn.cursor()

        query = "SELECT * FROM hotel_details WHERE 1=1"
        params = []

        if text:
            query += " AND (LOWER(hotel_name) LIKE %s OR LOWER(place) LIKE %s)"
            params.extend([f"%{text}%", f"%{text}%"])

        cu.execute(query, tuple(params))
        hotels = cu.fetchall()
        cu.close()
        conn.close()
        self.booking_manager.log_action1(
            "select_hotels",
            message=f"Fetched {len(hotels)} hotels using filter '{text}' (page={page})",
        )
        return hotels

    def refresh_hotel_list_page2(self):
        hotels = self.get_filtered_hotels(page=2)
        self.update_page2_hotel_display(hotels)

    def refresh_hotel_list_page3(self):
        hotels = self.get_filtered_hotels(page=3)
        self.update_page3_hotel_display(hotels)

    def update_page2_hotel_display(self, hotels):
        self.populate_table(
            self.table,
            hotels,
            ["hotel_id", "hotel_name", "place", "pin_code"],
            action_name="filter_hotels_page2",
            log_msg=f"Filtered {len(hotels)} hotels on page 2",
            no_data_message="No hotels available",
        )

    def update_page3_hotel_display(self, hotels):
        self.populate_table(
            self.table1,
            hotels,
            [
                "hotel_id",
                "hotel_name",
                "pin_code",
                "place",
            ],
            action_name="filter_hotels_page3",
            log_msg=f"Filtered {len(hotels)} hotels on page 3",
            no_data_message="No hotels available",
        )

    @staticmethod
    def show_bookings(hotel_id):
        viewer = BookingViewer(hotel_id)
        viewer.exec()

    def cell_clicked_book(self):

        hotel_id_item = self.table1.item(self.table1.currentRow(), 0)
        if not hotel_id_item:
            return

        hotel_id = int(hotel_id_item.text())

        loader = LoadingOverlay(
            self, gif_path=SPINNER_PATH, text="Preparing Booking Form..."
        )
        loader.show_overlay()
        QApplication.processEvents()

        class BookingLoadWorker(QObject):
            finished = pyqtSignal(object)

            def __init__(self, manager, hotel_id):
                super().__init__()
                self.manager = manager
                self.hotel_id = hotel_id

            def run(self):
                data = (
                    self.manager.get_hotel_data(self.hotel_id)
                    if hasattr(self.manager, "get_hotel_data")
                    else None
                )
                self.finished.emit(data)

        self.booking_thread = QThread()
        self.booking_worker = BookingLoadWorker(self.booking_manager, hotel_id)
        self.booking_worker.moveToThread(self.booking_thread)

        self.booking_thread.started.connect(self.booking_worker.run)
        self.booking_worker.finished.connect(
            lambda data: self.on_booking_loaded(loader, hotel_id, data)
        )
        self.booking_worker.finished.connect(self.booking_thread.quit)
        self.booking_worker.finished.connect(self.booking_worker.deleteLater)
        self.booking_thread.finished.connect(self.booking_thread.deleteLater)
        self.booking_thread.start()

    @staticmethod
    def on_booking_loaded(loader, hotel_id, data):

        loader.hide_overlay()

        dialog = BookingForm(hotel_id)
        dialog.resize(700, 500)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            pass

    def on_hotel_loaded(self, loader, hotel_id, data):

        loader.hide_overlay()

        login = LoginDialog(hotel_id, self)
        if login.exec() == QDialog.DialogCode.Accepted and login.authenticated:
            dialog = HotelForm(self, hotel_id=hotel_id)
            dialog.resize(700, 500)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.refresh_hotel_table(table=0)

    def show_about(self):
        RoundedDialog().show_about(self)

    def on_radio_selected(self):
        selected_id = self.button_group.checkedId()
        if selected_id != -1:
            selected_button = self.button_group.button(selected_id)
            self.selected_option = selected_button.text()
            self.submit_button.setEnabled(True)

    def refresh_hotel_table(self, table=0, force=False, background=True):

        cache_key = "management" if table == 0 else "booking"
        target_table = self.table if table == 0 else self.table1

        if self._table_cache.get(cache_key):
            if cache_key == "management":
                self.populate_table(
                    target_table,
                    self._table_cache[cache_key],
                    ["hotel_id", "hotel_name", "place", "pin_code"],
                )
            else:
                self.populate_table(
                    target_table,
                    self._table_cache[cache_key],
                    ["hotel_id", "hotel_name", "pin_code", "place"],
                )

        def fetch_fn():
            conn = create_connection()
            cur = conn.cursor(pymysql.cursors.DictCursor)

            if table == 0:
                cur.execute(
                    """
					SELECT hotel_id, hotel_name, place, pin_code
					FROM hotel_details
				"""
                )
            else:
                cur.execute(
                    """
					SELECT hotel_id, hotel_name, pin_code, place
					FROM hotel_details
				"""
                )

            data = cur.fetchall()
            conn.close()

            action_name = (
                "select_management_hotels" if table == 0 else "select_booking_hotels"
            )
            self.booking_manager.log_action1(
                action_name,
                message=f"Fetched {len(data)} {'management' if table == 0 else 'booking'} hotels",
            )
            return data

        loader = TableLoader(fetch_fn)
        loader.signals.finished.connect(
            lambda data: self._on_table_loaded(cache_key, data)
        )
        self.threadpool.start(loader)

    def start_page_change(self):
        self.submit_button.setEnabled(False)

        self.loader = LoadingOverlay(self, gif_path=SPINNER_PATH, text="Loading...")
        self.loader.show_overlay()
        QApplication.processEvents()

        QTimer.singleShot(0, self.change_page)

    def change_page(self):
        if self.pages_layout.currentIndex() == 0:
            self.next_page = self.selected_option
        QApplication.processEvents()

        self.toggle_menu_item.menuAction().setVisible(True)
        self.about_menu_item.menuAction().setVisible(True)
        loader = self.loader

        loader.show_overlay()
        QApplication.processEvents()

        if self.next_page == "Booking Portal":
            self.action_menu_item.menuAction().setVisible(False)
            self.action2_menu_item.menuAction().setVisible(True)

        elif self.next_page == "Management Portal":
            self.action2_menu_item.menuAction().setVisible(False)
            self.action_menu_item.menuAction().setVisible(True)

        QApplication.processEvents()

        self.page_thread = QThread()
        self.page_worker = PageWorker(
            self.next_page, self.booking_manager, self._table_cache
        )
        self.page_worker.moveToThread(self.page_thread)

        self.page_thread.started.connect(self.page_worker.run)
        self.page_worker.finished.connect(
            lambda b, m, p: self.on_page_data_loaded(loader, b, m, p)
        )
        self.page_worker.finished.connect(self.page_thread.quit)
        self.page_worker.finished.connect(self.page_worker.deleteLater)
        self.page_thread.finished.connect(self.page_thread.deleteLater)
        self.page_thread.start()

        QTimer.singleShot(0, self._refresh_after_switch_async)

    def on_page_data_loaded(self, loader, booking_data, management_data, next_page):
        if booking_data:
            self._table_cache["booking"] = booking_data
        if management_data:
            self._table_cache["management"] = management_data

        if next_page == "Booking Portal":
            self.pages_layout.setCurrentWidget(self.page3)
            self.title_label.setText("Booking Portal")
            self.setWindowTitle("Booking Portal")

            if self._table_cache.get("booking"):
                self.populate_table(
                    self.table,
                    self._table_cache["booking"],
                    ["hotel_id", "hotel_name", "place", "pin_code"],
                    action_name=None,
                )

        elif next_page == "Management Portal":
            self.pages_layout.setCurrentWidget(self.page2)
            self.title_label.setText("Management Portal")
            self.setWindowTitle("Management Portal")

            if self._table_cache.get("management"):
                self.populate_table(
                    self.table1,
                    self._table_cache["management"],
                    ["hotel_id", "hotel_name", "pin_code", "place"],
                    action_name=None,
                )

        self.next_page = (
            "Booking Portal"
            if self.next_page == "Management Portal"
            else "Management Portal"
        )

        self.update_menu_label()
        loader.hide_overlay()

    def _refresh_after_switch_async(self):
        if self.next_page == "Booking Portal":
            table = self.table1
            loader_fn = lambda: self.refresh_hotel_table(background=True, table=1)
        else:
            table = self.table
            loader_fn = lambda: self.refresh_hotel_table(background=True, table=0)
        table.setUpdatesEnabled(False)
        loader_fn()
        table.setUpdatesEnabled(True)

    def cell_clicked(self):

        hotel_id_item = self.table.item(self.table.currentRow(), 0)
        if not hotel_id_item:
            return

        hotel_id = int(hotel_id_item.text())

        self.booking_manager.log_action(
            "open_hotel_edit",
            hotel_id=hotel_id,
            message=f"Opened HotelForm for editing hotel {hotel_id}",
        )

        loader = LoadingOverlay(
            self, gif_path=SPINNER_PATH, text="Loading hotel data..."
        )
        loader.show_overlay()
        QApplication.processEvents()

        class HotelLoadWorker(QObject):
            finished = pyqtSignal(object)

            def __init__(self, manager, hotel_id):
                super().__init__()
                self.manager = manager
                self.hotel_id = hotel_id

            def run(self):
                data = (
                    self.manager.get_hotel_data(self.hotel_id)
                    if hasattr(self.manager, "get_hotel_data")
                    else None
                )
                self.finished.emit(data)

        self.hotel_thread = QThread()
        self.hotel_worker = HotelLoadWorker(self.booking_manager, hotel_id)
        self.hotel_worker.moveToThread(self.hotel_thread)

        self.hotel_thread.started.connect(self.hotel_worker.run)
        self.hotel_worker.finished.connect(
            lambda data: self.on_hotel_loaded(loader, hotel_id, data)
        )
        self.hotel_worker.finished.connect(self.hotel_thread.quit)
        self.hotel_worker.finished.connect(self.hotel_worker.deleteLater)
        self.hotel_thread.finished.connect(self.hotel_thread.deleteLater)
        self.hotel_thread.start()

    def update_menu_label(self):
        self.toggle_action.setText(f"Go to {self.next_page}")

    def open_hotel_form_dialog(self):
        dialog = HotelForm(self)
        dialog.resize(700, 500)
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self.refresh_hotel_table(table=0)


class LoadingOverlay(QWidget):
    def __init__(self, parent=None, gif_path=SPINNER_PATH, text="Loading..."):
        super().__init__(parent)
        self.parent = parent

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("background: transparent;")
        self.hide()

        self.blur_effect = QGraphicsBlurEffect(self)
        self.blur_effect.setBlurRadius(25)
        self.setGraphicsEffect(self.blur_effect)

        self.overlay_tint = QWidget(self)
        self.overlay_tint.setStyleSheet(
            """
			background-color: rgba(0, 0, 0, 120);
			border-radius: 10px;
		"""
        )
        self.overlay_tint.lower()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        self.spinner = QLabel(self)
        self.spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinner.setStyleSheet("background: transparent; border: none;")

        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(QSize(150, 150))
        self.spinner.setMovie(self.movie)
        self.movie.start()

        layout.addWidget(self.spinner)

        self.label = QLabel(text)
        self.label.setStyleSheet(
            """
			color: white;
			font-size: 15px;
			background: transparent;
			border: none;
		"""
        )
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(250)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        if parent:
            self._align_with_parent()
            parent.installEventFilter(self)

    def _align_with_parent(self):
        if not self.parent:
            return
        self.resize(self.parent.size())
        self.overlay_tint.resize(self.size())

    def eventFilter(self, obj, event):
        if obj == self.parent and event.type() in (event.Type.Move, event.Type.Resize):
            self._align_with_parent()
        return super().eventFilter(obj, event)

    def show_overlay(self, text=None):
        if text:
            self.label.setText(text)
        self._align_with_parent()
        self.show()
        if self.movie and self.movie.isValid():
            self.movie.start()

        self.fade_anim.stop()
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

    def hide_overlay(self):
        self.fade_anim.stop()
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.finished.connect(self._final_hide)
        self.fade_anim.start()

    def _final_hide(self):
        if self.movie:
            self.movie.stop()
        self.hide()


class PageWorker(QObject):
    finished = pyqtSignal(object, object, str)

    def __init__(self, target_page, booking_manager, cache):
        super().__init__()
        self.target_page = target_page
        self.booking_manager = booking_manager
        self.cache = cache

    def run(self):
        booking_data, management_data = None, None

        if self.target_page == "Booking Portal":
            if not self.cache.get("booking"):
                booking_data = self.booking_manager.get_management_data()
        elif self.target_page == "Management Portal":
            if not self.cache.get("management"):
                management_data = self.booking_manager.get_management_data()

        self.finished.emit(booking_data, management_data, self.target_page)


class UniqueRoomLineEdit(QLineEdit):
    def __init__(self, get_other_rooms_func, parent=None):
        super().__init__(parent)
        self.get_other_rooms = get_other_rooms_func
        self.textChanged.connect(self.prevent_duplicates)

    def prevent_duplicates(self, text):
        rooms = [r.strip() for r in text.split(",") if r.strip()]
        other_rooms = self.get_other_rooms()
        unique_rooms = []
        for r in rooms:
            if r not in unique_rooms and r not in other_rooms:
                unique_rooms.append(r)

        new_text = ", ".join(unique_rooms)
        if new_text != text:
            self.blockSignals(True)
            self.setText(new_text)
            self.blockSignals(False)


class HotelForm(RoundedDialog):
    def __init__(self, parent=None, hotel_id=None):
        super().__init__(parent)
        self.thread = None
        self.progress = None
        self.hotel_id = hotel_id
        self.booking_manager = BookingDataManagement()

        self.setWindowTitle("Hotel Registration Form")
        self.resize(850, 800)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(10, 10, 10, 10)

        container = QWidget()
        container.setStyleSheet(
            """
			QWidget {
				background-color: #ffffff;
				border-radius: 20px;
			}
		"""
        )
        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 80))
        container.setGraphicsEffect(shadow)
        outer_layout.addWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        title_label = QLabel("Hotel Registration")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: 600; color: #1F4E79;")
        main_layout.addWidget(title_label)

        close_x = QPushButton("\u00d7")
        close_x.setFixedSize(28, 28)
        close_x.setStyleSheet(
            """
			QPushButton {
				border: none;
				color: #666;
				font-size: 20px;
				font-weight: bold;
				border-radius: 14px;
				background-color: transparent;
			}
			QPushButton:hover { background-color: #EAECEE; }
		"""
        )

        close_x.clicked.connect(self.reject)

        main_layout.insertWidget(0, close_x, alignment=Qt.AlignmentFlag.AlignRight)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(scroll_bar())

        main_layout.addWidget(scroll)

        content_widget = QWidget()
        scroll.setWidget(content_widget)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_layout.setSpacing(16)

        summary_group = QGroupBox("Summary")
        summary_group.setStyleSheet(self._groupbox_style())
        summary_layout = QFormLayout()
        self.total_rooms_label = QLabel("0")
        self.available_rooms_label = QLabel("0")
        summary_layout.addRow("Total Rooms:", self.total_rooms_label)
        summary_layout.addRow("Available Rooms:", self.available_rooms_label)
        summary_group.setLayout(summary_layout)
        content_layout.addWidget(summary_group)

        self.avail_rooms_group = QGroupBox("Check Availability")
        self.avail_rooms_group.setStyleSheet(self._groupbox_style())

        avail_layout = QVBoxLayout()
        avail_layout.setSpacing(10)

        today = QDate.currentDate()
        max_date = today.addDays(80)

        date_row = QHBoxLayout()
        date_row.setSpacing(10)

        from_label = QLabel("From:")
        from_label.setStyleSheet("font-weight:500;")
        self.booked_from_input = QDateEdit()
        self.booked_from_input.setDisplayFormat("dd/MM/yyyy")
        self.booked_from_input.setDate(today)
        self.booked_from_input.setMinimumDate(today)
        self.booked_from_input.setMaximumDate(max_date)
        self.booked_from_input.setStyleSheet(self._line_edit_style())

        to_label = QLabel("To:")
        to_label.setStyleSheet("font-weight:500;")
        self.booked_to_input = QDateEdit()
        self.booked_to_input.setDisplayFormat("dd/MM/yyyy")

        self.booked_to_input.setDate(today.addDays(1))
        self.booked_to_input.setMinimumDate(today.addDays(1))
        self.booked_to_input.setMaximumDate(max_date)
        self.booked_to_input.setStyleSheet(self._line_edit_style())

        date_row.addWidget(from_label)
        date_row.addWidget(self.booked_from_input)
        date_row.addWidget(to_label)
        date_row.addWidget(self.booked_to_input)
        date_row.addStretch()

        avail_layout.addLayout(date_row)

        self.room_layout = QGridLayout()
        self.room_layout.setSpacing(10)

        self.room_container = QWidget()
        self.room_container.setLayout(self.room_layout)

        scroll_avail = QScrollArea()
        scroll_avail.setWidgetResizable(True)
        scroll_avail.setWidget(self.room_container)
        scroll_avail.setFixedHeight(60)
        scroll_avail.setStyleSheet(
            """
			QScrollArea { border: none; background-color: #fdfdfd; }
			QScrollBar:vertical { background: #eee; width: 10px; border-radius:5px; }
			QScrollBar::handle:vertical { background: #2E86C1; border-radius:5px; }
		"""
        )

        avail_layout.addWidget(scroll_avail)

        self.avail_rooms_group.setLayout(avail_layout)

        content_layout.addWidget(self.avail_rooms_group)

        self.avail_rooms_group.setVisible(bool(self.hotel_id))

        def update_to_date_constraints():
            from_date = self.booked_from_input.date()
            new_min = from_date.addDays(1)
            self.booked_to_input.setMinimumDate(new_min)
            if self.booked_to_input.date() < new_min:
                self.booked_to_input.setDate(new_min)

        self.booked_from_input.dateChanged.connect(update_to_date_constraints)
        self.booked_from_input.dateChanged.connect(self.on_dates_changed)
        self.booked_to_input.dateChanged.connect(self.on_dates_changed)

        if self.hotel_id:
            self.load_available_rooms()

        hotel_group = QGroupBox("Hotel Information")
        hotel_group.setStyleSheet(self._groupbox_style())

        hotel_layout = QFormLayout()
        self.hotel_name_input = QLineEdit()
        self.place_input = QLineEdit()
        self.pin_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.floor_input = QLineEdit()
        self.rooms_input = QLineEdit()
        self.room_no = QLineEdit()
        self.room_no.textChanged.connect(self.update_room_no_fields)

        self.floor_input.textChanged.connect(self.room_no_generator)
        self.rooms_input.textChanged.connect(self.room_no_generator)
        self.username_input = QLineEdit()
        self.password_input = PasswordLineEdit()

        for w in [
            self.hotel_name_input,
            self.place_input,
            self.pin_input,
            self.contact_input,
            self.floor_input,
            self.rooms_input,
            self.room_no,
            self.username_input,
            self.password_input,
        ]:
            w.setStyleSheet(self._line_edit_style())

        time_card = QFrame()
        time_card.setObjectName("timeCard")
        time_card.setStyleSheet(
            """
					QFrame#timeCard {
						background-color: #ffffff;
						border: 1.3px solid #d0d7de;
						border-radius: 12px;
						padding: 8px 12px;
					}
				"""
        )

        time_layout = QHBoxLayout(time_card)
        time_layout.setSpacing(15)
        time_layout.setContentsMargins(10, 6, 10, 6)

        label_style = """
					QLabel {
						font-size: 13px;
						font-weight: 600;
						color: #2E86C1;
						min-width: 95px;
					}
				"""

        time_style = """
					QTimeEdit {
						background-color: #fafbfc;
						border: 1.2px solid #ccd6dd;
						border-radius: 8px;
						padding: 4px 8px;
						font-size: 13px;
						color: #2c3e50;
						min-width: 95px;
						max-height: 26px;
					}
					QTimeEdit:hover {
						background-color: #eef6ff;
						border: 1.2px solid #2E86C1;
					}
					QTimeEdit:focus {
						border: 1.3px solid #3498db;
						background-color: #ffffff;
					}
				"""

        current = QTime(11, 0)

        checkin_label = QLabel("Check-in:")
        checkin_label.setStyleSheet(label_style)
        self.checkin_time_input = QTimeEdit()
        self.checkin_time_input.setDisplayFormat("hh:mm AP")
        self.checkin_time_input.setTime(current)
        self.checkin_time_input.setStyleSheet(time_style)

        checkout_label = QLabel("Check-out:")
        checkout_label.setStyleSheet(label_style)
        self.checkout_time_input = QTimeEdit()
        self.checkout_time_input.setDisplayFormat("hh:mm AP")
        self.checkout_time_input.setTime(current.addSecs(3600))
        self.checkout_time_input.setStyleSheet(time_style)

        time_layout.addWidget(checkin_label)
        time_layout.addWidget(self.checkin_time_input)
        time_layout.addSpacing(10)
        time_layout.addWidget(checkout_label)
        time_layout.addWidget(self.checkout_time_input)
        time_layout.addStretch()
        self.checkin_time_input.timeChanged.connect(self.validate_times)
        self.checkout_time_input.timeChanged.connect(self.on_checkout_changed)

        hotel_layout.addRow(time_card)
        hotel_layout.addRow("Hotel Name:", self.hotel_name_input)
        hotel_layout.addRow("Place:", self.place_input)
        hotel_layout.addRow("Pin Code:", self.pin_input)
        hotel_layout.addRow("Contact:", self.contact_input)
        hotel_layout.addRow("No. of Floors:", self.floor_input)
        hotel_layout.addRow("Rooms per Floor:", self.rooms_input)
        hotel_layout.addRow("Room Numbers:", self.room_no)

        hotel_layout.addRow("Username:", self.username_input)
        hotel_layout.addRow("Password:", self.password_input)

        hotel_group.setLayout(hotel_layout)

        scroll_hotel = QScrollArea()
        scroll_hotel.setWidgetResizable(True)
        scroll_hotel.setWidget(hotel_group)
        scroll_hotel.setMinimumHeight(280)
        scroll_hotel.setMaximumHeight(400)
        scroll_hotel.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_hotel.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_hotel.setStyleSheet(
            """
			QScrollArea { border: none; background-color: #ffffff; }
			QScrollBar:vertical { width: 0px; }
			QScrollBar:horizontal { height: 0px; }
		"""
        )

        content_layout.addWidget(scroll_hotel)

        room_group = QGroupBox("Room Types")
        room_group.setStyleSheet(self._groupbox_style())

        room_layout = QVBoxLayout()
        room_layout.setSpacing(10)

        spinbox_layout = QFormLayout()
        self.room_type_count = QSpinBox()
        self.room_type_count.setRange(1, 8)
        self.room_type_count.setValue(1)
        self.room_type_count.setStyleSheet(self._spinbox_style())
        spinbox_layout.addRow("Number of Room Types:", self.room_type_count)
        room_layout.addLayout(spinbox_layout)

        self.dynamic_fields_container = QWidget()
        self.dynamic_fields_layout = QGridLayout()
        self.dynamic_fields_layout.setSpacing(10)
        self.dynamic_fields_container.setLayout(self.dynamic_fields_layout)

        scroll_area_room_types = QScrollArea()
        scroll_area_room_types.setWidgetResizable(True)
        scroll_area_room_types.setWidget(self.dynamic_fields_container)
        scroll_area_room_types.setFixedHeight(110)
        scroll_area_room_types.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll_area_room_types.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll_area_room_types.setStyleSheet(
            """
			QScrollArea { border: none; background-color: #fdfdfd; }
			QScrollBar:vertical { background: #eee; width: 10px; border-radius:5px; }
			QScrollBar::handle:vertical { background: #2E86C1; border-radius:5px; }
		"""
        )

        room_layout.addWidget(scroll_area_room_types)

        room_group.setLayout(room_layout)
        content_layout.addWidget(room_group)

        self.assigned_rooms_group = QGroupBox("Assigned Rooms")
        self.assigned_rooms_group.setStyleSheet(self._groupbox_style())
        self.assigned_rooms_layout = QGridLayout()
        self.assigned_rooms_layout.setSpacing(10)
        self.assigned_rooms_group.setLayout(self.assigned_rooms_layout)

        scroll1 = QScrollArea()
        scroll1.setWidgetResizable(True)
        scroll1.setWidget(self.assigned_rooms_group)
        scroll1.setFixedHeight(180)
        scroll1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll1.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        content_layout.addWidget(scroll1)

        self.room_type_inputs = []
        self.room_price_inputs = []
        self.total_room_inputs = []
        self.room_no_inputs = []
        self.room_available_inputs = []
        self.assigned_labels = []
        self.room_type_ids = []
        self.booked_map = {}

        self.button_box = QDialogButtonBox()
        self.ok_button = self.button_box.addButton(
            "Save", QDialogButtonBox.ButtonRole.AcceptRole
        )
        self.cancel_button = self.button_box.addButton(
            "Cancel", QDialogButtonBox.ButtonRole.RejectRole
        )

        if self.hotel_id:
            self.delete_button = self.button_box.addButton(
                "Delete Hotel", QDialogButtonBox.ButtonRole.DestructiveRole
            )
            self.delete_button.setStyleSheet(
                """
						QPushButton { background-color:#E74C3C; color:white; font-weight:bold; border-radius:6px; padding:6px 12px; }
						QPushButton:hover { background-color:#C0392B; }
					"""
            )
            self.delete_button.clicked.connect(self.delete_hotel)

        self.ok_button.setStyleSheet(
            """
					QPushButton { background-color:#2E86C1; color:white; font-weight:bold; border-radius:6px; padding:6px 12px; }
					QPushButton:hover { background-color:#21618C; }
				"""
        )
        self.cancel_button.setStyleSheet(
            """
					QPushButton { background-color:#ccc; color:black; border-radius:6px; padding:6px 12px; }
					QPushButton:hover { background-color:#bbb; }
				"""
        )
        self.ok_button.clicked.connect(self.submit_data)
        self.cancel_button.clicked.connect(self.reject)
        content_layout.addWidget(
            self.button_box, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.room_type_count.valueChanged.connect(self.generate_room_fields)
        QTimer.singleShot(
            0, lambda: self.generate_room_fields(self.room_type_count.value())
        )

        if self.hotel_id:
            QTimer.singleShot(0, self.load_data)
        self.setUpdatesEnabled(True)
        QApplication.processEvents()

    @staticmethod
    def _spinbox_style():
        return """
		QSpinBox {
			border: 1px solid #ccc;
			border-radius: 6px;
			padding: 4px 8px;
			height: 28px;
			font-size: 14px;
		}
		QSpinBox:focus {
			border: 1px solid #2E86C1;
		}
		QSpinBox::up-button, QSpinBox::down-button {
			width: 20px;
			height: 20px;
		}
	"""

    @staticmethod
    def _line_edit_style():
        return """
		QLineEdit, QDateEdit {
			border: 1px solid #ccc;
			border-radius: 6px;
			padding: 6px 8px;
			height:28px;
			font-size: 14px;
		}
		QLineEdit:focus, QDateEdit:focus {
			border: 1px solid #2E86C1;
			background: #FDFEFE;
		}
	"""

    @staticmethod
    def _groupbox_style():
        return """
		QGroupBox {
			font-weight:bold;
			color: #1F4E79;
			border: 2px solid #AED6F1;
			border-radius: 12px;
			padding: 12px;
			background-color: #ffffff;
		}
	"""

    @staticmethod
    def _primary_btn_style():
        return """
		QPushButton {
			background-color: #2E86C1;
			color: white;
			font-weight: 600;
			font-size: 15px;
			border-radius: 10px;
			padding: 8px 18px;
		}
		QPushButton:hover { background-color: #1A5276; }
		QPushButton:pressed { background-color: #154360; }
	"""

    @staticmethod
    def _secondary_btn_style():
        return """
		QPushButton {
			background-color: #ccc;
			color: black;
			border-radius: 10px;
			padding: 8px 18px;
		}
		QPushButton:hover { background-color: #bbb; }
	"""

    def validate_times(self, new_checkin_time):
        checkout = self.checkout_time_input.time()

        if checkout <= new_checkin_time:
            self.checkout_time_input.blockSignals(True)
            self.checkout_time_input.setTime(new_checkin_time.addSecs(3600))
            self.checkout_time_input.blockSignals(False)

    def on_checkout_changed(self, new_checkout_time):
        checkin = self.checkin_time_input.time()

        if new_checkout_time <= checkin:
            self.checkin_time_input.blockSignals(True)
            self.checkin_time_input.setTime(new_checkout_time.addSecs(-3600))
            self.checkin_time_input.blockSignals(False)

    def get_all_other_rooms(self, exclude_index=None):
        all_rooms = []
        for i, field in enumerate(self.room_no_inputs):
            if exclude_index is not None and i == exclude_index:
                continue
            all_rooms.extend([r.strip() for r in field.text().split(",") if r.strip()])
        return all_rooms

    def on_dates_changed(self):
        booked_from = self.booked_from_input.date()
        booked_to = self.booked_to_input.date()

        if booked_to < booked_from:
            MessageBoxManager.warning(
                self, "Date Error", "Booked To date cannot be before Booked From date."
            )
            self.booked_to_input.setDate(booked_from)
            return
        self.load_available_rooms()
        self.booking_manager.log_action(
            "date_changed",
            hotel_id=self.hotel_id,
            message=f"Booking dates changed: {self.booked_from_input.date().toString()} to {self.booked_to_input.date().toString()}",
        )

    def load_available_rooms(self):
        try:
            while self.room_layout.count():
                item = self.room_layout.takeAt(0)
                if item and item.widget():
                    item.widget().deleteLater()

            booked_from = self.booked_from_input.date().toString("yyyy-MM-dd")
            booked_to = self.booked_to_input.date().toString("yyyy-MM-dd")

            available_rooms = self.booking_manager.get_available_rooms(
                self.hotel_id, booked_from, booked_to
            )

            if not available_rooms:
                lbl = QLabel("No rooms available for selected dates")
                lbl.setStyleSheet("color:red; font-weight:bold; font-size:13px;")
                self.room_layout.addWidget(lbl, 0, 0)
                self.available_rooms_label.setText("0")

                self.booking_manager.log_action(
                    "no_rooms_available",
                    hotel_id=self.hotel_id,
                    message=f"No rooms available from {booked_from} to {booked_to}",
                )
                return

            grouped = {}
            for r in available_rooms:
                grouped.setdefault(r["room_type"], []).append(r["room_no"])

            self.available_rooms_label.setText(
                str(sum(len(v) for v in grouped.values()))
            )

            row, col, max_cols = 0, 0, 2
            for rtype, rooms in grouped.items():
                rooms_str = ", ".join(rooms) if rooms else "None"
                count = len(rooms)
                color = "green" if count > 3 else "orange" if count > 0 else "red"

                lbl = QLabel(f"{rtype}: {rooms_str}")
                lbl.setStyleSheet(
                    f"font-weight: bold; color: {color}; font-size: 13px; padding: 4px;"
                )
                lbl.setWordWrap(True)
                self.room_layout.addWidget(lbl, row, col)

                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1

            self.booking_manager.log_action(
                "rooms_loaded",
                hotel_id=self.hotel_id,
                message=f"Available rooms loaded from {booked_from} to {booked_to}: {grouped}",
            )

        except Exception as e:
            lbl = QLabel(f"Error loading rooms: {e}")
            lbl.setStyleSheet("color:red; font-weight:bold; font-size:13px;")
            self.room_layout.addWidget(lbl, 0, 0)
            self.available_rooms_label.setText("0")
            self.booking_manager.log_action(
                "rooms_load_error",
                hotel_id=self.hotel_id,
                message=f"Error loading rooms: {e}",
            )

    def remove_assigned_row(self, index):
        layouts = [self.assigned_rooms_layout]
        for layout in layouts:
            for col in range(layout.columnCount()):
                item = layout.itemAtPosition(index, col)
                if item and item.widget():
                    w = item.widget()
                    if not sip.isdeleted(w):
                        w.deleteLater()
                    layout.removeItem(item)

    def generate_room_fields(self, count):
        old_types = [w.text() for w in getattr(self, "room_type_inputs", [])]
        old_prices = [w.text() for w in getattr(self, "room_price_inputs", [])]
        old_totals = [w.value() for w in getattr(self, "total_room_inputs", [])]
        old_ids = getattr(self, "room_type_ids", [])
        while self.dynamic_fields_layout.count():
            item = self.dynamic_fields_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        current_rows = len(self.room_no_inputs)
        if current_rows > count:
            for i in range(current_rows - 1, count - 1, -1):
                self.room_no_inputs.pop()
                if hasattr(self, "assigned_labels") and i < len(self.assigned_labels):
                    self.assigned_labels.pop()
                self.remove_assigned_row(i)

        self.room_type_inputs = []
        self.room_price_inputs = []
        self.total_room_inputs = []
        self.room_type_ids = []

        for i in range(count):
            type_input = QLineEdit()
            type_input.setStyleSheet(self._line_edit_style())
            price_input = QLineEdit()
            price_input.setPlaceholderText("Enter price")
            price_input.setStyleSheet(self._line_edit_style())
            total_input = QSpinBox()
            total_input.setRange(0, 1000)
            total_input.setStyleSheet(self._spinbox_style())
            if i < len(old_types):
                type_input.setText(old_types[i])
            if i < len(old_prices):
                price_input.setText(old_prices[i])
            if i < len(old_totals):
                total_input.setValue(old_totals[i])
            if i < len(old_ids):
                self.room_type_ids.append(old_ids[i])
            else:
                self.room_type_ids.append(None)
            self.dynamic_fields_layout.addWidget(QLabel(f"Room Type {i + 1}:"), i, 0)
            self.dynamic_fields_layout.addWidget(type_input, i, 1)
            self.dynamic_fields_layout.addWidget(QLabel("Price:"), i, 2)
            self.dynamic_fields_layout.addWidget(price_input, i, 3)
            self.dynamic_fields_layout.addWidget(QLabel("Total Rooms:"), i, 4)
            self.dynamic_fields_layout.addWidget(total_input, i, 5)
            if i >= len(getattr(self, "assigned_labels", [])):
                assigned_label = QLabel(f"{type_input.text() or f'Room Type {i + 1}'}:")
                assigned_label.setStyleSheet("font-weight:bold; color:#1F4E79;")
                self.assigned_rooms_layout.addWidget(assigned_label, i, 0)
                self.assigned_labels.append(assigned_label)

                room_no = UniqueRoomLineEdit(
                    lambda idx=i: self.get_all_other_rooms(exclude_index=idx)
                )
                room_no.setPlaceholderText("Rooms no.")
                room_no.setStyleSheet(self._line_edit_style())

                self.assigned_rooms_layout.addWidget(QLabel("Room No"), i, 1)
                self.assigned_rooms_layout.addWidget(room_no, i, 2)
                self.room_no_inputs.append(room_no)
            else:
                assigned_label = self.assigned_labels[i]
                room_no = self.room_no_inputs[i]
            room_no.textChanged.connect(self.sync_room_type_to_main)

            type_input.textChanged.connect(
                lambda text, lbl=assigned_label, i=i: lbl.setText(
                    f"{text or f'Room Type {i + 1}'}:"
                )
            )
            type_input.textChanged.connect(self.update_all_labels)
            total_input.valueChanged.connect(self.update_all_labels)
            total_input.valueChanged.connect(
                lambda _, rn_func=self.update_room_no_fields: QTimer.singleShot(
                    0, rn_func
                )
            )

            self.room_type_inputs.append(type_input)
            self.room_price_inputs.append(price_input)
            self.total_room_inputs.append(total_input)

        QTimer.singleShot(0, self.update_all_labels)
        QTimer.singleShot(0, self.update_room_no_fields)

    def sync_room_type_to_main(self):

        all_rooms = []
        for i, room_field in enumerate(self.room_no_inputs):
            rooms = self.parse_room_text(room_field.text())
            all_rooms.extend(rooms)

        unique_rooms = list(dict.fromkeys(all_rooms))
        self.room_no.blockSignals(True)
        self.room_no.setText(", ".join(unique_rooms))
        self.room_no.blockSignals(False)

    def update_room_no_fields(self):

        all_rooms = self.parse_room_text(self.room_no.text())
        assigned_index = 0

        for i, room_field in enumerate(self.room_no_inputs):
            total = (
                self.total_room_inputs[i].value()
                if i < len(self.total_room_inputs)
                else 0
            )
            slice_rooms = all_rooms[assigned_index : assigned_index + total]
            assigned_index += len(slice_rooms)

            room_field.blockSignals(True)
            room_field.setText(", ".join(slice_rooms))
            room_field.blockSignals(False)

        self.update_all_labels()

    def update_all_labels(self):
        total_rooms = sum(sp.value() for sp in self.total_room_inputs)
        total = total_rooms
        if hasattr(self, "booked_map"):
            total = total_rooms - sum(self.booked_map.values())
        self.total_rooms_label.setText(str(total_rooms))

    def load_data(self):
        if not self.hotel_id:
            return
        try:
            conn = create_connection()
            cu = conn.cursor(pymysql.cursors.DictCursor)
            cu.execute(
                "SELECT * FROM hotel_details WHERE hotel_id=%s", (self.hotel_id,)
            )
            hotel = cu.fetchone()
            cu.close()
            conn.close()

            if not hotel:
                MessageBoxManager.error(self, "Error", "Hotel not found.")
                return

            if hasattr(self, "booking_manager") and self.booking_manager:
                self.booking_manager.log_action(
                    "hotel_data_loaded",
                    hotel_id=self.hotel_id,
                    message=f"Hotel '{hotel.get('hotel_name')}' data loaded",
                )

            self.hotel_name_input.setText(str(hotel.get("hotel_name") or ""))
            self.place_input.setText(str(hotel.get("place") or ""))
            self.pin_input.setText(str(hotel.get("pin_code") or ""))
            self.contact_input.setText(str(hotel.get("contact_hotel") or ""))
            self.floor_input.setText(str(hotel.get("floor") or ""))
            self.rooms_input.setText(str(hotel.get("room") or ""))
            self.username_input.setText(str(hotel.get("username") or ""))
            self.password_input.setText(str(hotel.get("password") or ""))

            room_no_data = hotel.get("room_no") or "[]"
            try:
                room_list_global = json.loads(room_no_data)
            except Exception:
                try:
                    room_list_global = ast.literal_eval(room_no_data)
                except Exception:
                    room_list_global = []

            self.room_no.blockSignals(True)
            self.room_no.setText(", ".join(map(str, room_list_global)))
            self.room_no.blockSignals(False)

            conn = create_connection()
            cu = conn.cursor(pymysql.cursors.DictCursor)
            cu.execute(
                "SELECT * FROM room_types WHERE hotel_id=%s ORDER BY id",
                (self.hotel_id,),
            )
            rooms_load_data = cu.fetchall() or []
            cu.close()
            conn.close()

            room_count = len(rooms_load_data) if rooms_load_data else 1
            self.room_type_count.blockSignals(True)
            self.room_type_count.setValue(room_count)
            self.room_type_count.blockSignals(False)

            def populate():
                self.generate_room_fields(room_count)
                assigned_index = 0
                all_rooms = self.parse_room_text(self.room_no.text())

                for i, room in enumerate(rooms_load_data):
                    type_input = self.room_type_inputs[i]
                    price_input = self.room_price_inputs[i]
                    total_input = self.total_room_inputs[i]

                    type_input.blockSignals(True)
                    price_input.blockSignals(True)
                    total_input.blockSignals(True)

                    type_input.setText(str(room.get("room_type") or ""))
                    price_input.setText(str(room.get("price") or 0.0))
                    total_input.setValue(room.get("total") or 0)
                    self.room_type_ids[i] = room.get("id")

                    total = total_input.value()
                    slice_rooms = (
                        all_rooms[assigned_index : assigned_index + total]
                        if assigned_index < len(all_rooms)
                        else []
                    )

                    self.room_no_inputs[i].blockSignals(True)
                    self.room_no_inputs[i].setText(", ".join(slice_rooms))
                    self.room_no_inputs[i].blockSignals(False)

                    assigned_index += len(slice_rooms)

                    if i < len(self.assigned_labels):
                        self.assigned_labels[i].setText(
                            f"{type_input.text() or f'Room Type {i + 1}'}:"
                        )

                    type_input.blockSignals(False)
                    price_input.blockSignals(False)
                    total_input.blockSignals(False)

                self.update_all_labels()

            QTimer.singleShot(0, populate)

        except Exception as e:
            MessageBoxManager.error(self, "Error", f"Failed to load hotel: {e}")
            if hasattr(self, "booking_manager") and self.booking_manager:
                self.booking_manager.log_action(
                    "hotel_load_error",
                    hotel_id=getattr(self, "hotel_id", None),
                    message=f"Failed to load hotel data: {e}",
                )

    @staticmethod
    def parse_room_text(text):
        return [r.strip() for r in text.split(",") if r.strip()]

    def room_no_generator(self):

        floors_text = self.floor_input.text().strip()
        rooms_text = self.rooms_input.text().strip()
        if not floors_text or not rooms_text:
            self.room_no.clear()
            return

        try:
            floors = int(floors_text)
            rooms = int(rooms_text)
        except ValueError:
            self.room_no.clear()
            return
        room_list = [
            f"{f}{r:02d}" for f in range(1, floors + 1) for r in range(1, rooms + 1)
        ]
        unique_rooms = list(dict.fromkeys(room_list))

        self.room_no.blockSignals(True)
        self.room_no.setText(", ".join(unique_rooms))
        self.room_no.blockSignals(False)
        QTimer.singleShot(0, self.update_room_no_fields)

    def submit_data(self):
        try:
            is_new_hotel = self.hotel_id is None

            name = self.hotel_name_input.text().strip()
            place = self.place_input.text().strip()
            contact = self.contact_input.text().strip()
            pin_text = self.pin_input.text().strip()
            pin_code = int(pin_text) if pin_text.isdigit() else 0

            if not name or not place or not contact:
                raise ValueError("Please fill in all required hotel details.")

            room_text = self.room_no.text().strip()
            if not room_text:
                raise ValueError("Room numbers cannot be empty.")
            room_list = [r.strip() for r in room_text.split(",") if r.strip().isdigit()]
            total_rooms = sum(sp.value() for sp in self.total_room_inputs)
            if len(room_list) != total_rooms:
                MessageBoxManager.warning(
                    self,
                    "Room Count Mismatch",
                    f"Number of room numbers entered ({len(room_list)}) does not match total rooms ({total_rooms}).",
                )
                return

            conn = create_connection()
            cu = conn.cursor()

            room_list_db = json.dumps(room_list)
            check_in_time = self.checkin_time_input.time().toString("HH:mm:ss")
            check_out_time = self.checkout_time_input.time().toString("HH:mm:ss")

            if check_out_time <= check_in_time:
                MessageBoxManager.info(
                    self,
                    "Time Adjusted",
                    "Check-in/check-out times adjusted automatically.",
                )

            if is_new_hotel:
                username = self.username_input.text().strip()
                password = self.password_input.text().strip()

                if not username or not password:
                    raise ValueError("Username and password required for new hotel.")

                try:
                    cu.execute(
                        """INSERT INTO hotel_details
							(hotel_name, place, pin_code, contact_hotel, username, password,
							 floor, room, room_no, check_in, check_out)
						VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (
                            name,
                            place,
                            pin_code,
                            contact,
                            username,
                            password,
                            int(self.floor_input.text()),
                            int(self.rooms_input.text()),
                            room_list_db,
                            check_in_time,
                            check_out_time,
                        ),
                    )
                    self.hotel_id = cu.lastrowid

                    self.booking_manager.log_action(
                        "hotel_added",
                        hotel_id=self.hotel_id,
                        message=f"New hotel '{name}' added (ID {self.hotel_id})",
                    )
                except IntegrityError as e:
                    if e.args[0] == 1062:
                        MessageBoxManager.error(
                            self,
                            "Username Taken",
                            f"The username '{username}' is already taken.\nPlease choose another one.",
                        )
                        conn.rollback()
                        return
            else:
                cu.execute(
                    """UPDATE hotel_details
							  SET hotel_name=%s, place=%s, pin_code=%s, contact_hotel=%s,
								  floor=%s, room=%s, room_no=%s, check_in=%s, check_out=%s
							  WHERE hotel_id=%s""",
                    (
                        name,
                        place,
                        pin_code,
                        contact,
                        int(self.floor_input.text()),
                        int(self.rooms_input.text()),
                        room_list_db,
                        check_in_time,
                        check_out_time,
                        self.hotel_id,
                    ),
                )

                self.booking_manager.log_action(
                    "hotel_updated",
                    hotel_id=self.hotel_id,
                    message=f"Hotel '{name}' updated at {datetime.now()}",
                )

            cu.execute("SELECT id FROM room_types WHERE hotel_id=%s", (self.hotel_id,))
            existing_ids = [row["id"] for row in cu.fetchall()]
            current_ids = []

            for i in range(len(self.room_type_inputs)):
                room_type = self.room_type_inputs[i].text().strip()
                price_text = self.room_price_inputs[i].text().strip()
                total = self.total_room_inputs[i].value()
                room_no_text = self.room_no_inputs[i].text().strip()
                room_id = self.room_type_ids[i]

                if not room_type:
                    MessageBoxManager.error(
                        self, "Error", f"Room type name required at row {i + 1}."
                    )
                    return

                room_no_list = [r.strip() for r in room_no_text.split(",") if r.strip()]
                if len(room_no_list) != total:
                    MessageBoxManager.error(
                        self,
                        "Error",
                        f"Room numbers ({len(room_no_list)}) do not match total rooms ({total}) for '{room_type}'.",
                    )
                    return

                price = float(price_text) if price_text else 0.0
                room_no_json = json.dumps(room_no_list)

                if room_id:
                    if not is_new_hotel:
                        cu.execute(
                            """UPDATE room_types
									  SET room_type=%s, total=%s, room_no=%s, price=%s
									  WHERE id=%s""",
                            (room_type, total, room_no_json, price, room_id),
                        )
                        current_ids.append(room_id)
                        self.booking_manager.log_action(
                            "room_type_updated",
                            hotel_id=self.hotel_id,
                            message=f"Updated room type '{room_type}' for hotel {self.hotel_id}",
                        )
                else:
                    cu.execute(
                        """INSERT INTO room_types
								  (hotel_id, room_type, total, room_no, price)
								  VALUES (%s,%s,%s,%s,%s)""",
                        (self.hotel_id, room_type, total, room_no_json, price),
                    )
                    new_id = cu.lastrowid
                    current_ids.append(new_id)
                    self.booking_manager.log_action(
                        "room_type_added",
                        hotel_id=self.hotel_id,
                        message=f"Added room type '{room_type}' (ID {new_id}) for hotel {self.hotel_id}",
                    )

            if not is_new_hotel:
                to_delete = set(existing_ids) - set(current_ids)
                for rid in to_delete:
                    cu.execute("DELETE FROM room_types WHERE id=%s", (rid,))
                    self.booking_manager.log_action(
                        "room_type_deleted",
                        hotel_id=self.hotel_id,
                        message=f"Deleted room type ID {rid} for hotel {self.hotel_id}",
                    )

            conn.commit()
            cu.close()
            conn.close()

            parent = self.parent()
            if parent and hasattr(parent, "refresh_all_tables"):
                parent.refresh_all_tables(force=True)
            MessageBoxManager.info(self, "Success", "Hotel details saved successfully.")
            self.close()

        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            error_msg = f"{str(e)}"
            MessageBoxManager.error(self, "Error", f"Failed to save data:\n{error_msg}")
            self.booking_manager.log_action(
                "hotel_save_error",
                hotel_id=getattr(self, "hotel_id", None),
                message=f"Failed to save hotel data: {error_msg}",
            )

    def on_logs_finished(self):
        self.progress.close()
        MessageBoxManager.info(self, "Success", "Hotel details saved successfully.")
        self.accept()

    def start_room_log_worker(self):
        self.progress = QProgressDialog(
            "Creating rolling room logs...", "Cancel", 0, 0, self
        )
        self.progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress.setCancelButton(None)
        self.progress.show()

        self.thread = RoomLogWorker(self.booking_manager, self.hotel_id)
        self.thread.finished.connect(self.on_logs_finished)
        self.thread.error.connect(self.on_logs_error)
        self.thread.start()

    def on_logs_error(self, msg):
        self.progress.close()
        MessageBoxManager.error(self, "Error", f"Failed to create room logs:\n{msg}")

    def delete_hotel(self):
        if MessageBoxManager.confirm(
            self, "Delete Hotel", "Are you sure you want to delete this hotel?"
        ):
            try:
                conn = create_connection()
                cu = conn.cursor()
                cu.execute("DELETE FROM room_types WHERE hotel_id=%s", (self.hotel_id,))
                cu.execute(
                    "DELETE FROM hotel_bookings WHERE hotel_id=%s", (self.hotel_id,)
                )
                cu.execute(
                    "DELETE FROM hotel_details WHERE hotel_id=%s", (self.hotel_id,)
                )
                conn.commit()
                cu.close()
                conn.close()
                self.booking_manager.log_action(
                    action="Hotel deletion",
                    hotel_id=self.hotel_id,
                    message="Deleted hotel and all its data",
                )
                MessageBoxManager.info(self, "Deleted", "Hotel deleted successfully.")
                self.booking_manager.log_action1(
                    f"Hotel with ID{self.hotel_id} deleted",
                    message=f"ALl data related to hotel with ID{self.hotel_id} wiped out of db",
                )
                self.accept()
                parent = self.parent()
                if parent and hasattr(parent, "refresh_all_tables"):
                    parent.refresh_all_tables(force=True)
            except Exception as e:
                MessageBoxManager.error(self, "Error", f"Failed to delete hotel: {e}")


class PasswordLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.setStyleSheet(
            """
			QLineEdit {
				border: 1px solid #ccc;
				border-radius: 6px;
				padding-left: 8px;
				padding-right: 30px;
				height: 28px;
				font-size: 14px;
			}
			QLineEdit:focus {
				border: 1px solid #2E86C1;
			}
		"""
        )
        self.eye_button = QToolButton(self)
        self.eye_button.setIcon(QIcon(EYE_OPEN_PATH))
        self.eye_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.eye_button.setStyleSheet("border: none;")
        self.eye_button.setFixedSize(20, 20)
        self.eye_button.clicked.connect(self.toggle_password)
        self.setTextMargins(0, 0, 25, 0)
        self.setUpdatesEnabled(True)
        QApplication.processEvents()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.eye_button.move(self.rect().right() - 25, (self.rect().height() - 20) // 2)

    def toggle_password(self):
        if self.echoMode() == QLineEdit.EchoMode.Password:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_button.setIcon(QIcon(EYE_CLOSE_PATH))
        else:
            self.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_button.setIcon(QIcon(EYE_OPEN_PATH))

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() in (Qt.Key.Key_C, Qt.Key.Key_V, Qt.Key.Key_X):
                event.ignore()
                return
        super().keyPressEvent(event)

    def contextMenuEvent(self, event):
        pass


class LoginDialog(RoundedDialog):
    def __init__(self, hotel_id, parent=None):
        super().__init__(parent)
        self.hotel_id = hotel_id
        self.booking_manager = BookingDataManagement()
        self.setWindowTitle("Login")
        self.setFixedSize(370, 230)
        self.bg_frame = QFrame()
        self.bg_frame.setObjectName("bg_frame")
        self.bg_frame.setStyleSheet(
            """
			QFrame#bg_frame {
				background-color: qlineargradient(
					x1:0, y1:0, x2:1, y2:1,
					stop:0 #f0f4ff, stop:1 #e6ebf7
				);
				border-radius: 14px;
				border: none;
			}
		"""
        )
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        title = QLabel("Hotel Login")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "color: #2E86C1; margin-bottom: 15px; border: none; background: transparent;"
        )
        top_layout.addWidget(title)
        close_x = QPushButton("\u00d7")
        close_x.setFixedSize(28, 28)
        close_x.setStyleSheet(
            """
			QPushButton {
				border: none;
				color: #666;
				font-size: 20px;
				font-weight: bold;
				border-radius: 14px;
				background-color: transparent;
			}
			QPushButton:hover { background-color: #EAECEE; }
		"""
        )
        close_x.clicked.connect(self.reject)
        top_layout.addWidget(close_x, alignment=Qt.AlignmentFlag.AlignTop)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet(
            """
			QLineEdit {
				border: none;
				border-radius: 8px;
				padding: 6px 10px;
				height: 32px;
				font-size: 14px;
				background-color: #ffffff;
			}
			QLineEdit:focus {
				border: none;
				background-color: #f9fcff;
			}
			QLineEdit::placeholder {
				color: #90a4ae;
				font-style: italic;
			}
		"""
        )

        self.password_input = PasswordLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setStyleSheet(self.username_input.styleSheet())

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(15)
        form.addRow("Username:", self.username_input)
        form.addRow("Password:", self.password_input)
        self.button_box = QDialogButtonBox()
        self.ok_btn = self.button_box.addButton(
            "Login", QDialogButtonBox.ButtonRole.AcceptRole
        )
        self.cancel_btn = self.button_box.addButton(
            "Cancel", QDialogButtonBox.ButtonRole.RejectRole
        )

        self.ok_btn.setStyleSheet(
            """
			QPushButton {
				background-color: #2E86C1;
				color: white;
				border-radius: 6px;
				padding: 6px 15px;
				font-weight: bold;
			}
			QPushButton:hover {
				background-color: #21618C;
			}
		"""
        )
        self.cancel_btn.setStyleSheet(
            """
			QPushButton {
				background-color: #e0e0e0;
				color: black;
				border-radius: 6px;
				padding: 6px 15px;
			}
			QPushButton:hover {
				background-color: #bdbdbd;
			}
		"""
        )

        self.button_box.accepted.connect(self.authenticate)
        self.button_box.rejected.connect(self.reject)
        inner_layout = QVBoxLayout(self.bg_frame)
        inner_layout.setContentsMargins(20, 20, 20, 20)
        inner_layout.setSpacing(10)
        inner_layout.addLayout(top_layout)
        inner_layout.addLayout(form)
        inner_layout.addWidget(self.button_box, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.addWidget(self.bg_frame)

        self.authenticated = False
        QApplication.processEvents()

    def authenticate(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username and not password:
            MessageBoxManager.warning(
                self, "Validation Error", "Username and Password cannot be empty."
            )
            self.booking_manager.log_action(
                action="login_attempt",
                hotel_id=self.hotel_id,
                message=f"Login attempt for user '{username}' failed: empty username and password",
            )
            return
        elif not username:
            MessageBoxManager.warning(
                self, "Validation Error", "Username cannot be empty."
            )
            self.booking_manager.log_action(
                action="login_attempt",
                hotel_id=self.hotel_id,
                message=f"Login attempt for user '{username}' failed: empty username",
            )
            return
        elif not password:
            MessageBoxManager.warning(
                self, "Validation Error", "Password cannot be empty."
            )
            self.booking_manager.log_action(
                action="login_attempt",
                hotel_id=self.hotel_id,
                message=f"Login attempt for user '{username}' failed: empty username",
            )
            return

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, password FROM hotel_details WHERE hotel_id=%s",
            (self.hotel_id,),
        )
        record = cursor.fetchone()
        cursor.close()
        conn.close()

        if record:
            if username == record["username"] and password == record["password"]:
                self.authenticated = True
                self.booking_manager.log_action(
                    action="login_attempt",
                    hotel_id=self.hotel_id,
                    message=f"Login successful for user '{username}'",
                )
                self.accept()
                return

        MessageBoxManager.error(self, "Login Failed", "Invalid username or password.")
        self.booking_manager.log_action(
            action="login_attempt",
            hotel_id=self.hotel_id,
            message=f"Login attempt for user '{username}' failed: invalid credentials",
        )


class BookInitialDialog(RoundedDialog):
    def __init__(
        self,
        placeholder,
        title_obj,
        btn_text,
        parent=None,
    ):
        super().__init__(parent)
        self.title = title_obj
        self.booking_manager = BookingDataManagement()
        self.setWindowTitle(self.title)
        self.setFixedSize(370, 230)
        self.bg_frame = QFrame()
        self.bg_frame.setObjectName("bg_frame")
        self.bg_frame.setStyleSheet(
            """
			QFrame#bg_frame {
				background-color: qlineargradient(
					x1:0, y1:0, x2:1, y2:1,
					stop:0 #f0f4ff, stop:1 #e6ebf7
				);
				border-radius: 14px;
				border: none;
			}
		"""
        )
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        title = QLabel(self.title)
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "color: #2E86C1; margin-bottom: 15px; border: none; background: transparent;"
        )
        top_layout.addWidget(title)
        close_x = QPushButton("\u00d7")
        close_x.setFixedSize(28, 28)
        close_x.setStyleSheet(
            """
			QPushButton {
				border: none;
				color: #666;
				font-size: 20px;
				font-weight: bold;
				border-radius: 14px;
				background-color: transparent;
			}
			QPushButton:hover { background-color: #EAECEE; }
		"""
        )
        close_x.clicked.connect(self.reject)
        top_layout.addWidget(close_x, alignment=Qt.AlignmentFlag.AlignTop)

        self.reference = QLineEdit()
        self.reference.setPlaceholderText(placeholder)
        self.reference.setStyleSheet(
            """
			QLineEdit {
				border: none;
				border-radius: 8px;
				padding: 6px 10px;
				height: 32px;
				font-size: 14px;
				background-color: #ffffff;
			}
			QLineEdit:focus {
				border: none;
				background-color: #f9fcff;
			}
			QLineEdit::placeholder {
				color: #90a4ae;
				font-style: italic;
			}
		"""
        )

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(15)
        form.addRow(self.reference)
        self.button_box = QDialogButtonBox()
        self.ok_btn = self.button_box.addButton(
            btn_text, QDialogButtonBox.ButtonRole.AcceptRole
        )
        self.reference.returnPressed.connect(self.ok_btn.click)

        if btn_text == "Check":
            self.button_box.accepted.connect(self.check)
            self.ok_btn.setStyleSheet(
                """
						QPushButton {
							background-color: #2E86C1;
							color: white;
							border-radius: 6px;
							padding: 6px 15px;
							font-weight: bold;
						}
						QPushButton:hover {
							background-color: #21618C;
						}
					"""
            )
        else:
            self.button_box.accepted.connect(self.delete_book)
            self.ok_btn.setStyleSheet(
                """
									QPushButton {
										background-color: #FF0000;
										color: white;
										border-radius: 6px;
										padding: 6px 15px;
										font-weight: bold;
									}
									QPushButton:hover {
										background-color: #FF8080
									}
								"""
            )
        self.button_box.rejected.connect(self.reject)
        inner_layout = QVBoxLayout(self.bg_frame)
        inner_layout.setContentsMargins(20, 20, 20, 20)
        inner_layout.setSpacing(10)
        inner_layout.addLayout(top_layout)
        inner_layout.addLayout(form)
        inner_layout.addWidget(self.button_box, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(5, 5, 5, 5)
        outer_layout.addWidget(self.bg_frame)
        QApplication.processEvents()

    def delete_book(self):
        if MessageBoxManager.confirm(
            None, "Cancel Booking", "Are you sure you want to cancel this booking?"
        ):
            conn = create_connection()
            cu = conn.cursor()
            cu.execute(
                "SELECT 1 FROM hotel_bookings WHERE name=%s OR booking_id=%s",
                (self.reference.text(), self.reference.text()),
            )
            BookingDataManagement.log_action1(
                "Accessed table 'hotel_bookings'", "Validated name or booking_id"
            )
            result = cu.fetchall()
            if result == ():
                MessageBoxManager.info(None, "Error 404", "Booking Not Found")
            else:
                cu.execute(
                    "DELETE FROM hotel_bookings WHERE name=%s OR booking_id=%s",
                    (self.reference.text(), self.reference.text()),
                )
                BookingDataManagement.log_action1(
                    "Accessed table 'hotel_bookings'",
                    f"Deleted booking with name or booking_id={self.reference.text()}",
                )
                MessageBoxManager.success(
                    None, "Canceled Booking", "Booking cancelled successfully!"
                )
                conn.commit()
                cu.close()
                conn.close()

    def check(self):
        conn = create_connection()
        cu = conn.cursor()
        cu.execute(
            "SELECT 1 FROM hotel_bookings WHERE (name=%s OR booking_id=%s) AND date_to >= (CURDATE() - INTERVAL 1 DAY)",
            (self.reference.text(), self.reference.text()),
        )
        result = cu.fetchall()
        BookingDataManagement.log_action1(
            "Accessed table 'hotel_bookings'", "Validated name or booking_id"
        )
        if result == ():
            MessageBoxManager.info(None, "Error 404", "Booking Not Found")
        else:
            cu.execute(
                "SELECT * FROM hotel_bookings WHERE name=%s OR booking_id=%s",
                (self.reference.text(), self.reference.text()),
            )
            booking_data = cu.fetchone()
            BookingDataManagement().log_action(
                action="Accessed customer details",
                hotel_id=booking_data["hotel_id"],
                booking_id=booking_data["booking_id"],
                message="Accessed customer details for generating invoice",
            )
            days = (booking_data["date_to"] - booking_data["date_from"]).days
            booked_rooms, total_amount = self.extract_booking_details(
                booking_data, days
            )
            self.show_success_dialog(
                booked_rooms,
                total_amount,
                booking_data["name"],
                booking_data["phone"],
                booking_data["email"],
                booking_data["aadhar"],
                booking_data["date_from"],
                booking_data["date_to"],
                booking_data,
            )
            self.close_popup()
            cu.close()
            conn.close()

    @staticmethod
    def get_room_nos_by_booking_id(booking_id: str):

        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            query = "SELECT room_no FROM hotel_bookings WHERE booking_id = %s"
            cursor.execute(query, (booking_id.strip().upper(),))
            results = cursor.fetchall()

            data = [row["room_no"] for row in results] if results else []
            if data and isinstance(data[0], str):
                rooms = json.loads(data[0])
                result = ", ".join(rooms)
            else:
                result = ""
            return result

        except Exception as e:
            MessageBoxManager.warning(
                None,
                "Room No Error",
                f"Error fetching room numbers for booking_id {booking_id}: {e}",
            )
            return []

        finally:
            conn.close()

    def generate_invoice(
        self,
        booked_rooms,
        total_amount,
        name,
        phone,
        email,
        aadhar,
        booked_from,
        booked_to,
        booking_data,
    ):
        conn = create_connection()
        cu = conn.cursor()
        cu.execute(
            "SELECT * FROM hotel_details WHERE hotel_id=%s", (booking_data["hotel_id"],)
        )
        result = cu.fetchone()
        BookingDataManagement().log_action(
            action="Data access",
            hotel_id=result["hotel_id"],
            booking_id=booking_data["booking_id"],
            message="Accessed hotel details for invoice generation",
        )
        room_n = self.booking_manager.get_room_nos_by_booking_id(
            booking_data["booking_id"]
        )
        invoice = BookingInvoice(
            hotel_name=result["hotel_name"],
            hotel_address=result["place"],
            room_no=room_n,
            customer_name=name,
            customer_aadhar=aadhar,
            customer_phone=phone,
            booked_from=booked_from,
            booked_to=booked_to,
            customer_email=email,
            rooms=booked_rooms,
            total_amount=total_amount,
            booking_id=booking_data["booking_id"],
            app_name="EasyStay",
            app_logo_path=HOTEL_IMAGE_PATH,
        )
        MessageBoxManager.info(
            self,
            "Invoice Generated",
            f"Booking successful! Invoice saved as <b>{booking_data["booking_id"]}.pdf</b> at\n <b>{invoice.pdf_path}</b>",
        )

    def show_success_dialog(
        self,
        booked_rooms,
        total_amount,
        name,
        phone,
        email,
        aadhar,
        booked_from,
        booked_to,
        booking_data,
    ):

        dialog = RoundedDialog(self)
        dialog.setWindowTitle("Booking Found!")
        dialog.resize(460, 350)

        outer_layout = QVBoxLayout(dialog)
        outer_layout.setContentsMargins(10, 10, 10, 10)

        container = QDialog()
        container.setStyleSheet(
            """
			QDialog {
				background-color: #ffffff;
				border-radius: 20px;
			}
		"""
        )

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 80))
        container.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        close_x = QPushButton("\u00d7")
        close_x.setFixedSize(28, 28)
        close_x.setStyleSheet(
            """
			QPushButton {
				border: none;
				color: #666;
				font-size: 20px;
				font-weight: bold;
				border-radius: 14px;
				background-color: transparent;
			}
			QPushButton:hover { background-color: #EAECEE; }
		"""
        )
        close_x.clicked.connect(lambda: [dialog.reject(), self.close()])
        main_layout.addWidget(close_x, alignment=Qt.AlignmentFlag.AlignRight)

        success_icon = QLabel("\u2705")
        success_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        success_icon.setStyleSheet("font-size: 50px;")
        main_layout.addWidget(success_icon)

        title_label = QLabel("<b>Booking Found!</b>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; color:#2E86C1;")
        main_layout.addWidget(title_label)

        summary_frame = QFrame()
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setSpacing(5)
        summary_layout.addWidget(QLabel(f"<b>Name:</b> {name}"))
        summary_layout.addWidget(QLabel(f"<b>Phone:</b> {phone}"))
        summary_layout.addWidget(QLabel(f"<b>Email:</b> {email}"))
        summary_layout.addWidget(QLabel(f"<b>Aadhar No:</b> {aadhar}"))
        summary_layout.addWidget(
            QLabel(f"<b>From:</b> {booked_from.strftime("%Y-%m-%d")}")
        )
        summary_layout.addWidget(QLabel(f"<b>To:</b> {booked_to.strftime("%Y-%m-%d")}"))
        summary_layout.addWidget(
            QLabel(f"<b>Total Amount:</b> \u20b9{total_amount:,.2f}")
        )

        summary_frame.setStyleSheet(
            """
			QFrame {
				border-radius: 14px;
				padding: 12px;
				background: qlineargradient(
					spread:pad, x1:0, y1:0, x2:1, y2:1,
					stop:0 #E0F7FA, stop:1 #B2EBF2
				);
			}
			QLabel {
				font-size: 14px;
				padding: 2px;
			}
		"""
        )
        main_layout.addWidget(summary_frame)

        button_layout = QHBoxLayout()
        invoice_btn = QPushButton("Download Invoice")
        invoice_btn.setStyleSheet(
            """
			QPushButton {
				background-color: #28B463; color: white; font-weight: bold;
				padding: 8px 20px; border-radius: 8px;
			}
			QPushButton:hover { background-color: #1D8348; }
		"""
        )

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(
            """
			QPushButton {
				background-color: #E5E7E9; color: black; font-weight: bold;
				padding: 8px 20px; border-radius: 8px;
			}
			QPushButton:hover { background-color: #D5D8DC; }
		"""
        )

        def handle_close():
            dialog.accept()
            self.close()

        def handle_invoice():
            self.generate_invoice(
                booked_rooms,
                total_amount,
                name,
                phone,
                email,
                aadhar,
                booked_from,
                booked_to,
                booking_data,
            )
            dialog.accept()
            self.close()

        close_btn.clicked.connect(handle_close)
        invoice_btn.clicked.connect(handle_invoice)

        button_layout.addStretch()
        button_layout.addWidget(invoice_btn)
        button_layout.addWidget(close_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        outer_layout.addWidget(container)
        dialog.exec()

    @staticmethod
    def extract_booking_details(booking, days):
        room_type_ids = booking["room_type_id"].split(",")
        booked_rooms = []
        total_amount = 0

        conn = create_connection()
        cu = conn.cursor()

        for rt_id in set(room_type_ids):
            qty = room_type_ids.count(rt_id)

            cu.execute("SELECT room_type, price FROM room_types WHERE id=%s", (rt_id,))
            row = cu.fetchone()
            if not row:
                continue
            booked_rooms.append(
                {"room_type": row["room_type"], "price": row["price"], "quantity": qty}
            )

            total_amount += row["price"] * qty * days

        return booked_rooms, total_amount

    def close_popup(self):
        self.reject()


class BookingForm(RoundedDialog):
    proceed_to_payment = pyqtSignal(
        object, float, str, str, str, str, QDate, QDate, int
    )
    payment_success = pyqtSignal(object, float, str, str, str, str, QDate, QDate)

    def __init__(self, hotel_id):
        super().__init__()
        self.hotel_id = hotel_id
        self.setWindowTitle("Booking Page")
        self.resize(700, 600)
        self.room_booking_widgets = []
        self.booking_id = None

        self.setStyleSheet(
            """
			QDialog {
				background: qlineargradient(
					x1:0, y1:0, x2:1, y2:1,
					stop:0 #f0f4ff,
					stop:1 #e6ebf7
				);
				border-radius: 20px;
			}
		"""
        )

        self.booking_manager = BookingDataManagement()

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(15, 15, 15, 15)

        container = QWidget()
        container.setStyleSheet(
            """
			QWidget {
				background-color: #ffffff;
				border-radius: 20px;
			}
		"""
        )
        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 80))
        container.setGraphicsEffect(shadow)
        outer_layout.addWidget(container)

        self.container_layout = QVBoxLayout(container)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container_layout.setSpacing(15)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(scroll_bar())

        self.container_layout.addWidget(scroll)

        content_widget = QWidget()
        scroll.setWidget(content_widget)
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_layout.setSpacing(15)

        title_label = QLabel("Booking Form")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: 600; color: #1F4E79;")
        self.content_layout.addWidget(title_label)

        close_x = QPushButton("\u00d7")
        close_x.setFixedSize(28, 28)
        close_x.setStyleSheet(
            """
			QPushButton {
				border: none;
				color: #666;
				font-size: 20px;
				font-weight: bold;
				border-radius: 14px;
				background-color: transparent;
			}
			QPushButton:hover { background-color: #EAECEE; }
		"""
        )

        close_x.clicked.connect(self.reject)

        self.container_layout.insertWidget(
            0, close_x, alignment=Qt.AlignmentFlag.AlignRight
        )

        self.hotel_group = QGroupBox("Hotel Information")
        self.hotel_group.setStyleSheet(self._groupbox_style())
        hotel_layout = QGridLayout()
        hotel_layout.setVerticalSpacing(8)
        hotel_layout.setHorizontalSpacing(15)

        self.hotel_label = QLabel("")
        self.place_label = QLabel("")
        self.pin_code_label = QLabel("")
        self.contact_label = QLabel("")
        self.check_in = QLabel("")
        self.check_out = QLabel("")

        for lbl in [
            self.hotel_label,
            self.place_label,
            self.pin_code_label,
            self.contact_label,
            self.check_in,
            self.check_out,
        ]:
            lbl.setStyleSheet("font-size:14px;")

        hotel_layout.addWidget(
            QLabel("Hotel Name:"), 0, 0, alignment=Qt.AlignmentFlag.AlignRight
        )
        hotel_layout.addWidget(
            self.hotel_label, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft
        )
        hotel_layout.addWidget(
            QLabel("Check-in:"), 0, 2, alignment=Qt.AlignmentFlag.AlignRight
        )
        hotel_layout.addWidget(
            self.check_in, 0, 3, alignment=Qt.AlignmentFlag.AlignLeft
        )
        hotel_layout.addWidget(
            QLabel("Place:"), 1, 0, alignment=Qt.AlignmentFlag.AlignRight
        )
        hotel_layout.addWidget(
            self.place_label, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft
        )
        hotel_layout.addWidget(
            QLabel("Check-out:"), 1, 2, alignment=Qt.AlignmentFlag.AlignRight
        )
        hotel_layout.addWidget(
            self.check_out, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft
        )
        hotel_layout.addWidget(
            QLabel("Pin Code:"), 2, 0, alignment=Qt.AlignmentFlag.AlignRight
        )
        hotel_layout.addWidget(
            self.pin_code_label, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft
        )
        hotel_layout.addWidget(
            QLabel("Contact:"), 3, 0, alignment=Qt.AlignmentFlag.AlignRight
        )
        hotel_layout.addWidget(
            self.contact_label, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.hotel_group.setLayout(hotel_layout)
        self.content_layout.addWidget(self.hotel_group)

        self.room_group = QGroupBox("Room Types Available")
        self.room_group.setStyleSheet(self._groupbox_style())
        self.room_group1 = QVBoxLayout()
        self.room_group1.setSpacing(5)
        self.room_group.setLayout(self.room_group1)

        scroll_room_group = QScrollArea()
        scroll_room_group.setWidgetResizable(True)
        scroll_room_group.setWidget(self.room_group)
        scroll_room_group.setFixedHeight(100)
        scroll_room_group.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll_room_group.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll_room_group.setStyleSheet(
            """
			QScrollArea { border: none; background-color: #fdfdfd; }
		"""
        )

        self.content_layout.addWidget(scroll_room_group)

        self.booking_group = QGroupBox("Customer Booking Details")
        self.booking_group.setStyleSheet(self._groupbox_style())
        booking_layout = QFormLayout()
        booking_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        booking_layout.setVerticalSpacing(8)

        today = QDate.currentDate()
        max_date = today.addDays(80)

        self.name_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.email_input = QLineEdit()
        self.aadhar_no_input = QLineEdit()
        self.booked_from_input = QDateEdit()
        self.booked_from_input.setDisplayFormat("dd/MM/yyyy")

        self.booked_from_input.setDate(today)
        self.booked_from_input.setMinimumDate(today)
        self.booked_from_input.setMaximumDate(max_date)
        self.booked_from_input.setStyleSheet(self._line_edit_style())

        self.booked_to_input = QDateEdit()
        self.booked_to_input.setDisplayFormat("dd/MM/yyyy")

        self.booked_to_input.setDate(today.addDays(1))
        self.booked_to_input.setMinimumDate(today.addDays(1))
        self.booked_to_input.setMaximumDate(max_date)
        self.booked_to_input.setStyleSheet(self._line_edit_style())

        def update_to_date_constraints():
            from_date = self.booked_from_input.date()
            new_min = from_date.addDays(1)
            self.booked_to_input.setMinimumDate(new_min)
            if self.booked_to_input.date() < new_min:
                self.booked_to_input.setDate(new_min)

        self.booked_from_input.dateChanged.connect(update_to_date_constraints)
        self.age = QLineEdit()

        for w in [
            self.name_input,
            self.contact_input,
            self.email_input,
            self.aadhar_no_input,
            self.booked_from_input,
            self.booked_to_input,
            self.age,
        ]:
            w.setStyleSheet(self._line_edit_style())

        booking_layout.addRow("Name:", self.name_input)
        booking_layout.addRow("Phone:", self.contact_input)
        booking_layout.addRow("Email:", self.email_input)
        booking_layout.addRow("Aadhar No.:", self.aadhar_no_input)
        booking_layout.addRow("Age:", self.age)
        booking_layout.addRow("Booked From:", self.booked_from_input)
        booking_layout.addRow("Booked To:", self.booked_to_input)
        self.booking_group.setLayout(booking_layout)
        self.content_layout.addWidget(self.booking_group)

        self.room_group_avail = QGroupBox("Rooms to be Booked")
        self.room_group_avail.setStyleSheet(self._groupbox_style())
        self.rooms_layout = QFormLayout()
        self.rooms_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.rooms_layout.setVerticalSpacing(5)
        self.room_group_avail.setLayout(self.rooms_layout)

        scroll_room_group_avail = QScrollArea()
        scroll_room_group_avail.setWidgetResizable(True)
        scroll_room_group_avail.setWidget(self.room_group_avail)
        scroll_room_group_avail.setFixedHeight(110)
        scroll_room_group_avail.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll_room_group_avail.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll_room_group_avail.setStyleSheet(
            """
			QScrollArea { border: none; background-color: #fdfdfd; }
		"""
        )

        self.content_layout.addWidget(scroll_room_group_avail)

        btn_widget = QWidget()
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 20, 0, 0)
        btn_layout.setSpacing(15)

        self.save_btn = QPushButton("Make Payment")
        self.save_btn.setStyleSheet(self._primary_btn_style())
        self.save_btn.clicked.connect(self.validate)

        self.close_btn = QPushButton("Close")
        self.close_btn.setStyleSheet(self._secondary_btn_style())
        self.close_btn.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.close_btn)
        btn_layout.addStretch()
        self.content_layout.addWidget(btn_widget)

        self.load_hotel_info()
        self.load_rooms()
        self.load_room_labels()

        self.proceed_to_payment.connect(self.open_payment_dialog)
        self.payment_success.connect(self.show_success_dialog)
        self.booked_from_input.dateChanged.connect(self.on_dates_changed)
        self.booked_to_input.dateChanged.connect(self.on_dates_changed)
        self.setUpdatesEnabled(True)
        QApplication.processEvents()

    @staticmethod
    def _spinbox_style():
        return """
		QSpinBox {
			border: 1px solid #ccc;
			border-radius: 6px;
			padding: 4px 8px;
			height: 28px;
			font-size: 14px;
		}
		QSpinBox:focus {
			border: 1px solid #2E86C1;
		}
		QSpinBox::up-button, QSpinBox::down-button {
			width: 20px;
			height: 20px;
		}
	"""

    @staticmethod
    def _groupbox_style():
        return """
		QGroupBox {
			font-weight:bold;
			color: #1F4E79;
			border: 2px solid #AED6F1;
			border-radius: 12px;
			padding: 12px;
			background-color: #ffffff;
		}
	"""

    @staticmethod
    def _primary_btn_style():
        return """
		QPushButton {
			background-color: #2E86C1;
			color: white;
			font-weight: 600;
			font-size: 15px;
			border-radius: 10px;
			padding: 8px 18px;
		}
		QPushButton:hover { background-color: #1A5276; }
		QPushButton:pressed { background-color: #154360; }
	"""

    @staticmethod
    def _secondary_btn_style():
        return """
		QPushButton {
			background-color: #ccc;
			color: black;
			border-radius: 10px;
			padding: 8px 18px;
		}
		QPushButton:hover { background-color: #bbb; }
	"""

    @staticmethod
    def check_card_details(card_no_obj, card_holder_name_obj, cvv_obj, exp_obj):
        try:
            with open("card.txt", "r") as file:
                lines = file.readlines()[1:]
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) < 4:
                    continue
                card_no, holder_name, cvv, exp = parts
                if (
                    card_no.strip() == card_no_obj
                    and holder_name.strip().upper().replace(" ", "_")
                    == card_holder_name_obj
                    and cvv.strip() == cvv_obj
                    and exp.strip() == exp_obj
                ):
                    return True
        except Exception as e:
            MessageBoxManager.error("Error reading card.txt:", e)
        return False

    @staticmethod
    def _line_edit_style():
        return """
			QLineEdit, QDateEdit {
				border: 1px solid #ccc;
				border-radius: 6px;
				padding: 6px 8px;
				height:28px;
				font-size: 14px;
			}
			QLineEdit:focus, QDateEdit:focus {
				border: 1px solid #2E86C1;
				background: #FDFEFE;
			}
		"""

    def load_hotel_info(self):
        try:
            conn = create_connection()
            cu = conn.cursor()
            cu.execute(
                "SELECT * FROM hotel_details WHERE hotel_id=%s", (self.hotel_id,)
            )
            hotel = cu.fetchone()
            cu.close()
            conn.close()
            if hotel:
                self.hotel_label.setText(hotel["hotel_name"])
                self.place_label.setText(hotel["place"])
                self.pin_code_label.setText(str(hotel["pin_code"]))
                self.contact_label.setText(hotel["contact_hotel"])
                self.check_in.setText(str(hotel["check_in"]))
                self.check_out.setText(str(hotel["check_out"]))
        except Exception as e:
            MessageBoxManager.error(self, "Error", f"Failed to fetch hotel info: {e}")
        self.booking_manager.log_action(
            "load_hotel_info",
            hotel_id=self.hotel_id,
            message=f"Loaded hotel info for {self.hotel_label.text()}",
        )

    def on_dates_changed(self):
        booked_from = self.booked_from_input.date()
        booked_to = self.booked_to_input.date()

        if booked_to < booked_from:
            MessageBoxManager.warning(
                self, "Date Error", "Booked To date cannot be before Booked From date."
            )
            self.booked_to_input.setDate(booked_from)
            return

        self.load_rooms()
        self.load_room_labels()

    def load_room_labels(self):

        for i in reversed(range(self.room_group1.count())):
            item = self.room_group1.itemAt(i)
            if item:
                w = item.widget()
                if w:
                    w.setParent(None)

        booked_from = self.booked_from_input.date().toString("yyyy-MM-dd")
        booked_to = self.booked_to_input.date().toString("yyyy-MM-dd")

        try:
            rooms = self.booking_manager.get_available_rooms(
                self.hotel_id, booked_from, booked_to
            )
        except Exception as e:
            MessageBoxManager.error(self, "Error", f"Failed to fetch rooms: {e}")
            return

        try:
            conn = create_connection()
            cu = conn.cursor(pymysql.cursors.DictCursor)
            cu.execute(
                "SELECT room_type, price FROM room_types WHERE hotel_id=%s",
                (self.hotel_id,),
            )
            price_data = cu.fetchall()
            price_map = {r["room_type"]: r["price"] for r in price_data}
        except Exception as e:
            MessageBoxManager.error(self, "Error", f"Failed to fetch room prices: {e}")
            return
        finally:
            cu.close()
            conn.close()

        def get_color(remaining):
            if remaining == 0:
                return "red"
            elif remaining <= 3:
                return "orange"
            return "green"

        rooms_by_type = defaultdict(list)
        if rooms:
            for r in rooms:
                rooms_by_type[r["room_type"]].append(r)

        for room_type, price in price_map.items():
            total_available = len(rooms_by_type.get(room_type, []))
            color = get_color(total_available)

            lbl = QLabel(
                f"{room_type} | Price: \u20b9{price:.2f} | Available: {total_available}"
            )
            lbl.setStyleSheet(f"font-weight:bold; color:{color}; font-size:14px;")
            self.room_group1.addWidget(lbl)

        self.booking_manager.log_action(
            "load_rooms",
            hotel_id=self.hotel_id,
            message=f"Loaded rooms for dates {booked_from} to {booked_to}",
        )

    def load_rooms(self):
        self.room_booking_widgets.clear()

        for layout in [self.room_group1, self.rooms_layout]:
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if item:
                    w = item.widget()
                    if w:
                        w.setParent(None)

        booked_from = self.booked_from_input.date().toString("yyyy-MM-dd")
        booked_to = self.booked_to_input.date().toString("yyyy-MM-dd")

        try:
            rooms = self.booking_manager.get_available_rooms(
                self.hotel_id, booked_from, booked_to
            )
        except Exception as e:
            return

        try:

            conn = create_connection()
            cu = conn.cursor(pymysql.cursors.DictCursor)
            cu.execute(
                "SELECT room_type, id, price FROM room_types WHERE hotel_id=%s",
                (self.hotel_id,),
            )
            room_types_data = cu.fetchall()
            cu.close()
            conn.close()

            if not room_types_data:
                MessageBoxManager.info(
                    self, "Info", "No room types found for this hotel."
                )
                return

            rooms_by_type = defaultdict(list)
            if rooms:
                for r in rooms:
                    rooms_by_type[r["room_type"]].append(r)

            def get_color(remaining):
                if remaining == 0:
                    return "red"
                elif remaining <= 3:
                    return "orange"
                return "green"

            all_unavailable = True

            for rt in room_types_data:
                room_type = rt["room_type"]
                room_type_id = rt["id"]
                price = rt["price"]

                room_list = rooms_by_type.get(room_type, [])
                total_available = len(room_list)
                color = get_color(total_available)

                label = QLabel(room_type)
                label.setStyleSheet(f"font-weight:bold; color:{color}; font-size:14px;")

                spin = QSpinBox()
                spin.setStyleSheet(self._spinbox_style())
                spin.setRange(0, total_available)
                spin.setFixedWidth(60)
                spin.setEnabled(total_available > 0)

                avail_label = QLabel(f"{total_available} available")
                avail_label.setStyleSheet(f"color:{color}; font-size:13px;")

                if total_available > 0:
                    all_unavailable = False

                def make_on_spin_change(total_available_i, label_i, avail_label_i):
                    def on_spin_change(value):
                        remaining = total_available_i - value
                        color_i = get_color(remaining)
                        avail_label_i.setText(f"{remaining} available")
                        avail_label_i.setStyleSheet(f"color:{color_i}; font-size:13px;")
                        label_i.setStyleSheet(
                            f"font-weight:bold; color:{color_i}; font-size:14px;"
                        )

                    return on_spin_change

                spin.valueChanged.connect(
                    make_on_spin_change(total_available, label, avail_label)
                )

                h_layout = QHBoxLayout()
                h_layout.addWidget(label)
                h_layout.addStretch()
                h_layout.addWidget(spin)
                h_layout.addWidget(avail_label)
                container = QWidget()
                container.setLayout(h_layout)
                self.rooms_layout.addRow(container)

                self.room_booking_widgets.append(
                    {
                        "room_type": room_type,
                        "room_type_id": room_type_id,
                        "price": price,
                        "spinbox": spin,
                        "available": total_available,
                    }
                )

        except Exception as e:
            MessageBoxManager.error(
                self, "Error", f"Failed to process room availability: {e}"
            )
        self.booking_manager.log_action(
            "load_rooms",
            hotel_id=self.hotel_id,
            message=f"Loaded rooms for dates {booked_from} to {booked_to}",
        )

    def validate(self):
        name = self.name_input.text().strip()
        phone = self.contact_input.text().strip()
        email = self.email_input.text().strip()
        aadhar = self.aadhar_no_input.text().strip()
        booked_from = self.booked_from_input.date()
        booked_to = self.booked_to_input.date()
        age = self.age.text().strip()
        self.booking_manager.log_action(
            "validate_attempt",
            hotel_id=self.hotel_id,
            message=f"Validation attempted for customer {self.name_input.text()}",
        )

        if not all([name, phone, email, aadhar]):
            MessageBoxManager.warning(
                self, "Validation Error", "Please fill in all fields."
            )
            return

        if not phone.isdigit() or len(phone) != 10:
            MessageBoxManager.warning(
                self, "Validation Error", "Phone must be 10 digits."
            )
            return

        if int(age) < 18:
            MessageBoxManager.warning(
                self, "Validation Error", "Only adults can book the room."
            )
            return

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            MessageBoxManager.warning(
                self, "Validation Error", "Please enter a valid email address."
            )
            return

        if not aadhar.isdigit() or len(aadhar) != 12:
            MessageBoxManager.warning(
                self, "Validation Error", "Aadhar must be 12 digits."
            )
            return

        if booked_to < booked_from:
            MessageBoxManager.warning(
                self, "Validation Error", "Booked To cannot be before From date."
            )
            return

        booked_rooms = []
        total_amount = 0
        booked_from_str = booked_from.toString("yyyy-MM-dd")
        booked_to_str = booked_to.toString("yyyy-MM-dd")

        try:

            available_rooms_list = self.booking_manager.get_available_rooms(
                self.hotel_id, booked_from_str, booked_to_str
            )
        except Exception as e:
            MessageBoxManager.error(
                self, "Error", f"Failed to fetch available rooms: {e}"
            )
            return

        available_by_type = defaultdict(list)
        for room in available_rooms_list:
            available_by_type[room["room_type"]].append(room)

        for widget in self.room_booking_widgets:
            qty = widget["spinbox"].value()
            if qty <= 0:
                continue

            total_available = len(available_by_type.get(widget["room_type"], []))

            if qty > total_available:
                MessageBoxManager.warning(
                    self,
                    "Error",
                    f"Not enough available {widget['room_type']} rooms for selected dates! "
                    f"(Available: {total_available})",
                )
                return

            booked_rooms.append(
                {
                    "room_type": widget["room_type"],
                    "price": widget["price"],
                    "quantity": qty,
                }
            )
            total_amount += qty * widget["price"]

        if not booked_rooms:
            MessageBoxManager.warning(self, "Validation Error", "No rooms selected!")
            return

        self.booking_manager.log_action(
            "validation_success",
            hotel_id=self.hotel_id,
            message=f"Customer {self.name_input.text()} selected rooms: {booked_rooms}",
        )

        self.summary(
            booked_rooms,
            total_amount,
            name,
            phone,
            email,
            aadhar,
            booked_from,
            booked_to,
            int(age),
        )

    def summary(
        self,
        booked_rooms,
        total_amount,
        name,
        phone,
        email,
        aadhar,
        booked_from,
        booked_to,
        age,
    ):
        dialog = RoundedDialog(self)
        dialog.setWindowTitle("Booking Summary")
        dialog.resize(420, 450)

        outer_layout = QVBoxLayout(dialog)
        outer_layout.setContentsMargins(10, 10, 10, 10)

        container = QDialog()
        container.setStyleSheet(
            """
			QDialog {
				background-color: #ffffff;
				border-radius: 20px;
			}
		"""
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        container.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        title_label = QLabel("Review Booking Details")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            """
			font-size: 18px;
			font-weight: 600;
			color: #1F4E79;
		"""
        )
        main_layout.addWidget(title_label)

        customer_frame = QFrame()
        customer_layout = QVBoxLayout(customer_frame)
        customer_layout.setSpacing(5)
        customer_layout.addWidget(QLabel(f"Name: {name}"))
        customer_layout.addWidget(QLabel(f"Phone: {phone}"))
        customer_layout.addWidget(QLabel(f"Email: {email}"))
        customer_layout.addWidget(QLabel(f"Aadhar: {aadhar}"))
        customer_layout.addWidget(QLabel(f"From: {booked_from.toString('yyyy-MM-dd')}"))
        customer_layout.addWidget(QLabel(f"To: {booked_to.toString('yyyy-MM-dd')}"))

        customer_frame.setStyleSheet(
            """
			QFrame {
				border-radius: 14px;
				padding: 12px;
				background: qlineargradient(
					spread:pad, x1:0, y1:0, x2:1, y2:1, 
					stop:0 #E0F7FA, stop:1 #B2EBF2
				);
			}
		"""
        )
        main_layout.addWidget(customer_frame)

        rooms_frame = QFrame()
        rooms_layout = QVBoxLayout(rooms_frame)
        rooms_layout.setSpacing(5)
        days = booked_from.daysTo(booked_to)
        for room in booked_rooms:
            rooms_layout.addWidget(
                QLabel(f"{room['room_type']}: {room['quantity']}x {days} days")
            )
        total_amount = total_amount * days

        rooms_frame.setStyleSheet(
            """
			QFrame {
				border-radius: 14px;
				padding: 12px;
				background: qlineargradient(
					spread:pad, x1:0, y1:0, x2:1, y2:1, 
					stop:0 #FFF3E0, stop:1 #FFE0B2
				);
			}
		"""
        )
        main_layout.addWidget(rooms_frame)

        total_label = QLabel(f"Total Payable: \u20b9{total_amount:,.2f}")
        total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_label.setStyleSheet(
            """
			font-size: 16px;
			font-weight: bold;
			color: #0E6655;
			padding: 5px;
		"""
        )
        main_layout.addWidget(total_label)

        button_layout = QHBoxLayout()
        btn_make_payment = QPushButton("Proceed to Payment")
        btn_edit_details = QPushButton("Edit Details")
        btn_make_payment.setFixedHeight(36)
        btn_make_payment.setStyleSheet(
            """
			QPushButton {
				background-color: #2E86C1;
				color: white;
				font-weight: 600;
				font-size: 14px;
				border-radius: 10px;
				padding: 6px 14px;
			}
			QPushButton:hover { background-color: #1A5276; }
			QPushButton:pressed { background-color: #154360; }
		"""
        )
        btn_edit_details.setFixedHeight(36)
        btn_edit_details.setStyleSheet(
            """
			QPushButton {
				background-color: #EAECEE;
				color: #1F4E79;
				font-weight: 600;
				font-size: 14px;
				border-radius: 10px;
				padding: 6px 14px; 
			}
			QPushButton:hover { background-color: #D5DBDB; }
		"""
        )

        button_layout.addStretch()
        button_layout.addWidget(btn_make_payment)
        button_layout.addSpacing(15)
        button_layout.addWidget(btn_edit_details)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        def handle_make_payment():
            dialog.accept()
            self.booking_manager.log_action(
                "proceed_to_payment",
                hotel_id=self.hotel_id,
                message=f"Customer {name} proceeding to payment, total: \u20b9{total_amount:.2f}",
            )

            self.proceed_to_payment.emit(
                booked_rooms,
                total_amount,
                name,
                phone,
                email,
                aadhar,
                booked_from,
                booked_to,
                age,
            )

        btn_make_payment.clicked.connect(handle_make_payment)
        btn_edit_details.clicked.connect(dialog.reject)

        close_btn = QPushButton("\u00d7")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet(
            """
			QPushButton {
				border: none;
				color: #666;
				font-size: 20px;
				font-weight: bold;
				border-radius: 14px;
				background-color: transparent;
			}
			QPushButton:hover { background-color: #EAECEE; }
		"""
        )
        close_btn.clicked.connect(dialog.reject)
        main_layout.insertWidget(0, close_btn, alignment=Qt.AlignmentFlag.AlignRight)

        outer_layout.addWidget(container)
        dialog.exec()

    def open_payment_dialog(
        self,
        booked_rooms,
        total_amount,
        name,
        phone,
        email,
        aadhar,
        booked_from,
        booked_to,
        age,
    ):
        dialog = RoundedDialog(self)
        dialog.setWindowTitle("Payment Portal")
        dialog.resize(420, 430)

        outer_layout = QVBoxLayout(dialog)
        outer_layout.setContentsMargins(10, 10, 10, 10)

        container = QDialog()
        container.setStyleSheet(
            """
		QDialog {
			background-color: #ffffff;
			border-radius: 20px;
		}
	"""
        )

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 80))
        container.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        title_label = QLabel("Complete Your Payment")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            """
		font-size: 18px;
		font-weight: 600;
		color: #1F4E79;
	"""
        )
        main_layout.addWidget(title_label)

        total_label = QLabel(f"Total Amount: \u20b9{total_amount:,.2f}")
        total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_label.setStyleSheet(
            """
		font-size: 16px;
		font-weight: bold;
		color: #0E6655;
		padding: 5px;
	"""
        )
        main_layout.addWidget(total_label)

        card_group = QGroupBox("Card Details")
        card_group.setStyleSheet(
            """
		QGroupBox {
			font-weight: bold;
			color: #1F4E79;
			border: 2px solid #AED6F1;
			border-radius: 10px;
			margin-top: 15px;
			background-color: #ffffff;
		}
		QGroupBox:title {
			subcontrol-origin: margin;
			subcontrol-position: top center;
			padding: 0 8px;
		}
	"""
        )

        form_layout = QFormLayout(card_group)
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        name_input = QLineEdit()
        name_input.setPlaceholderText("John Doe")
        name_input.setStyleSheet(
            """
		QLineEdit {
			border: 1px solid #ccc;
			border-radius: 6px;
			padding: 6px 8px;
		}
		QLineEdit:focus {
			border: 1px solid #2E86C1;
			background: #FDFEFE;
		}
	"""
        )
        form_layout.addRow("Cardholder Name:", name_input)

        card_input = QLineEdit()
        card_input.setMaxLength(19)
        card_input.setPlaceholderText("1234 5678 9012 3456")
        card_input.setStyleSheet(
            """
		QLineEdit {
			border: 1px solid #ccc;
			border-radius: 6px;
			padding: 6px 8px;
			font-family: Consolas, monospace;
		}
		QLineEdit:focus {
			border: 1px solid #2E86C1;
		}
	"""
        )
        self.booking_manager.log_action(
            action="payment_initiated",
            hotel_id=self.hotel_id,
            message=f"Payment initiated for {name}, total_amount=\u20b9{total_amount:,.2f}",
        )

        def format_card_number(text):
            digits_only = text.replace(" ", "")
            new_text = " ".join(
                [digits_only[i : i + 4] for i in range(0, len(digits_only), 4)]
            )
            card_input.blockSignals(True)
            card_input.setText(new_text)
            card_input.blockSignals(False)
            card_input.setCursorPosition(len(new_text))

        card_input.textChanged.connect(format_card_number)
        form_layout.addRow("Card Number:", card_input)

        cvv_exp_layout = QHBoxLayout()
        cvv_input = QLineEdit()
        cvv_input.setMaxLength(3)
        cvv_input.setEchoMode(QLineEdit.EchoMode.Password)
        cvv_input.setPlaceholderText("123")
        cvv_input.setFixedWidth(80)
        cvv_input.setStyleSheet(
            """
		QLineEdit {
			border: 1px solid #ccc;
			border-radius: 6px;
			padding: 6px;
			text-align: center;
		}
		QLineEdit:focus {
			border: 1px solid #2E86C1;
		}
	"""
        )

        expiry_input = QDateEdit()
        expiry_input.setDisplayFormat("MM/yyyy")
        expiry_input.setDate(QDate.currentDate())
        expiry_input.setStyleSheet(self._line_edit_style())

        cvv_exp_layout.addWidget(QLabel("CVV:"))
        cvv_exp_layout.addWidget(cvv_input)
        cvv_exp_layout.addSpacing(20)
        cvv_exp_layout.addWidget(QLabel("Expiry:"))
        cvv_exp_layout.addWidget(expiry_input)
        form_layout.addRow(cvv_exp_layout)

        main_layout.addWidget(card_group)

        error_label = QLabel("")
        error_label.setStyleSheet("color:red; font-weight:bold;")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(error_label)

        pay_btn = QPushButton("Pay Now")
        pay_btn.setFixedHeight(40)
        pay_btn.setStyleSheet(
            """
		QPushButton {
			background-color: #2E86C1;
			color: white;
			font-weight: 600;
			font-size: 15px;
			border-radius: 10px;
			padding: 8px 18px;
		}
		QPushButton:hover {
			background-color: #1A5276;
		}
		QPushButton:pressed {
			background-color: #154360;
		}
	"""
        )
        main_layout.addWidget(pay_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        close_btn = QPushButton("\u00d7")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet(
            """
		QPushButton {
			border: none;
			color: #666;
			font-size: 20px;
			font-weight: bold;
			border-radius: 14px;
			background-color: transparent;
		}
		QPushButton:hover {
			background-color: #EAECEE;
		}
	"""
        )
        close_btn.clicked.connect(dialog.reject)
        main_layout.insertWidget(0, close_btn, alignment=Qt.AlignmentFlag.AlignRight)

        def process_payment():
            cardholder = name_input.text().strip().upper().replace(" ", "_")
            card_number = card_input.text().replace(" ", "")
            cvv = cvv_input.text().strip()
            exp = expiry_input.date().toString("MM/yyyy")

            if not cardholder or not card_number or not cvv:
                error_label.setText("All fields are required!")
                return
            if len(card_number) != 16 or not card_number.isdigit():
                error_label.setText("Invalid card number.")
                return
            if len(cvv) != 3 or not cvv.isdigit():
                error_label.setText("Invalid CVV.")
                return
            if not self.check_card_details(card_number, cardholder, cvv, exp):
                error_label.setText("Card details not found!")

                return

            dialog.accept()
            self.booking_manager.log_action(
                "payment_success",
                hotel_id=self.hotel_id,
                booking_id=self.booking_id,
                message=f"Payment successful for {name}, amount: \u20b9{total_amount:.2f}",
            )

            self.save_booking_to_db(
                total_amount, name, phone, email, aadhar, booked_from, booked_to, age
            )
            self.payment_success.emit(
                booked_rooms,
                total_amount,
                name,
                phone,
                email,
                aadhar,
                booked_from,
                booked_to,
            )

        pay_btn.clicked.connect(process_payment)

        outer_layout.addWidget(container)
        dialog.exec()

    def save_booking_to_db(
        self, total_amount, name, phone, email, aadhar, booked_from, booked_to, age
    ):
        try:
            rooms_with_id = []
            for widget in self.room_booking_widgets:
                qty = widget["spinbox"].value()
                if qty <= 0:
                    continue

                rooms_with_id.append(
                    {
                        "room_type": widget["room_type"],
                        "room_type_id": widget["room_type_id"],
                        "price": widget["price"],
                        "quantity": qty,
                    }
                )

            booking = {
                "hotel_id": int(self.hotel_id),
                "name": name,
                "room_type": rooms_with_id,
                "date_from": booked_from,
                "date_to": booked_to,
                "phone": int(phone),
                "aadhar": int(aadhar),
                "total_amount": float(total_amount),
                "age": age,
                "email": email,
            }

            self.booking_id = self.booking_manager.add_or_update_booking(booking)
            self.booking_manager.log_action(
                action="booking_saved",
                hotel_id=self.hotel_id,
                booking_id=self.booking_id,
                message=f"Booking saved to DB for {name}",
            )
            return True

        except Exception as e:
            MessageBoxManager.error(self, "Error", f"Error saving booking:\n{str(e)}")
            return False

    def show_success_dialog(
        self,
        booked_rooms,
        total_amount,
        name,
        phone,
        email,
        aadhar,
        booked_from,
        booked_to,
    ):

        dialog = RoundedDialog(self)
        dialog.setWindowTitle("Booking Successful")
        dialog.resize(460, 350)

        outer_layout = QVBoxLayout(dialog)
        outer_layout.setContentsMargins(10, 10, 10, 10)

        container = QDialog()
        container.setStyleSheet(
            """
			QDialog {
				background-color: #ffffff;
				border-radius: 20px;
			}
		"""
        )

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 80))
        container.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        close_x = QPushButton("\u00d7")
        close_x.setFixedSize(28, 28)
        close_x.setStyleSheet(
            """
			QPushButton {
				border: none;
				color: #666;
				font-size: 20px;
				font-weight: bold;
				border-radius: 14px;
				background-color: transparent;
			}
			QPushButton:hover { background-color: #EAECEE; }
		"""
        )
        close_x.clicked.connect(lambda: [dialog.reject(), self.close()])
        main_layout.addWidget(close_x, alignment=Qt.AlignmentFlag.AlignRight)

        success_icon = QLabel("\u2705")
        success_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        success_icon.setStyleSheet("font-size: 50px;")
        main_layout.addWidget(success_icon)

        title_label = QLabel("<b>Booking Successful!</b>")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; color:#2E86C1;")
        main_layout.addWidget(title_label)

        summary_frame = QFrame()
        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setSpacing(5)
        summary_layout.addWidget(QLabel(f"<b>Name:</b> {name}"))
        summary_layout.addWidget(QLabel(f"<b>Phone:</b> {phone}"))
        summary_layout.addWidget(QLabel(f"<b>Email:</b> {email}"))
        summary_layout.addWidget(QLabel(f"<b>Aadhar No:</b> {aadhar}"))
        summary_layout.addWidget(
            QLabel(f"<b>From:</b> {booked_from.toString('dd/MM/yyyy')}")
        )
        summary_layout.addWidget(
            QLabel(f"<b>To:</b> {booked_to.toString('dd/MM/yyyy')}")
        )
        summary_layout.addWidget(
            QLabel(f"<b>Total Amount:</b> \u20b9{total_amount:,.2f}")
        )
        self.booking_manager.log_action(
            action="booking_success",
            hotel_id=self.hotel_id,
            booking_id=self.booking_id,
            message=f"Booking successful for {name}, total_amount=\u20b9{total_amount:,.2f}",
        )

        summary_frame.setStyleSheet(
            """
			QFrame {
				border-radius: 14px;
				padding: 12px;
				background: qlineargradient(
					spread:pad, x1:0, y1:0, x2:1, y2:1,
					stop:0 #E0F7FA, stop:1 #B2EBF2
				);
			}
			QLabel {
				font-size: 14px;
				padding: 2px;
			}
		"""
        )
        main_layout.addWidget(summary_frame)

        button_layout = QHBoxLayout()
        invoice_btn = QPushButton("Download Invoice")
        invoice_btn.setStyleSheet(
            """
			QPushButton {
				background-color: #28B463; color: white; font-weight: bold;
				padding: 8px 20px; border-radius: 8px;
			}
			QPushButton:hover { background-color: #1D8348; }
		"""
        )

        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(
            """
			QPushButton {
				background-color: #E5E7E9; color: black; font-weight: bold;
				padding: 8px 20px; border-radius: 8px;
			}
			QPushButton:hover { background-color: #D5D8DC; }
		"""
        )

        def handle_close():
            dialog.accept()
            self.close()

        def handle_invoice():
            self.generate_invoice(
                booked_rooms,
                total_amount,
                name,
                phone,
                email,
                aadhar,
                booked_from,
                booked_to,
            )
            dialog.accept()
            self.close()

        close_btn.clicked.connect(handle_close)
        invoice_btn.clicked.connect(handle_invoice)

        button_layout.addStretch()
        button_layout.addWidget(invoice_btn)
        button_layout.addWidget(close_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        outer_layout.addWidget(container)
        dialog.exec()

    def generate_invoice(
        self,
        booked_rooms,
        total_amount,
        name,
        phone,
        email,
        aadhar,
        booked_from,
        booked_to,
    ):
        room_n = self.booking_manager.get_room_nos_by_booking_id(self.booking_id)
        invoice = BookingInvoice(
            hotel_name=self.hotel_label.text(),
            hotel_address=self.place_label.text(),
            room_no=room_n,
            customer_name=name,
            customer_aadhar=aadhar,
            customer_phone=phone,
            booked_from=booked_from,
            booked_to=booked_to,
            customer_email=email,
            rooms=booked_rooms,
            total_amount=total_amount,
            booking_id=self.booking_id,
            app_name="EasyStay",
            app_logo_path=HOTEL_IMAGE_PATH,
        )
        MessageBoxManager.info(
            self,
            "Invoice Generated",
            f"Booking successful! Invoice saved as <b>{self.booking_id}.pdf</b> at\n <b>{invoice.pdf_path}</b>",
        )
        self.booking_manager.log_action(
            "invoice_generated",
            hotel_id=self.hotel_id,
            booking_id=self.booking_id,
            message=f"Invoice generated for {name}, total: \u20b9{total_amount:.2f}",
        )


class BookingDataManagement:
    def __init__(self):
        self._setup_logging_table()

    def cleanup_old_bookings(self):
        conn = cur = None
        try:
            conn = create_connection()
            cur = conn.cursor()

            delete_query = """
					DELETE FROM hotel_bookings
					WHERE date_to < NOW() - INTERVAL 1 MONTH;
				"""
            cur.execute(delete_query)
            affected = cur.rowcount
            conn.commit()

            MessageBoxManager.success(
                None,
                f"Deletion successful: [{datetime.now()}] ",
                f"Deleted {affected} old bookings (>1 month).",
            )

            self.log_action1("monthly_cleanup", f"Deleted {affected} old bookings")

        except Exception as e:
            MessageBoxManager.warning(None, f"Cleanup error: [{datetime.now()}] ", e)
            self.log_action1("cleanup_error", str(e))
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def schedule_monthly_cleanup(self):

        def job():
            today = datetime.now()
            if today.day == 1:
                self.cleanup_old_bookings()

        schedule.every().day.at("02:00").do(job)

        t = threading.Thread(target=self._run_scheduler, daemon=True)
        t.start()

    @staticmethod
    def _run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)

    def get_management_data(self):
        conn = cur = None
        try:
            conn = create_connection()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(
                """
				SELECT * FROM hotel_details
				ORDER BY hotel_id ASC
			"""
            )
            data = cur.fetchall()

            self.log_action1(
                action="management_data_loaded", message=f"Loaded {len(data)} hotels"
            )

            return data
        except Exception as e:
            MessageBoxManager.error(None, "Management Data Error", str(e))
            self.log_action1("management_data_error", message=str(e))
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def _setup_logging_table_for_hotel(hotel_id):
        conn = cur = None
        try:
            conn = create_connection()
            cur = conn.cursor()
            table_name = f"booking_logs_{hotel_id}"
            cur.execute(
                f"""
					CREATE TABLE IF NOT EXISTS `{table_name}` (
						log_id INT AUTO_INCREMENT PRIMARY KEY,
						log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
						action VARCHAR(50),
						booking_id VARCHAR(15),
						message TEXT
					)
				"""
            )
            conn.commit()
        except Exception as e:
            MessageBoxManager.error(
                None, f"Hotel {hotel_id} Log Error", f"Error setting up log table: {e}"
            )
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def _setup_logging_table():
        conn = cur = None
        try:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(
                """
					CREATE TABLE IF NOT EXISTS logs (
						log_id INT AUTO_INCREMENT PRIMARY KEY,
						log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
						action VARCHAR(50),
						message TEXT
					)
				"""
            )
            conn.commit()
        except Exception as e:
            MessageBoxManager.error(
                None, f"Log Error", f"Error setting up log table: {e}"
            )
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def log_action(self, action, hotel_id=None, booking_id=None, message=None):
        if not hotel_id:
            MessageBoxManager.error(None, "Error", "Hotel ID required for logging")
            return

        class LogRunnable(QRunnable):
            def run(inner_self):
                self._setup_logging_table_for_hotel(hotel_id)
                conn = cur = None
                try:
                    conn = create_connection()
                    cur = conn.cursor()
                    table_name = f"booking_logs_{hotel_id}"
                    cur.execute(
                        f"""
						INSERT INTO `{table_name}` (action, booking_id, message)
						VALUES (%s, %s, %s)
					""",
                        (action, booking_id, message),
                    )
                    message1 = f"Accessed db for {message}"
                    cur.execute(
                        """
						INSERT INTO logs (action, message)
						VALUES (%s, %s)
					""",
                        (action, message),
                    )
                    conn.commit()
                except Exception as e:
                    MessageBoxManager.error(
                        None, f"Logging Failed for Hotel {hotel_id}", str(e)
                    )
                finally:
                    if cur:
                        cur.close()
                    if conn:
                        conn.close()

        QThreadPool.globalInstance().start(LogRunnable())

    def log_action1(self, action, message=None):
        class LogRunnable1(QRunnable):
            def run(inner_self):
                conn = cur = None
                try:
                    conn = create_connection()
                    cur = conn.cursor()
                    cur.execute(
                        """
						INSERT INTO logs (action, message)
						VALUES (%s, %s)
					""",
                        (action, message),
                    )
                    conn.commit()
                except Exception as e:
                    MessageBoxManager.error(None, "Logging Failed", str(e))
                finally:
                    if cur:
                        cur.close()
                    if conn:
                        conn.close()

        QThreadPool.globalInstance().start(LogRunnable1())

    def add_or_update_booking(self, booking_data):
        conn = cur = None
        try:
            conn = create_connection()
            cur = conn.cursor()

            hotel_id = int(booking_data["hotel_id"])

            booked_from_str = (
                booking_data["date_from"].toString("yyyy-MM-dd")
                if isinstance(booking_data["date_from"], QDate)
                else str(booking_data["date_from"])
            )
            booked_to_str = (
                booking_data["date_to"].toString("yyyy-MM-dd")
                if isinstance(booking_data["date_to"], QDate)
                else str(booking_data["date_to"])
            )

            cur.execute(
                "SELECT COUNT(*)+1 AS next_no FROM hotel_bookings WHERE hotel_id=%s",
                (hotel_id,),
            )
            next_no = cur.fetchone()["next_no"]
            booking_id_def = f"BK{hotel_id:02d}{next_no:04d}"
            booking_data["booking_id"] = booking_id_def

            available_rooms = self.get_available_rooms(
                hotel_id, booked_from_str, booked_to_str
            )
            final_assigned_rooms = []
            room_type_ids = []

            for rt in booking_data["room_type"]:
                room_type_id = rt["room_type_id"]
                quantity = rt.get("quantity", 1)

                candidates = [
                    r for r in available_rooms if r["room_type_id"] == room_type_id
                ]
                if len(candidates) < quantity:
                    conn.rollback()
                    self.log_action(
                        "booking_failed",
                        hotel_id,
                        booking_id_def,
                        f"Not enough rooms available for RoomType ID {room_type_id}",
                    )
                    return False

                selected = candidates[:quantity]
                for s in selected:
                    final_assigned_rooms.append(s["room_no"])
                    room_type_ids.append(room_type_id)

            if not final_assigned_rooms:
                MessageBoxManager.warning(self, "Error", "No rooms selected!")
                return False

            cur.execute(
                """
				INSERT INTO hotel_bookings
				(booking_id, hotel_id, name, room_no, room_type_id, date_from, date_to, phone, aadhar, age, email)
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
			""",
                (
                    booking_id_def,
                    hotel_id,
                    booking_data["name"],
                    json.dumps(final_assigned_rooms),
                    ",".join(str(rt_id) for rt_id in room_type_ids),
                    booked_from_str,
                    booked_to_str,
                    booking_data.get("phone"),
                    booking_data.get("aadhar"),
                    booking_data.get("age"),
                    booking_data.get("email"),
                ),
            )

            conn.commit()
            self.log_action(
                "booking_added",
                hotel_id,
                booking_id_def,
                f"Rooms booked: {final_assigned_rooms}",
            )
            return booking_id_def

        except Exception as e:
            if conn:
                conn.rollback()
            MessageBoxManager.warning(None, "Error", "No rooms selected!")
            self.log_action("booking_error", hotel_id, None, f"{e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def delete_booking(self, booking_id_def):
        conn = cur = None
        try:
            conn = create_connection()
            cur = conn.cursor(pymysql.cursors.DictCursor)

            cur.execute(
                """
				SELECT hotel_id, room_no, room_type, date_from, date_to
				FROM hotel_bookings
				WHERE booking_id=%s
			""",
                (booking_id_def,),
            )
            booking = cur.fetchone()
            if not booking:
                self.log_action(
                    "delete_failed", None, booking_id_def, "Booking not found"
                )
                return False

            cur.execute(
                "DELETE FROM hotel_bookings WHERE booking_id=%s", (booking_id_def,)
            )
            conn.commit()

            self.log_action(
                "booking_deleted",
                booking["hotel_id"],
                booking_id_def,
                f"Deleted booking from {booking['date_from']} to {booking['date_to']}",
            )
            return True

        except Exception as e:
            if conn:
                conn.rollback()
            MessageBoxManager.warning(None, "Delete Failed", "Booking not found")
            self.log_action("delete_error", None, booking_id_def, str(e))
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get_available_rooms(self, hotel_id, date_from, date_to):
        conn = cur = None
        try:
            conn = create_connection()
            cur = conn.cursor(pymysql.cursors.DictCursor)

            cur.execute(
                """
				SELECT id AS room_type_id, room_type, room_no, price
				FROM room_types
				WHERE hotel_id = %s
			""",
                (hotel_id,),
            )
            room_data = cur.fetchall()

            cur.execute(
                """
				SELECT room_type_id, room_no
				FROM hotel_bookings
				WHERE hotel_id = %s
				  AND (date_from < %s AND date_to > %s)
			""",
                (hotel_id, date_to, date_from),
            )
            booked_data = cur.fetchall()

            booked_map = {}
            for row in booked_data:
                rt_ids = [r.strip() for r in str(row["room_type_id"]).split(",")]

                try:
                    room_nos = (
                        json.loads(row["room_no"])
                        if str(row["room_no"]).startswith("[")
                        else str(row["room_no"]).split(",")
                    )
                except Exception:
                    room_nos = str(row["room_no"]).split(",")

                for rt in rt_ids:
                    booked_map.setdefault(rt, set()).update(r.strip() for r in room_nos)

            available_rooms = []
            for row in room_data:
                rt_id = str(row["room_type_id"])
                rt_price = row["price"]

                try:
                    all_rooms = (
                        json.loads(row["room_no"])
                        if str(row["room_no"]).startswith("[")
                        else str(row["room_no"]).split(",")
                    )
                except Exception:
                    all_rooms = str(row["room_no"]).split(",")

                booked_rooms = booked_map.get(rt_id, set())
                for rn in all_rooms:
                    rn = rn.strip()
                    if rn not in booked_rooms:
                        available_rooms.append(
                            {
                                "room_no": rn,
                                "room_type_id": int(rt_id),
                                "room_type": row["room_type"],
                                "price": rt_price,
                            }
                        )

            if not available_rooms:
                MessageBoxManager.warning(
                    None, "No Rooms", f"No rooms available for {date_from} to {date_to}"
                )

            return available_rooms

        except Exception as e:
            MessageBoxManager.error(None, "Availability Error", str(e))
            self.log_action("availability_error", hotel_id, None, str(e))
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def get_room_nos_by_booking_id(booking_id: str):

        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            query = "SELECT room_no FROM hotel_bookings WHERE booking_id = %s"
            cursor.execute(query, (booking_id.strip().upper(),))
            results = cursor.fetchall()

            data = [row["room_no"] for row in results] if results else []
            if data and isinstance(data[0], str):
                rooms = json.loads(data[0])
                result = ", ".join(rooms)
            else:
                result = ""
            return result

        except Exception as e:
            MessageBoxManager.warning(
                None,
                "Room No Error",
                f"Error fetching room numbers for booking_id {booking_id}: {e}",
            )
            return []

        finally:
            conn.close()


class MessageBoxManager(RoundedDialog):
    ICONS = {
        "error": QStyle.StandardPixmap.SP_MessageBoxCritical,
        "info": QStyle.StandardPixmap.SP_MessageBoxInformation,
        "warning": QStyle.StandardPixmap.SP_MessageBoxWarning,
        "success": QStyle.StandardPixmap.SP_DialogApplyButton,
    }

    COLORS = {
        "error": {"border": "#b71c1c", "text": "#b71c1c", "button": "#b71c1c"},
        "info": {"border": "#1565c0", "text": "#0d47a1", "button": "#1565c0"},
        "warning": {"border": "#ef6c00", "text": "#e65100", "button": "#ef6c00"},
        "success": {"border": "#2e7d32", "text": "#1b5e20", "button": "#2e7d32"},
    }

    def __init__(self, parent=None, title="Message", message="", msg_type="info"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setModal(True)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.setStyleSheet(
            """
			background-color: #ffffff;
			border-radius: 15px;  
		"""
        )
        self.setMinimumWidth(400)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        container = QWidget()
        container.setStyleSheet(
            """
			background-color: #ffffff;
			border-radius: 15px;
		"""
        )
        main_layout.addWidget(container)

        content_layout = QVBoxLayout(container)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(15)
        icon_text_layout = QHBoxLayout()
        icon_text_layout.setSpacing(15)

        icon_label = QLabel()
        icon_label.setFixedSize(32, 32)
        pixmap = self.style().standardPixmap(
            self.ICONS.get(msg_type, QStyle.StandardPixmap.SP_MessageBoxInformation)
        )
        icon_label.setPixmap(
            pixmap.scaled(
                32,
                32,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        icon_text_layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"""
			font-size: 18px;
			font-weight: 600;
			color: {self.COLORS[msg_type]['text']};
		"""
        )
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet(
            """
			font-size: 15px;
			color: #333333;
			line-height: 1.4;
		"""
        )

        text_layout.addWidget(title_label)
        text_layout.addWidget(message_label)

        icon_text_layout.addLayout(text_layout)
        content_layout.addLayout(icon_text_layout)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(28)
        ok_btn.setStyleSheet(
            f"""
			QPushButton {{
				background-color: {self.COLORS[msg_type]['button']};
				color: white;
				font-weight: bold;
				border-radius: 6px;
				padding: 4px 12px;
			}}
			QPushButton:hover {{
				background-color: {self._hover_color(self.COLORS[msg_type]['button'])};
			}}
		"""
        )
        ok_btn.clicked.connect(self._close_dialog)
        btn_layout.addWidget(ok_btn)
        content_layout.addLayout(btn_layout)

    def _close_dialog(self):
        self.done(QDialog.DialogCode.Accepted)
        self.close()

    @staticmethod
    def _hover_color(hex_color):
        c = QColor(hex_color)
        c = c.lighter(120)
        return c.name()

    @staticmethod
    def info(parent, title, message):
        MessageBoxManager(parent, title, message, "info").exec()

    @staticmethod
    def error(parent, title, message):
        MessageBoxManager(parent, title, message, "error").exec()

    @staticmethod
    def warning(parent, title, message):
        MessageBoxManager(parent, title, message, "warning").exec()

    @staticmethod
    def success(parent, title, message):
        MessageBoxManager(parent, title, message, "success").exec()

    @staticmethod
    def confirm(parent, title="Confirm", message="Are you sure?"):
        dialog = MessageBoxManager(parent, title, message, "warning")

        # Remove built-in buttons
        for btn in dialog.findChildren(QPushButton):
            btn.hide()

        # --- Create Yes/No buttons ---
        yes_btn = QPushButton("Yes")
        yes_btn.setFixedHeight(28)
        yes_btn.setStyleSheet(
            f"""
			QPushButton {{
				background-color: {dialog.COLORS['warning']['button']};
				color: white;
				font-weight: bold;
				border-radius: 6px;
				padding: 4px 12px;
			}}
			QPushButton:hover {{
				background-color: {dialog._hover_color(dialog.COLORS['warning']['button'])};
			}}
		"""
        )
        yes_btn.clicked.connect(lambda: dialog.done(QDialog.DialogCode.Accepted))

        no_btn = QPushButton("No")
        no_btn.setFixedHeight(28)
        no_btn.setStyleSheet(
            """
			QPushButton {
				background-color: #ccc;
				color: #333;
				font-weight: bold;
				border-radius: 6px;
				padding: 4px 12px;
			}
			QPushButton:hover {
				background-color: #bbb;
			}
		"""
        )
        no_btn.clicked.connect(lambda: dialog.done(QDialog.DialogCode.Rejected))

        # --- Button layout ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(yes_btn)
        btn_layout.addWidget(no_btn)

        # --- Insert inside content widget ---
        main_layout = dialog.layout()

        # The content is usually the first widget inside main_layout
        content_widget = main_layout.itemAt(0).widget()
        content_layout = content_widget.layout()

        content_layout.addSpacing(10)
        content_layout.addLayout(btn_layout)

        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted


class BookingInvoice:
    def __init__(
        self,
        hotel_name,
        hotel_address,
        room_no,
        customer_name,
        customer_aadhar,
        customer_phone,
        booked_from,
        booked_to,
        customer_email,
        rooms,
        total_amount,
        app_name,
        app_logo_path,
        booking_id,
    ):
        self.hotel_name = hotel_name
        self.hotel_address = hotel_address
        self.room_no = room_no
        self.customer_name = customer_name
        self.customer_aadhar = customer_aadhar
        self.customer_phone = customer_phone
        self.booked_from = self.to_pydate(booked_from)
        self.booked_to = self.to_pydate(booked_to)
        self.customer_email = customer_email
        self.rooms = rooms
        self.total_amount = total_amount
        self.app_name = app_name
        self.app_logo_path = app_logo_path
        self.booking_id = booking_id

        self.downloads_folder = pathlib.Path.home() / "Downloads"
        self.pdf_path = self.get_unique_filename()

        self.styles = getSampleStyleSheet()

        conn = create_connection()
        cu = conn.cursor()
        cu.execute(
            "SELECT hotel_id, contact_hotel, check_in, check_out FROM hotel_details WHERE hotel_name=%s",
            (self.hotel_name,),
        )
        self.result_obj = cu.fetchone()
        cu.close()
        conn.close()
        BookingDataManagement().log_action(
            "Accessed Info",
            hotel_id=self.result_obj["hotel_id"],
            booking_id=self.booking_id,
            message="Accessed hotel details for invoice generation",
        )
        self.build_invoice()

    def get_unique_filename(self):
        base = self.downloads_folder / f"{self.booking_id}.pdf"
        if not base.exists():
            return base

        counter = 1
        while True:
            new_path = self.downloads_folder / f"{self.booking_id} ({counter}).pdf"
            if not new_path.exists():
                return new_path
            counter += 1

    def to_pydate(self, value):
        if hasattr(value, "toPyDate"):  # QDate
            return value.toPyDate()
        if hasattr(value, "date"):  # datetime -> date
            return value.date()
        return value  # already a date

    def build_invoice(self):
        doc = SimpleDocTemplate(
            str(self.pdf_path),
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=60,
            bottomMargin=40,
        )

        story = []

        if self.app_logo_path:
            try:
                logo = Image(self.app_logo_path, width=1 * inch, height=1 * inch)
                logo.hAlign = "LEFT"
                story.append(logo)
            except Exception:
                pass

        story.append(
            Paragraph(
                "<para align='center'><font size=22 color='#2E86C1'><b>Booking Invoice</b></font></para>",
                self.styles["Title"],
            )
        )
        story.append(Spacer(1, 10))

        story.append(
            Paragraph(
                "<font size=14 color='#1F4E79'><b>Hotel Details</b></font>",
                self.styles["Heading3"],
            )
        )

        hotel_place = self.hotel_address
        hotel_phone = self.result_obj["contact_hotel"]

        hotel_details_table = Table(
            [
                [Paragraph(f"<b>Name:</b> {self.hotel_name}", self.styles["Normal"])],
                [Paragraph(f"<b>Place:</b> {hotel_place}", self.styles["Normal"])],
                [Paragraph(f"<b>Phone:</b> {hotel_phone}", self.styles["Normal"])],
            ],
            colWidths=[430],
        )

        hotel_details_table.setStyle(
            TableStyle(
                [
                    ("LEFTPADDING", (0, 0), (-1, -1), 20),
                ]
            )
        )

        story.append(hotel_details_table)

        story.append(Spacer(1, 10))
        story.append(
            Paragraph(
                "<font size=14 color='#1F4E79'><b>Booking Details</b></font>",
                self.styles["Heading3"],
            )
        )
        story.append(Spacer(1, 5))

        check_in, check_out = self.result_obj["check_in"], self.result_obj["check_out"]

        booking_table_data = [
            ["Booking No:", self.booking_id],
            ["Generated On:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Check In Time:", str(check_in)],
            ["Check Out Time:", str(check_out)],
        ]

        booking_table = Table(
            booking_table_data,
            colWidths=[140, 310],
        )

        booking_table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 1, colors.grey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONT", (0, 0), (-1, -1), "Helvetica"),
                    ("FONT", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.darkblue),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )

        story.append(booking_table)
        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<font size=14 color='#1F4E79'><b>Customer Details</b></font>",
                self.styles["Heading3"],
            )
        )

        customer_info = [
            [Paragraph(f"<b>Name:</b> {self.customer_name}", self.styles["Normal"])],
            [
                Paragraph(
                    f"<b>Aadhar:</b> {self.customer_aadhar}", self.styles["Normal"]
                )
            ],
            [Paragraph(f"<b>Phone:</b> {self.customer_phone}", self.styles["Normal"])],
            [Paragraph(f"<b>Email:</b> {self.customer_email}", self.styles["Normal"])],
            [
                Paragraph(
                    f"<b>Booking Period:</b> {self.booked_from.strftime('%d-%m-%Y')} → {self.booked_to.strftime('%d-%m-%Y')}",
                    self.styles["Normal"],
                )
            ],
        ]

        customer_table = Table(customer_info, colWidths=[450])
        customer_table.setStyle(
            TableStyle(
                [
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(customer_table)
        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "<font size=14 color='#1F4E79'><b>Room Details</b></font>",
                self.styles["Heading3"],
            )
        )
        story.append(Paragraph(f"Room No: {self.room_no}", self.styles["Normal"]))
        story.append(Spacer(1, 10))

        days = (self.booked_to - self.booked_from).days
        table_data = [["Room Type", "Qty", "Duration", "Price/Room", "Total"]]

        for room in self.rooms:
            total_price = room["quantity"] * room["price"] * days
            table_data.append(
                [
                    room["room_type"],
                    str(room["quantity"]),
                    str(days),
                    f"{room['price']:.2f} INR",
                    f"{total_price:.2f} INR",
                ]
            )

        table = Table(table_data, colWidths=[150, 50, 70, 80])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("BOX", (0, 0), (-1, -1), 1, colors.black),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 20))

        total_table = Table(
            [["Grand Total", f"{self.total_amount:.2f} INR"]],
            colWidths=[350, 90],
        )
        total_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("BOX", (0, 0), (-1, -1), 1, colors.white),
                    ("FONT", (0, 0), (0, 0), "Helvetica-Bold"),
                    ("TEXTCOLOR", (0, 0), (0, 0), colors.darkred),
                    ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ]
            )
        )
        story.append(total_table)
        story.append(Spacer(1, 30))

        story.append(
            Paragraph(
                "<para align='center'><font color='#7D3C98'><i>Thank you for your booking!</i></font></para>",
                self.styles["Italic"],
            )
        )

        doc.build(
            story,
            onFirstPage=self.add_page_number,
            onLaterPages=self.add_page_number,
        )

    def add_page_number(self, canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Oblique", 8)
        canvas.drawCentredString(A4[0] / 2.0, 15, f"Page {doc.page}")
        canvas.restoreState()


if __name__ == "__main__":
    try:
        setup_database()
    except ModuleNotFoundError as e:
        print("Module not found", e.name)
    BookingDataManagement().schedule_monthly_cleanup()
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec())
