from PyQt6.QtCore import QAbstractTableModel, Qt

class TableModel(QAbstractTableModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.rows = 5
        self.cols = 10
        self.matriz = [[0 for i in range(self.cols)] for j in range(self.rows)]

    def rowCount(self, parent):
        return self.rows

    def columnCount(self, parent):
        return self.cols

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.matriz[index.row()][index.column()]

    def setData(self, index, value, role):
        self.matriz[index.row()][index.column()] = value
        print(f"{index.row()}, {index.column()}: {role}")
        self.dataChanged.emit(index, index)
        return True

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEditable

