# -*- coding: utf-8 -*-
"""
Created on 2022-10-18 11:27:34
---------
@summary:
---------
@author: 苏寅
@目标：南华周报
@argv：host port username password db
"""
import sys
import time

import requests
import feapder
from feapder.db.mysqldb import MysqlDB


class ReportWeekly(feapder.AirSpider):
    __custom_setting__ = dict(
        LOG_LEVEL="INFO",
        # LOG_LEVEL="DEBUG",
        SPIDER_MAX_RETRY_TIMES=1,
        SPIDER_SLEEP_TIME=0,
        # REQUEST_FILTER_ENABLE=True
    )

    def start_requests(self):
        type_dict = {
            "油泊": "402201",
            "金属": "402202",
            "棉花": "402203",
            "能化": "402204",
            "白糖": "402205",
            "贵金属": "402206",
            "黑色": "402208",
            "玻璃": "402210",
            "股指": "402211",
            "国债": "402212",
            "粮食": "402213",
            "宏观经济": "402214",
            "CFTC持仓分析": "402215",
            "期权": "402216",
            "农副": "402217",
            "人民币汇率": "402219",
        }
        for tp_key, ty_value in type_dict.items():
            yield feapder.Request(ty_value=ty_value, page=1, callback=self.next_page)
            # break

    def download_midware(self, request):
        request.headers = {
            "Referer": "https://www.nanhua.net/subpage/research/report/weekly/weekly-cake.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        }
        request.url = "https://www.nanhua.net/jSearch/queryNewsListByTypeForJson.shtm"
        request.cookies = {"JSESSIONID": "30D279592C92978D00680F905A8485DD-n1"}
        request.params = {
            "site": "newnanhua",
            "type": request.ty_value,
            "start": request.page,
            "limit": "16",
            "t": str(time.time()).replace(".", "")[:-4],
        }
        return request

    def next_page(self, request, response):
        """
        抓取多页
        """
        # 总页码
        total_pages = response.json.get("totalPages")
        print(f"总页码：{total_pages}".center(60, "*"))
        for i in range(2, 3):
            yield feapder.Request(page=i, type=request.ty_value)

    def parse_info(self, response):
        # 报告列表
        record_list = response.get("recordList")
        for record in record_list:
            result = {}
            print("=" * 60)
            # 报告ID
            result["report_id"] = record.get("newsId")
            # 报告标题
            result["report_title"] = record.get("subject")
            # 报告作者
            result["report_author"] = record.get("author")
            # 报告时间
            result["report_time"] = record.get("createTime")
            # 报告类别
            result["report_type"] = record.get("typeName")
            # 报告链接
            result["report_url"] = "https://www.nanhua.net" + record.get("href")
            print(result)
            # 保存数据
            self.save_data(result)

    def save_data(self, result):
        """
        保存数据
        """
        db = MysqlDB.from_url(
            f"mysql://{sys.argv[3]}:{sys.argv[4]}@{sys.argv[1]}:{sys.argv[2]}/{sys.argv[5]}?charset=utf8"
        )
        # 查询所有数据表
        tables = [tb[0] for tb in db.find("show tables;")]
        if "test" not in tables:
            print("数据表创建中".center(60, "*"))
            sql = """
            CREATE TABLE `test` (
              `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id主键',
              `report_id` varchar(255) DEFAULT NULL COMMENT '报告ID',
              `report_title` varchar(255) DEFAULT NULL COMMENT '报告标题',
              `report_author` varchar(255) DEFAULT NULL COMMENT '报告作者',
              `report_time` varchar(255) DEFAULT NULL COMMENT '报告时间',
              `report_type` varchar(255) DEFAULT NULL COMMENT '报告类别',
              `report_url` varchar(1000) DEFAULT NULL COMMENT '报告链接',
              `crawl_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '采集时间',
              PRIMARY KEY (`id`),
              UNIQUE KEY `idx` (`report_id`) USING BTREE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
            db.execute(sql)
        else:
            db.add_smart("test", result)


if __name__ == "__main__":
    ReportWeekly(thread_count=10).start()
