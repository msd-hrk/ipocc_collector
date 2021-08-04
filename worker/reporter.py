from collector import ipo_detail_page, utils
from dbutils import dbCommon
from logging import config,getLogger
import time

def reporter_main():
    # ログ設定ファイルからログ設定を読み込み
    config.fileConfig('log/logging.conf')
    logger = getLogger()
    logger.debug("reporter_main処理開始")
    try:

        # mongoDb接続
        dbutil = dbCommon.DbUtils()

        # コードリスト内のreporter処理対象メソッドの取得
        targetList = dbutil.reporter_target()

        for data in targetList:
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
            dbutil.update_with_sec_no(data["securitiesNo"], update_data)

            time.sleep(1)
        return True
    except Exception as err:
        logger.exception('Error dosomething: %s', err)
        return False

