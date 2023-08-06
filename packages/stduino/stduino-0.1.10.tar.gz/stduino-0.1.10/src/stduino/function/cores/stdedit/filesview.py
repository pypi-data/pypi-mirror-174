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


import os

from PyQt5.QtWidgets import QListView

from PyQt5.QtWidgets import QWidget,QLabel,QGridLayout,QAbstractItemView,QFileDialog


from . import stdinit
from PyQt5.QtCore import QStringListModel

# 开发本软件消耗了太多时间精力，一路走来，太不容易，写下此行留为纪念，尤其感谢几位学弟（林鉴波、梁莅、房杰、刘席鸣等一直以来的各方面支持）。——2019.10.22晚

#pos = os.path.abspath('.')
#path = pos + "\\tool\msy"

#os.chdir("C:\stwork\stdemo2019827\dist\Stduinodebug\main")  # 通过更改当前运行目录F:\BaiduNetdiskDownload\stpython\stdemo\main



class StdFilesView(QWidget):

    # Create a Json file for a better path management

    def __init__(self):
        try:

            # self.staus_change.connect(self.staus_change.emit)
            # if

            super(StdFilesView, self).__init__()
            # self.setWindowOpacity(0.7)
            # self.setGeometry(50, 50, 50, 30)
            # self.my_signal_findboard.connect(self.sig_find_boards)
            # self.setFixedSize(420, 220)
            # self.setWindowTitle('New Project')
            # 置顶及去标题栏

            #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            # self.setWindowIcon(QIcon("appearance/img/st.PNG"))
           # self.setStyleSheet('background: DimGrey')

            self.start_up_label = QLabel(self)
            self.start_up_label.setStyleSheet('font-size:25px;color:Ivory')
            # self.begin_label.setGeometry(QtCore.QRect(20, 5, 225, 22))
            self.start_up_label.setText("启动")
            self.start_up_label.setObjectName("start_up")
            self.start_up_buttons = QListView(self)
            self.start_up_buttons.setMaximumWidth(400)
            self.start_up_buttons.setStyleSheet('border:none;text-align:left;font-size:20px;color:MediumBlue')
            self.start_up_buttons_model = QStringListModel(self)
            self.start_up_buttons.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.start_up_buttons_model_list = ["新建工程...","打开工程...","打开使用帮助...","主题设置..."]

            self.start_up_buttons_model.setStringList(self.start_up_buttons_model_list)
            self.start_up_buttons.setModel(self.start_up_buttons_model)
            self.start_up_buttons.clicked.connect(self.start_buttons_clicked)


            self.recently_files_label = QLabel(self)


            self.recently_files_label.setMinimumWidth(260)
            # self.board_label.setGeometry(QtCore.QRect(20, 40, 225, 22))
            self.recently_files_label.setText("最近")
            self.recently_files_label.setStyleSheet('font-size:25px;color:Ivory')

            self.recently_files_label.setObjectName("recently_files_label")
            self.projects_path_model_list=[]

            # self.pio_pro_boards = self.pio_pro.project_boards()

            # wlayout = QVBoxLayout()
            self.projects_path=QListView(self)
            self.projects_path.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.projects_path.setMaximumWidth(560)
            self.projects_path.setStyleSheet('border:none;text-align:left;font-size:20px;color:MediumBlue')
            self.projects_path_model = QStringListModel(self)



            self.recently_files_path_list()
            self.projects_path_model.setStringList(self.projects_path_model_list)
            self.projects_path.setModel(self.projects_path_model)
            self.projects_path.clicked.connect(self.open_recently_project_click)

            # 局部布局：水平，垂直，网格，表单
            glayout = QGridLayout()
            # line edit
            # LineEdit1 = QLineEdit()

            glayout.setSpacing(10)
            glayout.addWidget(self.start_up_label,0, 1)
            glayout.addWidget(self.start_up_buttons, 1, 1)



            glayout.addWidget(self.recently_files_label, 0,2)  # name platform board fromwork  下载方式

            glayout.addWidget(self.projects_path, 1, 2)





            #glayout.setRowStretch(0, 1)
            # 准备四个控件
            # gwg = QWidget()
            # # 使用四个控件设置局部布局
            # gwg.setLayout(glayout)
            # # 将四个控件添加到全局布局中
            # wlayout.addWidget(gwg)
            self.setLayout(glayout)
        except:
            print(232)
            # stdinit.std_signal_gobal.stdprintln()
    def show2(self):
        self.show()
    def recently_files_path_list(self):
        for i in stdinit.File_tree_view.ProjectXmltreeRoot:

            self.projects_path_model_list.append(i.attrib['projectpath'])
    def open_recently_project_click(self,qModelIndex):
        action_num = qModelIndex.row()
        stdinit.std_signal_gobal.std_project_path_observer(self.projects_path_model_list[action_num])
        stdinit.std_signal_gobal.std_main_ui_setview(0)
        pass



    def start_buttons_clicked(self,qModelIndex):
        action_num = qModelIndex.row()
        if action_num==0:
            stdinit.find_boards.load_boards()
            stdinit.find_boards.show()
        elif action_num==1:
            m = QFileDialog.getExistingDirectory(None, "选取工程文件夹", stdinit.projects_dir)  # 起始路径
            if os.path.exists(m):
                stdinit.std_signal_gobal.std_project_path_observer(m)
                stdinit.std_signal_gobal.std_main_ui_setview(0)

            pass
        elif action_num==2:
            stdinit.std_signal_gobal.std_echo_msg(1,"先手动打开wiki.stduino.com吧，后面我再继续优化这个功能")

        elif action_num==3:
            stdinit.std_signal_gobal.std_echo_msg(1,"抱歉哈，您先再等等，我还在继续搞这块的功能，待更新")

        pass



# if __name__ == '__main__':  # main函数
#     app = QApplication(sys.argv)
#     try:
#
#
#         find_boards = StdFilesView()
#         find_boards.show()
#
#
#     except:
#
#         sys.exit(app.exec_())
#
#     sys.exit(app.exec_())

