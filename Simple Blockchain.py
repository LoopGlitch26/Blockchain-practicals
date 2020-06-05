import datetime
import hashlib

from flask import Flask, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine

db_connect = create_engine('sqlite:////chinook.db')  # The path depends on where you have the database stored
app = Flask(__name__)
api = Api(app)


class Block(Resource):
    blockNo = 0
    data = None
    next = None
    hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data

    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(self.data).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.blockNo).encode('utf-8')
        )
        return h.hexdigest()

    def __str__(self):
        return jsonify("Block Hash: " + str(self.hash()) + "\nBlockNo: " + str(self.blockNo) + "\nBlock Data: " + str(
            self.data) + "\nHashes: " + str(self.nonce) + "\n--------------")


class Blockchain(Resource):
    diff = 20
    maxNonce = 2 ** 32
    target = 2 ** (256 - diff)

    block = Block("Genesis")
    dummy = head = block

    def add(self, block):

        block.previous_hash = self.block.hash()
        block.blockNo = self.block.blockNo + 1

        self.block.next = block
        self.block = self.block.next

    def mine(self, block):
        for n in range(self.maxNonce):
            if int(block.hash(), 16) <= self.target:
                self.add(block)
                print(block)
                conn = db_connect.connect()
                return jsonify(block)
                break
            else:
                block.nonce += 1


""" Example of resource on flask
class Employees(Resource):
    def get(self):
        conn = db_connect.connect() # Connection to the Database
        query = conn.execute("select * from employees")  # This line executes a query and returns a json as a result
        return {'employees': [i[0] for i in query.cursor.fetchall()]}  # The first column that is EmployeeId is obtained

    def post(self):
        conn = db_connect.connect()
        last_name = request.json['LastName']
        first_name = request.json['FirstName']
        title = request.json['Title']
        reports_to = request.json['ReportsTo']
        birth_date = request.json['BirthDate']
        hire_date = request.json['HireDate']
        address = request.json['Address']
        city = request.json['City']
        state = request.json['State']
        country = request.json['Country']
        postal_code = request.json['PostalCode']
        phone = request.json['Phone']
        fax = request.json['Fax']
        email = request.json['Email']
        query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}', \
                             '{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}', \
                             '{13}')".format(last_name,first_name,title,
                                             reports_to, birth_date, hire_date, address,
                                             city, state, country, postal_code, phone, fax,
                                             email))
        return {'status': 'Nuevo empleado añadido'}


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        return jsonify(result)
"""

blockchain = Blockchain

for n in range(10):
    blockchain.mine(Block("Block " + str(n + 1)))

while blockchain.head != None:
    print(blockchain.head)
    blockchain.head = blockchain.head.next

api.add_resource(Block, '/block')  # Route_1
api.add_resource(Blockchain, '/blockchain')  # Route_2

if __name__ == '__main__':
    app.run(port='5000')
