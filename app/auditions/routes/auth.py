from http import HTTPStatus
from flask import Blueprint, request

from app.handlers.response_handler import ResponseHandler
from app.handlers.error_handler import ErrorResponseHandler
from app.auditions.services.auth_service import AuthService

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=['POST'], strict_slashes=True)
def register():
    '''Register user.'''
    try:
        response = AuthService.register(request)
    except Exception as e:
        return ErrorResponseHandler.handle_error(message=str(e), status_code=HTTPStatus.BAD_REQUEST)
    
    return ResponseHandler.handle_response(response, status_code=HTTPStatus.CREATED, message=HTTPStatus.CREATED.phrase)


@auth_blueprint.route('/verify', methods=['GET'], strict_slashes=True)
def verify_account():
    '''Verify user account'''
    # get token from request arguments
    try:
        response = AuthService.verify_account(request)
    except Exception as e:
        return ErrorResponseHandler.handle_error(message=str(e), status_code=HTTPStatus.BAD_REQUEST)

    return ResponseHandler.handle_response(response, status_code=HTTPStatus.OK, message=HTTPStatus.OK.phrase)
    


@auth_blueprint.route('/login', methods=['POST'], strict_slashes=True)
def login():
    '''Login user.'''
    try:
        response = AuthService.login(request)
    except Exception as e:
        return ErrorResponseHandler.handle_error(message=str(e), status_code=HTTPStatus.BAD_REQUEST)

    return ResponseHandler.handle_response(response, status_code=HTTPStatus.OK, message=HTTPStatus.OK.phrase)
