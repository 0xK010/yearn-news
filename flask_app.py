from flask import Flask, render_template
import requests, json

app = Flask(__name__)

@app.route('/')
def index():
    # get price data
    coin_gecko_url = 'https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e&vs_currencies=USD'

    yfi_price = requests.get(coin_gecko_url)
    price_json_obj = yfi_price.json()
    YFI = '${:,.2f} USD'.format(price_json_obj['0x0bc529c00c6401aef6d220be8c6ea1667f6ad93e']['usd'])

    # get TVL data
    defi_pulse_url = 'https://data-api.defipulse.com/api/v1/defipulse/api/GetProjects?api-key=06f9063a11d3f6d69594c9304d074cde1f92f4dfe86b1668704da3a12cee'

    total_value_locked = requests.get(defi_pulse_url)
    json_obj = total_value_locked.json()

    for project in json_obj:
        name = project.get("name")
        if name == 'yearn.finance':
            TVL = '${:,.2f} USD'.format(project['value']['tvl']['USD'].get("value"))
            #ETH_TVL = '{:,.2f} ETH'.format(project['value']['tvl']['ETH'].get("value"))
    #TVL = 'disabled'
    #ETH_TVL = 'disabled'

    return render_template('index.html', YFI = YFI, TVL = TVL)

@app.route('/newsletters/<number>')
def show_newsletter(number):
    route_url = 'newsletters/' + number + '.html'
    return render_template(route_url)

@app.route('/archive')
def show_archive():
    return render_template('newsletters/archive.html')


if __name__ == '__main__':
    app.run()
