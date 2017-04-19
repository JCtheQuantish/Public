# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 12:15:16 2017

@author: Jeff Cribbett, JeffCribbett@gmail.com
"""

# SimVest Interface

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time


def SelInit():
    driver = webdriver.Chrome()

    return driver


def SimVestLogin(driver, SVUser, SVPass):
    driver.get('http://www.simvest.com')
    liun = driver.find_element_by_xpath('//*[@id="mod_login_username"]')
    liun.send_keys(SVUser)
    time.sleep(1)
    paun = driver.find_element_by_xpath('//*[@id="mod_login_password"]')
    paun.send_keys(SVPass)
    liun.submit()

    return driver


def SVPortfolio(driver, PortName):
    if PortName == '':
        Pnum = 0

    driver.get('http://www.simvest.com/trading/account.php?portid='+str(Pnum))

    CashAvail = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[3]/tbody/tr/td[2]/div').text
    CashAvail1 = CashAvail.replace('$', '').replace(',', '')
    CashAvail = float(CashAvail1)
    print(CashAvail)
    NAV = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[3]/tbody/tr/td[5]/div').text
    NAV1 = NAV.replace('$', '').replace(',', '').replace('?', '')
    NAV = float(NAV1)
    print(NAV)
    PL = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[3]/tbody/tr/td[7]/div/div/span').text
    PL1 = PL.replace('$', '').replace(',', '')
    # PL = float(PL1)
    print(PL1)

    # Create List of Instruments Held
    IList = []
    LList = []
    SList = []
    VListP = []
    VListN = []
    TData = []

    try:
        for TR in range(2, 30):
            RowData = []
            I = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr['+str(TR)+']/td[1]/a[1]').text
            # print(I)
            # print(IList)
            IV = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr['+str(TR)+']/td[7]').text
            Q = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr['+str(TR)+']/td[2]').text
            E = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr['+str(TR)+']/td[3]').text
            L = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr['+str(TR)+']/td[4]/span').text
            DG = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr['+str(TR)+']/td[8]').text
            PG = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr['+str(TR)+']/td[9]').text
            CL = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/table[2]/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/div/span/table/tbody/tr['+str(TR)+']/td[10]/a').get_attribute('href')
            IList.append(I)
            RowData.append(I)
            RowData.append(IV)
            RowData.append(Q)
            RowData.append(E)
            RowData.append(L)
            RowData.append(DG)
            RowData.append(PG)
            RowData.append(CL)
            try:
                if RowData in TData:
                    pass
                else:
                    TData.append(RowData)
            except Exception:
                print('RD Fault')
            IV2 = IV.replace(',', '')
            if float(IV2) > 0:
                LList.append(I)
            else:
                SList.append(I)

    except Exception:
        print('No further TRs')

    print(TData)

    return driver, CashAvail, NAV, IList, LList, SList, TData


def SVTrade(driver, Stock, Units, Direction):
    driver.get('http://www.simvest.com/trading/trade.php')
    time.sleep(5)
    Sbox = driver.find_element_by_name('numsharesfield')
    Sbox.send_keys(Units)
    Symbox = driver.find_element_by_name('symbolfield')
    Symbox.send_keys(Stock)


    if Direction == 'Long':
        Dirb = driver.find_element_by_xpath('//*[@id="buy"]')
        Dirb.click()
    if Direction == 'Short':
        Dirb = driver.find_element_by_xpath('//*[@id="short"]')
        Dirb.click()
    if Direction == 'Sell':
        Dirb = driver.find_element_by_xpath('//*[@id="sell"]')
        Dirb.click()
    if Direction == 'Cover':
        Dirb = driver.find_element_by_xpath('//*[@id="cover"]')
        Dirb.click()

    Submitbutton = driver.find_element_by_xpath('//*[@id="tradeTable"]/tbody/tr/td/table[1]/tbody/tr[2]/td[4]/span/input')
    Submitbutton.click()

    time.sleep(10)

    S2button = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/form/div[1]/input[14]')
    S2button.click()

    return driver


def SVLimitTrade(driver, Stock, Units, Direction, Limit):
    driver.get('http://www.simvest.com/trading/trade.php')
    time.sleep(5)
    Sbox = driver.find_element_by_name('numsharesfield')
    Sbox.send_keys(Units)
    Symbox = driver.find_element_by_name('symbolfield')
    Symbox.send_keys(Stock)

    if Direction == 'Long':
        Dirb = driver.find_element_by_xpath('//*[@id="buy"]')
        Dirb.click()
    if Direction == 'Short':
        Dirb = driver.find_element_by_xpath('//*[@id="short"]')
        Dirb.click()
    if Direction == 'Sell':
        Dirb = driver.find_element_by_xpath('//*[@id="sell"]')
        Dirb.click()
    if Direction == 'Cover':
        Dirb = driver.find_element_by_xpath('//*[@id="cover"]')
        Dirb.click()

    OrderType = driver.find_element_by_xpath('//*[@id="orderTypeSelect"]')
    OrderType.select_by_index(2)

    LimitBox = driver.find_element_by_xpath('//*[@id="limitPriceField"]')
    Limit = str(Limit)
    LimitBox.send_keys(Limit)

    Submitbutton = driver.find_element_by_xpath('//*[@id="tradeTable"]/tbody/tr/td/table[1]/tbody/tr[2]/td[4]/span/input')
    Submitbutton.click()

    time.sleep(5)

    S2button = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/form/div[1]/input[14]')
    S2button.click()

    return driver


def SVClose(driver, PortName, Stock, TData):
    CLF = False
    while CLF is False:
        for R in TData:
            if Stock in R:
                print(R[7])
                CloseLink = R[7]
                CLF = True

    driver.get(CloseLink)
    time.sleep(2.5)

    Submitbutton = driver.find_element_by_xpath('//*[@id="tradeTable"]/tbody/tr/td/table[1]/tbody/tr[2]/td[4]/span/input')
    Submitbutton.click()

    S2button = driver.find_element_by_xpath('//*[@id="mainbody"]/div/div/div/div/div/div/table/tbody/tr/td[2]/div[1]/div/table[2]/tbody/tr/td/form/div[1]/input[14]')
    S2button.click()

    return driver


if __name__ == "__main__":
    pass
