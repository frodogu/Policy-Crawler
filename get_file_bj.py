# import json
# import random
# import re
# import time
import pandas as pd
# import requests
# from bs4 import BeautifulSoup
from lxml import etree
import crawlertools as ct


def parse_url_list(response):
    datas = etree.HTML(response)
    datas = datas.xpath("//html//body//div[3]//div[2]//ul")
    # table = res_elements.xpath('//table[@id="table1"]')
    policy_url_list = pd.DataFrame(columns=['title', 'url'])
    for i in range(1, 22):
        try:
            policy_url = "http://rsj.beijing.gov.cn/xxgk/zcwj" + ''.join(
                datas[0].xpath(".//li[%s]//a/@href" % i)[0].split())[1:]
            policy_title = datas[0].xpath(".//li[%s]//text()" % i)[0]
            data = {  # 用数据字典，存储需要的信息
                'title': policy_title,
                'url': policy_url
            }
            policy_url_list = policy_url_list.append(data, ignore_index=True)
        except IndexError:
            break
    return policy_url_list


def parse_policy_list(response):
    datas = etree.HTML(response)
    datas = datas.xpath("//html//body//div[4]//div//ol")
    value_list, col_list = [], []
    for i in range(1, 9):
        if len(datas[0].xpath(".//li[%s]//text()" % i)) == 2:
            policy_value = datas[0].xpath(".//li[%s]//text()" % i)[1]
        else:
            policy_value = ''
        value_list.append(policy_value)
        col_name = datas[0].xpath(".//li[%s]//text()" % i)[0][1:-1]
        col_list.append(col_name)

    data = {  # 用数据字典，存储需要的信息
        '%s' % (col_list[x]): value_list[x] for x in range(8)
    }

    return data


if __name__ == "__main__":

    sleep_time = 0.1
    main_url = "http://rsj.beijing.gov.cn/xxgk/zcwj/"
    url_list = [
        "http://rsj.beijing.gov.cn/xxgk/zcwj/index.html"
    ]

    for i in range(1, 25):
        new_url = main_url + "index_%s.html" % i
        url_list.append(new_url)

    total_url = pd.DataFrame()
    for url in url_list:
        response = ct.getURL(url)
        table = parse_url_list(response)
        total_url = total_url.append(table, ignore_index=True)

    final_policy = pd.DataFrame()
    for i in range(total_url.shape[0]):
        url = str(total_url['url'][i])
        response = ct.getURL(url)
        policy_dict = parse_policy_list(response)
        policy_dict['标题'] = total_url['title'][i]
        policy_dict['url'] = total_url['url'][i]
        final_policy = final_policy.append(policy_dict, ignore_index=True)

    final_policy.to_excel('bj_policy_list.xlsx', index=False)
