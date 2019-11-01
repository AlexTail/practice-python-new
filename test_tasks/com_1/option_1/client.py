import requests
import json
import time


def main():
    url = "http://localhost:4000/jsonrpc" 
    headers = {'content-type': 'application/json'}
    print('(1) Создать счет (2) Посмотреть баланс счета (3) Перевод на другой счет')
    inp = input()
    if '1' in inp.lower(): 
        payload = create()
    elif '2' in inp.lower():
        payload = balance()
    else:
        payload = transfer()
        
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()
    print(response['result'])
    time.sleep(60)
    

def balance():
    print('id счета')
    user_id = input()
    
    payload = {
        "method": "balance",
        "params": [user_id],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return payload


def transfer():
    print('id счета донора')
    first_user_id = input()
    print('id счета получателя')
    second_user_id = input()
    print('Сумма перевода')
    money = input()
    
    payload = {
        "method": "transfer",
        "params": [first_user_id, second_user_id, money],
        "jsonrpc": "2.0",
        "id": 0,
    }    
    return payload

    
def create():
    
    print("Валюта(RUB, EUR, USD):")
    currency = input()
    
    while currency not in ['RUB', 'EUR', 'USD']:
        print("Введите одну из этих валют(RUB, EUR, USD):")
        currency = input()
        
    print('Флаг овердрафности(true, false)')
    flag = input()
    
    while flag.lower().strip() not in ['false', 'true']:
        print("true, false:")
        flag = input()
        
    if flag.lower().strip() == 'true':
        flag = True
    else:
        flag = False
        
    payload = {
        "method": "create",
        "params": [currency, flag],
        "jsonrpc": "2.0",
        "id": 0,
    }
    return payload
    
    
if __name__ == "__main__":
    main()