import threading
import yfinance as yf

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

parsingCompanies = ["TSLA", "AAPL", "MSFT"]
# {
#   TSLA: []
# }
parsingPrices = {
    "TSLA": [],
    "AAPL": [],
    "MSFT": []
}


def parseCompanies():
    for i in range(len(parsingCompanies)):
        shares = yf.Ticker(parsingCompanies[i])

        parsingPrices[parsingCompanies[i]].append(int(shares.info["currentPrice"]))

        if len(parsingPrices[parsingCompanies[i]]) == 11:
            parsingPrices[parsingCompanies[i]].pop(0)

    print(parsingPrices)

