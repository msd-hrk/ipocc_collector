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
        yahoo_page = 'https://www.traders.co.jp/ipo/' + securities_no
        html = requests.get(yahoo_page)
        soup = BeautifulSoup(html.content, 'html.parser')
        self.logger.debug("データ取得先：%s", yahoo_page)
        self.base_info = None
        self.bussiness_detail = None
        zone =  soup.select(".zone")
        for i in range(0, len(zone), 1):
            zone_title = zone[i].select(".zone_title")
            if len(zone_title) == 0:
                # 値が存在しない場合は次へ
                continue
            title_str = utils.arange_data(zone_title[0].get_text())
            if title_str == "基本情報":
                self.base_info = zone[i].select("table")
            if title_str == "事業詳細":
                self.bussiness_detail = zone[i].select(".ipo_comment_container")
                
    def get_business(self):
        tr = self.base_info[0].select("tr")[4]
        business = tr.select("td")[0].get_text()
        return business

    def get_business_detail(self):
        buss_detail = self.bussiness_detail[0].get_text()
        return utils.del_str(buss_detail, "<br>")
    
    def get_web(self):
        tr = self.base_info[0].select("tr")[5]
        web = tr.select("a")[0].get_text()
        return web
    
    def get_build(self):
        tr = self.base_info[0].select("tr")[2]
        td = tr.select("td")[0].get_text()
        build = utils.del_str(td, "年")
        return build
    
    def get_employee(self):
        tr = self.base_info[0].select("tr")[3]
        td = tr.select("td")[0].get_text()
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
        tr = self.base_info[0].select("tr")[6]
        td = tr.select("td")[0].get_text()
        num = re.search(r'\d*人', str(td)).group()
        holder_num = int(utils.del_str(num, "人"))
        return holder_num
    
    def get_capital(self):
        tr = self.base_info[0].select("tr")[7]
        td = tr.select("td")[0].get_text()
        num = re.search(r'.*円', str(td)).group()
        capital = int(utils.del_str(num, "円", ","))
        return capital
