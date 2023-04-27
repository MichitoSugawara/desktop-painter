import sys,os

from dotenv import load_dotenv

from PyQt5.QtWidgets import (
    QApplication, QColorDialog, QDesktopWidget, 
    QGridLayout, QMainWindow, QLabel, 
    QFrame, QWidget,
)

from PyQt5.QtGui import (
    QColor, QCursor, QFont,
    QPainter, QPixmap, QIcon
)

from PyQt5.QtCore import (
    QPoint, QRect, QSize, 
    QTimer, Qt,
)

from keyboard import (
    is_pressed
)

# envファイルを読み込む
load_dotenv()

# スクリーン情報取得
def getScreenGeomtry():
    pos = QCursor().pos()
    qdt = QDesktopWidget()
    for i in range(qdt.screenCount()):
        sgm = qdt.screen(i).geometry()
        bwX = pos.x() >= sgm.left() and pos.x() <= sgm.right()
        bwY = pos.y() >= sgm.top() and pos.y() <= sgm.bottom()
        if bwX and bwY:
            return sgm
    return QRect(0,0,0,0)
        

# QWidget系に追加したいmethod用
class myQWidget():

    # QWidgetのstyleSheetを変更するための
    def changeStyleSheet(self: QWidget, property: str, value: str):
        ss = "".join(self.styleSheet().split())
        p1 = ss.find(property+":")
        if p1 == 0 or ss[p1-1] == ";":
            p2 = ss.find(":", p1)
            p3 = ss.find(";", p2)
            ss = ss[:p2+1] + value + ss[p3:]
        else:
            ss = ss + property+":"+value+";"
        self.setStyleSheet(ss)

    # cursor位置とmappingを一緒にして上にあればTrue
    def isCursorOnMe(self: QWidget):
        gm = self.geometry()
        pos = self.mapFromGlobal(QCursor.pos())
        bwX = (pos.x() >= 0) and (pos.x() <= gm.width())
        bwY = (pos.y() >= 0) and (pos.y() <= gm.height())
        if bwX and bwY:
            return True
        else:
            return False

    def setPosition(self, point: QPoint):
        gm = self.geometry()
        self.setGeometry(point.x(), point.y(), gm.width(), gm.height())


# メニュー用のクラス
class dpMenuFrame(QFrame, myQWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.prevFocusLabel = (0, 0)
        self.isVertical = True
        self.myPositionPercent = (80,20)
        self.initLayout()

    # 基本レイアウトとラベル定義
    def initLayout(self):
        self.setLayout(QGridLayout())
        self.layout().setAlignment(Qt.AlignCenter)
        self.labelList = [
            self.dpLabel(self, "…", 30),
            self.dpLabel(self, "✖", 30, "rgba(255,0,0,200)"),
            self.dpLabel(self, "筆", 30),
            self.dpLabel(self, "色", 30),
            self.dpLabel(self, "消", 30),
        ]
        for w in self.labelList:
            self.layout().addWidget(w)
        self.adjustSize()
        self.setStyleSheet(
            f"background-color:rgba(0,0,0,100);border-radius:{min(self.width(),self.height())/2.5}px;")

    def getFocusLabel(self):
        for c in self.findChildren(self.dpLabel):
            if c.isCursorOnMe():
                self.prevFocusLabel = (c, self.prevFocusLabel[0])
                return c
        self.prevFocusLabel = (0, self.prevFocusLabel[0])
        return 0

    def togleLayout(self):
        for w in self.labelList:
            self.layout().removeWidget(w)
        for i in range(len(self.labelList)):
            if self.isVertical:
                self.layout().addWidget(self.labelList[i], 0, i)
            else:
                self.layout().addWidget(self.labelList[i], i, 0)
        self.isVertical = not self.isVertical
        self.adjustSize()

    def setHorizontalLayout(self):
        self.isVertical = False
        for w in self.labelList:
            self.layout().removeWidget(w)
        for i in range(len(self.labelList)):
            self.layout().addWidget(self.labelList[i], 0, i)
        self.adjustSize()
    
    def setPositionPercent(self, x_percent:int,y_percent:int):
        parent = self.parent()
        self.setGeometry(
            int(parent.width()*(x_percent/100)),
            int(parent.height()*(y_percent/100)),
            self.width(),self.height()
            )
        self.myPositionPercent = (x_percent,y_percent)

    # dpmenu用のlabel
    class dpLabel(QLabel, myQWidget):
        def __init__(self, parent: QWidget = None, text: str = "text", size: int = 30, textColor: str = "rgba(255,255,255,200)"):
            super().__init__(parent)
            self.setAlignment(Qt.AlignCenter)
            self.setText(text)
            self.setFontSize(size)
            self.adjustSize()
            self.setStyleSheet(f"""
            color : {textColor};
            background-color : rgba(0,0,0,50);
            border-radius : {int(size/2.5)}px;
            """)

        def setFontSize(self, size: int = 20):
            f = QFont()
            f.setPixelSize(size)
            self.setFont(f)

# canvas用クラス
class dpCanvas(QLabel,myQWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.canvasColor = QColor(255, 255, 255, 0)
        self.setGeometry(0, 0, parent.width(), parent.height())
        self.setCanvas(self.size(), self.canvasColor)

    def setCanvas(self, size: QSize, color: QColor = QColor(255, 255, 255, 0)):
        self.setGeometry(0, 0, size.width(), size.height())
        self.setPixmap(QPixmap(size.width(), size.height()))
        self.pixmap().fill(color)

    def drawLine(self, start: QPoint, end: QPoint, width: int = 5, color: QColor = QColor(0, 0, 0)):
        painter = QPainter(self.pixmap())
        pen = painter.pen()
        pen.setWidth(width)
        pen.setColor(color)
        painter.setPen(pen)
        painter.drawLine(start.x(), start.y(), end.x(), end.y())
        painter.end()
        self.update()

# 非アクティブ透過ウィンドウクラス
class myMainWindow(QMainWindow):
    def __init__(self):
        super(myMainWindow, self).__init__()
        self.setWindowTitle(os.getenv("WINDOW_TITLE"))
        self.setWindowIcon(QIcon(os.getenv("ICON_PATH")))
        self.setGeometry(-500, -300, 500, 300)
        self.setAttribute(Qt.WA_TranslucentBackground)#背景透過
        self.setAttribute(Qt.WA_ShowWithoutActivating)#アクティブなしで表示
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint#初期フレームなし,常に最前面
        |Qt.WindowTransparentForInput|Qt.WindowDoesNotAcceptFocus)#入力すり抜け,フォーカス拒否

    def closeEvent(self, _) -> None:
        sys.exit()


# アプリケーションメインクラス
class myApp(QApplication):
    def __init__(self):
        super(myApp, self).__init__(sys.argv)

        self.setWindowIcon(QIcon(os.getenv("ICON_PATH")))
        self.targetScreenGeometry = QRect(0,0,0,0)
        self.actionKey = (False, False)
        self.pushedLabel = 0

        self.prevCursorPos = QCursor().pos()
        self.isPenActive = False
        self.penColor = QColor(255, 255, 255)

        self.dpTimer = QTimer(self)
        self.dpTimer.timeout.connect(self.mainloop)
        self.dpTimer.setInterval(10)

        self.dpWindow = myMainWindow()
        self.canvas = dpCanvas(self.dpWindow)
        self.dpMenu = dpMenuFrame(self.dpWindow)


        self.isVisible = True

        self.mainloop()
        self.exec_()

    def mainloop(self):
        # サイズ更新
        sgm = getScreenGeomtry()
        if sgm != self.targetScreenGeometry:
            self.dpWindow.setGeometry(sgm)
            self.canvas.setCanvas(sgm.size())
            self.dpMenu.setPositionPercent(self.dpMenu.myPositionPercent[0],self.dpMenu.myPositionPercent[1])
            self.targetScreenGeometry = sgm

        # キー情報 actionKey[0] - 押しているか？   actionKey[1] - 直後か？
        if self.actionKey[1] == True:
            self.actionKey = (self.actionKey[0], False)
        if(is_pressed("ctrl") and not self.actionKey[0]):
            self.actionKey = (True, True)
        elif(not is_pressed("ctrl") and self.actionKey[0]):
            self.actionKey = (False, True)

        # 表示扱いで非表示なら表示　または　逆
        if self.isVisible and not self.dpWindow.isVisible():
            self.dpWindow.show()
        elif not self.isVisible and self.dpWindow.isVisible():
            self.dpWindow.hide()

        # dplabel更新
        self.dpMenu.getFocusLabel()
        flp = self.dpMenu.prevFocusLabel
        if flp[0] != flp[1]:
            if flp[0] != 0:
                flp[0].changeStyleSheet("background-color", "rgba(0,100,100,100)")
            if flp[1] != 0:
                flp[1].changeStyleSheet("background-color", "rgba(0,0,0,50)")

        if self.actionKey == (True, True):  # キーを押したとき
            if flp[0] != 0:
                None
            else:
                None

            self.pushedLabel = flp[0]
        elif self.actionKey == (False, True):  # キーを離したとき
            if flp[0] != 0:   #　dpLabelなら
                if self.pushedLabel == self.dpMenu.labelList[0] and flp[0] == self.dpMenu.labelList[0]:
                    self.dpMenu.togleLayout()
                if self.pushedLabel == self.dpMenu.labelList[1] and flp[0] == self.dpMenu.labelList[1]:
                    sys.exit()
                if self.pushedLabel == self.dpMenu.labelList[2] and flp[0] == self.dpMenu.labelList[2]:
                    if not self.isPenActive:
                        self.isPenActive = not self.isPenActive
                        flp[0].changeStyleSheet("color","rgba(255,255,0,200)")
                    else:
                        self.isPenActive = not self.isPenActive
                        flp[0].changeStyleSheet("color","rgba(255,255,255,200)")
                if self.pushedLabel == self.dpMenu.labelList[3] and flp[0] == self.dpMenu.labelList[3]:
                    color = QColorDialog().getColor(
                        self.penColor, self.dpWindow, "色を選択")
                    self.penColor = color
                    flp[0].changeStyleSheet(
                        "color", f"rgb({color.red()},{color.green()},{color.blue()})")
                if self.pushedLabel == self.dpMenu.labelList[4] and flp[0] == self.dpMenu.labelList[4]:
                    self.canvas.setCanvas(self.dpWindow.size())
            else: #label以外
                if self.pushedLabel == self.dpMenu.labelList[0]:
                    pos = self.dpWindow.mapFromGlobal(QCursor.pos())
                    xp = int(100*pos.x()/self.dpWindow.width())
                    yp = int(100*pos.y()/self.dpWindow.height())
                    self.dpMenu.setPositionPercent(xp,yp)
        
            self.pushedLabel = 0
            
        if self.actionKey[0] == True:
            if flp[0] != 0:
                None
            else:
                if self.canvas.isCursorOnMe() and self.isPenActive:
                    self.canvas.drawLine(self.canvas.mapFromGlobal(self.prevCursorPos),self.canvas.mapFromGlobal(QCursor().pos())
                    ,5,self.penColor)


        # cursorﾊﾞｯﾌｧ更新
        self.prevCursorPos = QCursor().pos()

        # ループ用タイマー
        self.dpTimer.start()


if __name__ == "__main__":
    myApp()
