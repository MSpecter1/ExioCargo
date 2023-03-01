import tkinter as tk
import time

root = tk.Tk()
running = True

# Define a function to start the loop
def on_start():
   global running
   running = True

# Define a function to stop the loop
def on_stop():
   global running
   running = False

button_grid = []
def gridSetup():
    for i in range(8):
        button_row = []
        for j in range(12):
            global button
            button = tk.Button(root, text="", height=5, width=10, bg='white',activebackground='lightgrey', command=lambda row=i, column=j: print(row, column))
            button.grid(row=i, column=j)
            button_row.append(button)
        button_grid.append(button_row)

def pairChangeButtonColor(pair1, pair2):
    a, b = pair1
    print(a, b)
    c, d = pair2
    print(c, d)

    while True:
        button1 = button_grid[a][b]
        button1.config(bg="pink")
        button1.update()
        # time.sleep(1)
        # apparently it's recommended to use .after() instead of time.sleep() bc it could interfere with mainloop(); https://stackoverflow.com/questions/39555463/tkinter-how-to-stop-a-loop-with-a-stop-button
        root.after(700) 
        button1.config(bg="white")
        button1.update()

        button2 = button_grid[c][d]
        button2.config(bg="pink")
        button2.update()
        # time.sleep(1)
        root.after(700)
        button2.config(bg="white")
        button2.update()

        if running == False:  #add condition for when user hits "Next", stop the loop so it can go to next step's new animation
            break       
        

def main():
    gridSetup()

    button = tk.Button(root, text="Next", height=1, width=8, command=on_stop)
    button.grid(row=9, column=6)
    pairChangeButtonColor((0,0), (3,3))
    
    print("Broke out of animation loop!") #break out of loop from pairChangeButtonColor((0,0), (3,3))
    root.mainloop()

if __name__ == '__main__':
    main()