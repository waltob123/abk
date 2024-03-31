from flask import Blueprint, render_template, request, redirect, url_for


test_blueprint = Blueprint('test', __name__)


@test_blueprint.route('/test', methods=['GET'], strict_slashes=True)
def test():
    return {'message': 'This is a test route.'}