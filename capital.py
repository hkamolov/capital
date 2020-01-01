# IMPORT PACKAGES #
import PySimpleGUI as sg
from datetime import datetime
import calendar
from dateutil.relativedelta import *
import export_file
import pandas as pd
# import Demo_Table_Pandas

# How to sort list of dictionaries: (with 'operator's itemgetter) - ascending or descending
# https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
from operator import itemgetter


# GET TODAY'S DATE
get_time = datetime.now()
date_format = get_time.strftime("%b %d, %Y")
current_month_year = get_time.strftime("%B %Y")
current_year = get_time.strftime("%Y")
current_month = get_time.strftime("%b")
today = get_time.day
chosen = ''
date_export = get_time.strftime("%Y-%m-%d")

# SET ALL WINDOWS APPEARANCE #
sg.ChangeLookAndFeel('Reddit')
sg.SetOptions(element_padding=(0,8) #, 
                # background_color='black'
                )



# DICTIONARY FOR DATA - stores details of every new transaction made by a user in ADD TRANSACTION WINDOW
transaction_details = {
    'Date': '', 'Income/Expenses': '', 'Category': '', 'Memo': '', 'Amount': 0
    }
# list filled with transaction_details dictionary
transaction_list = [] # list[dict, dict, dict, ...]
sortedlist = [] # sorted list of transaction_list 
headlines = ['Date', 'Income/Expenses', 'Category', 'Memo', 'Amount']
headline_keys = ['ainvisiblekey', 'atypekey', 'acategorykey', 'amemokey', 'aamountkey']



# IMPORT - from MENU LIST
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Pandas.py
def table_example():
    
    sg.set_options(auto_size_buttons=True)
    filename = sg.popup_get_file(
        'filename to open', no_window=True, file_types=(("CSV Files", "*.csv"),))
    # --- populate table with file contents --- #
    if filename == '':
        return

    data = []
    header_list = []
    button = sg.popup_yes_no('Does this file have column names already?')

    if filename is not None:
        try:
            # Header=None means you directly pass the columns names to the dataframe
            df = pd.read_csv(filename, sep=',', engine='python', header=None)
            data = df.values.tolist()               # read everything else into a list of rows
            if button == 'Yes':                     # Press if you named your columns in the csv
                # Uses the first row (which should be column names) as columns names
                header_list = df.iloc[0].tolist()
                # Drops the first row in the table (otherwise the header names and the first row will be the same)
                data = df[1:].values.tolist()
            elif button == 'No':                    # Press if you didn't name the columns in the csv
                # Creates columns names for each column ('column0', 'column1', etc)
                header_list = ['column' + str(x) for x in range(len(data[0]))]
        except:
            sg.popup_error('Error reading file')
            return

    layout = [
        [sg.Table(values=data,
                  headings=header_list,
                  display_row_numbers=True,
                  auto_size_columns=False,
                  num_rows=min(25, len(data)))]
    ]

    window = sg.Window(filename, layout, grab_anywhere=False)
    event, values = window.read()
    window.close()



# -----------------------READ FILE DATA for only CSV FILES

# ---------MAIN WINDOW LAYOUT---------------------------------- #
# Main window: Menu list
menu_list = [['&File', ['&Save', '&Import', 'Settings', '---', '&Exit']],
            ['&View', ['Chart', ['Expenses', 'Income', 'Total'], '---', 'Categories']],
            ['&Help', ['Check for Updates...', 'About']] ]



# -----------CALENDAR LAYOUT------------------------------------
# Main window: Calendar layout in Main Layout
list_days_obj = calendar.Calendar()
saved = list_days_obj.monthdayscalendar(get_time.year, get_time.month)
# print(saved)
for i in range(5):
    for j in range(7):
        if saved[i][j] is 0:
            saved[i][j] = '-'
see_my = [ [sg.T(current_month_year, size=(18, 1), pad=((60,0),0), font=('Roboto', 10, 'bold'))] ]
# set weekdays layout
weekdays = [' Mo ', ' Tu ', ' We ', ' Th ', ' Fr ', ' Sa ', ' Su ']
header =  [[sg.Text(h, size=(3,1), pad=((5,5),2), font=('Roboto', 8)) for h in weekdays]]

# set monthdays layout
month_days = [[sg.B(saved[row][col], size=(3,1), key=saved[row][col], pad=((5,5),3), 
                border_width=0, font=('Roboto', 8), 
                button_color=('black', 'white')) for col in range(7)] for row in range(5)]

layout_calendar = see_my + header + month_days
# --------------CALENDAR LAYOUT END-----------------------------------------------


# main window: 1ST COLUMN
first_column_frame = [ [sg.B('Add transaction', key='maddkey', button_color=sg.TRANSPARENT_BUTTON, 
                            image_filename='images\\add_transaction.png', font=('Roboto', 11),
                            image_size=(148,58), image_subsample=1, border_width=False, pad=(0,0))]
                              ]

# 2ND COLUMN elements
second_column_element_income =  [[sg.B('Income', size=(10,3), key='mincomebtnkey', border_width=0, button_color=('black', 'white'))], 
                [sg.T('0', size=(10, 1), key='mshowincomeskey', justification='center')] ]
second_column_element_expenses = [[sg.B('Expenses', size=(10,3), key='mexpensesbtnkey', border_width=0, button_color=('black', 'white'))], 
                [sg.T('0', size=(10, 1), key='mshowexpenseskey', justification='center')] ]
second_column_element_networth =   [[sg.B('Balance', size=(10,3), key='mtotalsbtnkey', border_width=0, button_color=('black', 'white'))], 
                [sg.T('0', size=(10, 1), key='mshowtotalskey', justification='center')] ]

# Main window: 2ND COLUMN
second_column_frame = [ [sg.Column(second_column_element_income), sg.VerticalSeparator(), 
                         sg.Column(second_column_element_expenses), sg.VerticalSeparator(), 
                         sg.Column(second_column_element_networth)] ]

second_column = [ [sg.Frame('', first_column_frame, border_width=False, pad=((0,40),0)),
                   sg.Frame('', second_column_frame, border_width=True,
                                pad=(30,0), relief="raised")],
                #   [sg.T('See how you are doing here')],
                  [sg.T('Your transactions show up here as a list: ', key='mshowlistskey',
                            size=(40,1), pad=(0,(50,20))
                             )],
                    [sg.Table(values=transaction_list, 
                                headings=headlines,
                                display_row_numbers=True,
                                auto_size_columns=False,
                                num_rows=min(25, 14),
                                key='mtablekey') ] ]


# Main layout: 3RD COLUMN
third_column = [ [sg.CalendarButton(date_format, button_color=sg.TRANSPARENT_BUTTON, 
                    image_filename='images\\calendar.png', font=('Roboto', 10), bind_return_key=True,
                    image_size=(119,29), image_subsample=1, border_width=False, pad=((0,58),10),
                    key='mshowdatekey', target='minvisiblekey', format=("%b %d, %Y")),
                 sg.In(key='minvisiblekey', enable_events=True, do_not_clear=False, visible=False)], 
                [sg.Column(layout_calendar, pad=((100,0),0), key='third_column_for_cal' )] ]

# Main layout
layout_mainwin = [ [sg.Menu(menu_list, tearoff=True)],
                    [
                     sg.Column(second_column, 
                            element_justification='left', 
                            size=(750,550),
                            pad=(10, 8) 
                            # background_color='red'
                            ),
                        # sg.Frame('', first_column_frame, background_color='red',
                        #     element_justification='left', 
                        #     relief='sunken', 
                        #     border_width=False),
                     sg.Column(third_column, 
                            element_justification='right', 
                            size=(430,350))],
                     
                    [sg.T('Made in ' + str(get_time.year), 
                            size=(15,1), pad=(0,30), 
                            font=('Roboto', 7), 
                            justification='left')]  ]
# -----------MAIN LAYOUT END---------------------------------------------





# --------------EXPORT WINDOW LAYOUT---------------------------------------- #
# Export window: 5th Column has - 3 texts, 2 calendar buttons, 1 combobox drop down, 2 buttons(Ok, Cancel) 
column_for_export_window =  [   [sg.T('Start Date:', size=(10,1), pad=(10,0)), 
                 sg.CalendarButton(date_export, button_color=sg.TRANSPARENT_BUTTON, bind_return_key=True,
                                image_filename='images\\general.png', font=('Roboto', 10),
                                image_size=(140,34), image_subsample=1, border_width=False,
                                key='efromdatekey', target='einvisiblefromkey', format=("%Y-%m-%d")), 
                 sg.In(key='einvisiblefromkey', enable_events=True, default_text=date_export, visible=False)],
                [sg.T('End Date:', size=(10,1), pad=(10,0)), 
                 sg.CalendarButton(date_export, button_color=sg.TRANSPARENT_BUTTON, bind_return_key=True, 
                                image_filename='images\\general.png', font=('Roboto', 10),
                                image_size=(140,34), image_subsample=1, border_width=False,
                                key='etodatekey', target='einvisibletokey', format=("%Y-%m-%d")),
                 sg.In(key='einvisibletokey', enable_events=True, default_text=date_export, visible=False)],
                [sg.T('File Format:', size=(10,1), pad=(10,0)), sg.Combo(('.csv', '.xlsx'), size=(13,1), 
                    default_value='.csv', key='efileformatkey', readonly=True)],
                #  [sg.FileSaveAs('  Save as  ', target='einsaveaskey', key='esaveaskey', 
                #                 button_color=('white','black'), 
                #                 file_types=(('CSV', '.csv'),('Excel files', '*.xlsx .xls'),))],
                # [sg.In(key='einsaveaskey', size=(28,1), disabled=True, pad=(10,3))], 
                [sg.B('Save', key='eokkey', pad=(10,30), button_color=sg.TRANSPARENT_BUTTON, 
                                image_filename='images\\okcancel.png', font=('Roboto', 11),
                                image_size=(100,36), image_subsample=1, border_width=False),
                 sg.B('Close', key='ecancelkey', button_color=sg.TRANSPARENT_BUTTON, 
                                image_filename='images\\okcancel.png', font=('Roboto', 11),
                                image_size=(100,36), image_subsample=1, border_width=False)] ]
#---------------EXPORT WINDOW LAYOUT END-------------------------------------------#



# ---------------ADD WINDOW LAYOUT------------------------------------------------- #
# Add window: Two Lisboxes layouts have - values to choose transaction's Category
listbox_expenses = ['Food', 'Shopping', 'Transportation', 'Bills', 'Home', 'Car', 'Entertainment', 
                    'Clothing', 'Insurance', 'Tax', 'Telephone', 'Cigarette', 'Health', 'Sport',
                    'Baby', 'Pet', 'Beauty', 'Electronics', 'Hamburger', 'Wine', 'Vegetables',
                    'Snacks', 'Gift', 'Social', 'Travel', 'Education', 'Fruits', 'Book', 'Office',
                    'Others']
listbox_income = ['Salary', 'Awards', 'Grants', 'Sale', 'Rental', 'Refunds', 'Coupons', 
                    'Lottery', 'Dividends', 'Investments', 'Others']

listbox_expenses.sort() # sorting list values in expenses listbox
listbox_income.sort()   # sorting list values in income listbox


# Add window: 6th Column for Add Window Layout
column_for_add_window = [ [sg.T('Add a new transaction into the list')],
            [sg.T('Choose date: ', size=(30,1), pad=(5,0)), 
             sg.CalendarButton(date_export, button_color=sg.TRANSPARENT_BUTTON, 
                    image_filename='images\\general.png', font=('Roboto', 10),
                    image_size=(140,34), image_subsample=1, border_width=False, target='ainvisiblekey',
                    key='adatekey', format=("%Y-%m-%d")),
             sg.In(key='ainvisiblekey', enable_events=True, default_text=date_export, visible=False)],
            [sg.T('Choose type: ', size=(30,1), pad=(5,0)), 
             sg.Combo(('Income', 'Expenses'), size=(13,1), readonly=True,
                    default_value='Expenses', key='atypekey', enable_events=True)],
            [sg.T('Choose category ', size=(30,1), pad=(5,0)), 
             sg.Listbox(values=(listbox_expenses), default_values=(listbox_expenses[0]),
                    key='acategorykey', size=(14, 10), enable_events=True, bind_return_key=True)],
            [sg.T('', size=(30,1), pad=(5,0)), 
             sg.B('Add category', key='ausercategory', button_color=sg.TRANSPARENT_BUTTON, 
                    image_filename='images\\general.png', font=('Roboto', 10),
                    image_size=(140,34), image_subsample=1, border_width=False)],
            [sg.T('Paid amount: ', size=(30,1), pad=(5,0)), 
             sg.In(1000, size=(16,1), text_color='grey', 
                key='aamountkey')],
            [sg.T('Write a memo: ', size=(30,1), pad=(5,0)), 
             sg.In('Ex: Paid taxes', size=(16,1), text_color='grey', 
                key='amemokey')], 
            [sg.B('Add', key='aaddkey', pad=(5,30), button_color=sg.TRANSPARENT_BUTTON, 
                    image_filename='images\\okcancel.png', font=('Roboto', 11),
                    image_size=(100,36), image_subsample=1, border_width=False), 
             sg.CButton('Close', key='acancelkey', pad=(5,5), button_color=sg.TRANSPARENT_BUTTON, 
                    image_filename='images\\okcancel.png', font=('Roboto', 11),
                    image_size=(100,36), image_subsample=1, border_width=False)] ]
#--------------------ADD WINDOW LAYOUT END-----------------------------------------------#



# MAIN WINDOW CREATION #
in_mainwin = sg.Window('Capital Management', layout_mainwin,  border_depth=True, grab_anywhere=False, 
                        font=("Roboto", 12), icon='images\\app_icon16x16.ico',
                        use_default_focus=False, resizable=True).Finalize()




# FLAGS # 
# Setting flags to check which window is currently opened
mainWIN_OPENED = True
exportWIN_OPENED = False
addWIN_OPENED = False
writecatWIN_OPENED = False



in_mainwin.Maximize()



key_is = 1
in_mainwin[today](button_color=('white', '#4285F4'))
col_row = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,
            31,32,33,34,35,36,37,38,39,40,41,42,43]


# ------------------WHILE LOOP EVENTS------------------------------------- #
# To run every window and handle events caused by a user
while True:


    # GET MAIN WINDOW EVENTS AND ITS VALUES
    mainwin_event, mainwin_values = in_mainwin.read(timeout=100)

    # close main window
    if mainwin_event in (None, 'Exit'):
        break
    
    if mainwin_event is not None:
        # set variables if there is any here
        try:
            if mainwin_event in col_row:

                if key_is is not mainwin_event:
                    in_mainwin[key_is](button_color=('black', 'white'))
                    key_is = mainwin_event
                    # datetime.strptime(chosen, '%d %b, %Y') 
                in_mainwin[key_is](button_color=('#4285F4', '#DDD5FF'))
                chosen = current_month + ' ' +str(key_is) + ', ' + current_year

                in_mainwin['minvisiblekey'](chosen)
                in_mainwin[today](button_color=('white', '#4285F4'))

                if today is mainwin_event:
                    in_mainwin[today](button_color=('#DDD5FF', '#4285F4'))

                # key_is=1
                # sg.Popup('titile', 'which event key', event, values)
                # sg.Popup('no', 'no', mainwin_event, mainwin_values)

            # buttons clicked
            if mainwin_event == 'mincomebtnkey':
                in_mainwin['mshowincomeskey'](1)
                # in_mainwin['mshowincomeskey'](in_mainwin.GetScreenDimensions())

            if mainwin_event == 'mexpensesbtnkey':
                in_mainwin['mshowexpenseskey'](1)
                # in_mainwin.Move(10,10)

            if mainwin_event == 'mtotalsbtnkey':
                in_mainwin['mshowtotalskey'](1)
                # in_mainwin['mshowtotalskey'](in_mainwin.current_location())
                
            if mainwin_values['minvisiblekey']:
                in_mainwin['mshowdatekey'](mainwin_values['minvisiblekey'])
                # in_mainwin['mshowdatekey'](disabled=False)

            if mainwin_event == 'mshowdatekey':
                # in_mainwin['mshowdatekey'](disabled=True)
                sg.Popup('no', 'no', mainwin_event, mainwin_values)

            if mainwin_event == 'Import':
                # in_mainwin['mshowincomeskey'](5)
                table_example()
                # mainwin_event['mtablekey'](values=values_imported[1], headings=values_imported[0])
                # in_mainwin['mloginkey'](visible=False)   



            # EXPORT EVENT IN MAIN WINDOW #
            if not exportWIN_OPENED and mainwin_event == 'Save':

                # Opening the Export Window
                exportWIN_OPENED = True

                # Setting Export Window's layout
                layout_exportwin = [ [sg.Column(column_for_export_window, element_justification='center')] ]

                # EXPORT WINDOW CREATION #
                in_exportwin = sg.Window('Export form', layout_exportwin, icon='images\\app_icon16x16.ico',
                                        font=('Roboto', 12), use_default_focus=False)


            # ADD EVENT IN MAIN WINDOW
            if not addWIN_OPENED and mainwin_event == 'maddkey':
                
                # Opening the Add Window
                addWIN_OPENED = True # flag is activating the add window
                # in_mainwin['mloginkey'](visible=True) # login button shows up in the main window

                # Setting Add Window's layout
                layout_addwin = [ [sg.Column(column_for_add_window, element_justification='left')]  ]
                
                # ADD WINDOW CREATION #
                in_addwin = sg.Window('Add Transactions', layout_addwin, 
                                        icon='images\\app_icon16x16.ico', font=('Roboto', 12), 
                                        use_default_focus=False)
                # in_mainwin['mshowexpenseskey'](window.get_screen_size())
        except ValueError:
            sg.Popup('Error','Check entries and try again') 

    if addWIN_OPENED:
        # GET ADD WINDOW EVENTS AND ITS VALUES #
        addwin_event, addwin_values = in_addwin.read(timeout=100)
        # close add window
        if addwin_event in (None, 'Exit'):
            addWIN_OPENED = False
            in_addwin.close()
        if addwin_event is not None:
            try: 
                if addwin_event is 'ainvisiblekey':
                    in_addwin['adatekey'](addwin_values['ainvisiblekey'])      
                
                if addwin_event is 'atypekey':
                    if addwin_values['atypekey'] is 'Income':
                        in_addwin['acategorykey'](values=listbox_income)
                    if addwin_values['atypekey'] is 'Expenses':
                        in_addwin['acategorykey'](values=listbox_expenses)

                if addwin_event is 'acancelkey':
                    addWIN_OPENED = False
                    in_addwin.close()

                if addwin_event == 'aaddkey':
                    # zip - iterate through two lists in parallel in a for loop
                    # https://stackoverflow.com/questions/1663807/how-to-iterate-through-two-lists-in-parallel
                    
                    for (i, j) in zip(headlines, headline_keys): 
                        transaction_details[i] = (addwin_values[j])
                        # tables_list.append = (addwin_values[j])
                        # print(transaction_details)
                    transaction_list.append(dict(transaction_details))
                    
                    # How to sort list of dictionaries: (with 'operator's itemgetter) - ascending or descending
                    # https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
                    sortedlist = sorted(transaction_list, key = itemgetter('Date'), reverse=True)
                    print()
                    print('transaction_list: list[dict, dict, dict, ...]')
                    print(transaction_list)
                    # https://stackoverflow.com/questions/20891141/convert-list-of-dicts-to-list
                    full=[]
                    chosen_date=[]
                    for field in sortedlist:
                        # reference: stackoverflow.com/questions/16228248/how-can-i-get-list-of-values-from-dict
                        full.append(list(field.values()))
                        # chosen_date.append(field['Date'])
                    print()
                    print('full: list[list, list, ...]')
                    print(full)
                    print()
                    print('HOW TO GET DIFFERENT PERIOD FOR DATES: ')
                    # print(chosen_date)
                    
                    in_mainwin['mtablekey'](values=full)
                    
                    # in_addwin.close()
                
        #     in_addwin.close()
                if not writecatWIN_OPENED and addwin_event is 'ausercategory':
    
                    writecatWIN_OPENED = True
                    layout_writecatwin = [ [sg.T('Write your own category:', size=(25,1), justification='center')], 
                                            [sg.Multiline(' ', pad=(10,10), key='wcinnamekey', 
                                                    text_color='grey', enable_events=True, size=(15,3),
                                                    enter_submits=True ), 
                                                    sg.T(' ', key='wcoutputkey', size=(15,3))],
                                            [sg.B('Ok', key='wcokkey', pad=((75,5),30), 
                                                    button_color=sg.TRANSPARENT_BUTTON, 
                                                    image_filename='images\\okcancel.png', 
                                                    font=('Roboto', 11),
                                                    image_size=(100,36), image_subsample=1, 
                                                    border_width=False), 
                                                sg.B('Cancel', key='wccancelkey', button_color=sg.TRANSPARENT_BUTTON, 
                                                        image_filename='images\\okcancel.png', 
                                                        font=('Roboto', 11),
                                                        image_size=(100,36), image_subsample=1, 
                                                        border_width=False, pad=(5,5))] ]
                    
                    if addwin_values['atypekey'] is 'Income':
                        in_writecatwin = sg.Window('Add income category', layout_writecatwin, 
                                                icon='images\\app_icon16x16.ico', font=('Roboto', 11))
                    if addwin_values['atypekey'] is 'Expenses': 
                        in_writecatwin = sg.Window('Add expense category', layout_writecatwin, 
                                                icon='images\\app_icon16x16.ico', font=('Roboto', 11))
                
            except ValueError:
                sg.Popup('Error','Check entries and try again') 

        if writecatWIN_OPENED:
            # GET ADD WINDOW EVENTS AND ITS VALUES #
            writecatwin_event, writecatwin_values = in_writecatwin.read(timeout=100)
            
            # close add window
            if writecatwin_event in (None, 'Exit', 'wccancelkey'):
                writecatWIN_OPENED = False
                in_writecatwin.close()

            if writecatwin_event is not None:
                try:
                    if writecatwin_event is 'wcinnamekey':
                        in_writecatwin['wcoutputkey'](writecatwin_values['wcinnamekey'])

                    if writecatwin_event is 'wcokkey':
    
                        if addwin_values['atypekey'] is 'Income':
                            listbox_income.append(writecatwin_values['wcinnamekey'])
                            listbox_income.sort()
                            in_addwin['acategorykey'](values=listbox_income)
                            sg.Popup('title', 'content', 'main: event and values', mainwin_event, mainwin_values, 
                                'export: event and values', exportwin_event, exportwin_values, 
                                'add: event and values', addwin_event, addwin_values)
                            in_writecatwin.close()

                        else:
                            listbox_expenses.append(writecatwin_values['wcinnamekey'])
                            listbox_expenses.sort()
                            in_addwin['acategorykey'](values=listbox_expenses)
                            in_writecatwin.close()

                        in_writecatwin.close()

                except ValueError:
                    sg.Popup('Error','Check entries and try again') 

            #------------WRITE YOUR OWN CATEGORY WINDOW CLOSES------------------------------#

        #--------------ADD WINDOW CLOSES--------------------------------------------#




    if exportWIN_OPENED:
        # GET EXPORT WINDOW EVENTS AND ITS VALUES #
        exportwin_event, exportwin_values = in_exportwin.read(timeout=100)

        # Close export window
        if exportwin_event in (None, 'Exit', 'ecancelkey'):
            exportWIN_OPENED = False
            in_exportwin.close()

        if exportwin_event is not None:
            # creating a path for this file
            # repository for below line: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/ProgrammingClassExamples/MacOS%20versions/7c%20PSG%20(add%20get%20pathname%20to%20save%20and%20retrieve%20files).py
            
            # directory, filename = os.path.split(os.path.abspath(__file__))
            # adding period name to filename path
            # path = os.path.join(directory) 
            
            try: 
                if exportwin_event is 'einvisiblefromkey':
                    in_exportwin['efromdatekey'](exportwin_values['einvisiblefromkey'])
                
                if exportwin_event is 'einvisibletokey':
                    in_exportwin['etodatekey'](exportwin_values['einvisibletokey'])

                if exportwin_event == 'eokkey':
                    
                    # file_type = exportwin_values['efileformatkey']
                    name_file = exportwin_values['einvisiblefromkey'] + '-' + exportwin_values['einvisibletokey'] + exportwin_values['efileformatkey']
                    start_date = exportwin_values['einvisiblefromkey']
                    end_date = exportwin_values['einvisibletokey']
                    
                    # print(file_type)
                    # print(period)
                    # print(period+file_type)
                    # Calling 'create_file()' function from 'export_file' module 
                    # to create a new file with 4 parameters to the function 
                    export_file.create_file(start_date, end_date, headlines, sortedlist, name_file)
            
            except ValueError:
                sg.Popup('Error','Check entries and try again') 
            
            # in_exportwin.close()
    
   #     in_exportwin.close()
    #---------------EXPORT FORM WINDOW CLOSES------------------------------#
                
# ---------------------------WHILE LOOP ENDS--------------------------------------------#          


# CLOSE WINDOW
in_mainwin.close()
# sg.Popup('Title', event_list, event, icon='images\\budget_manager_app_icon20x20.ico')


