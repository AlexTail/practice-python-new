from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

import sqlite3

db_path = "new.db" # path to the DB new.db

@dispatcher.add_method 
def create(currency, flag):
    """
    Function to create a new account
    """
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    result = cur.execute("""SELECT id FROM account
                            WHERE id > 0""").fetchall()
    if len(result) > 0:
        user_id = max(result[-1]) + 1 
    else:
        user_id = 1 
    money = 0 
    cur.execute("""INSERT INTO account(id,money,flag,currency) 
                   VALUES(""" + str(user_id) + ',' + str(money) + ',"' + 
                   str(flag) + '","' + currency + '")') 
    con.commit() 
    con.close()     
    return user_id 


@dispatcher.add_method 
def balance(user_id):
    """
    Function for getting account balance
    """
    
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    result = cur.execute("""SELECT money,currency FROM account
                            WHERE id == """ + str(user_id)).fetchone() 
    con.close()  
    return result 


@dispatcher.add_method 
def transfer(first_id, second_id, money):
    """
    Function for exchanging between different accounts
    """
    
    exchange_rate = {
    ('EUR', 'USD'): 1.24,
    ('USD', 'EUR'): 0.8064516129032258,
    ('RUB', 'EUR'): 0.01417836381681554, 
    ('EUR', 'RUB'): 70.53,
    ('RUB', 'USD'): 0.017605633802816902,
    ('USD', 'RUB'): 56.8
    } 
    
    money = int(money)
    
    start_money = money 
    
    con = sqlite3.connect(db_path) 
    cur = con.cursor()
    money_first_id = cur.execute("""SELECT money,currency,flag FROM account
                                    WHERE id == """ + str(first_id)).fetchone() 
    money_second_id = cur.execute("""SELECT money,currency FROM account
                                     WHERE id == """ + str(second_id)).fetchone() 
    
    if money_first_id[2] == 'True': 
        flag = True 
    else:
        flag = False
    
    if int(money_first_id[0]) >= money or flag: 
      
        
        if money_first_id[1] == money_second_id[1]:
            end_second_money = int(money_second_id[0]) + money  
        else:
            money *= exchange_rate[(money_first_id[1], money_second_id[1])]
            end_second_money = int(money_second_id[0]) + money 
        
        exchange = money_first_id[1] + '->' + money_second_id[1]       
        string = str(first_id) + ',' + str(second_id) + ',' + str(start_money) + ',"' + exchange + '")'

        cur.execute("""INSERT INTO transactions(donor_id,recipient_id,money,currency) 
                       VALUES(""" + string) 
              
        cur.execute("""UPDATE account
                       SET money = money - """ + str(start_money) +
                       " WHERE id = " + str(first_id))
        
        cur.execute("""UPDATE account
                       SET money = """ + str(end_second_money) +
                       " WHERE id = " + str(second_id))
        con.commit()
        con.close()
        end = 'Успех'
    else:
        end = 'Не удалось совершить перевод'
    return end
    

@Request.application 
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)