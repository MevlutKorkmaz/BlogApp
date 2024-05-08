from flask_restx import Resource, Namespace, fields
from Service.AuthService import *
from extensions import api

auth_ns = Namespace('auth', description='Authentication  operations')

user_registration_model = auth_ns.model('UserRegistration', {
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

user_login_model = auth_ns.model('UserLogin', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})
reset_password_model = auth_ns.model('UserResetPassword', {
    'email': fields.String(required=True, description='Email')
})
update_password_model = auth_ns.model('UserUpdatePassword', {
    'new_password': fields.String(required=True, description='New Password')
})


@api.errorhandler(UserAlreadyExistsException)
def handle_user_already_exists_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(InvalidPasswordException)
def handle_invalid_password_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(InvalidEmailException)
def handle_invalid_email_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(InvalidCredentialsException)
def handle_invalid_credentials_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(MailSendException)
def handle_mail_send_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(TokenExpiredException)
def handle_token_expired_exception(error):
    return {'message': error.message}, error.status_code


@api.errorhandler(TokenInvalidException)
def handle_token_invalid_exception(error):
    return {'message': error.message}, error.status_code


# auth specific operations
@auth_ns.route('/register')
class UserRegistration(Resource):
    # register a new user
    @auth_ns.expect(user_registration_model, validate=True)
    @auth_ns.marshal_with(user_registration_model)
    def post(self):
        data = auth_ns.payload
        return AuthService.register_user(username=data['username'], email=data['email'], password=data['password'])


@auth_ns.route('/login')
class UserLogin(Resource):
    @auth_ns.expect(user_login_model, validate=True)
    def post(self):
        data = auth_ns.payload
        token = AuthService.login_user(username=data['username'], password=data['password'])
        return {'token': token}, 200


@auth_ns.route('/change-password-request')
class ChangePasswordRequest(Resource):
    @auth_ns.expect(reset_password_model, validate=True)
    def post(self):
        data = auth_ns.payload
        email = data['email']
        response = AuthService.reset_password_request(email)
        return {'message': response}, 200


@auth_ns.route('/reset-password/<token>')
class ResetPassword(Resource):
    @auth_ns.expect(update_password_model, validate=True)
    def put(self, token):
        data = auth_ns.payload
        new_password = data['new_password']
        response = AuthService.change_password(token, new_password)
        return {'message': response}, 200
