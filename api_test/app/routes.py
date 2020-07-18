from .views import CheckBalance, WalletApi, Home

def initialize_routes(api):
    api.add_resource(Home, '/')
    api.add_resource(WalletApi, '/wallet')
    api.add_resource(CheckBalance, '/fetch/balance')
