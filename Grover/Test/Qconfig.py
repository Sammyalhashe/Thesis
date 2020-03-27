# Before you can use the jobs API, you need to set up an access token.
# Log in to the IBM Q experience. Under "Account", generate a personal
# access token. Replace 'PUT_YOUR_API_TOKEN_HERE' below with the quoted
# token string. Uncomment the APItoken variable, and you will be ready to go.

APItoken = 'fa990f5e816bd5f800fc269a9b3f4fbe85c11f8969ea229ecc7a247c97f100ae5324c5fbedec09aa89db39db83e013b61cac3ed5ad10bded16e3080026f7b388'

config = {
    'url': 'https://quantumexperience.ng.bluemix.net/api',

    # If you have access to IBM Q features, you also need to fill the "hub",
    # "group", and "project" details. Replace "None" on the lines below
    # with your details from Quantum Experience, quoting the strings, for
    # example: 'hub': 'my_hub'
    # You will also need to update the 'url' above, pointing it to your custom
    # URL for IBM Q.
    'hub': None,
    'group': None,
    'project': None
}

if 'APItoken' not in locals():
    raise Exception('Please set up your access token. See Qconfig.py.')
