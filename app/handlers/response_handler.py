from flask import jsonify


class ResponseHandler:
    '''Handle responses.'''
    
    @staticmethod
    def handle_response(response, message=None, status_code=None):
        '''Handle response.'''
        return {
            'message': message,
            'status_code': status_code,
            'data': response
        }
