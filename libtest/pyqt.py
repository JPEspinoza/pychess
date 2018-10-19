import sys
import PyQt5.QtWidgets as qtw

if __name__ == '__main__':
    
    app = qtw.QApplication(sys.argv)

    w = qtw.QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
    sys.exit(app.exec_())