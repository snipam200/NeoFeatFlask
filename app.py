from flask import Flask, jsonify, request
from employees_service import EmployeesService
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
service = EmployeesService()

uri = os.getenv('URI')
user = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
driver = GraphDatabase.driver(uri, auth=(user, password),database="neo4j")


@app.route('/employees', methods=['GET'])
def get_employees():
    sort = request.args.get("sort")
    filter = request.args.get("filter")
    try:
        response = service.get_employees(sort, filter)
    except Exception as e:
       return jsonify({'message': e.args[0]}), 404
    return jsonify(response), 200

@app.route('/employees', methods=['POST'])
def create_employee():
    employee = request.get_json()
    try:
        response, code = service.create_employee(employee)
        return jsonify(response), code
    except Exception as e:
        return jsonify({'message': e.args[0]}), 409

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    try:
        employee = request.get_json()
        response, code = service.update_employee(id, employee)
        return jsonify(response), code
    except Exception as e:
        return jsonify({'message': e.args[0]}), 404

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    response, code = service.delete_employee(id)
    return jsonify(response), code

@app.route('/employees/<int:id>/subordinates', methods=['GET'])
def get_subordinates(id):
    try:
        response = service.get_subordinates(id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'message': e.args[0]}), 404

@app.route('/employees/<int:id>/department', methods=['GET'])
def get_departments_by_employees_id(id):
    try:
        response = service.get_department_by_employees_id(id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'message': e.args[0]}), 404

if __name__ == '__main__':
    app.run()

