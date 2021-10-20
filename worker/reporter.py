from collector import ipo_detail_page, utils
from dbutils import dbCommon
from logging import config,getLogger
import time
from app_info import config as app_conf

def reporter_main():
    # 設定値の取得
    conf = app_conf.Config()

    # ログ設定ファイルからログ設定を読み込み
    config.fileConfig('log/logging.conf')
    logger = getLogger()
    logger.debug("reporter_main処理開始")
    err_securities_no_list = []

    # mongoDb接続
    dbutil = dbCommon.DbUtils()

    # コードリスト内のreporter処理対象メソッドの取得
    targetList = dbutil.reporter_target()

    for data in targetList:
        try:
            # 無視する証券コードの場合
            if data["securitiesNo"] in conf.ignore_nums:
                continue

            # 証券コードから詳細ページの取得
            detail_colector = ipo_detail_page.DetailCollector(data["securitiesNo"])

            init_price = detail_colector.get_init_price() # 初値

            if not utils.int_check(init_price):
                # 初値が決まらなかった場合
                continue

            # データ作成
            update_data = {
                "initPrice": int(init_price),# 初値
                "InitPriceSellProfit": (int(init_price) - data["pubOfferPrice"]) * data["unitShare"], # 初値売り損益
                "rfRate": round((int(init_price) / data["pubOfferPrice"]) * 100 ,2), # 騰落率, 
            }
            logger.debug(update_data)
            if conf.data_insert_flg:
                dbutil.update_with_sec_no(data["securitiesNo"], update_data)
                logger.debug("insert DB [%s]", data["securitiesNo"])

            time.sleep(1)

        except Exception as err:
            err_securities_no_list.append(data["securitiesNo"])
            logger.exception('Error securitiesNo at %s: %s',data["securitiesNo"], err)
            continue

    return len(err_securities_no_list)
