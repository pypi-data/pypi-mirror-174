# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
__author__ = 'Su Jin Qiang'
import subprocess
import os
from .stdmsg import reso
from PyQt5.QtWidgets import QMessageBox,QFileDialog,QCompleter, QTreeWidget,QTreeWidgetItem,QComboBox,QWidget,QLabel, QLineEdit,QPushButton,QGridLayout
import threading
from .stdedit import stdinit
from ..piobuilder.pioproject import PioProjectManage
from PyQt5.QtCore import Qt, QSortFilterProxyModel

# 开发本软件消耗了太多时间精力，一路走来，太不容易，写下此行留为纪念，尤其感谢几位学弟（林鉴波、梁莅、房杰、刘席鸣等一直以来的各方面支持）。——2019.10.22晚

#pos = os.path.abspath('.')
#path = pos + "\\tool\msy"

#os.chdir("C:\stwork\stdemo2019827\dist\Stduinodebug\main")  # 通过更改当前运行目录F:\BaiduNetdiskDownload\stpython\stdemo\main


class StdComboBox(QComboBox):
    def __init__(self, parent=None):
        super(StdComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)


        # add a filter model to filter matching items
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)


    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            self.activated[str].emit(self.itemText(index))


    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(StdComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)


    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(StdComboBox, self).setModelColumn(column)


class StdFindBoards(QWidget):

    # Create a Json file for a better path management

    def __init__(self):
        try:
            self.pio_pro = PioProjectManage()
            # self.staus_change.connect(self.staus_change.emit)
            # if

            super(StdFindBoards, self).__init__()
            # self.setWindowOpacity(0.7)
            # self.setGeometry(50, 50, 50, 30)
            # self.my_signal_findboard.connect(self.sig_find_boards)
            # self.setFixedSize(420, 220)
            # self.setWindowTitle('New Project')
            # 置顶及去标题栏
            self.Boardstree = QTreeWidget(self)
            self.Boardstree.setHeaderHidden(True)
            self.Boardstree.setMinimumWidth(380)
            # self.Boardstree.doubleClicked.connect(self.ondoubleClicked)
            self.Boardstree.clicked.connect(self.boards_select)
            self.current_select_boardindex=0
            self.root_list = []
            self.root_dict = {}
            self.boards_list = []
            # self.Boardstree.doubleClicked.connect(self.ondoubleClicked)

            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            # self.setWindowIcon(QIcon("appearance/img/st.PNG"))
            self.setStyleSheet('background: DimGrey')

            # self.centralwidget = QtWidgets.QWidget(self)
            # self.centralwidget.setObjectName("centralwidget")
            self.project_label = QLabel(self)
            # self.begin_label.setGeometry(QtCore.QRect(20, 5, 225, 22))
            self.project_label.setText(reso.project_set)
            self.project_label.setObjectName("project_label")

            self.project_name_label = QLabel(self)
            self.current_platform=''

            self.project_name_label.setMinimumWidth(360)
            # self.board_label.setGeometry(QtCore.QRect(20, 40, 225, 22))
            self.project_name_label.setText(reso.project_name)
            self.project_name_label.setObjectName("project_name_label")
            self.project_nameEdit = QLineEdit("")
            self.project_nameEdit.textChanged.connect(self.pro_name_change)

            self.board_label = QLabel(self)
            self.board_label.setMinimumWidth(360)
            # self.board_label.setGeometry(QtCore.QRect(20, 120, 225, 22))
            self.board_label.setText(reso.board_core_type)
            self.board_label.setObjectName("board_label")
            self.board = QLabel(self)
            self.board.setMinimumWidth(360)
            #
            # self.board.setMinimumWidth(360)
            # self.board.setObjectName("board")
            # self.board.activated.connect(self.to_board)

            self.framework_label = QLabel(self)
            self.framework_label.setMinimumWidth(360)
            # self.framework_label.setGeometry(QtCore.QRect(20, 200, 225, 22))
            self.framework_label.setText(reso.project_framework)
            self.framework_label.setObjectName("framework_label")
            self.framework = QComboBox(self)
            self.framework.setMinimumWidth(360)

            self.upload_method_label = QLabel(self)
            self.upload_method_label.setMinimumWidth(360)
            # self.upload_method_label.setGeometry(QtCore.QRect(20, 600, 225, 22))
            self.upload_method_label.setText(reso.board_debug)
            self.upload_method_label.setObjectName("upload_method_label")
            self.upload_method = QComboBox(self)
            self.upload_method.setMinimumWidth(360)
            # self.upload_method.activated.connect(lambda: self.to_upload_method(self.upload_method.currentText()))
            self.upload_method.setObjectName("upload_method")
            self.project_build = QPushButton(reso.project_build, self)
            self.project_build.clicked.connect(self.project_build_f)
            self.project_build.setStyleSheet('background: SlateGrey')
            self.project_build.setEnabled(False)
            self.project_cancel = QPushButton(reso.cancel, self)
            self.project_cancel.setStyleSheet('background: SlateGrey')
            self.project_cancel.clicked.connect(self.project_build_c)
            self.line_label = QLabel(self)
            self.line_label.setMinimumWidth(360)

            self.project_path_label = QLabel(self)
            self.project_path_label.setMinimumWidth(360)
            # self.upload_method_label.setGeometry(QtCore.QRect(20, 600, 225, 22))
            self.project_path_label.setText("项目存储位置")
            self.project_path_label.setObjectName("project_path_label")
            self.project_path = QLineEdit("")
            self.project_path.setMinimumWidth(360)
            # self.upload_method.activated.connect(lambda: self.to_upload_method(self.upload_method.currentText()))
            self.project_path.setObjectName("project_path")
            self.project_path_button=QPushButton("自定义", self)
            self.project_path_button.setStyleSheet('background: SlateGrey')
            self.project_path_button.clicked.connect(self.choose_path)
            # self.pio_pro_boards = self.pio_pro.project_boards()

            # wlayout = QVBoxLayout()

            # 局部布局：水平，垂直，网格，表单
            glayout = QGridLayout()
            # line edit
            # LineEdit1 = QLineEdit()
            glayout.addWidget(self.Boardstree,0, 0, -1, 1)
            glayout.addWidget(self.project_label, 1,1)  # name platform board fromwork  下载方式
            glayout.addWidget(self.project_name_label, 2, 1)
            glayout.addWidget(self.project_nameEdit, 3, 1)
            glayout.addWidget(self.board_label, 4, 1)

            glayout.addWidget(self.board, 5, 1)
            glayout.addWidget(self.framework_label, 6, 1)
            glayout.addWidget(self.framework, 7, 1)
            glayout.addWidget(self.upload_method_label, 8, 1)

            glayout.addWidget(self.upload_method, 9, 1)
            #

            glayout.addWidget(self.project_path_label, 10, 1)
            glayout.addWidget(self.project_path, 11, 1)
            glayout.addWidget(self.project_path_button, 11, 2)
            glayout.addWidget(self.line_label, 12, 1)
            glayout.addWidget(self.project_build, 13, 1)
            glayout.addWidget(self.project_cancel, 13, 2)
            glayout.setRowStretch(0, 1)
            # 准备四个控件
            # gwg = QWidget()
            # # 使用四个控件设置局部布局
            # gwg.setLayout(glayout)
            # # 将四个控件添加到全局布局中
            # wlayout.addWidget(gwg)
            self.setLayout(glayout)
        except:
            stdinit.std_signal_gobal.stdprintln()
    def choose_path(self):
        directory = QFileDialog.getExistingDirectory(None, "选取存储文件位置", "C:/")  # 起始路径
        if directory!="":
            stdinit.projects_dir=directory + "/"
            self.project_path.setText(directory + "/" + self.project_nameEdit.text())

    def pro_name_change(self):
        # print()
        path=stdinit.projects_dir+self.project_nameEdit.text()
        self.project_path.setText(path)
    def boards_select(self):
        try:
            text=self.Boardstree.currentItem().text(0)

            if text in self.root_list:
                pass
            else:
                self.board.setText(text)
                self.select_a_board(text)
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def select_a_board(self,textt):
        try:
            self.current_select_boardindex = self.boards_list.index(textt)

            stdinit.board_id = stdinit.pio_boards[self.current_select_boardindex]['id']
            self.current_platform = stdinit.pio_boards[self.current_select_boardindex]['platform']
            self.project_build.setEnabled(True)
            num = len(stdinit.pio_boards[self.current_select_boardindex]['frameworks'])
            self.framework.clear()
            for i in range(num):
                self.framework.addItem(stdinit.pio_boards[self.current_select_boardindex]['frameworks'][i])

            if 'debug' in stdinit.pio_boards[self.current_select_boardindex]:
                self.upload_method.clear()
                for key, value in stdinit.pio_boards[self.current_select_boardindex]['debug']['tools'].items():
                    self.upload_method.addItem(key)
            else:
                self.upload_method.clear()
                self.upload_method.addItem("Disable")

            # self.staus_change.emit(cmd_args["cmd_boards_num"], cmd_args["cmd_upMethod"])
            #             # os.chdir(pos)
        except:
            stdinit.std_signal_gobal.stdprintln()

    # cmd_boards  cmd_boards_num cmd_upMethod cmd_xserial cmd_usb cmd_xusb cmd_opt cmd_rtlib
    def load_board(self):
        try:
            if stdinit.pio_boards == None:
                if self.pio_pro.project_boards():
                    num = len(stdinit.pio_boards)

                    for i in range(num):
                        plt=stdinit.pio_boards[i]['platform']
                        if plt in self.root_list:
                            child = QTreeWidgetItem(self.root_dict[plt])
                            child.setText(0, stdinit.pio_boards[i]['name'])
                        else:
                            self.root_list.append(plt)
                            self.root_dict[plt] = QTreeWidgetItem(self.Boardstree)
                            self.root_dict[plt].setText(0, plt)
                            child = QTreeWidgetItem(self.root_dict[plt])
                            child.setText(0, stdinit.pio_boards[i]['name'])

                        self.boards_list.append(stdinit.pio_boards[i]['name'])
                    #self.board.addItems(self.boards_list)
                    self.line_label.setText("")

                else:
                    target = stdinit.stdenv + "/.stduino/packages/pioenv/pioboards.json"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
                    if os.path.exists(target):
                        self.line_label.setText("哪里发生了问题！")
                        self.line_label.setStyleSheet("color:DeepSkyBlue")
                        self.project_build.setEnabled(False)
                        stdinit.std_signal_gobal.std_echo_msg(0, "请重启软件后再次执行该操作，若还存在该问题请至插件安装界面卸载并重新安装Platformio！")
                    else:
                        if stdinit.pio_boards == None:
                            #self.line_label.setText("请重新安装Platformio！")
                            self.line_label.setStyleSheet("color:DeepSkyBlue")
                            self.project_build.setEnabled(False)
                            stdinit.std_signal_gobal.std_echo_msg(0,"当前插件安装存在文件缺失，请至插件安装界面卸载并重新安装Platformio！")

                        else:
                            num = len(stdinit.pio_boards)

                            for i in range(num):

                                self.boards_list.append(stdinit.pio_boards[i]['name'])
                                root = QTreeWidgetItem(self.Boardstree)
                                root.setText(0, stdinit.pio_boards[i]['name'])
                            #self.board.addItems(self.boards_list)
                            #self.line_label.setText("请先安装PlatformIO！")
                            self.line_label.setStyleSheet("color:DeepSkyBlue")
        except:
            stdinit.std_signal_gobal.stdprintln()

        # print(1)


    def load_boards(self):
        try:
            if stdinit.pio_boards == None:
                t1 = threading.Thread(target=self.load_board, name='load_board', args=())
                t1.setDaemon(True)
                t1.start()

        except:
            stdinit.std_signal_gobal.stdprintln()

        #print(1)

    def is_stduino_plat(self):
        try:
            if stdinit.pio_boards[self.current_select_boardindex]["platforms"]=="stduino":
                stdinit.run_platforms = "stduino"
                return True


        except:
            stdinit.run_platforms = "platformio"
            return False

    def is_stduino_plat_installed(self):
        try:

            curat = stdinit.std_platform_dir + "/" + stdinit.pio_boards[self.board.currentIndex()]['platform']
            if os.path.exists(curat):
                return True
            else:
                cmd = "C:/Users/debug/PycharmProjects/pyst123test/venv/Scripts/python.exe D:/pythonpro/stduinocore/src/stduino/function/cores/commands/commands.py platform install -p "

                cmd=cmd+self.current_platform
                try:
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                    for line in iter(proc.stdout.readline, b''):
                        try:
                            s1 = str(line, encoding='gbk')
                        except:
                            s1 = str(line)
                        stdinit.std_signal_gobal.std_echo_msg(1, s1)
                        if not subprocess.Popen.poll(proc) is None:
                            if line == "":
                                break
                    proc.stdout.close()
                except:
                    pass
            return True
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False




    def project_init(self):
        try:
            stdinit.std_signal_gobal.std_process(1, "正在构建")
            target = stdinit.stdenv + "/.stduino/packages/pioenv/pioboards.json"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
            if os.path.exists(target):

                if self.is_stduino_plat():

                    if self.is_stduino_plat_installed():
                        if self.pio_pro.project_std_init(self.upload_method.currentText(),
                                                         self.framework.currentText()):
                            stdinit.std_signal_gobal.std_process(0, "构建完成！")
                            stdinit.std_signal_gobal.std_echo_msg(1, "构建完成！")
                        else:
                            stdinit.std_signal_gobal.std_process(0, "构建失败！")
                            stdinit.std_signal_gobal.std_echo_msg(0, "构建失败！")
                    else:
                        stdinit.std_signal_gobal.std_echo_msg(0, "构建失败！")


                else:

                    if self.pio_pro.project_init(self.upload_method.currentText(), self.framework.currentText()):
                        stdinit.std_signal_gobal.std_process(0, "构建完成！")
                        stdinit.std_signal_gobal.std_echo_msg(0, "构建完成！")
                    else:
                        stdinit.std_signal_gobal.std_process(0, "构建失败！")
                        stdinit.std_signal_gobal.std_echo_msg(0, "构建失败！")

            else:
                stdinit.std_signal_gobal.std_echo_msg(0, "开始安装PlatformIO~")
                if stdinit.Pio_install.pio_install():
                    stdinit.std_signal_gobal.std_echo_msg(0, "PlatformIO安装成功！")
                    if self.is_stduino_plat():



                        if self.pio_pro.project_std_init(self.upload_method.currentText(), self.framework.currentText()):
                            stdinit.std_signal_gobal.std_process(0, "构建完成！")
                            stdinit.std_signal_gobal.std_echo_msg(0, "构建完成！")
                        else:
                            stdinit.std_signal_gobal.std_process(0, "构建失败！")
                            stdinit.std_signal_gobal.std_echo_msg(0, "构建失败！")


                    else:
                        if self.pio_pro.project_init(self.upload_method.currentText(), self.framework.currentText()):
                            stdinit.std_signal_gobal.std_process(0, "构建完成！")
                            stdinit.std_signal_gobal.std_echo_msg(0, "构建完成！")
                        else:
                            stdinit.std_signal_gobal.std_process(0, "构建失败！")
                            stdinit.std_signal_gobal.std_echo_msg(0, "构建失败！")
                else:
                    stdinit.std_signal_gobal.std_echo_msg(0, "PlatformIO安装失败，暂不可构建项目！")
                    stdinit.std_signal_gobal.std_process(0, "构建失败！")

        except:
            stdinit.std_signal_gobal.stdprintln()


    def project_build_f(self):
        try:
            if self.project_nameEdit.text() == "":
                QMessageBox.warning(self, "Warning",
                                    "警告：请输入项目名称!\n",
                                    QMessageBox.Yes)
            elif os.path.isdir(os.path.join(stdinit.projects_dir,self.project_nameEdit.text())):
                QMessageBox.warning(self, "Warning",
                                    "警告：该工程名已被占用，请重新命名!\n",
                                    QMessageBox.Yes)

            else:
                try:
                    stdinit.project_name = self.project_nameEdit.text()
                    t1 = threading.Thread(target=self.project_init, name='load_board', args=())
                    t1.setDaemon(True)
                    t1.start()
                    stdinit.find_boards.close()
                    stdinit.std_signal_gobal.std_find_staus_change()
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    stdinit.find_boards.close()
                    stdinit.std_signal_gobal.std_find_staus_change()

        except:
            stdinit.std_signal_gobal.stdprintln()



        # if stdinit.pio_boards == None:
        #     t1 = threading.Thread(target=self.load_board, name='load_board', args=())
        #     t1.setDaemon(True)
        #     t1.start()
        # else:
        #     pass
    def project_build_c(self):
        try:
            stdinit.find_boards.close()
            stdinit.std_signal_gobal.std_find_staus_change()
        except:
            stdinit.std_signal_gobal.stdprintln()


    def to_board(self):
        try:
            text = self.board.currentIndex()
            stdinit.board_id = stdinit.pio_boards[text]['id']
            self.current_platform= stdinit.pio_boards[text]['platform']
            self.project_build.setEnabled(True)
            num = len(stdinit.pio_boards[text]['frameworks'])
            self.framework.clear()
            for i in range(num):
                self.framework.addItem(stdinit.pio_boards[text]['frameworks'][i])

            if 'debug' in stdinit.pio_boards[text]:
                self.upload_method.clear()
                for key, value in stdinit.pio_boards[text]['debug']['tools'].items():
                    self.upload_method.addItem(key)
            else:
                self.upload_method.clear()
                self.upload_method.addItem("Disable")


            # self.staus_change.emit(cmd_args["cmd_boards_num"], cmd_args["cmd_upMethod"])
            #             # os.chdir(pos)
        except:
            stdinit.std_signal_gobal.stdprintln()




# class Model(object):
#     def logic(self):
#         data = "Got it"
#         print("Model: Crunching data as per business logic")
#         return data
#
#
# class View(object):
#     def updata(self, data):
#         print("View:Updating the view with results: ", data)
#
#
# class Controller(object):
#     def __init__(self):
#         self.model = Model()
#         self.view = View()
#
#     def interface(self):
#         print("Controller: Relayed the Client asks")
#         data = self.model.logic()
#         self.view.updata(data)