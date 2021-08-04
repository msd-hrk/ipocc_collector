from collector import ipo_detail_page
from dbutils import dbCommon
from logging import config,getLogger
import time

def geek_main():
    # ログ設定ファイルからログ設定を読み込み
    config.fileConfig('log/logging.conf')
    logger = getLogger()
    logger.debug("geek_main処理開始")
    
    try:
        # mongoDb接続
        dbutil = dbCommon.DbUtils()

        # コードリスト内のcolector処理対象メソッドの取得
        targetList = dbutil.geek_target()

        for data in targetList:
            # 証券コードから詳細ページの取得
            detail_colector = ipo_detail_page.DetailCollector(data["securitiesNo"])

            # データ作成
            update_data = {
                "pubOfferPrice": int(detail_colector.get_pub_offer_price()), # 公募価格
                "unitShare":int(detail_colector.get_unit_share()), # 単元株,
            }
            logger.debug(update_data)
            dbutil.update_with_sec_no(data["securitiesNo"], update_data)

            time.sleep(1)
        return True
    except Exception as err:
        logger.exception('Error dosomething: %s', err)
        return False

