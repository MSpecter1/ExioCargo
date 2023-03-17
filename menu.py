#import PySimpleGUI as sg
import tkinter as tk


def optionsWin():
    window2 = tk.Toplevel()
    
   
     

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
            


def main():
    greeting = tk.Label(text="Main Menu",
    fg="white",
    bg="black",
    width=20,
    height=5
    )
    button1 = tk.Button(
    text="Transfer",
    width=25,
    height=2,
    bg="blue",
    fg="yellow",
    )
    button2 = tk.Button(
    text="Balance",
    width=25,
    height=2,
    bg="yellow",
    fg="blue",
    )
    greeting.pack()
    button1.pack()
    button2.pack()
    window = tk.Tk()
    optionsWin()
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