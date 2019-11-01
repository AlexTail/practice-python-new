RU: Python3 + FLASK + SQLITE3

Для работы приложения, необходимо:

Установить пакеты:
	SQLAlchemy==1.3.10
	flask-marshmallow==0.10.1
	Flask-SQLAlchemy==2.4.1
	Flask==1.1.1

Запустить crud.py

Примеры JSON-запросов в Postman:

GET http://127.0.0.1:5000/allbas

--- --- --- --- ---

POST http://127.0.0.1:5000/ba

{
	"accountID": 10
}

--- --- --- --- ---

POST http://127.0.0.1:5000/newba

{
	"balance": 100,
	"currency": "EUR",
	"overdraft": true
}

--- --- --- --- ---

PUT http://127.0.0.1:5000/transaction
{
	"donorID": 11,
	"recipientID": 12,
	"value": 1000
}

--- --- --- --- ---

DELETE http://127.0.0.1:5000/deleteaccount

{
	"accountID": 13
}
