from collector import ipo_detail_page,yahoo_detail_page
from dbutils import dbCommon
from logging import config,getLogger
import time

def collector_main():
    # ログ設定ファイルからログ設定を読み込み
    config.fileConfig('log/logging.conf')
    logger = getLogger()
    logger.debug("collector_main処理開始")
    try:

        # mongoDb接続
        dbutil = dbCommon.DbUtils()

        # コードリスト内のcolector処理対象メソッドの取得
        targetList = dbutil.colector_target()

        for data in targetList:
            # 証券コードから詳細ページの取得クラスの呼出
            detail_colector = ipo_detail_page.DetailCollector(data["securitiesNo"])
            yahoo_colector = yahoo_detail_page.YahooDetailCollector(data["securitiesNo"])

            # データ作成
            update_data = {
                "market": detail_colector.get_market(), # 市場
                "category": detail_colector.get_category(), # 業種
                "winningNum": detail_colector.get_winning_num(), # 当選口数
                "issuedShares": detail_colector.get_issued_shares(), # 発行済株式数
                "oar": detail_colector.get_oar(), # オファリングレシオ
                "pubOfferedShares": detail_colector.get_pub_offered_shares(), # 公募株数
                "sellShares": detail_colector.get_sell_shares(), # 売出株数
                "oaShared": detail_colector.get_oa_shared(), # O.A分
                "pdd": detail_colector.get_pdd(), # 公募価格決定日 
                "purchasePeriod": detail_colector.get_purchase_period(), # 購入期間
                "indpndntFinInfo":detail_colector.get_indpndnt_fin_info(), # 単独財務情報
                "cnsldtdFinInfo":detail_colector.get_cnsldtd_fin_info(), # 連結財務情報
                "shareholders":detail_colector.get_share_holders(), # 上位10株主
                "bank":detail_colector.get_bank_data(), # 主幹事データ
                "expectedProfitBeforeTD":detail_colector.get_expected_profit_befTD(), # 予想利益（仮条件決定前）
                "expectedProfitAfterTD":detail_colector.get_expected_profit_aftTD(), # 予想利益（仮条件決定前）
                "unitShare":int(detail_colector.get_unit_share()), # 単元株,
                "capital": yahoo_colector.get_capital(), # 資本金
                "business": yahoo_colector.get_business(), # 事業内容
                "employee": yahoo_colector.get_employee(), # 従業員情報
                "build": yahoo_colector.get_build(), # 設立
                "holder_num": yahoo_colector.get_holder_num(), # 株主数
                "web": yahoo_colector.get_web(), # サイト
            }
            # 吸収金額算出
            update_data["absorbentAmount"] = {
                "beforePD": (update_data["pubOfferedShares"] + update_data["sellShares"] + update_data["oaShared"]) \
                    * update_data["expectedProfitAfterTD"]["tdPrice"]["max"],
            }
            # 時価総額算出
            update_data["mrktcptlz"] = {
                "beforePD": update_data["issuedShares"] * update_data["expectedProfitAfterTD"]["tdPrice"]["max"],
            }
            logger.debug(update_data)
            dbutil.update_with_sec_no(data["securitiesNo"], update_data)

            time.sleep(1)
        return True
    except Exception as err:
        logger.exception('Error dosomething: %s', err)
        return False