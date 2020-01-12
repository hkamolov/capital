# Capital Management for a Family

<img src="images/logo-capital.png" width="200" >


## Capital Desktop Application that Helps Families Track Their Expenses, Income, and Balance Sheets Daily

![Capital-Logo](screenshots/10.%20last%20view.png)


## Class Project

Languages:  `Python` 

Frameworks: `PySimpleGUI`


![pysimplegui_logo](https://user-images.githubusercontent.com/13696193/43165867-fe02e3b2-8f62-11e8-9fd0-cc7c86b11772.png)


## Requirements

To use the program you will need to install PySimpleGUI (http://www.PySimpleGUI.org for instructions)

One of these will install it for you:
```
pip install PySimpleGUI
pip3 install PySimpleGUI
```


## Running

Once the packages are installed, put these two files - `capital.py`, `export_file.py` and a folder - `images` found in this repository  in the same directory and you only need to run the single Python file - `capital.py`


## Functionalities of the Program:

For now app has functionalities for:

- adding new transactions with `Add Transaction` button in the main window.
- saving newly added transactions as a `CSV` or `Excel` file into `\...\Documents\Capital` folder with `Save` button from the menu `File`.
- importing saved transaction files with `Import` button from the menu `File`.


## More details

Finally, what has been done in the final program until now:

DONE:

### 1. Adding transactions with details (date, income/expenses, category, memo, amount) -> `Add Transaction` button in the main window


![capital-add-transaction](screenshots/2.%20add%20a%20new%20transaction.png)


![capital-add-transaction](screenshots/3.%20add%20a%20new%20transaction%202.png)



### 2. File creation (CSV, Excel) -> `Save` button from the menu `File`


![capital-save-transactions](screenshots/5.%20saving%20added%20transactions.png)


![capital-save-transactions](screenshots/6.%20saving%20(in%20export%20form)%20as%20a%20CSV_Excel%20file.png)



### 3. Importing files that were created by the Capital app -> `Import` button from the menu `File`


![capital-save-transactions](screenshots/7.%20importing%20an%20existing%20file%20from%20Capital%20folder.png)


![capital-save-transactions](screenshots/8.%20choosing%20an%20existing%20CSV%20file%20to%20import.png)


![capital-save-transactions](screenshots/9.%20result%20of%20importing%20the%20CSV%20file.png)



### 4. Showing added transactions in main window list


![capital-save-transactions](screenshots/4.%20added%20transactions%20in%20main%20window.png)



### 5. Showing calendar inside the main window


![capital-save-transactions](screenshots/1.%20main%20window.png)



UNDONE:
```
6.  analytics page (diagrams for [income/expenses])
7.  yearly, monthly daily targets
8.  welcome page with icon
9.  make .exe file
10. Notification alarm
```
