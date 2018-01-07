import main_window,sys,json,_cffi_backend,bcrypt,base64
from PyQt5 import QtCore, QtGui, QtWidgets
from encryption import decrypt_password,encrypt_password,get_iv
from main import apply_register,login_verify,error_message,populate_data,add_password,update_password,delete_password


# Global variable to get the actual Key Password to decode the other ones
user_password = ''

# Global variables to use for edditing and deleting content
edit_row = ''
edit_name = ''


# The main login panel
class LoginDialog(QtWidgets.QMainWindow, main_window.Ui_MainWindow):

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setupUi(self)
        self.central_widget = QtWidgets.QStackedWidget()
        self.registerButton.clicked.connect(self.register_clicked)  #Direct you to the register window if 'Register' was clicked
        self.loginButton.clicked.connect(self.login_clicked) #Verify your login details and direct you to the passwords table

#Func to derirect to a register gui
    def register_clicked(self):
        self.register_form = RegisterDialog(self)
        self.register_form.show()


#Func to verify if the user is registered and the password is correct, if not raise error_message()!
    def login_clicked(self):
        global user_password
        username = self.userForm.text()
        password = self.passwordForm.text()
        if login_verify(username,password):
            user_password = login_verify(username,password)
            PasswordDialgo(self).show()
            self.destroy()


#Register window
class RegisterDialog(QtWidgets.QMainWindow, main_window.Ui_Register):

    def __init__(self, parent=None):
        super(RegisterDialog, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setupUi(self)
        self.registerButton.clicked.connect(self.apply) #Register the user in the JSON file

    def apply(self):
        username = self.userForm.text() #Gets the input username
        password = self.passwordForm.text() #Gets the Password input
        password_2 = self.passwordForm_2.text()

        apply_register(username,password,password_2)
        self.destroy()


#The actual GUI to see the stored passwords with names
class PasswordDialgo(QtWidgets.QMainWindow, main_window.Ui_Table):

    def __init__(self, parent=None):
        super(PasswordDialgo, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setupUi(self)
        self.populateButton.clicked.connect(self.populate)
        self.addButton.clicked.connect(self.add)



#Fun to populate the table rows and columns with Names and Passwords
    def populate(self):
        global user_password

        data = populate_data(user_password)

        self.tableWidget.clear()
        row = 0
        try:
            for value, key in enumerate(data):
                name = QtWidgets.QTableWidgetItem(key)
                password = QtWidgets.QTableWidgetItem(data[key])

                self.editButton = QtWidgets.QPushButton('Edit')
                self.verticalLayout.addWidget(self.editButton)  #Create an Edit button for each row
                self.tableWidget.setItem(row,0,name) #Create the row and the Name and populate it
                self.tableWidget.setItem(row,1,password) #Create the column for the password and populate it
                self.tableWidget.setCellWidget(row,2,self.editButton) #Place the button in the third column

                index = QtCore.QPersistentModelIndex(
                    self.tableWidget.model().index(row,2)) #This one was a bit tricky, we are getting the Index(row,column) and sending it to the editItem func every time we press the Edit button

                self.editButton.clicked.connect(
                lambda *args, index=index: self.editItem(index))

                row +=1
        except:
            error_message("No data file","Creating data file now...","Data Error")

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
        UpdatePassword(self).exec_()





#The Add Password Dialog
class Add_Password(QtWidgets.QDialog, main_window.Ui_Add):
    def __init__(self, parent=None):
        super(Add_Password, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.setupUi(self)
        self.buttonBox.accepted.connect(self.add_item_to_json) #Make sure the func will run when user press 'Ok'

#Func to add new password to the database
    def add_item_to_json(self):
        global user_password
        website = self.websiteForm.text()
        password = self.passwordForm.text()
        add_password(website,password,user_password)

#The Update Dialog
class UpdatePassword(QtWidgets.QDialog, main_window.Ui_UpdateDialog):

    def __init__(self, parent=None):
        super(UpdatePassword, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.setupUi(self)
        self.table = PasswordDialgo()
        self.buttonBox.accepted.connect(self.update)        #Run the update func when 'Ok' pressed
        self.deleteButton.clicked.connect(self.delete)      #Delete the Name and Password from the database

#Func to update a password
    def update(self):         #Getting the global variables that we set with the editItem func in the Table class
        global edit_name
        global user_password
        new_password = self.updateForm.text()
        update_password(edit_name,new_password,user_password)


#Func to delete a password from the database!
#Simple, just gets the row and name variable del the item from the Dictonary, then close the dialog!
    def delete(self):
        global edit_name
        delete_password(edit_name)
        self.destroy()


#Making sure the Login Class runs first!
def main():
    app = QtWidgets.QApplication(sys.argv)
    form = LoginDialog()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
