import base64
from ui import register,main_window,table,add_item,update
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
import bcrypt


user_password = ''
edit_row = ''
edit_name = ''

def encode_password(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    encoded_string = encoded_string.encode()
    return base64.urlsafe_b64encode(encoded_string)

def decode_password(key, string):
    decoded_chars = []
    string = base64.urlsafe_b64decode(string)
    string = string.decode()
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
        decoded_chars.append(encoded_c)
    decoded_string = "".join(decoded_chars)
    return decoded_string

class Login(QtWidgets.QMainWindow, main_window.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.central_widget = QtWidgets.QStackedWidget()
        self.registerButton.clicked.connect(self.register)
        self.loginButton.clicked.connect(self.login_verify)


    def register(self):
        self.register_form = Register(self)
        self.register_form.show()

    def error_message(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)

        msg.setText("Username or Password is incorrect")
        msg.setInformativeText("Please try again")
        msg.setWindowTitle("Login Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.exec_()

    def login_verify(self):
        with open('users.json', 'r') as f:
            user_dict = json.load(f)
            f.close()
        username = self.userForm.text()
        if username in user_dict:
            hash_password = user_dict[username]
            hash_password = hash_password.encode()
            password = self.passwordForm.text()
            password = password.encode()

            if bcrypt.hashpw(password, hash_password) == hash_password:
                global user_password
                user_password = password.decode()
                Table(self).show()
                self.destroy()
            else:
                self.error_message()
        else:
            self.error_message()


class Register(QtWidgets.QMainWindow, register.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Register, self).__init__(parent)
        self.setupUi(self)
        self.registerButton.clicked.connect(self.apply)

    def apply(self):
        username = self.userForm.text()
        password = self.passwordForm.text()
        password_2 = self.passwordForm_2.text()
        if password == password_2:
            password = password.encode()
            hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
            dict = {username:hash_password.decode()}
            with open('users.json', 'w') as f:
                json.dump(dict, f)
                f.close()
            self.destroy()
        else:
            self.error_message()


    def error_message(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)

        msg.setText("Passwords dosen't match!")
        msg.setInformativeText("Please try again")
        msg.setWindowTitle("Register Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.exec_()




class Table(QtWidgets.QMainWindow, table.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.setupUi(self)
        self.populateButton.clicked.connect(self.populate)
        self.addButton.clicked.connect(self.add)
        #self.editButton.clicked.connect(self.editItem)



    def populate(self):
        global user_password
        with open('data.json', 'r') as f:
            data = json.load(f)

        self.tableWidget.clear()
        row = 0
        for value, key in enumerate(data):
            name = QtWidgets.QTableWidgetItem(key)
            key_password = QtWidgets.QTableWidgetItem(data[key])
            key_password = key_password.text()
            key_password = decode_password(user_password,key_password)
            self.editButton = QtWidgets.QPushButton('Edit')
            self.verticalLayout.addWidget(self.editButton)
            self.tableWidget.setItem(row,0,name)
            self.tableWidget.setItem(row,1,QtWidgets.QTableWidgetItem(key_password))
            self.tableWidget.setCellWidget(row,2,self.editButton)

            index = QtCore.QPersistentModelIndex(
                self.tableWidget.model().index(row,2))

            self.editButton.clicked.connect(
                lambda *args, index=index: self.editItem(index))

            row +=1

    def add(self):
        Add_Password(self).exec_()

    def editItem(self,index):
        global user_password
        global edit_row
        global edit_name
        edit_row = index.row()
        edit_name = self.tableWidget.item(edit_row, 0).text()
        Update_Password(self).exec_()






class Add_Password(QtWidgets.QDialog, add_item.Ui_Add):
    def __init__(self, parent=None):
        super(Add_Password, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.add_item_to_json)

    def add_item_to_json(self):
        global user_password
        data_dict = {}
        website = self.websiteForm.text()
        password = self.passwordForm.text()
        password = encode_password(user_password,password)
        password = password.decode()

        with open('data.json','r') as f:
            data_dict = json.load(f)
            f.close()
        data_dict[website] = password
        with open('data.json','w') as f:
            json.dump(data_dict, f)
            f.close()

class Update_Password(QtWidgets.QDialog, update.Ui_Dialog):

    def __init__(self, parent=None):
        super(Update_Password, self).__init__(parent)
        self.setupUi(self)
        self.table = Table()
        self.buttonBox.accepted.connect(self.update)
        self.deleteButton.clicked.connect(self.delete)

    def update(self):
        global edit_row
        global edit_name
        data_dict = {}
        New_Password = self.updateForm.text()
        New_Password = encode_password(user_password,New_Password)
        New_Password = New_Password.decode()

        with open('data.json','r') as f:
            data_dict = json.load(f)
            f.close()
        data_dict[edit_name] = New_Password
        with open('data.json','w') as f:
            json.dump(data_dict, f)
            f.close()

    def delete(self):
        global edit_row
        global edit_name

        with open('data.json','r') as f:
            data_dict = json.load(f)
            f.close()
        del data_dict[edit_name]
        with open('data.json','w') as f:
            json.dump(data_dict, f)
            f.close()
        self.destroy()



def main():
    app = QtWidgets.QApplication(sys.argv)
    form = Login()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
