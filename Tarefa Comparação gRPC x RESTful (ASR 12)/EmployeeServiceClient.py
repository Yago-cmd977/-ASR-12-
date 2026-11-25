import os
import requests
import const

# Base URL can be overridden with the EMPDB_URL environment variable
# (e.g. for testing against a local server).
BASE_URL = os.environ.get('EMPDB_URL',
                          'http://' + const.IP_ADD + ':' + str(const.PORT))


def show(method, url, **kwargs):
    print('Calling ' + method + ' on endpoint: ' + url)
    response = requests.request(method, url, **kwargs)
    try:
        body = response.json()
    except ValueError:
        body = 'non-JSON response (' + response.reason + ')'
    print('  HTTP ' + str(response.status_code) + ' -> ' + str(body))
    return response


def serviceTester():
    api_base_url = BASE_URL + '/empdb/employee'
    print('Will connect to: ' + api_base_url)

    # GET all employees
    show('GET', api_base_url)

    # GET one employee
    show('GET', api_base_url + '/201')

    # PUT: update title
    show('PUT', api_base_url + '/101', json={'title': 'Programmer'})

    # PUT: update salary (path form)
    show('PUT', api_base_url + '/201/4000')

    # PUT: update salary (JSON form)
    show('PUT', api_base_url + '/101', json={'salary': 2500})

    # POST: create employee (with salary)
    show('POST', api_base_url, json={'id': '301', 'name': 'Juaríssimo Salvo',
                                     'title': 'Sr Programmer', 'salary': '3000'})

    # GET: average salary
    show('GET', api_base_url + '/average')

    # DELETE employee
    show('DELETE', api_base_url + '/101')

    # ---- Error cases ----
    print('\n--- Error cases ---')
    show('GET', api_base_url + '/999')                             # 404: not found
    show('PUT', api_base_url + '/999/1000')                        # 404: update missing employee
    show('PUT', api_base_url + '/201/-50')                         # 400: negative salary
    show('PUT', api_base_url + '/201/abc')                         # 400: non-numeric salary
    show('POST', api_base_url, json={'id': '301', 'name': 'x',
                                     'title': 'y', 'salary': 1})    # 409: duplicate id
    show('POST', api_base_url, json={'id': '400'})                 # 400: missing fields
    show('DELETE', api_base_url + '/999')                          # 404: delete missing employee
    show('PUT', api_base_url + '/201/40000/Programmer')            # 404: nonexistent route


if __name__ == '__main__':
    serviceTester()
