import requests as req
import json
from sys import exit, argv


def get_json(stock_no):
    print("{} 資料下載中⋯⋯".format(stock_no))
    url = "https://www.twse.com.tw/exchangeReport/FMNPTK"
    payload = {"response": "json", "stockNo": stock_no}
    r = req.get(url, params=payload)
    print("伺服器回應：{}".format(r.json()["stat"]))
    if len(r.json()) < 2:
        exit()
    return r.json()


def save_json(rawD, fileName):
    print("資料處理中⋯⋯")
    j = {}
    j["title"] = rawD["title"].replace(" ", "")
    j["col"] = [rawD["fields"][i] for i in [0, 6, 4, 2, 1]]
    j["data"] = []
    for row in rawD["data"]:
        k = []
        k.append(row[0] + 1911)
        k.append(float(row[6]))
        k.append(float(row[4]))
        k.append(int(str(row[2]).replace(",", "")))
        k.append(int(str(row[1]).replace(",", "")))
        j["data"].append(k)
    with open(fileName, 'w') as f:
        f.write(json.dumps(j, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    def usageError():
        print("用法：python3 yearly.py <股票代號> [-o <輸出檔名>]")
        exit()

    if len(argv) not in [2, 4]:
        usageError()
    if len(argv) == 4 and argv[3] != "-o":
        usageError()

    stock_no = argv[1]
    fileName = argv[3] if len(argv) == 4 else stock_no + "y"
    if ".json" not in fileName:
        fileName += ".json"

    save_json(get_json(stock_no), fileName)
