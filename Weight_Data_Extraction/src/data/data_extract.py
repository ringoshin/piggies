#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:38:53 2019

@author: ringoshin
"""

import re
import pandas as pd
from bs4 import BeautifulSoup


def Is_Date(text):
    """
    Perform simple validation if text is a date value
    """
    # Find date values in this format: dd mmmm yyyy
    match = re.search(r'(\d\d?) (\w+) (\d{4})', text)
    
    # Return a formatted date if it is one, else just empty str
    if match:
        date = '-'.join([match.group(1), match.group(2).capitalize(), match.group(3)])
    else:
        date = ''
    return match, date
        
    
def Get_Name_Weight(text):
    """
    Identify the piggy name and its weight from the text.
    Return name and weight
    """
    # Looking for single or double name, follows by weight in grams
    match = re.search(r"([a-zA-Z ]+)\s(\d+)", text)
    return match.group(1), match.group(2)

def ExtractReqFields(text_list):
    """
    Go through all strings in the list and extract only the dates, names and weights.
    A Pandas Dataframe is returned
    """
    cur_date = ''
    date_list, name_list, weight_list = [], [], []
    
    # Generate lists keeping track of each weight logged per name and date
    for text in text_list:
        is_date, date = Is_Date(text)
        if is_date:
            cur_date = date
        else:
            name, weight = Get_Name_Weight(text)
            date_list.append(cur_date)
            name_list.append(name)
            weight_list.append(weight)
            
    return pd.DataFrame({'date': date_list, 'name': name_list,
                         'weight': weight_list})

def ExtractFromHTMLFiles():
    """
    1. Read HTML files under 'data/raw' folder
    2. For each file, identify dates, piggy names and weights
    3. Save in a database format and return it
    """
    soup = BeautifulSoup(open("../../data/raw/Piggies weight - 2019.html"), "html.parser")
    # print(soup.prettify())

    # Filter only text strings and replace all char 160 with a space
    text_list = [div.text.replace(u'\xa0', u' ') for div in soup.find_all('div') if div.text]
    return ExtractReqFields(text_list[2:])
    

def main():
    piggy_data = ExtractFromHTMLFiles()
    print(piggy_data)

    
if __name__ == "__main__":
    main()