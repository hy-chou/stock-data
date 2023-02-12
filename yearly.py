from sys import exit, argv
import requests as req
# import json


def get_yearly(stockNo):
    print('正在下載{}資料⋯⋯'.format(stockNo))
    url = 'https://www.twse.com.tw/exchangeReport/FMNPTK'
    payload = {'response': 'json', 'stockNo': stockNo}
    r = req.get(url, params=payload)
    print('伺服器回應：{}'.format(r.json()['stat']))
    if len(r.json()) < 2:
        exit()
    return r.json()


def save2csv(raw, fileName):
    print('資料處理中⋯⋯')
    csv = '年,均價\n'
    for row in raw['data']:
        # [年度, 成交股數, 成交金額, 成交筆數, 最高價, 日期, 最低價, 日期, 收盤平均價]
        csv += '{},'.format(int(row[0]) + 1911)  # year
        tVol = int(row[1].replace(',', ''))
        tVal = int(row[2].replace(',', ''))
        csv += '{:.2f}\n'.format(tVal / tVol)  # average price
        # csv += '{},{},'.format(row[6], row[4])  # lowest / highest price
        # csv += '{:.2e},{:.2e}\n'.format(tVal, tVol)  # trade value / volumn
    with open(fileName, 'w') as f:
        f.write(csv)
    print('已儲存至{}'.format(fileName))


# def save2json(rawD, fileName):
#     print('資料處理中⋯⋯')
#     j = {}
#     j['title'] = rawD['title'].replace(' ', '')
#     j['col'] = [rawD['fields'][i] for i in [0, 6, 4, 2, 1]]
#     j['data'] = []
#     for row in rawD['data']:
#         k = []
#         k.append(row[0] + 1911)
#         k.append(float(row[6]))
#         k.append(float(row[4]))
#         k.append(int(str(row[2]).replace(',', '')))
#         k.append(int(str(row[1]).replace(',', '')))
#         j['data'].append(k)
#     with open(fileName, 'w') as f:
#         f.write(json.dumps(j, ensure_ascii=False, separators=(',', ':')))


if __name__ == '__main__':
    def usage_error():
        print('用法：python3 yearly.py <股票代號> [-o <輸出檔名>]')
        exit()

    if len(argv) not in [2, 4]:
        usage_error()
    if len(argv) == 4 and argv[2] != '-o':
        usage_error()

    stockNo = argv[1]
    fileName = argv[3] if len(argv) == 4 else stockNo + 'y'
    if '.csv' not in fileName:
        fileName += '.csv'

    save2csv(get_yearly(stockNo), fileName)
