from collector import yahoo_page, utils
import datetime
from dbutils import dbCommon
from logging import config,getLogger
import time

def secretary_main():
    # ログ設定ファイルからログ設定を読み込み
    config.fileConfig('log/logging.conf')
    logger = getLogger()
    logger.debug("secretary_main処理開始")
    try:              

        # mongoDb接続
        dbutil = dbCommon.DbUtils()

        # コードリスト内のreporter処理対象メソッドの取得
        targetList = dbutil.secretary_target()

        for data in targetList:
            try:         
                # 証券コードから詳細ページの取得
                yahoo_collector = yahoo_page.YahooCollector(data["securitiesNo"])

                today_data = []
                # 今日の日付も格納
                now = datetime.date.today()
                now_yyyymmdd = now.strftime("%Y%m%d")
                credit_unpurchased = yahoo_collector.get_credit_unpurchased()
                credit_unsold = yahoo_collector.get_credit_unsold()
                margin_rate = "---"
                if utils.int_check(credit_unpurchased) \
                    and utils.int_check(credit_unsold):
                    credit_unpurchased = int(credit_unpurchased)
                    credit_unsold = int(credit_unsold)
                    if credit_unpurchased == 0 or credit_unsold == 0:
                        margin_rate = 0
                    else:
                        credit_unpurchased = int(credit_unpurchased)
                        credit_unsold = int(credit_unsold)
                        margin_rate = round(float(credit_unpurchased / credit_unsold), 2)

                today_data.append(now_yyyymmdd) # 日付
                today_data.append(yahoo_collector.get_open_price()) # 始値
                today_data.append(yahoo_collector.get_closing_price()) # 終値
                today_data.append(yahoo_collector.get_high_price()) # 高値
                today_data.append(yahoo_collector.get_low_price()) # 安値
                today_data.append(credit_unpurchased) # 信用買残
                today_data.append(credit_unsold) # 信用売残
                today_data.append(margin_rate) # 信用倍率

                # priceDiaryフィールドが存在するか
                if not utils.check_exist_key(data, "priceDiary"):
                    logger.debug("初登録の証券コード：%s",data["securitiesNo"])
                    data["priceDiary"] = []
                data["priceDiary"].append(today_data)

                logger.debug(data["priceDiary"])
                dbutil.update_with_sec_no(data["securitiesNo"], data)

                time.sleep(1)
            except Exception as err:
                logger.exception('Error dosomething: %s', err)
                logger.error("エラー発生証券コード：%s", data["securitiesNo"])
                continue
        return True
    except Exception as err:
        logger.exception('Error dosomething: %s', err)
        return False

