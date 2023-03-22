import tkinter as tk
from tkinter import *

#reference for sign in window: https://pythonexamples.org/python-tkinter-login-form/


def close():
   #https://stackoverflow.com/questions/26086486/python-tkinter-toplevel-destroy-vs-quit-not-working-as-intended
   tkWindow.quit()
   tkWindow.destroy()

def saveUsername():
    global username #https://stackoverflow.com/questions/17911831/python-global-variable-not-updating
    username = usernameEntry.get()
    print(username, "SIGNS IN")
    return usernameEntry.get()
    

def startUp():
    #window
    global tkWindow
    # tkWindow = Toplevel()#tk.Tk()
    tkWindow.geometry('400x150')  
    tkWindow.title('Sign In')


    #username label and text entry box
    usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    username = StringVar()
    global usernameEntry
    usernameEntry = Entry(tkWindow, textvariable=username)
    usernameEntry.grid(row=0, column=1)  

    #login button
    loginButton = Button(tkWindow, text="Login", command=lambda: [saveUsername(), close()])
    loginButton.grid(row=4, column=0)  

    tkWindow.mainloop()


def main():
    startUp()
    # username = saveUsername()
    # print("hellooo", username)

if __name__ == '__main__':
    main()




# import tkinter as tk
# from tkinter import *

# #reference: https://pythonexamples.org/python-tkinter-login-form/
# #window
# tkWindow = tk.Tk()  
# tkWindow.geometry('400x150')  
# tkWindow.title('Tkinter Login Form - pythonexamples.org')

# global username
# username = ""

# def close():
#    #win.destroy()
#    tkWindow.quit()


# def saveUsername():
#     username = usernameEntry.get()
#     print(username)
#     close()


# #username label and text entry box
# usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
# username = StringVar()
# usernameEntry = Entry(tkWindow, textvariable=username)
# usernameEntry.grid(row=0, column=1)  

# #login button
# loginButton = Button(tkWindow, text="Login", command=saveUsername)
# loginButton.grid(row=4, column=0)  


# tkWindow.mainloop()

# print(username.get())