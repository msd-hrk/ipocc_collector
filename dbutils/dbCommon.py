from mail.mail import con
from pymongo import MongoClient
import datetime
from collector import utils
from app_info import config

class DbUtils():
    def __init__(self):
        # 設定値取得
        conf = config.Config()
        # クライアント取得
        self.client = MongoClient(conf.mongo_url)
        self.db = self.client.ipocc
        self.code_list = self.db.codelist

    def search_code_list(self, code_no):
        return self.code_list.find_one({'securitiesNo': code_no})

    def insert_exploer_data_one(self, data): 
        self.code_list.insert(data)

    def colector_target(self):
        now = datetime.date.today()
        now_yyyymmdd = now.strftime("%Y%m%d")
        mongo_data = self.code_list.find()
        target = []
        for data in mongo_data:
            if int(data["tdd"]) < int(now_yyyymmdd) \
                and int(data["listingDate"]) >= int(now_yyyymmdd):
                target.append(data)
        
        return target
    
    def update_with_sec_no(self, securitiesNo, data):
        self.code_list.update({'securitiesNo': securitiesNo}, {'$set': data})
    
    def reporter_target(self):
        now = datetime.date.today()
        now_yyyymmdd = now.strftime("%Y%m%d")
        mongo_data = self.code_list.find()
        target = []
        for data in mongo_data:
            if int(data["listingDate"]) > int(now_yyyymmdd):
                # 上場日が今日より先のものは除外
                continue
        
            if utils.check_exist_key(data, "initPrice"):
                # 初値があるものは除外
                continue
            target.append(data)
        print(len(target))
        return target
    
    def geek_target(self):
        now = datetime.date.today()
        now_yyyymmdd = now.strftime("%Y%m%d")
        mongo_data = self.code_list.find()
        target = []
        for data in mongo_data:
            if not utils.check_exist_key(data, "pdd"):
                # 公募価格決定日が未取得ものは除外
                continue

            if int(data["pdd"]) > int(now_yyyymmdd):
                # 公募価格決定日が今日より先のものは除外
                continue
        
            if utils.check_exist_key(data, "pubOfferPrice"):
                # 公募価格があるものは除外
                continue
            target.append(data)
        print(len(target))
        return target
    
    def secretary_target(self):
        now = datetime.date.today()
        now_yyyymmdd = now.strftime("%Y%m%d")
        mongo_data = self.code_list.find()
        target = []
        for data in mongo_data:

            if int(data["listingDate"]) > int(now_yyyymmdd):
                # 上場日が未到来ものは除外
                continue

            if utils.check_exist_key(data, "priceDiary"):
                # priceDiaryフィールドがある
                if len(data["priceDiary"]) > 250:
                    # 250日（1年の平日の数）を超えるものは除外
                    continue
        
            target.append(data)
        return target

        
        
        
