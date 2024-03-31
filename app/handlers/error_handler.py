class ErrorResponseHandler:
    '''Handle error responses.'''

    @staticmethod
    def handle_error(status_code, message):
        '''Handle error response.'''
        return {'message': message, 'status_code': status_code }
