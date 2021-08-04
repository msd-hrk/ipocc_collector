import requests
from bs4 import BeautifulSoup
import re
import datetime
from collector import utils
from logging import config,getLogger

class YahooDetailCollector():
    def __init__(self, securities_no):
        config.fileConfig('log/logging.conf')
        self.logger = getLogger()
        yahoo_page = 'https://www.traders.co.jp/ipo_info/schedule/ipo_info.asp?no=' + securities_no
        html = requests.get(yahoo_page)
        soup = BeautifulSoup(html.content, 'html.parser')
        self.logger.debug("データ取得先：%s", yahoo_page)

        self.table = soup.select(".IPO_PAGE")
    
    def get_business(self):
        tr = self.table[0].select("tr")[2]
        business = tr.select("td")[1].get_text()
        return business
    
    def get_web(self):
        tr = self.table[0].select("tr")[12]
        web = tr.select("a")[0].get_text()
        return web
    
    def get_build(self):
        tr = self.table[0].select("tr")[15]
        td = tr.select("td")[1].get_text()
        build = utils.del_str(td, "年")
        return build
    
    def get_employee(self):
        tr = self.table[0].select("tr")[16]
        td = tr.select("td")[1].get_text()
        num = re.search(r'\d*人', str(td)).group()
        age = re.search(r'平均.*歳', str(td)).group()
        salary = re.search(r'年収.*万', str(td)).group()
        employee = {
            "num": int(utils.del_str(num, "人")),
            "age": int(round(float(utils.del_str(age, "歳","平均")), 0)),
            "salary": int(round(float(utils.del_str(salary, "年収","万")), 0)),
        }
        return employee
    
    def get_holder_num(self):
        tr = self.table[0].select("tr")[17]
        td = tr.select("td")[1].get_text()
        num = re.search(r'\d*人', str(td)).group()
        holder_num = int(utils.del_str(num, "人"))
        return holder_num
    
    def get_capital(self):
        tr = self.table[0].select("tr")[18]
        td = tr.select("td")[1].get_text()
        num = re.search(r'.*円', str(td)).group()
        capital = int(utils.del_str(num, "円", ","))
        return capital
