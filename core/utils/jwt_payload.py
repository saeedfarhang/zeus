import jwt
from datetime import datetime
from graphql_jwt.settings import jwt_settings
    
def jwt_payload(user, context=None):
    jwt_datetime = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA
    jwt_expires = int(jwt_datetime.timestamp())
    payload = {}
    payload['username'] = str(user.email) # For library compatibility
    payload['sub'] = str(user.id)
    payload['role'] = user.role.role
    payload['sub_email'] = user.email
    payload['exp'] = jwt_expires
    return payload
