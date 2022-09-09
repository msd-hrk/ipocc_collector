import requests
from bs4 import BeautifulSoup
import re
import datetime
from logging import config,getLogger
from collector import utils

class YahooCollector():
    def __init__(self, securities_no):
        config.fileConfig('log/logging.conf')
        self.logger = getLogger()

        url_1 = 'https://finance.yahoo.co.jp/quote/'+securities_no
        self.logger.info("%s", url_1)
        html = requests.get(url_1)
        soup = BeautifulSoup(html.content, 'html.parser')
        self.logger.debug("データ取得先：%s", url_1)
        
        self.realtime_block = soup.select("._1nb3c4wQ")[0] 
        self.basic_block = soup.select("#detail")[0]
        self.margin_block = soup.select("#margin")[0]

    def get_closing_price(self):
        price = self.realtime_block.select("header ._3rXWJKZF")[0].get_text()
        closing_price = int(utils.del_str(price, ","))
        return closing_price
    
    def get_open_price(self):
        o_b = self.basic_block.select("ul li")[1]
        price = o_b.select("dd ._3rXWJKZF")[0].get_text()
        open_price = int(utils.del_str(price, ","))
        return open_price
    
    def get_high_price(self):
        o_b = self.basic_block.select("ul li")[2]
        price = o_b.select("dd ._3rXWJKZF")[0].get_text()
        high_price = int(utils.del_str(price, ","))
        return high_price
    
    def get_low_price(self):
        o_b = self.basic_block.select("ul li")[3]
        price = o_b.select("dd ._3rXWJKZF")[0].get_text()
        low_price = int(utils.del_str(price, ","))
        return low_price
    
    def get_volume_price(self):
        o_b = self.basic_block.select("ul li")[4]
        price = o_b.select("dd ._3rXWJKZF")[0].get_text()
        volume_price = int(utils.del_str(price, ","))
        return volume_price
    
    def get_trading_price(self):
        o_b = self.basic_block.select("ul li")[5]
        price = o_b.select("dd ._3rXWJKZF")[0].get_text()
        trading_price = int(utils.del_str(price, ",")) * 1000
        return trading_price
    
    def get_credit_unpurchased(self):
        m_b = self.margin_block.select("ul li")[0]
        amount = m_b.select("dd ._3rXWJKZF")[0].get_text()
        credit_unpurchased = utils.del_str(amount, ",")
        return credit_unpurchased
    
    def get_credit_unsold(self):
        m_b = self.margin_block.select("ul li")[3]
        amount = m_b.select("dd ._3rXWJKZF")[0].get_text()
        credit_unsold = utils.del_str(amount, ",")
        return credit_unsold
