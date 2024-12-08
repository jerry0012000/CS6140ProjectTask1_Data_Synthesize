Overview

This script automates the integration of Principal Component (PC) data from a CSV file into a TXT file, ensuring that each date in the TXT file is appropriately matched with the PC values based on quarterly financial report dates. It is designed to handle datasets where companies report data on different dates, dynamically matching and appending Principal Component 1 and 2 values to the TXT file.
Features

    Dynamic Date Matching: Ensures that each row in the TXT file is assigned the correct Principal Component data based on the corresponding company's financial report release date.
    Flexible File Selection: Allows users to select the TXT and CSV files through a graphical file dialog.
    Automated Data Integration: Reads, processes, and appends new columns (Principal Component 1 and 2) to the TXT file.
    Version Control: Generates a new, timestamped TXT file to preserve the original data.
    Sorted Results: The updated TXT file is sorted by date in descending order for consistency.

How It Works

    Input Files:
        TXT File: Contains dates and other data to which the Principal Components will be added.
        CSV File: Contains dates and corresponding Principal Component 1 and 2 values. Dates in the CSV are assumed to be in descending order.
    Process:
        The script reads the CSV file, extracts and sorts the Principal Component data.
        For each date in the TXT file:
            If the date corresponds to a financial report period, the PC values from the CSV are appended.
            If the date falls outside the report range, placeholders ("None") are added.
        New dates from the CSV file that do not exist in the TXT file are appended with their respective PC values.
    Output:
        A new TXT file is generated with the additional columns for Principal Component 1 and 2, ensuring data integrity and separation.

Usage Instructions

    Run the Script:
        Ensure you have Python installed with the required libraries (tkinter, csv, and datetime).
        Execute the script using python AddComponents.py.
    File Selection:
        A dialog box will appear for selecting the TXT file. Choose the desired file.
        A second dialog box will appear for selecting the CSV file. Choose the file containing Principal Component data.
    Output File:
        The script will generate a new TXT file in the same directory as the original file, with a timestamp in the filename (e.g., data_20241207_103015.txt).
