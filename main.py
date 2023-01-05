from scraper import setupWebDriver, getKarlilikData, getCarpanlarData, initializeDataframe
from selenium.webdriver.common.by import By
import time


URL = "https://www.halkyatirim.com.tr/skorkart/"

karlilik_features = ["brut_kar_marj_ceyrek", "brut_kar_marj_yil", "faaliyet_gider_marj_ceyrek", "faaliyet_gider_marj_yil",
                     "favok_marj_ceyrek", "favok_marj_yil", "net_kar_marj_ceyrek", "net_kar_marj_yil", "ozsermaye_karlilik",
                     "aktif_karlilik", "netborc_favok", "netfinansmangelir_favok", "netborc_nbartiozsermaye"]

carpanlar_features = ["fiyat", "piyasa_degeri", "fk", "pd_dd", "fd_favok", "fd_satislar", "hbk", "hbk_yil",
                      "hbtemettu", "temettu_verim", "alacak_tahsil", "borc_odeme_gun", "stok_tutma_suresi"]

#karlilik_features_indices = [1,2,5,6,7,8,9,11] 

bist30_tickers = ["AKSEN", "ARCLK", "ASELS", "BIMAS", "DOHOL", "EKGYO",
                  "EREGL", "FROTO", "GUBRF", "KRDMD", "KCHOL", "KOZAL",
                  "KOZAA", "ODAS",  "PGSUS", "PETKM", "SAHOL", "SASA",
                  "SISE",  "TAVHL", "TKFEN", "THYAO", "TOASO", "TUPRS",
                  "TTKOM", "TCELL", "VESTL"]



def main():
    karlilik_df = initializeDataframe(karlilik_features)
    carpanlar_df = initializeDataframe(carpanlar_features)

    driver = setupWebDriver()
    driver.get(URL)
    driver.implicitly_wait(5)
    time.sleep(10)

    for ticker in bist30_tickers:
        element_tickers = driver.find_element(By.ID, "DropDownEnstrumanKodu")
        all_options_tickers = element_tickers.find_elements(By.TAG_NAME, "option")

        for option in all_options_tickers:
            if (option.get_attribute("value") == ticker):
                option.click()
                print(f"Ticker {ticker} is found.")
                break
        
        time.sleep(10)

        element_quarters = driver.find_element(By.ID, "DropDownHesapDonem")
        all_options_quarters = element_quarters.find_elements(By.TAG_NAME, "option")

        available_quarters = []

        for option in all_options_quarters:
            #print(f'Quarter: {option.get_attribute("value")}')
            available_quarters.append(option.get_attribute("value"))

        last_quarter = available_quarters[0]
        while (last_quarter != available_quarters[len(available_quarters) - 1]):
            curr = 0
            for i in range(len(available_quarters)):
                if (last_quarter == available_quarters[i]):
                    curr = i + 1

            all_options_quarters[curr].click()
            time.sleep(10)

            karlilik_df, last_quarter = getKarlilikData(driver, karlilik_df, ticker)
            carpanlar_df, _ = getCarpanlarData(driver, carpanlar_df, ticker)
            print(f"Ticker: {ticker}, last quarter fetched: {last_quarter}")
        print(f"Scraping data for the ticker {ticker} is finished.\n\n")

    karlilik_df.to_csv("karlilik_bist30.csv")
    carpanlar_df.to_csv("carpanlar_bist30.csv")

if __name__ == "__main__":
    main()