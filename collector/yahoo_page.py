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
        self.referenc_block = soup.select("#referenc")[0]

    def get_closing_price(self):
        price = utils.del_str(self.realtime_block.select("header ._3rXWJKZF")[0].get_text(),",")
        if not utils.int_check(price):
            return ""
        closing_price = str(utils.del_str(price, ","))
        return closing_price
    
    def get_open_price(self):
        o_b = self.basic_block.select("ul li")[1]
        price = utils.del_str(o_b.select("dd ._3rXWJKZF")[0].get_text(), ",")
        if not utils.int_check(price):
            return ""
        return price
    
    def get_high_price(self):
        o_b = self.basic_block.select("ul li")[2]
        price = utils.del_str(o_b.select("dd ._3rXWJKZF")[0].get_text(), ",")
        if not utils.int_check(price):
            return ""
        return price
    
    def get_low_price(self):
        o_b = self.basic_block.select("ul li")[3]
        price = utils.del_str(o_b.select("dd ._3rXWJKZF")[0].get_text(), ",")
        if not utils.int_check(price):
            return ""
        return price
    
    def get_volume_price(self):
        o_b = self.basic_block.select("ul li")[4]
        price = utils.del_str(o_b.select("dd ._3rXWJKZF")[0].get_text(), ",")
        if not utils.int_check(price):
            return ""
        return price
    
    def get_trading_price(self):
        o_b = self.basic_block.select("ul li")[5]
        price = utils.del_str(o_b.select("dd ._3rXWJKZF")[0].get_text(), ",")
        if not utils.int_check(price):
            return ""
        return price
    
    def get_credit_unpurchased(self):
        m_b = self.margin_block.select("ul li")[0]
        amount = utils.del_str(m_b.select("dd ._3rXWJKZF")[0].get_text(), ",")
        if not utils.int_check(amount):
            return ""
        return amount
    
    def get_credit_unsold(self):
        m_b = self.margin_block.select("ul li")[3]
        amount = utils.del_str(m_b.select("dd ._3rXWJKZF")[0].get_text(), ",")
        if not utils.int_check(amount):
            return ""
        return amount

    def get_issued_shares(self):
        r_b = self.referenc_block.select("ul li")[1]
        shares = utils.del_str(r_b.select("dd ._3rXWJKZF")[0].get_text(), ",")
        if not utils.int_check(shares):
            return ""
        return shares

    def get_dividend(self):
        r_b = self.referenc_block.select("ul li")[3]
        dividend = r_b.select("dd ._3rXWJKZF")[0].get_text()
        return dividend

    def get_PER(self):
        r_b = self.referenc_block.select("ul li")[4]
        per = r_b.select("dd ._3rXWJKZF")[0].get_text()
        if not utils.float_check(per):
            return ""
        return per

    def get_PBR(self):
        r_b = self.referenc_block.select("ul li")[5]
        pbr = r_b.select("dd ._3rXWJKZF")[0].get_text()
        if not utils.float_check(pbr):
            return ""
        return pbr

    def get_EPS(self):
        r_b = self.referenc_block.select("ul li")[6]
        eps = r_b.select("dd ._3rXWJKZF")[0].get_text()
        if not utils.float_check(eps):
            return ""
        return eps

    def get_BPS(self):
        r_b = self.referenc_block.select("ul li")[7]
        bps = r_b.select("dd ._3rXWJKZF")[0].get_text()
        if not utils.float_check(bps):
            return ""
        return bps
