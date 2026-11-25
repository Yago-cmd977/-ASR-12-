#
# The original code for this example is credited to S. Subramanian,
# from this post on DZone: https://dzone.com/articles/restful-web-services-with-python-flask
#
# Extended for the ASR 12 assignment: salary storage/update, error handling
# (HTTP 400/404/409), and average salary endpoint.
#

from flask import Flask
from flask import jsonify
from flask import request

import const

app = Flask(__name__)

empDB = [
    {'id': '101', 'name': 'Arício Segundo', 'title': 'Technical Leader', 'salary': 2000.0},
    {'id': '201', 'name': 'Rusmão Terceiro', 'title': 'Sr Software Engineer', 'salary': 3000.0},
]


def error(status, message):
    return jsonify({'error': message}), status


def findEmp(empId):
    matches = [emp for emp in empDB if emp['id'] == empId]
    return matches[0] if matches else None


def parseSalary(value):
    """Converts a salary to a non-negative float. Returns None if invalid."""
    try:
        salary = float(value)
    except (TypeError, ValueError):
        return None
    if salary != salary or salary < 0:  # NaN or negative
        return None
    return salary


@app.route('/empdb/employee', methods=['GET'])
def getAllEmp():
    return jsonify({'emps': empDB})


# Static route: must not be confused with /empdb/employee/<empId>
@app.route('/empdb/employee/average', methods=['GET'])
def getAverageSalary():
    if len(empDB) == 0:
        return error(404, 'No employees registered')
    average = sum(emp['salary'] for emp in empDB) / len(empDB)
    return jsonify({'average_salary': round(average, 2), 'count': len(empDB)})


@app.route('/empdb/employee/<empId>', methods=['GET'])
def getEmp(empId):
    emp = findEmp(empId)
    if emp is None:
        return error(404, 'Employee ' + empId + ' not found')
    return jsonify({'emp': [emp]})


@app.route('/empdb/employee/<empId>', methods=['PUT'])
def updateEmp(empId):
    emp = findEmp(empId)
    if emp is None:
        return error(404, 'Employee ' + empId + ' not found')

    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error(400, 'Request body must be a JSON object')

    if 'name' in body:
        emp['name'] = body['name']
    if 'title' in body:
        emp['title'] = body['title']
    if 'salary' in body:
        salary = parseSalary(body['salary'])
        if salary is None:
            return error(400, 'Salary must be a non-negative number')
        emp['salary'] = salary

    return jsonify({'emp': [emp]})


@app.route('/empdb/employee/<empId>/<empSal>', methods=['PUT'])
def updateEmpSal(empId, empSal):
    emp = findEmp(empId)
    if emp is None:
        return error(404, 'Employee ' + empId + ' not found')

    salary = parseSalary(empSal)
    if salary is None:
        return error(400, 'Salary must be a non-negative number')

    emp['salary'] = salary
    return jsonify({'emp': [emp]})


@app.route('/empdb/employee', methods=['POST'])
def createEmp():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return error(400, 'Request body must be a JSON object')

    missing = [f for f in ('id', 'name', 'title', 'salary') if f not in body]
    if missing:
        return error(400, 'Missing fields: ' + ', '.join(missing))

    if findEmp(str(body['id'])) is not None:
        return error(409, 'Employee ' + str(body['id']) + ' already exists')

    salary = parseSalary(body['salary'])
    if salary is None:
        return error(400, 'Salary must be a non-negative number')

    dat = {
        'id': str(body['id']),
        'name': body['name'],
        'title': body['title'],
        'salary': salary,
    }
    empDB.append(dat)
    return jsonify({'emp': [dat]}), 201


@app.route('/empdb/employee/<empId>', methods=['DELETE'])
def deleteEmp(empId):
    emp = findEmp(empId)
    if emp is None:
        return error(404, 'Employee ' + empId + ' not found')
    empDB.remove(emp)
    return jsonify({'response': 'Success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=const.PORT)
