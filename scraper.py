from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

def setupWebDriver() -> webdriver.Chrome: 
    options = Options()
    options.headless = True

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver


def getKarlilikData(driver : webdriver.Chrome, df : pd.DataFrame, ticker : str):
    karlilik_table = driver.find_element(By.ID, "TBLFINANSALVERİLER2")
    karlilik_table_body = karlilik_table.find_element(By.TAG_NAME, "tbody")
    karlilik_table_rows = karlilik_table_body.find_elements(By.TAG_NAME, "tr")

    for i, row in enumerate(karlilik_table_rows):
        karlilik_table_cols = row.find_elements(By.TAG_NAME, "td")
        if (karlilik_table_cols[0].text[0] != '2' and karlilik_table_cols[0].text[0] != '1'):
            break
        quarter = karlilik_table_cols[0].text
        data_row = [ticker, quarter]

        for j, col in enumerate(karlilik_table_cols):
            if (j != 0):
                try:
                    data_row.append(float(col.text))
                except:
                    data_row.append(col.text)

        df.loc[len(df)] = data_row
    
    return df, quarter

def getCarpanlarData(driver : webdriver.Chrome, df : pd.DataFrame, ticker : str):
    carpanlar_table = driver.find_element(By.ID, "TBLFINANSALVERİLER1")
    carpanlar_table_body = carpanlar_table.find_element(By.TAG_NAME, "tbody")
    carpanlar_table_rows = carpanlar_table_body.find_elements(By.TAG_NAME, "tr")

    for i, row in enumerate(carpanlar_table_rows):
        carpanlar_table_cols = row.find_elements(By.TAG_NAME, "td")
        if (carpanlar_table_cols[0].text[0] != '2' and carpanlar_table_cols[0].text[0] != '1'):
            break
        quarter = carpanlar_table_cols[0].text
        data_row = [ticker, quarter]

        for j, col in enumerate(carpanlar_table_cols):
            if (j != 0):
                try:
                    data_row.append(float(col.text))
                except:
                    data_row.append(col.text)

        df.loc[len(df)] = data_row
    
    return df, quarter


def initializeDataframe(selected_features):
    cols = ["ticker", "quarter"] + selected_features
    df = pd.DataFrame(columns=cols)

    return df
