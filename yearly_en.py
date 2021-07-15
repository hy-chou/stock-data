import requests as req
import json
from sys import exit, argv


def get_json(stock_no):
    print("{} loading...".format(stock_no))
    url = "https://www.twse.com.tw/en/exchangeReport/FMNPTK"
    payload = {"response": "json", "stockNo": stock_no}
    r = req.get(url, params=payload)
    print("Server replies: {}".format(r.json()["stat"]))
    if len(r.json()) < 2:
        exit()
    return r.json()


def save_json(rawD, fileName):
    print("Processing data...")
    j = {}
    j["title"] = rawD["title"]
    j["col"] = [rawD["fields"][i] for i in [0, 6, 4, 2, 1]]
    j["data"] = []
    for row in rawD["data"]:
        k = []
        k.append(row[0])
        k.append(float(row[6]))
        k.append(float(row[4]))
        k.append(int(str(row[2]).replace(",", "")))
        k.append(int(str(row[1]).replace(",", "")))
        j["data"].append(k)
    with open(fileName, 'w') as f:
        f.write(json.dumps(j, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    def usageError():
        print("usage: python3 yearly_en.py <stockNo> [-o <outputFile>]")
        exit()

    if len(argv) not in [2, 4]:
        usageError()
    if len(argv) == 4 and argv[3] != "-o":
        usageError()

    stock_no = argv[1]
    fileName = argv[3] if len(argv) == 4 else stock_no + "y_en"
    if ".json" not in fileName:
        fileName += ".json"

    save_json(get_json(stock_no), fileName)
