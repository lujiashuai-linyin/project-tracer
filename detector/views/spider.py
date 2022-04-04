#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import json


def baidu_translate():
    # 1.指定url
    post_url = 'https://fanyi.baidu.com/sug'
    # 2.进行UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    # 3.post请求参数处理（同get请求一致）
    word = input('enter a word:')
    data = {'kw': word}
    # 4.请求发送
    response = requests.post(
        url=post_url,
        data=data,
        headers=headers,
    )
    # 5.获取响应数据:json()方法返回的是obj（如果确认响应数据是json类型的，才可以使用json（））
    dic_obj = response.json()
    data = dic_obj.get('data')
    v = data[0]['v']

    fileName = word + '.json'
    with open(fileName, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data[0], ensure_ascii=False))
    print(f'{word} >>>> {v}')

def douban_movie():

    url = 'https://movie.douban.com/j/chart/top_list'
    param = {
        'type': '24',
        'interval_id': '100:90',
        'action':'',
        'start': '0',#从库中的第几部电影去取
        'limit': '20',#一次取出的个数
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

    }
    response = requests.get(url=url,params=param,headers=headers)

    list_data = response.json()

    with open('./douban.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(list_data, ensure_ascii=False))
if __name__ == '__main__':
    douban_movie()
