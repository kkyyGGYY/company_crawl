import random

import time
from fake_useragent import UserAgent
import pandas as pd
import requests
import json
from multiprocessing import Pool
from requests.exceptions import ReadTimeout, ConnectionError, RequestException, ProxyError

df = pd.read_csv('companydata.csv')
COM_LIST = df.iloc[:, 0].values
UA_LIST = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',

    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',

    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',

    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',


    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',

    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)',

    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',

    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',

    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',

    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
]


def get_random_ua():
    return UA_LIST[random.randint(0, len(UA_LIST)-1)]


def get_proxy():
    headers = {
        'user-agent': get_random_ua()
    }
    ip = requests.get('http://tvp.daxiangdaili.com/ip/?tid=557172982574022&num=1&protocol=https&delay=5&filter=on', headers=headers)
    return ip.text


def get_company_name_list():
    company_name_list = []
    for name in COM_LIST:
        if ' ' in name:
            name = ''.join(name.split(' '))
        company_name_list.append(name)
    return company_name_list


def get_company_crn(name):

    proxies = {
        "https": "http://{0}".format(get_proxy()),
    }
    headers = {
        'user-agent': get_random_ua()
    }
    print(proxies)
    try:
        response = requests.get(
            'https://api.riskstorm.com/company/search?from=0&keyword={name}&size=20&tab_type=general'.format(
                name=name), headers=headers, proxies=proxies, timeout=2)
        # t = response.elapsed.microseconds
        # print(response.text)
        # print(t)
        com_json = json.loads(response.text)
        print(com_json)
        return com_json['companies'][0]['crn']

    except ReadTimeout:
        print('Timeout')
        get_company_crn(name)
    except ConnectionError:
        print('Connection error')
        get_company_crn(name)
    except RequestException:
        print('Error')
        get_company_crn(name)
        # finally:
        #     get_company_crn(name)

    # print(response.text)
    # com_json = json.loads(response.text)
    # print(com_json['companies'][0]['crn'])
    # return com_json['companies'][0]['crn']


def main(company_name):
    company_crn = get_company_crn(company_name)
    print(company_crn)


if __name__ == '__main__':
    company_name_list = get_company_name_list()
    # main(company_name_list[58])
    # for name in company_name_list:
    #     print(name)
    #     main(name)
        # time.sleep(1)
    # get_proxy()
    pool = Pool()
    pool.map(main, company_name_list)
    # print(get_random_ua())