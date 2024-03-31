from http import HTTPStatus
from flask import Blueprint, request

from app.handlers.response_handler import ResponseHandler
from app.handlers.error_handler import ErrorResponseHandler
from app.auditions.services.audition_service import AuditionService


audition_blueprint = Blueprint('audition', __name__, url_prefix='/auditions')


@audition_blueprint.route('', methods=['POST'], strict_slashes=True)
def create_audition():
    '''Create audition.'''
    try:
        response = AuditionService.create_audition(request)
    except Exception as e:
        return ErrorResponseHandler.handle_error(message=str(e), status_code=HTTPStatus.BAD_REQUEST)
    
    return ResponseHandler.handle_response(response, status_code=HTTPStatus.CREATED, message=HTTPStatus.CREATED.phrase)