# import json
# import random
# import re
# import time
import os
import pandas as pd
# import requests
# from bs4 import BeautifulSoup
from lxml import etree
# import pdfkit
import crawlertools as ct


def parse_policy_list(response):
    datas = etree.HTML(response)
    datas = datas.xpath("//table//tr[position()>=0]")
    # table = res_elements.xpath('//table[@id="table1"]')
    col_name = datas[0].xpath(".//th[position()>=0]//text()")
    col_name.extend(["url", "标签"])
    df_policy = pd.DataFrame(columns=col_name)

    for policy in datas[1:]:  # 遍历tr列表
        policy_id = ''.join(policy.xpath(".//td[1]//text()"))  # 获取当前tr标签下的第一个td标签，并用text()方法获取文本内容，赋值给p
        policy_title = ''.join(policy.xpath(".//td[2]//a/@title"))
        policy_date = ''.join(policy.xpath(".//td[3]//text()"))
        policy_num = ''.join(policy.xpath(".//td[4]//text()"))
        policy_url = ''.join(policy.xpath(".//td[2]//a/@href"))
        policy_tag = ''.join(policy.xpath(".//td[2]//em//text()"))

        data = {  # 用数据字典，存储需要的信息
            '序号': policy_id,
            '标题': policy_title,
            '发布日期': policy_date,
            '文号': policy_num,
            'url': policy_url,
            '标签': policy_tag
        }

        df_policy = df_policy.append(data, ignore_index=True)

    return df_policy


def get_policy_table():
    url_list = [
        "http://hrss.sz.gov.cn/szsi/sbjxxgk/zcfggfxwj/zcfg/index.html",
        "http://hrss.sz.gov.cn/szsi/sbjxxgk/zcfggfxwj/zcfg/index_2.html",
        "http://hrss.sz.gov.cn/szsi/sbjxxgk/zcfggfxwj/zcfg/index_3.html"
    ]
    final_policy = pd.DataFrame()
    for url in url_list:
        response = ct.get_url(url)
        table = parse_policy_list(response)
        final_policy = final_policy.append(table, ignore_index=True)

    if 'origin' not in os.listdir(os.getcwd()):
        os.mkdir('origin')
    final_policy.to_excel('origin/sz_policy_list.xlsx', index=False)

    for i in range(final_policy.shape[0]):
        # ct.save_to_pdf(final_policy['url'][i], final_policy['标题'][i])
        ct.save_to_word(final_policy['url'][i], final_policy['标题'][i])
