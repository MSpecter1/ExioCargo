import PySimpleGUI as sg

sg.theme('Default')

containers = {}

layout = [[sg.Text('8x12 Ship Grid')]]

for row in range(8):
    new_row = []
    for col in range(12):
        new_row.append(sg.Button(size=(5,3), key=(row, col), button_color=("white", "white"), mouseover_colors = ("snow3", "snow3"), pad = (0.5,0.5))) #key=(row,col) represents the grid coordinate for each button 
        #USE TOOLTIP so user can see container name bigger when hovering over a button/container
    layout.append(new_row)
layout.append([sg.Button('Exit')])

window = sg.Window('8x12 Ship Grid', layout, use_default_focus=False)

while True:
    event, values = window.read()
    print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()