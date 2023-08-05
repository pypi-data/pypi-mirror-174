# Form implementation generated from reading ui file 'qt/aqt/forms/stats.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from aqt.utils import tr



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(607, 556)
        Dialog.setWindowTitle("Statistics")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.web = AnkiWebView(Dialog)
        self.web.setProperty("url", QtCore.QUrl("about:blank"))
        self.web.setObjectName("web")
        self.verticalLayout.addWidget(self.web)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_3.setSpacing(8)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groups = QtWidgets.QRadioButton(self.groupBox_2)
        self.groups.setText("deck")
        self.groups.setChecked(True)
        self.groups.setObjectName("groups")
        self.horizontalLayout_2.addWidget(self.groups, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.all = QtWidgets.QRadioButton(self.groupBox_2)
        self.all.setText("collection")
        self.all.setObjectName("all")
        self.horizontalLayout_2.addWidget(self.all, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.month = QtWidgets.QRadioButton(self.groupBox)
        self.month.setText("1 month")
        self.month.setChecked(True)
        self.month.setObjectName("month")
        self.horizontalLayout.addWidget(self.month, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.year = QtWidgets.QRadioButton(self.groupBox)
        self.year.setText("1 year")
        self.year.setObjectName("year")
        self.horizontalLayout.addWidget(self.year, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.life = QtWidgets.QRadioButton(self.groupBox)
        self.life.setText("deck life")
        self.life.setObjectName("life")
        self.horizontalLayout.addWidget(self.life, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore  # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        pass
from aqt.webview import AnkiWebView