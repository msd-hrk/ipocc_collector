import requests
from bs4 import BeautifulSoup
import re
import datetime
from dbutils import dbCommon
from logging import config,getLogger
from collector import utils, ipo_list_page
import time
from app_info import config as app_conf

def explorer_main():
    # 設定値読み込み
    conf = app_conf.Config()

    # ログ設定ファイルからログ設定を読み込み
    config.fileConfig('log/logging.conf')
    logger = getLogger()
    logger.debug("explorer_main処理開始")
    try:

        # mongoDb接続
        dbutil = dbCommon.DbUtils()

        # 取得サイトURL
        url_1 = 'https://ipokabu.net/yotei/'
        html = requests.get(url_1)
        soup = BeautifulSoup(html.content, 'html.parser')

        # テーブル部分のデータ取得
        tbl_data = soup.select('.nosp table tr')

        data_up = []
        data_down = []

        for i in range(0, len(tbl_data), 2):
            # タイトル部分を除外
            if re.search('.*<th>.*</th>.*',str(tbl_data[i])):
                continue
            
            data_up.append(tbl_data[i])

        for i in range(1, len(tbl_data), 2):
            if re.search('.*<th>.*</th>.*',str(tbl_data[i])):
                continue
            
            data_down.append(tbl_data[i])

        if(len(data_up) != len(data_down)):
            logger.warning('テーブルの上段と下段のデータ数相違　上段:下段[%s:%s]', len(data_up), len(data_down))
            raise ValueError("データ取得時の上段と下段の個数が違います。（%s)", url_1)

        for i in range(0, len(data_down)):
            list_collector = ipo_list_page.ListCollector(data_up[i], data_down[i])
            securities_no = list_collector.get_securitiesNo()

            if dbutil.search_code_list(securities_no) is not None:
                logger.info("securitiesNo[%s]はすでに存在しています", securities_no)
                continue

            # 上場済みか？
            now = datetime.date.today().strftime("%Y%m%d")
            listingDate = list_collector.get_listingDate()
            if int(now) >= int(listingDate):
                continue

            data = {
                "company": list_collector.get_company(),
                "securitiesNo": list_collector.get_securitiesNo(),
                "bookbuilding": {
                    "start": list_collector.get_bookbilding_start(),
                    "end": list_collector.get_bookbilding_end(),
                },
                "listingDate":list_collector.get_listingDate(),
                "grade": list_collector.get_grade(),
            }

            # 仮条件決定日を取得し登録　      
            url_1 = 'https://ipokabu.net/ipo/'+data["securitiesNo"]
            html = requests.get(url_1)
            soup = BeautifulSoup(html.content, 'html.parser')

            tdd_slush = soup.select('.ta_syosai_sp')[1].select('tr')[6].select('td')[0].get_text()
            tdd = re.search(r'\d{1,2}/\d{1,2}', str(tdd_slush)).group()
            data["tdd"] = utils.str_to_int(utils.convesion_date_format(tdd)) # 仮条件決定日

            logger.info(data)
            if conf.data_insert_flg:
                # mongoDBへ登録
                dbutil.insert_exploer_data_one(data)
                logger.debug("insert DB [%s]", data["securitiesNo"])

            time.sleep(1)
        return True
    except Exception as err:
        logger.exception('Error dosomething: %s', err)
        return False
