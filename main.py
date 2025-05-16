from PyQt5 import QtWidgets
from gui import LibraryGUI
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    gui = LibraryGUI()
    gui.show()
    sys.exit(app.exec_())