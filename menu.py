#import PySimpleGUI as sg
import tkinter as tk
from tkinter import ttk
window = tk.Tk()
window.geometry("750x400")
name_var=tk.StringVar()
loadInput = [""]
global username
username = ""
def optionsWin():
    window2 = tk.Toplevel()
    window2.title("Toplevel1")
    window2.geometry("200x100")
    label = tk.Label(window2, text = "This is a Toplevel2 window")
    button = tk.Button(window2, text = "Exit", command = window2.destroy)
    button1 = tk.Button(window2,
    text="Load",
    width=25,
    height=2,
    bg="yellow",
    fg="blue",
    command = loadWin
    )
    button2 = tk.Button(window2,
    text="Unload",
    width=25,
    height=2,
    bg="yellow",
    fg="red",
    )
    button3 = tk.Button(window2,
    text="Begin Ordering",
    width=25,
    height=2,
    bg="yellow",
    fg="green",
    )
    label.pack()
    button.pack()
    button1.pack()
    button2.pack()
    button3.pack()
    window2.mainloop()

def saveInput(name):
    name=name_var.get()
    
    loadInput.append(name)
    for i in loadInput:
        print(i)

def loadWin():
    

    
    window3 = tk.Toplevel()
    window3.title("Toplevel2")
    window3.geometry("200x100")
    label = tk.Label(window3, text = "This is a Toplevel2 window")
    label2 = tk.Label(window3, text = "Enter the containers needed to be loaded here")
    entry = tk.Entry(window3, textvariable = name_var, fg="yellow", bg="blue", width=200)
    #textInput = tk.Text(window3, wrap=WORD)
    label3= tk.Label(window3, text="test", font=('Helvetica 13'))
    button2 =tk.Button(window3, text= "enter",width= 20, command= lambda: saveInput(name_var))
    
    
    button = tk.Button(window3, text = "Exit", command = window3.destroy)
   
    label.pack()
    label2.pack()
    label3.pack()
    entry.pack()
    button.pack()
    button2.pack()
    
    window3.mainloop()

     

    # layout2 = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(12,1), key='-OUTPUT-')],
    #        [sg.Input(key='-IN-')],
    #        [sg.Button('Show'), sg.Button('Exit'), sg.Button('Old Window')]]
    # window2 = sg.Window('Window Title2', layout2, modal = True)
    # while True:  # Event Loop
    
    #     event, values = window2.read()
    #     print(event, values)
    #     if event ==  'Exit' or event == sg.WIN_CLOSED :
    #         break
    #     if event == 'Show':
    #         window2['-OUTPUT-'].update(values['-IN-'])
    # window2.close()   
            
def saveInput2(name):
    username=name_var.get()
    print(username)
def signInWin():
    

    
    window4 = tk.Toplevel()
    window4.title("SIGN IN WINDOW")
    window4.geometry("200x100")
    label = tk.Label(window4, text = "SIGN IN")
    label2 = tk.Label(window4, text = "Please sign in with you username below")
    entry = tk.Entry(window4, textvariable = name_var, fg="yellow", bg="blue", width=200)
    #textInput = tk.Text(window3, wrap=WORD)
    label3= tk.Label(window4, text="test", font=('Helvetica 7'))
    button2 =tk.Button(window4, text= "enter",width= 20, command= lambda: saveInput2(name_var))
    
    
    button = tk.Button(window4, text = "Exit", command = window4.destroy)
   
    label.pack()
    label2.pack()
    label3.pack()
    entry.pack()
    button2.pack()
    button.pack()
    
    
    window4.mainloop()

def updateUser():
    window5 = tk.Toplevel()
    test = "hi"
    User = tk.Label(window5, text=test,
    bg="white",
    fg="black",
    width=20,
    height=5
    )
    #User.place(x = 700, y = 700) 
    User.pack()

def main():
    
    profileButton=tk.Button(window, text = "Username update",
    width=12,
    height=2,
    bg="green",
    fg="black",
    command = updateUser
    )
    profileButton.place(x=1,y=1)
   
    greeting = tk.Label(window, text="Main Menu",
    bg="white",
    fg="black",
    width=20,
    height=5
    )
    button1 = tk.Button(window,
    text="Transfer",
    width=25,
    height=2,
    bg="blue",
    fg="yellow",
    command = optionsWin
    )
    button2 = tk.Button(window,
    text="Balance",
    width=25,
    height=2,
    bg="yellow",
    fg="blue",
    )
    signInButton = tk.Button(window,
    text="Sign In Here",
    width=25,
    height=2,
    bg="black",
    fg="white",
    command = signInWin
    )
    signInButton.place(x=20,y=20)
    profileButton.pack()
    signInButton.pack()
    greeting.pack()
    button1.pack()
    button2.pack()
    
    
    window.mainloop()
    # sg.theme('Dark Blue 3')  # please make your windows colorful
    
    # layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(12,1), key='-OUTPUT-')],
    #       [sg.Input(key='-IN-')],
    #       [sg.Button('Show'), sg.Button('Exit'), sg.Button('New Window')]]

    # window = sg.Window('Window Title', layout)
   
    # while True:  # Event Loop
        
    #     event, values = window.read()
          
    #     print(event, values)
    #     if event == sg.WIN_CLOSED or event == 'Exit':
    #         break
    #     if event == 'Show':
    #         # change the "output" element to be the value of "input" element
            
    #         window['-OUTPUT-'].update(values['-IN-'])
    #     if event == 'New Window':
            
    #         optionsWin()
        
        


    # window.close()
if __name__ == "__main__":

    main()
