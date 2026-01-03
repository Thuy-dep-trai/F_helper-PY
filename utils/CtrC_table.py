
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,QTableView
)
from PySide6.QtGui import QKeySequence,QShortcut
import sys

def copy_from_active_table():
    focus_widget = QApplication.focusWidget()
    # Chỉ thao tác nếu widget đang focus là QTableView
    if isinstance(focus_widget, QTableView):
        indexes = focus_widget.selectionModel().selectedIndexes()
        if not indexes:
            return

        # Gom dữ liệu theo hàng
        data = {}
        for idx in indexes:
            row, col = idx.row(), idx.column()
            text = idx.data()  # lấy text từ model
            data.setdefault(row, {})[col] = text

        # Sắp xếp và tạo chuỗi
        lines = []
        for row in sorted(data):
            cols = sorted(data[row])
            line = "\t".join(data[row][c] for c in cols)
            lines.append(line)

        QApplication.clipboard().setText("\n".join(lines))

    else:
        # Không phải table đang focus
        return