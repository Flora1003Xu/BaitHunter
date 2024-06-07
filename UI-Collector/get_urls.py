# -*- coding: UTF-8 -*-
import json
import os
import re
import sys
import time

import requests
from lxml import etree


def get_pp_from_mi_store(pkg_name):
    response = requests.get('https://app.mi.com/details?id={}&ref=search'.format(pkg_name))
    html_content = response.text
    tree = etree.HTML(html_content)
    href = tree.xpath('//div[@class="float-right"]//a/@href')
    try:
        print(href[0])
        url_to_return = href[0]
        return url_to_return
    except IndexError:
        return None


def get_pp_from_tencent(pkg_name):
    response = requests.get('https://sj.qq.com/appdetail/{}'.format(pkg_name))
    html_content = response.text

    url_pattern = r'<a.*?href="(.*?)".*?>隐私政策</a>'
    matches = re.findall(url_pattern, html_content)
    if matches:
        if len(matches[0]) > 1:
            return matches[0][:]
        else:
            return None
    else:
        return None


def get_pkg_names_from_apk_pkgNametxt():
    with open('./AppUIAutomator2Navigation/apk_pkgName.txt') as f:
        lines = f.readlines()
    pkg_name_list = []
    for line in lines:
        pkg_name_list.append(line.split(' | ')[0])
    return pkg_name_list


def get_pkg_names_from_input_list(pkg_name_list):
    return pkg_name_list


def get_pp_from_app_store(pkg_names):
    pp_urls = {}
    missing_urls = set()
    for pkg_name in pkg_names:
        pp_url = None
        # 重复请求5次，如果三次都没有拿到隐私政策，那就没办法了
        cnt = 5
        if len(pkg_name) > 3:
            while cnt >= 0:
                try:
                    pp_url = get_pp_from_tencent(pkg_name)
                except Exception:
                    print('==========================================')
                    print('error occurred in get_pp_from_tencent...')
                    print('missing app is {}'.format(pkg_name))
                    print('==========================================')
                if pp_url is None:
                    try:
                        pp_url = get_pp_from_mi_store(pkg_name)
                    except Exception:
                        print('==========================================')
                        print('error occurred in get_pp_from_mi_store...')
                        print('missing app is {}'.format(pkg_name))
                        print('==========================================')
                    if pp_url is None:
                        print('==========================================')
                        print('{} not in store...'.format(pkg_name))
                        print('==========================================')
                        missing_urls.add(pkg_name)
                    else:
                        pp_urls[pkg_name] = pp_url
                        # print(pp_url)
                else:
                    pp_urls[pkg_name] = pp_url
                    # print(pp_url)
                if pp_url is None:
                    cnt -= 1
                    print(f'fail to find {pkg_name} in app store, try again...')
                    time.sleep(3)
                else:
                    break
    return pp_urls, missing_urls


if __name__ == '__main__':
    choice = True
    try:
        user_choice = sys.argv[1][:]
        if user_choice == 'y':
            choice = True
        else:
            choice = False
    except Exception:
        print('no user input.')
        if os.path.exists('./Privacy-compliance-detection-2.1/core/pkgName_url.json'):
            print(
                'pkgName_url exists,enter y to get privacy policy url from app store again,n to reuse privacy policy urls in pkgName_url.json.')
            input_ = input()
            if input_ == 'y':
                choice = True
            elif input_ == 'n':
                choice = False
            else:
                print('error input...')
    if choice:
        pp_urls, missing_urls = get_pp_from_app_store(get_pkg_names_from_apk_pkgNametxt())
        # 需要读取apk_pkgName.txt里的应用名记录
        with open(os.path.join('AppUIAutomator2Navigation', 'apk_pkgName.txt'), 'r', encoding='utf-8') as f:
            content = f.readlines()
        pkgName_appName_list = [item.rstrip('\n') for item in content]
        # 保存包名/应用名键值对到字典中
        pkgName_appName_dict = {}
        for pkgName_appName in pkgName_appName_list:
            pkgName, appName = pkgName_appName.split(' | ')
            appName = appName.strip('\'')
            pkgName_appName_dict[pkgName] = appName
        for key, val in pp_urls.items():
            if type(val) == list:
                pp_urls[key] = [pkgName_appName_dict[key], val]
            else:
                pp_urls[key] = [pkgName_appName_dict[key], [val]]
        with open('./Privacy-compliance-detection-2.1/core/pkgName_url.json', 'w') as f:
            json.dump(pp_urls, f, indent=4, ensure_ascii=False)
        if len(missing_urls) > 0:
            with open('./apps_missing_pp_url.txt', 'w') as f:
                for app in missing_urls:
                    f.write(app)
                    f.write('\n')
