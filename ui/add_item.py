# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_item.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Add(object):
    def setupUi(self, Add):
        Add.setObjectName("Add")
        Add.setEnabled(True)
        Add.resize(388, 133)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Add.sizePolicy().hasHeightForWidth())
        Add.setSizePolicy(sizePolicy)
        Add.setMinimumSize(QtCore.QSize(388, 133))
        Add.setMaximumSize(QtCore.QSize(388, 133))
        self.formLayout = QtWidgets.QFormLayout(Add)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Add)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.websiteForm = QtWidgets.QLineEdit(Add)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.websiteForm.sizePolicy().hasHeightForWidth())
        self.websiteForm.setSizePolicy(sizePolicy)
        self.websiteForm.setText("")
        self.websiteForm.setObjectName("websiteForm")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.websiteForm)
        self.label_2 = QtWidgets.QLabel(Add)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.passwordForm = QtWidgets.QLineEdit(Add)
        self.passwordForm.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.passwordForm.sizePolicy().hasHeightForWidth())
        self.passwordForm.setSizePolicy(sizePolicy)
        self.passwordForm.setObjectName("passwordForm")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.passwordForm)
        self.buttonBox = QtWidgets.QDialogButtonBox(Add)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(Add)
        self.buttonBox.accepted.connect(Add.accept)
        self.buttonBox.rejected.connect(Add.reject)
        QtCore.QMetaObject.connectSlotsByName(Add)

    def retranslateUi(self, Add):
        _translate = QtCore.QCoreApplication.translate
        Add.setWindowTitle(_translate("Add", "Add Item"))
        self.label.setText(_translate("Add", "Website / Name: "))
        self.label_2.setText(_translate("Add", "Password: "))

