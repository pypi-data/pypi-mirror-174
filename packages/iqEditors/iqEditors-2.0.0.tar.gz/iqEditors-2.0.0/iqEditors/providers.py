import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets
import logging
from pathlib import Path
from iqEditors.styles import formStyle, editorStyle


class HelpLayerProvider(QtWidgets.QDialog):
    """ окно справки на основе информационного слоя iQMemo и оно ничего не возвращает"""
    def setViewerStyle(self, style):
        self.text1.setStyleSheet(style)
        self.text2.setStyleSheet(style)
        self.text3.setStyleSheet(style)

    def __init__(self,parent=None, **kwargs):
        class Viewer(QtWidgets.QTextEdit):
            def __init__(self, parent):
                super().__init__(parent)

            def mousePressEvent(self, e):
                super().mousePressEvent(e)  # выполнились действия в родителе (стандарт)
                # дообработка клика по ссылке
                self.anchor = self.anchorAt(e.pos())
                if self.anchor:
                    QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)

            def mouseReleaseEvent(self, e):
                super().mouseReleaseEvent(e)
                # дообработка клика по ссылке
                if self.anchor:
                    QDesktopServices.openUrl(QUrl(self.anchor))
                    QApplication.setOverrideCursor(Qt.ArrowCursor)
                    self.anchor = None

        class HelpFile:
            """ файл справки"""
            # который обычный слой, созданный в этой же программе
            def __init__(self, parent, file):
                if Path(file).exists():
                    try:
                        with open(file,'r') as f:
                            d = json.load(f)
                        parent.text1.setHtml(d["panel1"])
                        parent.text2.setHtml(d["panel2"])
                        parent.text3.setHtml(d["panel3"])
                    except Exception:
                        logging.error('файл справки поврежден!')
                        QtWidgets.QMessageBox.about(parent, 'Ошибка!', "Файл справки поврежден! Обратитесь к руководству по устранению проблем.")
                else:
                    logging.error('файл справки отсутсвует')
                    QtWidgets.QMessageBox.about(parent, 'Ошибка!', "Файл справки отсутствует, хотя только что был - чудишь, пользователь 8-))).")

        def set_Attr(obj):
            """ установка атрибутов вьюверов """
            #obj.setStyleSheet(editorStyle)
            obj.setTabStopWidth(20)
            obj.setReadOnly(True)
            obj.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            obj.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            pass

        QtWidgets.QDialog.__init__(self, parent)
        hk = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)
        # закрыть окно по ескейпу
        hk.activated.connect(self.close)
        self.setWindowTitle("iQMemo: Справочная система")
        self.setStyleSheet(formStyle)
        self.layer = QtWidgets.QHBoxLayout(self)
        self.text1 = Viewer(self)
        self.text2 = Viewer(self)
        self.text3 = Viewer(self)
        set_Attr(self.text1)
        set_Attr(self.text2)
        set_Attr(self.text3)
        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.addWidget(self.text1)
        self.splitter.addWidget(self.text2)
        self.splitter.addWidget(self.text3)
        self.splitter.setSizes([2000,1200,1000]) # 2:1:1, я так мыслю
        self.layer.addWidget(self.splitter)
        self.helpFile = HelpFile(self,kwargs['helpFile'])
        self.showFullScreen()

class HelpBookProvider(QtWidgets.QDialog):
    """ окно справки на основе книги iQNote и оно теже ничего не возвращает"""
    # появится позже
    pass

if __name__ == "__main__":
    logging.info("тест классов")
    app = QtWidgets.QApplication(sys.argv)
    window = HelpLayerProvider(helpFile='')
    window.setViewerStyle(editorStyle)
    window.show()
    app.exec_()