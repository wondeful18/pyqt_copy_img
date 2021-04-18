# -*- coding: utf-8 -*-
import sys
# import PyQt5.sip
from PyQt5 import sip  # noqa
from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush, QColor, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog, QButtonGroup, QListWidget, QWidget, QListView, QHBoxLayout, QListWidgetItem
import time
import json
import os
import re
import copy
import subprocess
import shutil


# 配置文件路径
config_json_path = "./path_config.json"
qtCreatorFile = "./img_copy.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# 系统调用
def call_system(cmd):
    print("call_system", cmd)
    t1 = time.time()
    # assert( os.system("time "+cmd)==0)
    if os.system(cmd) != 0:
        raise Exception("ASSERT ERROR")
    t2 = time.time()
    print("use", t2 - t1)


# 获取文件名列表，无需扩展名的
def getFileNameListFmtNoExt(dirPath, fileNameFmt):
    retList = []

    for f in os.listdir(dirPath):
        fp = os.path.join(dirPath, f)

        if os.path.isdir(fp):
            continue

        if not os.path.exists(fp):
            continue

        if re.match(fileNameFmt, f):
            lastDotI = f.rfind(".")
            fileNameNoExt = f[:lastDotI]
            retList.append(fileNameNoExt)

    return retList

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        global gPathConfigs
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.dest_path = ""
        self.pre_file_name = ""

        # 选择路径的按钮
        self.selPathBtn.clicked.connect(self.OnSelPathBtn)
        self.clear_all_img.clicked.connect(self.ClearImg)
        self.clear_some_img.clicked.connect(self.Clear1236Img)
        self.do_btn.clicked.connect(self.OnDoBtn)
        # QMessageBox.information(self, "info", "点我干嘛？")

        self.img_paths = [self.img_path1, self.img_path2, self.img_path3, self.img_path4, self.img_path5, self.img_path6]
        self.imgs = [self.img1, self.img2, self.img3, self.img4, self.img5, self.img6]

        self.img_path1.textChanged.connect(self.img_path1_change)
        self.img_path2.textChanged.connect(self.img_path2_change)
        self.img_path3.textChanged.connect(self.img_path3_change)
        self.img_path4.textChanged.connect(self.img_path4_change)
        self.img_path5.textChanged.connect(self.img_path5_change)
        self.img_path6.textChanged.connect(self.img_path6_change)

    def on_img_path_change(self, path_ctrl, img_ctrl):
        
        path_text = path_ctrl.toPlainText()
        pre_i = path_text.find('file:///')
        if pre_i >= 0:
            path_ctrl.setText(path_text[pre_i + 8:])

        path = path_ctrl.toPlainText()
        img_pixmap = QtGui.QPixmap(path).scaled(img_ctrl.width(), img_ctrl.height())
        img_ctrl.setPixmap(img_pixmap)

    def img_path1_change(self):
        path_ctrl = self.img_path1
        img_ctrl = self.img1
        self.on_img_path_change(path_ctrl, img_ctrl)

    def img_path2_change(self):
        path_ctrl = self.img_path2
        img_ctrl = self.img2
        self.on_img_path_change(path_ctrl, img_ctrl)

    def img_path3_change(self):
        path_ctrl = self.img_path3
        img_ctrl = self.img3
        self.on_img_path_change(path_ctrl, img_ctrl)

    def img_path4_change(self):
        path_ctrl = self.img_path4
        img_ctrl = self.img4
        self.on_img_path_change(path_ctrl, img_ctrl)

    def img_path5_change(self):
        path_ctrl = self.img_path5
        img_ctrl = self.img5
        self.on_img_path_change(path_ctrl, img_ctrl)

    def img_path6_change(self):
        path_ctrl = self.img_path6
        img_ctrl = self.img6
        self.on_img_path_change(path_ctrl, img_ctrl)

    def OnSelPathBtn(self):
        # QMessageBox.information(self, "info", "点我干嘛？")
        directory1 = QFileDialog.getExistingDirectory(
            self, "选择目标路径", "./")
        print(directory1)

        self.dest_path = directory1
        self.enginePath.setText(directory1)

    def ClearImg(self):
        for i, img_path_ctrl in enumerate(self.img_paths):
            img_path_ctrl.setText("")

    def Clear1236Img(self):
        for i, img_path_ctrl in enumerate(self.img_paths):
            if i in (0,1,2,5):
                img_path_ctrl.setText("")

    def OnDoBtn(self):
        self.pre_file_name = self.preNameEd.toPlainText()

        if self.pre_file_name == "":
            QMessageBox.information(self, "info", "请输入前缀")
            return
        if self.dest_path == "":
            QMessageBox.information(self, "info", "请选择目标目录")
            return

        copy_count = 0

        for i, img_path_ctrl in enumerate(self.img_paths):
            img_path = img_path_ctrl.toPlainText()
            if os.path.exists(img_path):
                ext_name_i = img_path.rfind(".")
                ext_name = ""
                if (ext_name_i >= 0):
                    ext_name = img_path[ext_name_i:]
                print(ext_name)
                img_dest_name = self.pre_file_name + ("p%d" % (i + 1)) + ext_name
                img_dest_path = self.dest_path + "/" + img_dest_name
                shutil.copyfile(img_path, img_dest_path)
                copy_count += 1

        QMessageBox.information(self, "info", "成功拷贝%d个文件" % copy_count)

app = QApplication(sys.argv)
window = MyApp()
window.show()
# mainwin = IconListWidget()
# mainwin.show()
sys.exit(app.exec_())
