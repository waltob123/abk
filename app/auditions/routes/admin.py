from http import HTTPStatus
from flask import Blueprint, request

from app.handlers.response_handler import ResponseHandler
from app.handlers.error_handler import ErrorResponseHandler
from app.auditions.services.admin_service import AdminService


admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@admin_blueprint.route('/auditions/all', methods=['GET'], strict_slashes=True)
def get_all_auditions():
    '''Get all auditions.'''
    try:
        response = AdminService.get_all_auditions()
    except Exception as e:
        return ErrorResponseHandler.handle_error(message=str(e), status_code=HTTPStatus.BAD_REQUEST)
    
    return ResponseHandler.handle_response(response, status_code=HTTPStatus.OK, message=HTTPStatus.OK.phrase)


@admin_blueprint.route('/auditions/<string:audition_id>', methods=['GET'], strict_slashes=True)
def get_audition(audition_id):
    '''Get audition.'''
    try:
        response = AdminService.get_audition(audition_id)
    except Exception as e:
        return ErrorResponseHandler.handle_error(message=str(e), status_code=HTTPStatus.BAD_REQUEST)
    
    return ResponseHandler.handle_response(response, status_code=HTTPStatus.OK, message=HTTPStatus.OK.phrase)
