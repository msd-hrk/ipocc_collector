from worker import collector,explorer,geek,reporter,secretary
from mail import mail
from collector import utils
import sys
from logging import config,getLogger
from app_info import config

if not utils.check_work_day():
    sys.exit()

# 設定値の取得
conf = config.Config()


address = conf.address
pwd = conf.password
sub = "ipocc result"
main_msg_list = []

# 情報取得処理の実行
if not explorer.explorer_main():
    main_msg_list.append("explorer：失敗")

err_cnt_collector = collector.collector_main()
if err_cnt_collector > 0:
    main_msg_list.append("collector：" + str(err_cnt_collector) + "件 失敗")

err_cnt_geek = geek.geek_main()
if err_cnt_geek > 0:
    main_msg_list.append("geek：" + str(err_cnt_geek) + "件 失敗")

err_cnt_reporter = reporter.reporter_main()
if err_cnt_reporter > 0:
    main_msg_list.append("reporter：" + str(err_cnt_reporter) + "件 失敗")

err_cnt_secretary = secretary.secretary_main()
if err_cnt_secretary > 0:
    main_msg_list.append("secretary：" + str(err_cnt_secretary) + "件 失敗")

# 情報取得処理の判定とメール送信
main_msg = "情報取得処理成功"
if len(main_msg_list) > 0:
    main_msg = "\r\n".join(main_msg_list)

mail.send(address, pwd, sub, main_msg)

