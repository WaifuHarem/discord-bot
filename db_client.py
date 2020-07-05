import requests
import logging
import json


class DbClient():

    session = requests.session()

    REQUEST_NOP       = 0
    REQUEST_ADD_SCORE = 1

    REPLY_GOOD = 0

    logger = logging.getLogger('bot.DbClient')
    

    @staticmethod
    def request(opcode, userid, data):
        request = {
            'cmd'    : opcode,
            'userid' : userid,
            'data'   : data
        }

        try: response = DbClient.session.post('http://127.0.0.1:8000', data=request)
        except requests.exceptions.ConnectionError as e:
            DbClient.logger.error(e)
            return

        #status = DbClient.validate_response(response)
        data = json.loads(response.text)
        DbClient.logger.info(data)


    ''' TODO
    @staticmethod
    def validate_response(response):
        status_code = response.status_code

        if response.status_code == 200: return 200  # Ok
        if response.status_code == 400: raise Exception(SessionMgr._logger, 'Error 400: Unable to process request')
        if response.status_code == 401: return 401  # Need to log in
        if response.status_code == 403: return 403  # Forbidden
        if response.status_code == 404: return 404  # Resource not found
        if response.status_code == 405: raise Exception(SessionMgr._logger, 'Error 405: Method not allowed')
        if response.status_code == 407: raise Exception(SessionMgr._logger, 'Error 407: Proxy authentication required')
        if response.status_code == 408: raise Exception(SessionMgr._logger, 'Error 408: Request timeout')
        if response.status_code == 429: return 429  # Too many requests
        if response.status_code == 500: raise Exception(SessionMgr._logger, 'Error 500: Internal server error')
        if response.status_code == 502: raise Exception(SessionMgr._logger, 'Error 502: Bad Gateway')
        if response.status_code == 503: raise Exception(SessionMgr._logger, 'Error 503: Service unavailable')
        if response.status_code == 504: raise Exception(SessionMgr._logger, 'Error 504: Gateway timeout')
    '''