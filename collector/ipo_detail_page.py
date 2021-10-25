import requests
from bs4 import BeautifulSoup
import re
import datetime
from collector import utils
from logging import config,getLogger
import time


class DetailCollector():
    def __init__(self, securities_no):
        # ログ設定ファイルからログ設定を読み込み
        config.fileConfig('log/logging.conf')
        self.logger = getLogger()
        ipo_net_page = 'https://ipokabu.net/ipo/'+ securities_no
        html = requests.get(ipo_net_page)
        soup = BeautifulSoup(html.content, 'html.parser')
        self.logger.debug("データ取得先：%s", ipo_net_page)
        
        # ページデータ
        self.page_all = soup
        
        # 基本データ
        self.sammary_block = soup.select('.ta_syosai_sp')[0]
        
        # ブックビルディングデータ
        self.book_block = soup.select('.ta_syosai_sp')[1]
        
        # 初値ブロック
        self.init_block = soup.select('.ta_syosai_sp')[2]

        # 予想ブロック
        self.expected_block = soup.select('.ta_syosai_sp')[3]

        # 単独・連結財務データ（ない場合あり）
        finance_block = soup.select('.arrow-parent')
        if len(finance_block) > 0:
            self.solo_finance_block = finance_block[0]
        else:
            self.solo_finance_block = None

        if len(finance_block) > 1:
            self.multi_finance_block = finance_block[1]
        else:
            self.multi_finance_block = None
        
        # ロックアップデータ
        lockup = soup.select('.ta_base')
        if len(lockup) >1:
            self.bank_block = lockup[0]
            self.lockup_block = lockup[1]
        else:
            # 証券会社か株主情報か判定
            table_name = lockup[0].select("tr th")[0].get_text()            
            if table_name == "証券会社":
                self.bank_block = lockup[0]
                self.lockup_block = None
            else:
                self.bank_block = None
                self.lockup_block = lockup[0]
        
    def get_market(self):
        market_and_categoly = self.sammary_block.select('tr')[1]
        market = market_and_categoly.select('td')[0].get_text()
        return market        

    def get_category(self):
        market_and_categoly = self.sammary_block.select('tr')[1]
        market = market_and_categoly.select('td')[1].get_text()
        return market
        
    def get_winning_num(self):
        winning_line = self.book_block.select('tr')[2]
        winning_num = winning_line.select('span')[0].get_text()
        aft_del = str(winning_num).replace("口","")
        int_only = utils.delete_canma(aft_del)
        return int(int_only)
        
    def get_issued_shares(self):
        issued_s_line = self.book_block.select('tr')[3]
        issued_s = issued_s_line.select('td')[0].get_text()
        aft_del = str(issued_s).replace("株","")
        int_only = utils.delete_canma(aft_del)
        return int(int_only)
        
    def get_oar(self):
        oar_line = self.book_block.select('tr')[3]
        oar = oar_line.select('td')[1].get_text()
        percent = str(oar).replace("％","")
        rate = float(percent) / 100
        return round(rate, 2)
        
    def get_pub_offered_shares(self):
        pub_offerd_s_line = self.book_block.select('tr')[4]
        pub_offered = pub_offerd_s_line.select('td')[0].get_text()
        aft_del = str(pub_offered).replace("株","")
        int_only = utils.delete_canma(aft_del)
        return int(int_only)
        
    def get_sell_shares(self):
        sell_shares_line = self.book_block.select('tr')[4]
        sell_s = sell_shares_line.select('td')[1].get_text()
        aft_del = str(sell_s).replace("株","")
        int_only = utils.delete_canma(aft_del)
        return int(int_only)
        
    def get_oa_shared(self):
        oa_shares_line = self.book_block.select('tr')[5]
        oa_s = oa_shares_line.select('td')[1].get_text()
        aft_del = str(oa_s).replace("株","")
        int_only = utils.delete_canma(aft_del)
        return int(int_only)
        
    def get_tdd(self):
        tdd_line = self.book_block.select('tr')[6]
        tdd_slush = tdd_line.select('td')[0].get_text()
        tdd = re.search(r'\d{1,2}/\d{1,2}', str(tdd_slush)).group()
        return utils.str_to_int(utils.convesion_date_format(tdd))
        
    def get_pdd(self):
        pdd_line = self.book_block.select('tr')[6]
        pdd_slush = pdd_line.select('td')[1].get_text()
        pdd = re.search(r'\d{1,2}/\d{1,2}', str(pdd_slush)).group()
        return utils.str_to_int(utils.convesion_date_format(pdd))

    def get_purchase_period(self):
        p_period_l = self.book_block.select('tr')[7]
        array = str(p_period_l.select('td')[0].get_text()).split("～")
        start_date = re.search(r'\d{1,2}/\d{1,2}', str(array[0])).group()
        start_date_yyyymmdd = utils.convesion_date_format(start_date)
        end_date = re.search(r'\d{1,2}/\d{1,2}', str(array[1])).group()
        end_date_yyyymmdd = utils.convesion_date_format(end_date)
        return {
            "start": utils.str_to_int(start_date_yyyymmdd),
            "end": utils.str_to_int(end_date_yyyymmdd)
        }

    def get_indpndnt_fin_info(self):
        # 返却用配列
        data = []
        if self.solo_finance_block is not None:
            fiscal_year_l = self.solo_finance_block.select('.f_1110 th')
            for i in range(utils.counter_column(fiscal_year_l), len(fiscal_year_l), 1):
                # 決算期  str
                fiscal_year = utils.convert_yyyymm(fiscal_year_l[i].get_text())
                # 売上高  int
                am_l = self.solo_finance_block.select('tr')[1]
                amount_of_salls = utils.delete_canma(am_l.select('td')[i].get_text())
                if not utils.int_check(amount_of_salls):
                    amount_of_salls = 0
                # 経常利益  int
                ord_in_l = self.solo_finance_block.select('tr')[2]
                ordinary_income = utils.delete_canma(ord_in_l.select('td')[i].get_text())
                # 当期利益  int
                net_i_l = self.solo_finance_block.select('tr')[3]
                net_income = utils.delete_canma(net_i_l.select('td')[i].get_text())
                # 純資産  int
                w_l = self.solo_finance_block.select('tr')[4]
                net_worth = utils.delete_canma(w_l.select('td')[i].get_text())
                # 配当金  int
                div_l = self.solo_finance_block.select('tr')[5]
                div = div_l.select('td')[i].get_text()
                dividend = 0
                if re.match(r'\d{1}', div) is not None:
                    dividend = utils.delete_canma(div_l.select('td')[i].get_text())
                # EPS  float
                eps_l = self.solo_finance_block.select('tr')[6]
                eps = utils.delete_canma(eps_l.select('td')[i].get_text())
                # BPS  float
                bps_l = self.solo_finance_block.select('tr')[7]
                bps = utils.delete_canma(bps_l.select('td')[i].get_text())
                
                # 各期ごとのデータ作成
                column = {
                    "fiscalYear":fiscal_year,
                    "amountOfSalls":int(amount_of_salls) * 1000,
                    "ordinaryIncome":int(ordinary_income) * 1000,
                    "netIncome":int(net_income) * 1000,
                    "netWorth":int(net_worth) * 1000,
                    "dividend":round(float(dividend), 2),
                    "bps":round(float(bps), 2),
                    "eps":round(float(eps), 2),
                }
                data.append(column)
        else:
            data.append(None)
        return data

    def get_cnsldtd_fin_info(self):
        # 返却用配列
        data = []
        if self.multi_finance_block is not None:
            fiscal_year_l = self.multi_finance_block.select('.f_1110 th')
            for i in range(utils.counter_column(fiscal_year_l), len(fiscal_year_l), 1):
                # 決算期  str
                fiscal_year = utils.convert_yyyymm(fiscal_year_l[i].get_text())
                # 売上高  int
                am_l = self.multi_finance_block.select('tr')[1]
                amount_of_salls = utils.delete_canma(am_l.select('td')[i].get_text())
                # 経常利益  int
                ord_in_l = self.multi_finance_block.select('tr')[2]
                ordinary_income = utils.delete_canma(ord_in_l.select('td')[i].get_text())
                # 当期利益  int
                net_i_l = self.multi_finance_block.select('tr')[3]
                net_income = utils.delete_canma(net_i_l.select('td')[i].get_text())
                # 純資産  int
                w_l = self.multi_finance_block.select('tr')[4]
                net_worth = utils.delete_canma(w_l.select('td')[i].get_text())
                # EPS  float
                eps_l = self.multi_finance_block.select('tr')[5]
                eps = utils.delete_canma(eps_l.select('td')[i].get_text())
                # BPS  float
                bps_l = self.multi_finance_block.select('tr')[6]
                bps = utils.delete_canma(bps_l.select('td')[i].get_text())
                
                # 各期ごとのデータ作成
                column = {
                    "fiscalYear":fiscal_year,
                    "amountOfSalls":int(amount_of_salls) * 1000,
                    "ordinaryIncome":int(ordinary_income) * 1000,
                    "netIncome":int(net_income) * 1000,
                    "netWorth":int(net_worth) * 1000,
                    "bps":round(float(bps), 2),
                    "eps":round(float(eps), 2),
                }
                data.append(column)
        else:
            data.append(None)
        return data
    
    def get_share_holders(self):
        # 返却用リスト
        data = []
        if self.lockup_block is None:
            return data
            
        lockup_list = self.lockup_block.select("tr")
        # 売り出しフラグ（売出株数が記載されているかどうか）
        out_stock_flg = self.lockup_block.select("tr th")[2].get_text() == "売出数"
        for i in range(1, len(lockup_list), 1):
            lockup_l = lockup_list[i].select("td")
            # 株主名 str
            name_b = lockup_l[0].contents
            name = utils.arange_data(name_b[0])
            # 役職 str
            position = "-"
            if len(name_b) > 1:
                position = lockup_l[0].select("span")[0].get_text()
            # 所有株数 int
            stock_b = lockup_l[1].contents
            shered_num = utils.arange_data(utils.delete_canma(str(stock_b[0]).replace("株","")))
            # 比率 str
            rate = ""
            if out_stock_flg:
                rate = lockup_l[1].select(".kome")[0].get_text()
            else:
                rate = lockup_l[2].get_text()
            # 潜在株数 int
            potential_shares = 0
            if len(stock_b) > 3:
                pot_s = lockup_l[1].select("div")[1].get_text()
                potential_shares = utils.del_str(pot_s,"（","）",",")
            # 売出数 int
            out_shares = 0
            if out_stock_flg:
                out_b = utils.arange_data(utils.del_str(lockup_l[2].get_text(),",","株"))
                if utils.int_check(out_b):
                    out_shares = out_b
            # ロックアップ情報
            lockup_b = lockup_l[3].get_text()
            lockup = {
                "day": 0,
                "rate": 0,
                "status": ""
            }
            array = str(lockup_b).split("/")
            if len(array) > 1:
                lockup["day"] = int(utils.del_str(str(array[0]),"日間"))
                lockup["rate"] = round(float(utils.del_str(str(array[1]), "倍")), 2)
            else:
                l_info = utils.del_str(str(array[0]),"日間")
                if utils.int_check(l_info):
                    lockup["day"] = int(utils.del_str(str(array[0]),"日間"))
                else:
                    lockup["status"] = str(array[0])
                
            column = {
                "name": str(name),
                "position": str(position),
                "sheredNum": int(shered_num),
                "potentialShares": int(potential_shares),
                "rate": str(rate),
                "outShares": int(out_shares),
                "lockup":lockup,
            }
            data.append(column)
        return data
        
    def get_bank_data(self):
        if self.bank_block is None:
            # 主幹事データなしのとき
            data = {
                "name": "データなし",
                "rate": "不明"
            }
            return data
        else:
            # 主幹事データあり
            data = {
                "name": str(self.bank_block.select("tr")[1].select("a")[0].get_text()),
                "rate": str(self.bank_block.select("tr")[1].select("td")[1].get_text()),
            }
            return data
    
    def get_expected_profit_befTD(self):
        ex_l = ''
        length = len(self.page_all.select(".yoso_mae"))
        if length == 0:
            return {
                "tdPrice": {
                    "min": 0,
                    "max": 0,
                },
                "initPriceEx": {
                    "min": 0,
                    "max": 0,
                },
                "exProfit": {
                    "min": 0,
                    "max": 0,
                },
            }
        elif length == 1:
            ex_l = self.page_all.select(".yoso_mae")[0]
        else:
            ex_l = self.page_all.select(".yoso_mae")[1]

        # 想定価格
        ex_p = ex_l.select("tr")[0].select("td span")[0].get_text()
        ex_price = utils.del_str(re.search(r".*円",str(ex_p)).group(),",","円")
        # 初値予想
        ini_ex_b = ex_l.select("tr")[1].select("td .f_yoso")[0].get_text()
        ini_ex_arry = str(ini_ex_b).split("～")
        init_ex_price = {
            "min": int(utils.del_str(ini_ex_arry[0]," ",",","円")),
            "max": int(utils.del_str(ini_ex_arry[1]," ",",","円")),
        }
        # 予想利益
        ex_pro = ex_l.select("tr")[2].select("td .f_yoso_soneki")[0].get_text()
        pro_arry = str(ex_pro).split("～")
        ex_profit = {
            "min": int(utils.del_jp_price(pro_arry[0])),
            "max": int(utils.del_jp_price(pro_arry[1])),
        }
        
        data = {
            "exPrice": int(ex_price),
            "initPriceEx": init_ex_price,
            "exProfit": ex_profit,
        }
        return data
    
    def get_expected_profit_aftTD(self):
        ex_l = ''
        length = len(self.page_all.select(".yoso_mae"))
        if length < 2:
            return {
                "tdPrice": {
                    "min": 0,
                    "max": 0,
                },
                "initPriceEx": {
                    "min": 0,
                    "max": 0,
                },
                "exProfit": {
                    "min": 0,
                    "max": 0,
                },
            }
        else:
            ex_l = self.page_all.select(".yoso_mae")[0]

        # 想定価格
        ex_p = ex_l.select("tr")[0].select("td span")[0].get_text()
        p_arry = str(ex_p).split("～")
        td_price = {
            "min": int(utils.del_str(re.search(r".*円",str(p_arry[0])).group(),",","円")),
            "max": int(utils.del_str(re.search(r".*円",str(p_arry[1])).group(),",","円")),
        }
        # 初値予想
        ini_ex_b = ex_l.select("tr")[1].select("td .f_yoso")[0].get_text()
        ini_ex_arry = str(ini_ex_b).split("～")
        init_ex_price = {
            "min": int(utils.del_str(ini_ex_arry[0]," ",",","円")),
            "max": int(utils.del_str(ini_ex_arry[1]," ",",","円")),
        }
        # 予想利益
        ex_pro = ex_l.select("tr")[2].select("td .f_yoso_soneki")[0].get_text()
        pro_arry = str(ex_pro).split("～")
        ex_profit = {
            "min": int(utils.del_jp_price(pro_arry[0])),
            "max": int(utils.del_jp_price(pro_arry[1])),
        }
        
        data = {
            "tdPrice": td_price,
            "initPriceEx": init_ex_price,
            "exProfit": ex_profit,
        }
        return data

    def get_init_price(self):
        i_l = self.init_block.select("tr")[1]
        i_b = i_l.select("td")[1].getText()
        init_price = utils.del_str(i_b,",","円")
        print(init_price)
        return init_price

    def get_pub_offer_price(self):
        i_l = self.init_block.select("tr")[1]
        i_b = i_l.select("td")[0].getText()
        pub_offer_price = utils.del_str(i_b,",","円")
        return pub_offer_price

    def get_unit_share(self):
        market_and_categoly = self.sammary_block.select('tr')[2]
        u_share = market_and_categoly.select('td')[1].get_text()
        unit_share = utils.del_str(u_share,"株")
        return unit_share
