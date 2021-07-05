import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtWidgets import QMainWindow, QFileDialog, QRubberBand, QLabel
from PySide2.QtGui import QPixmap
import signal



class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()
        self.getfiles()

    def initUI(self):
        self.imagebox = QLabel(self)
        self.imagebox.move (50, 100)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('mark date')
        self.setCentralWidget(self.imagebox)
        self.show()
        self.setMouseTracking(True)
        self.rubberband = QRubberBand(QRubberBand.Rectangle, self.imagebox)

    def done(self):
        self.loadfile()

    def loadfile(self):
        if len(self.filelist) > 0:
            self.fname = self.filelist.pop()
            pixmap = QPixmap(self.fname)
            self.imagebox.setPixmap(pixmap)
            self.resize(pixmap.width(), pixmap.height())
            self.imgHeight = pixmap.height()
            self.imgWidth = pixmap.width()
        else:
            sys.exit()

    def getfiles(self):
        caption = 'Open file'
        # use current/working directory
        directory = './'
        filter_mask = "Image files (*.jpg *.png)"

        self.filelist = QFileDialog.getOpenFileNames(None, caption, directory, filter_mask)[0]
        self.loadfile()

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberband.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()) )
        self.rubberband.show()

    def mouseMoveEvent(self, event):
        if self.rubberband.isVisible():
            #Control the Rubber within the imageViewer!!!
            self.rubberband.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized() & self.imagebox.rect())

    def outputResult(self, geom):

        print("UNASSIGNED, {}, {}, {}, {},,, {}, {},,".format(
            self.fname, 
            label, 
            geom.x() / self.imgWidth, 
            geom.y() / self.imgHeight, 
            (geom.x() + geom.width()) / self.imgWidth, 
            (geom.y() + geom.height()) / self.imgHeight
            ))

        self.loadfile()

    def mouseReleaseEvent(self, event):
        if self.rubberband.isVisible():
            self.rubberband.hide()
            rect = self.rubberband.geometry()
            self.outputResult(rect)


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    label = sys.argv[1]
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    run()
