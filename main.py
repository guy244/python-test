import sys,json,_cffi_backend,bcrypt,base64,main
from PyQt5 import QtCore, QtGui, QtWidgets
from encryption import encrypt_password, decrypt_password, get_iv



#Func to derirect to a register gui
def login_verify(username,password):
    with open('users.json', 'r') as f:
        user_dict = json.load(f)
        f.close()

        #If the username is registered, takes the stored bcrypt password and compare it to the password inserted
    if username in user_dict:
        hash_password = user_dict[username]
        hash_password = hash_password.encode()
        password = password.encode()

        if bcrypt.hashpw(password, hash_password) == hash_password: #Hash the password the users insert and compare it to the actually stored one
            password = password.decode()
            if len(password) < 16:
                while len(password) < 16:
                    password = password + 'g'

                    if len(password) == 16:
                        user_password = password
                        break
            elif len(password) > 16:
                password = password[:16]
                user_password = password
            return user_password
            return True
        else:
            error_message("Username or Password is incorrect","Please try again","Login Error") #Raised error if it dosent match
    else:

        error_message("Username or Password is incorrect","Please try again","Login Error")    #Rasie error if the username isn't registered



#func to see if the register form is valid, and apply it
def apply_register(username,password,password_2):
    if password == password_2:          # Make sure the passwords match
        password = password.encode()
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt()) #Bcrypt func to Hash the password
        dict = {username:hash_password.decode()}

        with open('users.json', 'w') as f:
            json.dump(dict, f)                  # Storing the hashed password in the JSON file
            f.close()
        return True                      #Make sure the window is closed after
    else:
        error_message("Passwords dosen't match","Make sure you put the same password twice","Password Error")


#Func to populate the GUI Table with the names and passwords
def populate_data(user_password):

    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except:
        error_message("No data file","Creating data file now...","Data Error")

    decrypted_data = {}

    for value, key in enumerate(data):
        name = key
        key_password = data[key][0]
        IV = data[key][1]
        key_password = decrypt_password(user_password,key_password,IV)
        key_password = key_password.decode()
        decrypted_data[name] = key_password

    return decrypted_data


def add_password(name,password,user_password):

    data_dict = {}
    IV = get_iv()
    password = encrypt_password(user_password,password,IV) #Encoding the password, so someone with access to the computer won't be able to get it!
    password = password.decode()
    IV = base64.urlsafe_b64encode(IV)
    IV = IV.decode()

    try:
        with open('data.json','r') as f:    #First reading the data file and getting the Dictonary inside
            data_dict = json.load(f)
            f.close()
            data_dict[name] = [password,IV]

    except:
        error_message("No data file","Creating data file now...","Data Error")

    with open('data.json','w') as f:    #Then writing the new Dictonary with the new Name and Password
        json.dump(data_dict, f)
        f.close()


def update_password(name,new_password,user_password):

    data_dict = {}
    IV = get_iv()
    password = encrypt_password(user_password,new_password,IV)      #Make sure the new password is incoded with the Key Password
    password = password.decode()
    IV = base64.urlsafe_b64encode(IV)
    IV = IV.decode()

    try:
        with open('data.json','r') as f:    #Again read the Dictonary from the JSON file and then write the updated one!
            data_dict = json.load(f)
            f.close()
            data_dict[name] = [password,IV]
    except:
        error_message("No data file","Creating data file now...","Data Error")

    with open('data.json','w') as f:
        json.dump(data_dict, f)
        f.close()


def delete_password(name):
    with open('data.json','r') as f:
        data_dict = json.load(f)
        f.close()

    del data_dict[name]

    with open('data.json','w') as f:
        json.dump(data_dict, f)
        f.close()










#Func to raise username/password is incorrect!
def error_message(text,info,title):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)

    msg.setText(text)
    msg.setInformativeText(info)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    msg.exec_()
