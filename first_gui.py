# Using PySimpleGUI to make my first GUI interface

import PySimpleGUI as sg 

layout =    [[sg.Text('Please scan an item: ', font='Arial 20'), sg.Input(key='-IN-')], #row 1
             [sg.Text('Our output will go here', key='-OUT-')], # row 2
             [sg.Button('Ok'), sg.Button('Tote Report'), #row 3
              sg.Button('Opti Reprot'), sg.Button('Check'),
              sg.Button('Undo'), sg.Button('Exit')]]

window = sg.Window('Big Sexy Window', layout)

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    window['-OUT-'].update(values['-IN-'])

window.close()



