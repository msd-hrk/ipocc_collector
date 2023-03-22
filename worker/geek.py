from collector import ipo_detail_page
from dbutils import dbCommon
from logging import config,getLogger
import time
from app_info import config as app_conf

def geek_main():
    # 設定値の取得
    conf = app_conf.Config()

    # ログ設定ファイルからログ設定を読み込み
    config.fileConfig('log/logging.conf')
    logger = getLogger()
    logger.debug("geek_main処理開始")
    err_securities_no_list = []
    # mongoDb接続
    dbutil = dbCommon.DbUtils()

    # コードリスト内のcolector処理対象メソッドの取得
    targetList = dbutil.geek_target()

    tbl = str.maketrans("SABCD", "ＳＡＢＣＤ")
    for data in targetList:
        try:
                
            # 無視する証券コードの場合
            if data["securitiesNo"] in conf.ignore_nums:
                continue

            # 証券コードから詳細ページの取得
            detail_colector = ipo_detail_page.DetailCollector(data["securitiesNo"])
            grade = data["grade"]
            if grade == "未定":
                grade = str(detail_colector.get_grade()).translate(tbl)
            else:
                grade_now = str(detail_colector.get_grade()).translate(tbl)
                if grade != grade_now:
                    grade = grade + "->" +grade_now
                    
            # データ作成
            update_data = {
                "pubOfferPrice": int(detail_colector.get_pub_offer_price()), # 公募価格
                "unitShare": int(detail_colector.get_unit_share()), # 単元株,
                "grade": grade, # 評価
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