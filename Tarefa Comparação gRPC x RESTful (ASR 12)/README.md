# RESTful-WS-Example

Simple RESTful Web Service used to illustrate the concept (based on the example by S. Subramanian on DZone.com). Starter code for the assignment described below.

## What was done on this assignment

a) **Store and update the salary of the employee.** Each employee has a `salary` field (number). It is set on creation (`POST`) and changed with `PUT`, either through the JSON body or the path form.

b) **Error checking.** Requests that refer to a missing employee return `404`; malformed or invalid input returns `400`; creating an existing employee returns `409`.

c) **Average salary.** `GET /empdb/employee/average` returns the average salary considering all employees.

d) **Documentation** of the API (below).

## How to run

Install Flask and requests:

    $:> python3 -m pip install flask requests

Start the server (on the EC2 machine):

    $:> python3 EmployeeService.py

Run the client test on another machine. Edit `const.py` with the server IP, or override it with an environment variable:

    $:> python3 EmployeeServiceClient.py
    $:> EMPDB_URL=http://<server-ip>:5678 python3 EmployeeServiceClient.py

Note: open port 5678 on the firewall at EC2 (security group).

## API

Base URL: `http://<server-ip>:5678/empdb/employee`

All request and response bodies are JSON. Each employee has the fields `id` (string), `name`, `title`, and `salary` (number, non-negative).

| Method | Endpoint | Description | Success | Errors |
|--------|----------|-------------|---------|--------|
| GET | `/empdb/employee` | List all employees | 200 `{"emps": [...]}` | — |
| GET | `/empdb/employee/average` | Average salary of all employees | 200 `{"average_salary": 3166.67, "count": 3}` | 404 if there are no employees |
| GET | `/empdb/employee/<id>` | Get one employee | 200 `{"emp": [{...}]}` | 404 if not found |
| POST | `/empdb/employee` | Create an employee | 201 `{"emp": [{...}]}` | 400 missing fields or invalid salary; 409 id already exists |
| PUT | `/empdb/employee/<id>` | Update name, title and/or salary (JSON body, e.g. `{"title": "Programmer", "salary": 2500}`) | 200 `{"emp": [{...}]}` | 400 invalid body or salary; 404 not found |
| PUT | `/empdb/employee/<id>/<salary>` | Update only the salary (salary in the path, e.g. `/201/4000`) | 200 `{"emp": [{...}]}` | 400 invalid salary; 404 not found |
| DELETE | `/empdb/employee/<id>` | Delete an employee | 200 `{"response": "Success"}` | 404 not found |

### Examples

    curl http://<server-ip>:5678/empdb/employee/average

    curl -X POST -H "Content-Type: application/json" \
         -d '{"id":"301","name":"Juaríssimo Salvo","title":"Sr Programmer","salary":"3000"}' \
         http://<server-ip>:5678/empdb/employee

    curl -X PUT http://<server-ip>:5678/empdb/employee/201/4000

### Error response format

Errors return the HTTP status code and a JSON object with an `error` message, for example:

    HTTP 404 {"error": "Employee 999 not found"}
