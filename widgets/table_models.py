from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from typing import List, Any, Dict

class GenericTableModel(QAbstractTableModel):
    """
    Model genérico para lidar com grandes listas de dicionários ou Pydantic Models.
    Permite renderização rápida no QTableView (Lazy Loading via Qt).
    """
    def __init__(self, data: List[Dict[str, Any]], headers: List[str], keys: List[str], parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = headers
        self._keys = keys

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            
            item = self._data[row]
            key = self._keys[col]
            value = item.get(key, "")
            
            # Formatação base
            if isinstance(value, float):
                if "valor" in key or "caucao" in key:
                    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                return f"{value:.2f}"
            
            if isinstance(value, str) and "data" in key.lower():
                try:
                    # Se vier como string datetime ISO, converte (simplificado)
                    return value[:10]
                except:
                    pass
                    
            return str(value) if value is not None else "-"
            
        elif role == Qt.TextAlignmentRole:
            key = self._keys[index.column()]
            if "valor" in key or "km" in key:
                return int(Qt.AlignRight | Qt.AlignVCenter)
            return int(Qt.AlignLeft | Qt.AlignVCenter)

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None

    def update_data(self, new_data: List[Dict[str, Any]]):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

    def get_item(self, row: int) -> Dict[str, Any]:
        if 0 <= row < len(self._data):
            return self._data[row]
        return {}
