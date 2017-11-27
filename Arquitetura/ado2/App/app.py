from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from flask_cors import CORS

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

CORS(app)

class Customer(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from customers")
        return {'customers': [i[0] for i in query.cursor.fetchall()]}

class Customer_Id(Resource):
    def get(self, customer_id):
        conn = db_connect.connect()
        query = conn.execute("select * from customers where CustomerId =%d "  %int(customer_id))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

class Customer_Id_Delete(Resource):
	def delete(self, customer_id):
		conn = db_connect.connect()
		query = conn.execute("delete from customers where CustomerId = %d" %int(customer_id))

class Customers_Id_Company_Update(Resource):
	def post(self, customer_id):
		conn = db_connect.connect()
		newCompany = request.data
		sql = "update customers set Company=? where CustomerId=?"
		conn.execute(sql,(newCompany,customer_id))

api.add_resource(Customer, '/customers')
api.add_resource(Customer_Id, '/customers/<customer_id>')
api.add_resource(Customers_Id_Delete,'/customer_delete/<customer_id>')
api.add_resource(Customers_Id_Company_Update,'/customer_update/<customer_id>')

if __name__ == '__main__':
     app.run(host='0.0.0.0',port='5002')
