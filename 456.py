import sys
from PyQt5.Qt import *
from PyQt5.QtGui import *
from MainWindows import Ui_MainWindow
import cv2 as cv
import sys
import PySide2
import os
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.setWindowTitle('异物入侵检测系统')
        self.name = ""
        self.image = None
        self.frame = None
        self.net = cv.dnn_DetectionModel('yolov3.cfg', 'yolov3.weights')
        self.net.setInputSize(416, 416)
        self.net.setInputScale(1.0 / 255)
        self.net.setInputSwapRB(True)
        with open('things.names', 'rt') as f:
            self.names = f.read().rstrip('\n').split('\n')
        # self.get_test()

    def get_test(self):
        with open("test.txt") as fp:
            names = fp.read().rstrip('\n').split('\n')
        import os
        import shutil
        if not os.path.exists("test_images"):
            os.mkdir("test_images")
        for name in names:
            shutil.copyfile(f"image/{name}.jpg", f"test_images/{name}.jpg")

    def set_ui(self):
        self.ui = Ui_MainWindow()  # 实例化对象
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.TestImage)
        self.ui.actionopen.triggered.connect(self.ReadImage)
        self.ui.actionexit.triggered.connect(qApp.quit)
        self.ui.actionsave.triggered.connect(self.SaveImage)
        self.ui.actionforecast.triggered.connect(self.forecast)

    def forecast(self):
        dirname = QFileDialog.getExistingDirectory(self, "选择要预测的文件夹", ".")
        dirname2 = QFileDialog.getExistingDirectory(self, "选择要存放结果的文件夹", ".")
        print(dirname2)

        import os
        for name in os.listdir(dirname):
            self.image = cv.imread(os.path.join(dirname, name))
            frame = self.image.copy()
            classes, confidences, boxes = self.net.detect(frame, confThreshold=0.1, nmsThreshold=0.4)
            if len(classes) > 0:
                for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
                    label = '%.2f' % confidence
                    label = '%s: %s' % (self.names[classId], label)
                    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    left, top, width, height = box
                    top = max(top, labelSize[1])
                    cv.rectangle(frame, box, color=(0, 0, 255), thickness=5)
                    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 10)
                _image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
                _image = QImage(_image.data,
                                _image.shape[1],
                                _image.shape[0],
                                _image.shape[1] * 3,
                                QImage.Format_RGB888)
                jpg_out = QPixmap(_image).scaled(self.ui.label.width(), self.ui.label.height())  # 设置图片大小
                self.ui.label.setPixmap(jpg_out)  # 设置图片显示
                print(dirname2 + f"/{name}")
                cv.imwrite(dirname2 + f"/{name}", frame)
                cv.waitKey(30)

            else:
                pass
        QMessageBox.about(self, "提示", f"预测结果已经保存在{dirname2}文件夹")

    def TestImage(self):
        frame = self.image.copy()
        classes, confidences, boxes = self.net.detect(frame, confThreshold=0.1, nmsThreshold=0.4)
        if len(classes) > 0:
            for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
                label = '%.2f' % confidence
                label = '%s: %s' % (self.names[classId], label)
                labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                left, top, width, height = box
                top = max(top, labelSize[1])
                cv.rectangle(frame, box, color=(0, 0, 255), thickness=5)
                cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 10)
            self.frame = frame
            _image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
            _image = QImage(_image.data,
                            _image.shape[1],
                            _image.shape[0],
                            _image.shape[1] * 3,
                            QImage.Format_RGB888)
            jpg_out = QPixmap(_image).scaled(self.ui.label.width(), self.ui.label.height())  # 设置图片大小
            self.ui.label.setPixmap(jpg_out)  # 设置图片显示
        else:
            QMessageBox.warning(self, "提示", "无异物")

    def ReadImage(self):
        self.name, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "./",
                                                          "图片文件 (*.jpg *.png)")  # 设置文件扩展名过滤,注意用双分号间隔

        if not self.name == "":
            self.image = cv.imread(self.name)
            _image = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
            _image = QImage(_image.data,
                            _image.shape[1],
                            _image.shape[0],
                            _image.shape[1] * 3,
                            QImage.Format_RGB888)
            jpg_out = QPixmap(_image).scaled(self.ui.label.width(), self.ui.label.height())  # 设置图片大小
            self.ui.label.setPixmap(jpg_out)  # 设置图片显示

    def SaveImage(self):
        name, filetype = QFileDialog.getSaveFileName(self,
                                                     "保存文件",
                                                     "./",
                                                     "所有文件(*.*);;文本文件(*.txt);;图片文件(*.jpg*.png)")
        if not name == "":
            try:
                cv.imwrite(name, self.frame)
            except:
                QMessageBox.warning(self, "警告", "保存图片失败")
            finally:
                return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
