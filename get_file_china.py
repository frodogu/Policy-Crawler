# import json
# import random
# import re
# import time
import pandas as pd
# import requests
# from bs4 import BeautifulSoup
from lxml import etree
import crawlertools as ct


def parse_policy_list(response):
    datas = etree.HTML(response)
    datas = datas.xpath("//table//tbody")
    # table = res_elements.xpath('//table[@id="table1"]')
    col_list = []
    for i in range(1, 5):
        col_name = ''.join(datas[0].xpath(".//tr[%s]//td[1]//text()" % i)[0].split())
        col_list.append(col_name)
        col_name = ''.join(datas[0].xpath(".//tr[%s]//td[3]//text()" % i)[0].split())
        col_list.append(col_name)
    col_list.append('url')

    df_policy = pd.DataFrame(columns=col_list)

    for i in range(len(datas)):
        value_list = []
        for j in range(1, 5):
            if j != 3:
                if datas[i].xpath(".//tr[%s]//td[2]//text()" % j):
                    policy_value = ''.join(datas[i].xpath(".//tr[%s]//td[2]//text()" % j)[0].split())
                else:
                    policy_value = ''
                value_list.append(policy_value)
                if datas[i].xpath(".//tr[%s]//td[4]//text()" % j):
                    policy_value = ''.join(datas[i].xpath(".//tr[%s]//td[4]//text()" % j)[0].split())
                else:
                    policy_value = ''
                value_list.append(policy_value)
            else:
                if datas[i].xpath(".//tr[%s]//td[2]//text()" % j):
                    policy_value = ''.join(datas[i].xpath(".//tr[%s]//td[2]//text()" % j)[1].split())
                else:
                    policy_value = ''
                value_list.append(policy_value)
                if datas[i].xpath(".//tr[%s]//td[4]//text()" % j):
                    policy_value = ''.join(datas[i].xpath(".//tr[%s]//td[4]//text()" % j)[0].split())
                else:
                    policy_value = ''
                value_list.append(policy_value)
        url_value = 'http://www.mohrss.gov.cn/xxgk2020/fdzdgknr/zcfg/gfxwj/shbx'+''.join(datas[i].xpath(".//tr[3]//a/@href")[0].split())[2:]
        value_list.append(url_value)
        if value_list[7] != '':
            value_list[6] = '已废止'
        else:
            value_list[6] = '有效'

        data = {  # 用数据字典，存储需要的信息
            '%s' % (col_list[x]): value_list[x] for x in range(9)
        }

        df_policy = df_policy.append(data, ignore_index=True)

        df_policy = df_policy.append(data, ignore_index=True)

    return df_policy


if __name__ == "__main__":
    main_url = "http://www.mohrss.gov.cn/xxgk2020/fdzdgknr/zcfg/gfxwj/shbx/"
    url_list = [
        "http://www.mohrss.gov.cn/xxgk2020/fdzdgknr/zcfg/gfxwj/shbx/index.html"
    ]

    for i in range(1, 18):
        new_url = main_url + "index_%s.html" % i
        url_list.append(new_url)

    final_policy = pd.DataFrame()
    for url in url_list:
        response = ct.get_url(url)
        table = parse_policy_list(response)
        final_policy = final_policy.append(table, ignore_index=True)

    final_policy.to_excel('china_policy_list.xlsx', index=False)
