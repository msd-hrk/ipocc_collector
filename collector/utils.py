import datetime
import requests
from bs4 import BeautifulSoup
import re
from dateutil.relativedelta import relativedelta


def convesion_date_format(mm_slush_dd):
    now = datetime.date.today()
    year = now.year
    month = mm_slush_dd.split('/')[0]
    day = mm_slush_dd.split('/')[1]
    yyyymmdd = datetime.date(now.year, int(month), int(day)).strftime("%Y%m%d")
    return yyyymmdd

def delete_canma(with_canma):
    del_canma = str(with_canma).replace(",","")
    return del_canma

def convert_yyyymm(yyyy_year_m_month):
    array = str(yyyy_year_m_month).split("年")
    month = array[1]
    m = month.replace("月","")
    if len(m) < 2:
        m = "0" + m
    return array[0] + m

def counter_column(table_data):
    counter = 1
    for i in range(1, len(table_data), 1):
        if re.search(r'\d', table_data[i].get_text()) is None:
            counter = counter + 1 
    return counter

def arange_data(str_data):
    return str(str_data).replace(" ","").replace("　","").replace("\r\n","").replace("\n","")

def del_str(before_data, *args):
    target = before_data
    for item in args:
        target = str(target).replace(item, "")
    return target

def int_check(target):
    try:
        int(target)
        return True
    except Exception:
        return False

def float_check(target):
    try:
        float(target)
        return True
    except Exception:
        return False

def del_jp_price(target):
    price = str(target)
    flg_dot = False
    flg_10000 = False
    
    # "."があるか（7.5万　2万　1500）
    if re.search(r"\.", price):
        flg_dot = True
        price = price.replace(".","")
    
    if re.search(r"万", price):
        flg_10000 = True
        price = price.replace("万","")
    
    price = del_str(price, ",", "円")
    if flg_10000:
        if flg_dot:
            price = price.__add__("000")
        else:
            price = price.__add__("0000")
    
    return price

def check_exist_key(data, key):
    try:
        data[key]
        return True
    except Exception:
        return False

def check_work_day():
    now = datetime.date.today()
    workday_int = int(now.strftime("%Y%m%d"))

    yahoo_page = 'https://finance.yahoo.co.jp/quote/9434.T'
    html = requests.get(yahoo_page)
    soup = BeautifulSoup(html.content, 'html.parser')
    span = soup.select("._6wHOvL5")[6].get_text()
    array = del_str(str(span), "(", ")").split("/")
    before_workday = datetime.date(now.year, int(array[0]), int(array[1])).strftime("%Y%m%d")

    if workday_int == int(before_workday):
        return True
    else:
        return False

def day_to_int(day):
    return int(day.strftime("%Y%m%d"))
    
def get_today():
    now = datetime.date.today()
    return int(now.strftime("%Y%m%d"))

def str_to_int(str_yyyymmdd):
    return int(str_yyyymmdd)