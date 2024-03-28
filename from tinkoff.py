from tinkoff.invest import Client

TOKEN = ''

with Client(TOKEN) as client:
    accounts = client.users.get_accounts()
    for id in [acc.id for acc in accounts.accounts]:
        for x in client.operations.get_portfolio(account_id=id).positions:
            print(x.figi)
        print('-------')
        