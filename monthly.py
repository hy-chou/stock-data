from sys import exit, argv
import requests as req


def get_monthly(yyyy, stockNo):
    print('正在下載{}年{}資料⋯⋯'.format(yyyy, stockNo))
    url = 'https://www.twse.com.tw/exchangeReport/FMSRFK'
    payload = {'response': 'json', 'date': yyyy + '0101', 'stockNo': stockNo}
    r = req.get(url, params=payload)
    print('伺服器回應：{}'.format(r.json()['stat']).replace('81', '1992'))
    if len(r.json()) < 2:
        exit()
    return r.json()


def save2csv(raw, fileName):
    print('資料處理中⋯⋯')
    csv = '年,月,均價\n'
    for row in raw['data']:
        # [年度, 月份, 最高價, 最低價, 加權(A/B)平均價, 成交筆數, 成交金額(A), 成交股數(B), 週轉率(%)]
        csv += '{},{},'.format(int(row[0]) + 1911, row[1])  # year / month
        tVal = int(row[6].replace(',', ''))
        tVol = int(row[7].replace(',', ''))
        csv += '{:.2f}\n'.format(tVal / tVol)  # average price
    with open(fileName, 'w') as f:
        f.write(csv)
    print('已儲存至{}'.format(fileName))


if __name__ == '__main__':
    def usage_error():
        print('用法：python3 monthly.py <股票代號> <查詢年份> [-o <輸出檔名>]')
        exit()

    if len(argv) not in [3, 5]:
        usage_error()
    if len(argv) == 5 and argv[3] != '-o':
        usage_error()

    stockNo = argv[1]
    yyyy = argv[2] if int(argv[2]) > 1911 else str(int(argv[2]) + 1911)
    fileName = argv[4] if len(argv) == 5 else stockNo + 'm' + yyyy
    if '.csv' not in fileName:
        fileName += '.csv'

    save2csv(get_monthly(yyyy, stockNo), fileName)
