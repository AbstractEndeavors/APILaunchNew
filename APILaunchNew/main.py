#!/usr/bin/env python
import PySimpleGUI as sg
import rpc as rpcFuns
import slectApi as selApi
import functions as fun
import json,urllib.request
def getKeys():
    return fun.getKeys()
def sites(A):
    U = [A]
    reqTimer()
    for url in U:
        X = str(U[0])
        r = requests.get(X)
        PS = r.text
        JS = json.loads(PS)['result']
        changeGlob('lastRequest',time.time())
    return JS
def sites_scan(x):
    import json,urllib.request
    end = 0
    print(x)
    while end == 0:
        output = selApi.getRound(x)
        print(output)
        if output == {'status': '0', 'message': 'No records found', 'result': []}:
            return 
    if str(output['result']) == '{}':
        return 0
    try:
        js = output[x]['results']
        c = ','
        if len(curr_prices) == 0:
            c = ''
        pen(str(curr_prices).replace('}','')+c+'"'+str(x)+'":"'+str(js)+'"}','price_now.txt')
        return js
    except:
        print('scan sleeping ')
        print(x,output)
        time.sleep(20)
def second_window():
    sg.theme('DarkGrey14')
    menu_def = [['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
                ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo', 'Options::this_is_a_menu_key'], ],
                ['&Toolbar', ['---', 'Command &1', 'Command &2','---', 'Command &3', 'Command &4']],
                ['&NetworkTools', ['---','RPC',['Add RPC', 'Choose RPC','get Manual RPC'], 'Choose RPC &2','---', 'Command &3', 'Command &4']],
                ['APIs',['chainScan'],
                ['&Help', ['&About...']]]]
    right_click_menu = ['Unused', ['Right', '!&Click', '&Menu', 'E&xit', 'Properties']]
    layout = [[sg.Menu(menu_def, tearoff=True, font='_ 12', key='-MENUBAR-')],
        [sg.Text('Right click me for a right click menu example')],
        [sg.ButtonMenu('ButtonMenu',  right_click_menu, key='-BMENU-', text_color='red', disabled_text_color='green'), sg.Button('Plain Button')],
        [sg.Text('Script output....', size=(40, 1))],
        [sg.Output(size=(88, 20), font='Courier 10')],
        [sg.Button('create API'), sg.Button('Preset API'),sg.Button('Choose RPC'),sg.Button('Add RPC'),sg.Button('EXIT')],
        [sg.Text(size=(15, 1)), sg.Input('input scan URL',focus=True,  key='scan'), sg.Button('SCAN'), sg.Button('Run No Wait')],
        [sg.Frame('',[[sg.Text('Network Name'),sg.Input('',key='NetworkName'),sg.Push()],[sg.Text('network'),sg.Combo(['Mainnet','TestNet'],key='network'),sg.Push()],[sg.Text('nativeCurrency'),sg.Input('',key='nativeCurrency'),sg.Push()],[sg.Text('chainId'),sg.Input('',key='chainId'),sg.Push()],[sg.Text('RPC'),sg.Input('',key='RPC'),sg.Push()],[sg.Text('BlockExplorer'),sg.Input('',key='BlockExplorer'),sg.Push()],[sg.Text('RPC'),sg.Input('',key='contractName'),sg.Push()]],pad=(0,0),visible=True, background_color='#1B2838', expand_x=True, border_width=0, grab= True)]]
    window = sg.Window('Script launcher', layout)
    # ---===--- Loop taking in user input and using it to call scripts --- #
    while True:
        event, values = window.read()
        if event == 'EXIT'  or event == sg.WIN_CLOSED:
            break # exit button clicked
        if event == 'create API':
            selApi.createMix()
        elif event == 'Preset API':
            scanUrl = selApi.buildApi()
            window['scan'].update(value=scanUrl)
        elif event == 'SCAN':
              data = urllib.request.urlopen(values['scan']).read()
        elif event == 'Choose RPC':
            rpcFuns.chooseDefaultRPC()
        elif event == 'Add RPC':
            rpcFuns.AddRPC()
def test_menus():
    sg.theme('LightGreen')
    sg.set_options(element_padding=(0, 0))
    # ------ Menu Definition ------ #

    # ------ GUI Defintion ------ #
    layout = [[sg.Menu(menu_def, tearoff=True, font='_ 12', key='-MENUBAR-')],
        [sg.Text('Right click me for a right click menu example')],
        [sg.Output(size=(60, 20))],
        [sg.ButtonMenu('ButtonMenu',  right_click_menu, key='-BMENU-', text_color='red', disabled_text_color='green'), sg.Button('Plain Button')],
        [sg.Button('Run'), sg.Button('Shortcut 1'), sg.Button('Fav Program'), sg.Button('EXIT')],[sg.Text('Your output will go here', size=(40, 1))],[sg.Output(size=(127, 30), font=('Helvetica 10'))],[sg.Text('Command History'),sg.Text('', size=(20, 3), key='history')],[sg.ML(size=(85, 5), enter_submits=True, key='query', do_not_clear=False),sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))],]
    window = sg.Window("Windows-like program",layout,default_element_size=(12, 1),default_button_element_size=(12, 1))
    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        # ------ Process menu choices ------ #
        if event == 'chainScan':
            second_window()
        if event == 'About...':
            window.disappear()
            sg.popup('About this program', 'Version 1.0', 'PySimpleGUI Version', sg.get_versions())
            window.reappear()
        elif event == 'Open':
            filename = sg.popup_get_file('file to open', no_window=True)
        elif event == 'Properties':
            second_window()
    window.close()
second_window()
