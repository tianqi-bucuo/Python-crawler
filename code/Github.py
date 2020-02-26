import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
}
first_url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'
ids = [1]
for page in range(1, 5):
    data = {
        'on': 'true',
        'page': str(page),
        'pageSize': '15',
        'productName': '',
        'conditionType': '1',
        'applyname': '',
        'applysn': '',
    }

    response = requests.post(url=first_url, data=data, headers=headers)
    if response.headers['Content-Type'] == 'application/json;charset=UTF-8':
        json_obj = response.json()
        for dic in json_obj['list']:
            ids.append(dic['ID'])
print(ids)
