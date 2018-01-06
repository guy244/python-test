import base64
from ui import register,main_window,table,add_item,update
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import json
import bcrypt

# Global variable to get the actual Key Password to decode the other ones
user_password = ''

# Global variables to use for edditing and deleting content
edit_row = ''
edit_name = ''


#Funcations for encrypting and decrypting the user passwords with a Key Password and then using Base64, to give it a better "hashed look"
def encrypt_password(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    encoded_string = encoded_string.encode()
    return base64.urlsafe_b64encode(encoded_string)

def decrypt_password(key, string):
    decoded_chars = []
    string = base64.urlsafe_b64decode(string)
    string = string.decode()
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(abs(ord(string[i]) - ord(key_c) % 256))
        decoded_chars.append(encoded_c)
    decoded_string = "".join(decoded_chars)
    return decoded_string

# The main login panel
class Login(QtWidgets.QMainWindow, main_window.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.central_widget = QtWidgets.QStackedWidget()
        self.registerButton.clicked.connect(self.register)  #Direct you to the register window if 'Register' was clicked
        self.loginButton.clicked.connect(self.login_verify) #Verify your login details and direct you to the passwords table

#Func to derirect to a register gui
    def register(self):
        self.register_form = Register(self)
        self.register_form.show()

#Func to raise username/password is incorrect!
    def error_message(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)

        msg.setText("Username or Password is incorrect")
        msg.setInformativeText("Please try again")
        msg.setWindowTitle("Login Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.exec_()

#Func to verify if the user is registered and the password is correct, if not raise error_message()!
    def login_verify(self):
        with open('users.json', 'r') as f:
            user_dict = json.load(f)
            f.close()
        username = self.userForm.text()

        #If the username is registered, takes the stored bcrypt password and compare it to the password inserted
        if username in user_dict:
            hash_password = user_dict[username]
            hash_password = hash_password.encode()
            password = self.passwordForm.text()
            password = password.encode()

            if bcrypt.hashpw(password, hash_password) == hash_password: #Hash the password the users insert and compare it to the actually stored one
                global user_password
                user_password = password.decode()
                Table(self).show()
                self.destroy()
            else:
                self.error_message() #Raised error if it dosent match
        else:
            self.error_message()    #Rasie error if the username isn't registered


#Register window
class Register(QtWidgets.QMainWindow, register.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Register, self).__init__(parent)
        self.setupUi(self)
        self.registerButton.clicked.connect(self.apply) #Register the user in the JSON file

    def apply(self):
        username = self.userForm.text() #Gets the input username
        password = self.passwordForm.text() #Gets the Password input
        password_2 = self.passwordForm_2.text()
        if password == password_2:          # Make sure the passwords match
            password = password.encode()
            hash_password = bcrypt.hashpw(password, bcrypt.gensalt()) #Bcrypt func to Hash the password
            dict = {username:hash_password.decode()}
            with open('users.json', 'w') as f:
                json.dump(dict, f)                  # Storing the hashed password in the JSON file
                f.close()
            self.destroy()                      #Make sure the window is closed after
        else:
            self.error_message()


#Same as the login error, raises if passwords dosen't match
    def error_message(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)

        msg.setText("Passwords dosen't match!")
        msg.setInformativeText("Please try again")
        msg.setWindowTitle("Register Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.exec_()



#The actual GUI to see the stored passwords with names
class Table(QtWidgets.QMainWindow, table.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Table, self).__init__(parent)
        self.setupUi(self)
        self.populateButton.clicked.connect(self.populate)
        self.addButton.clicked.connect(self.add)
        #self.editButton.clicked.connect(self.editItem)



#Fun to populate the table rows and columns with Names and Passwords
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
            key_password = decrypt_password(user_password,key_password)      # Before the password is shown in the table, we most make sure we Decode it using the func we created, unless we will get gibberish
            self.editButton = QtWidgets.QPushButton('Edit')
            self.verticalLayout.addWidget(self.editButton)  #Create an Edit button for each row
            self.tableWidget.setItem(row,0,name) #Create the row and the Name and populate it
            self.tableWidget.setItem(row,1,QtWidgets.QTableWidgetItem(key_password)) #Create the column for the password and populate it
            self.tableWidget.setCellWidget(row,2,self.editButton) #Place the button in the third column

#This one was a bit tricky, we are getting the Index(row,column) and sending it to the editItem func every time we press the Edit button
#Send it thru the index var
            index = QtCore.QPersistentModelIndex(
                self.tableWidget.model().index(row,2))

            self.editButton.clicked.connect(
                lambda *args, index=index: self.editItem(index))

            row +=1

#Func to open the Add Password Dialog
    def add(self):
        Add_Password(self).exec_()

#Func to edit password of a given row, appends the index and the name to a Global Variable so we can use it in the Update_Password gui
    def editItem(self,index):
        global user_password
        global edit_row
        global edit_name
        edit_row = index.row()
        edit_name = self.tableWidget.item(edit_row, 0).text()
        Update_Password(self).exec_()





#The Add Password Dialog
class Add_Password(QtWidgets.QDialog, add_item.Ui_Add):
    def __init__(self, parent=None):
        super(Add_Password, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.add_item_to_json) #Make sure the func will run when user press 'Ok'

#Func to add new password to the database
    def add_item_to_json(self):
        global user_password
        data_dict = {}
        website = self.websiteForm.text()
        password = self.passwordForm.text()
        password = encrypt_password(user_password,password) #Encoding the password, so someone with access to the computer won't be able to get it!
        password = password.decode()

        with open('data.json','r') as f:    #First reading the data file and getting the Dictonary inside
            data_dict = json.load(f)
            f.close()
        data_dict[website] = password
        with open('data.json','w') as f:    #Then writing the new Dictonary with the new Name and Password
            json.dump(data_dict, f)
            f.close()

#The Update Dialog
class Update_Password(QtWidgets.QDialog, update.Ui_Dialog):

    def __init__(self, parent=None):
        super(Update_Password, self).__init__(parent)
        self.setupUi(self)
        self.table = Table()
        self.buttonBox.accepted.connect(self.update)        #Run the update func when 'Ok' pressed
        self.deleteButton.clicked.connect(self.delete)      #Delete the Name and Password from the database

#Func to update a password
    def update(self):
        global edit_row         #Getting the global variables that we set with the editItem func in the Table class
        global edit_name
        data_dict = {}
        New_Password = self.updateForm.text()
        New_Password = encrypt_password(user_password,New_Password)      #Make sure the new password is incoded with the Key Password
        New_Password = New_Password.decode()

        with open('data.json','r') as f:    #Again read the Dictonary from the JSON file and then write the updated one!
            data_dict = json.load(f)
            f.close()
        data_dict[edit_name] = New_Password
        with open('data.json','w') as f:
            json.dump(data_dict, f)
            f.close()

#Func to delete a password from the database!
#Simple, just gets the row and name variable del the item from the Dictonary, then close the dialog!
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


#Making sure the Login Class runs first!
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = Login()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
