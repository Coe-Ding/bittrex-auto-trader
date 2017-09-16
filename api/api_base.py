import json
import http.client
import hashlib
import hmac
import time

# YOUR API KEY AND SECRET
KEY = ''
SECRET = ''


def get_conn():
    return http.client.HTTPSConnection('bittrex.com')


def get_api_header(uri):
    return {'apisign': str(hmac.new(SECRET.encode(encoding='UTF-8'), uri.encode(encoding='UTF-8'), hashlib.sha512).hexdigest())}


def print_error(msg, endpoint, params, r):
    print('\nERROR', msg, '\n', endpoint, params, '\n', r)


def get_result(response, endpoint, params):
    result = json.loads(response.read())

    if result['message']:
        print_error(result['message'], endpoint, params, result)
        return result['message']
    elif result['result']:
        return result['result']
    elif not(result['success']):
        print_error('No result or message', endpoint, params, response.status)

    # print_error('No result or message', endpoint, params, response.status)


def get_response(conn, endpoint, params, headers):
    uri = '/api/v1.1/' + endpoint + '?' + params if params != '' else '/api/v1.1/' + endpoint
    conn.request('GET', uri, {}, headers)
    response = conn.getresponse()
    
    if response.status == 200:
        return response
    else:
        print_error('status ' + str(response.status), endpoint, params, response)


def make_api_request(endpoint, params):
    conn = get_conn()
    response = get_response(conn, endpoint, params, {})
    result = get_result(response, endpoint, params)

    conn.close()
    return result


def make_api_auth_request(endpoint, params):
    nonce = str(int(time.time() * 1000))
    all_params = 'apikey=' + KEY + '&nonce=' + nonce + params
    headers = get_api_header('https://bittrex.com/api/v1.1/' + endpoint + '?' + all_params)

    conn = get_conn()
    response = get_response(conn, endpoint, all_params, headers)
    
    if response:
        result = get_result(response, endpoint, all_params)
        conn.close()
        return result

    conn.close()
