import PyQt5.QtWidgets as qt
import sys

if __name__ == '__main__':
    
    app = qt.QApplication(sys.argv)

    w = qt.QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    qt.QStylePainter
    
    sys.exit(app.exec_())