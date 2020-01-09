# ------------------------------- IMPORT PACKAGES ---------------------------------#

import csv
import os
# from tempfile import NamedTemporaryFile
# import shutil
# import sys
from pathlib import Path
import datetime



# ------------------------------- GET ALL THE TRANSACTIONS BETWEEN TWO DATES GIVEN BY USER -----------#

# https://stackoverflow.com/questions/6899101/select-a-range-of-dates-in-python-dictionary
# returns list[dict, dict, dict, ...] just cut from sorted list 
def get_range_dates(sortedlist, start_date, end_date):

    range_list=[]

    for field in sortedlist:

        if start_date <= field['Date'] <= end_date:
            range_list.append(dict(field))
            
    # print('RANGE LIST STARTS HERE: \n', range_list)
    return range_list        




# ------------------------------- SAVE FILE AS CSV/EXCEL IN THE NEWLY CREATED CAPITAL FOLDER ---------#

# fieldnames = ['Date', 'Income/Expenses', 'Category', 'Memo', 'Amount'] or headlines parameter
def create_file(start_date, end_date, headlines, sortedlist, name_file):

    # To get transactions only within range(start_date, end_date) in sorted list 
    # format: list[dict, dict, dict, ...]
    my_range = get_range_dates(sortedlist, start_date, end_date)

    # FOLDER CREATION IF NOT EXIST: 
    # REPOSITORY for a line below: https://www.bogotobogo.com/python/python_files.php
    foldername = os.path.join(os.path.expanduser('~'), 'Documents', 'Capital')

    # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
    Path(foldername).mkdir(parents = True, exist_ok=True)
    
    # REPOSITORY for a line below: https://www.bogotobogo.com/python/python_files.php
    pathname = os.path.join(foldername, name_file)
    # filename = rawfilename.replace('\\\\', '\\')
    
    with open(pathname, 'w', newline='') as new_file:

        csv_writer = csv.DictWriter(new_file, fieldnames=headlines)
        csv_writer.writeheader()

        # for head in headlines:
        csv_writer.writerows(my_range)