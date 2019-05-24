import bs4 as bs
import requests

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    # print(resp.text)
    soup = bs.BeautifulSoup(resp.text)
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers =[]
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open('sp500tickers.txt', 'w') as f:
        for ticker in tickers:    
            f.write(ticker)

        print(tickers)
        
        return tickers

save_sp500_tickers()

def show_tickers():
    with open('sp500tickers.pickle', 'rb') as ticker_file:
        tickers = ticker_file.read()
    print(tickers)

# show_tickers()
