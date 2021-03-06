import json
import os
from bs4 import BeautifulSoup
import requests
from django.http import JsonResponse, HttpResponse
import csv
import string


# 编程试题（一）
def get_epidemic_data(request):
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner#tab4"
    res = requests.get(url)
    html_path = os.sep.join(['project_app', 'html', 'epidemic_data.htm'])
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(res.text)
    soup = BeautifulSoup(open(html_path, encoding='utf-8'), features='html.parser')  # features值可为lxml
    lilist = json.loads(soup.find('script', {'id': 'captain-config'}).contents[0])
    csvpath = os.sep.join(['project_app', 'csv', 'epidemic_data.csv'])
    with open(csvpath, 'w', newline='') as c:
        head = ['地区', '新增', '现有', '累计', '治愈', '死亡']
        write = csv.writer(c)
        write.writerow(head)
        for info in lilist['component']:
            for single in info['caseList']:
                row = [single['area'], single['confirmedRelative'], single['curConfirm'],
                       single['confirmed'], single['crued'], single['died']]
                write.writerow(row)
    ret = {'code': 200, 'status': 'ok', 'message': '文件生成成功！'}
    return JsonResponse(ret)


# 编程试题（二）
def longtext_format(request):
    long_text = """
    Variopartner SICAV
    529900LPCSV88817QH61
    1. TARENO GLOBAL WATER SOLUTIONS FUND
    LU2001709034
    LU2057889995
    LU2001709547
    2. TARENO FIXED INCOME FUND
    LU1299722972
    3. TARENO GLOBAL EQUITY FUND
    LU1299721909
    LU1299722113
    LU1299722030
    4. MIV GLOBAL MEDTECH FUND
    LU0329630999
    LU0329630130
    """
    # 字符串截取之后经过处理的list
    text_list = []
    # 循环截取的字符串并且去除空格,追加到list
    for i in long_text.split('\n'):
        if len(i) > 0 and len(i.strip()) > 0:
            text_list.append(i.strip())
    # 处理结果字典初始化
    text_dict = dict()
    # 字典中key为sub_fund的list初始化
    text_dict['sub_fund'] = []
    # 循环字符串截取之后经过处理的list
    for index in range(len(text_list)):
        # 第一个元素为name
        if index == 0:
            text_dict['name'] = text_list[index]
        # 第二元素为lei
        elif index == 1:
            text_dict['lei'] = text_list[index]
        else:

            # 用ASCII，判断首位的编码是不是在大小写字母编码范围内
            letters_list = list(string.ascii_letters)
            # 用来取得数组下一个元素的count
            count = 1
            # sub_fund中的单一元素字典初始化
            sub_fund_ele = dict()
            # 判断是否以数字为开头，如果以数字开头则为title，否则追加到isin中
            if str(text_list[index])[0] not in letters_list:
                sub_fund_ele['title'] = str(text_list[index]).split('.')[1].strip()
                sub_fund_ele['isin'] = []
                # 这里做一个无限循环
                while True:
                    # 如果在以数字开头的元素之后的元素为字母开头,则追加到数组,否则跳出无限循环
                    if text_list[index + count][0] in letters_list:
                        sub_fund_ele['isin'].append(text_list[index + count])
                        # 下标与count的和不能超过数组长度-1，否则跳出
                        if index + count < len(text_list) - 1:
                           count += 1
                        else:
                            break
                    else:
                        break
            # 长度大于0的字典然后追加,因为在上面的操作中会生成空的字典
            if len(sub_fund_ele) > 0:
                text_dict['sub_fund'].append(sub_fund_ele)
    ret = {'code': 200, 'status': 'ok', 'message': text_dict}
    return JsonResponse(ret)
