import PySimpleGUI as sg

import amino

#proxies = {"http": "46.52.170.87:8080", "https": "188.166.220.163:8080"}
#client = amino.Client(proxies=proxies)
client = amino.Client()

def window_login():
    layout = [
        [sg.Text('Email:')],
        [sg.Input(key='mail')],
        [sg.Text('Password:')],
        [sg.Input(key='passw', password_char="*")],
        [sg.Button('Login', key='con1'), sg.Button('Exit', key='exit')]
    ]
    return sg.Window('Login - Check-in gui', layout=layout, finalize=True)

def window_comu():
    layout = [
        [sg.Text('Write AminoID. Example: Amine')],
        [sg.Input(key='aid')],
        [sg.Button('Continue', key='con2'), sg.Button('Back', key='exit')]
    ]
    return sg.Window('AminoID - Check-in gui', layout=layout, finalize=True)

def window_checkin():
    layout = [
        [sg.Button('Check-in', key='cin'), sg.Button('Back', key='exit')]
    ]
    return sg.Window('Check-in - Check-in gui', layout=layout, finalize=True)

w1, w2, w3 = window_login(), None, None

while True:
    window,event,values = sg.read_all_windows()
    if window == w1 and event == sg.WIN_CLOSED:
        break
    if window == w1 and event == 'exit':
        break
    if window == w1 and event == 'con1':
        try:
            client.login(email=values['mail'], password=values['passw'])
            sg.popup(f'Welcome! {client.get_user_info(userId=client.userId).nickname}')
            w2 = window_comu()
            w1.hide()
        except amino.lib.util.exceptions.InvalidAccountOrPassword:
            sg.popup('Ups! Invalid account or password.')
        except amino.lib.util.InvalidPassword:
            sg.popup('Ups! Invalid password.')
        except amino.lib.util.AccountDoesntExist:
            sg.popup('Ups! The account dont exist.')

    if window == w2 and event == sg.WIN_CLOSED:
        break
    if window == w2 and event == 'exit':
        w2.hide()
        w1.un_hide()

    if window == w2 and event == 'con2':
        try:
            subclient = amino.SubClient(aminoId=values["aid"], profile=client.profile)
            sg.popup(f'Sucess!')
            w3 = window_checkin()
            w2.hide()
        except amino.lib.util.exceptions.CommunityNotFound:
            sg.popup(f'Ups! Community dont found.')
    if window == w3 and event == sg.WIN_CLOSED:
        break
    if window == w3 and event == 'exit':
        w3.hide()
        w2.un_hide()
    if window == w3 and event == 'cin':
        try:
            days = subclient.get_user_checkins(subclient.profile.userId).consecutiveCheckInDays
            subclient.check_in()
            sg.popup(f'Check-in sucess! You have {days} consecutive days!')
        except amino.lib.util.exceptions.AlreadyCheckedIn:
            sg.popup('Ups! You already checked in.')