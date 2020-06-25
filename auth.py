import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-l3k-hury.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Casting Agency'

'''
AuthError Exception
A standard way to communicate auth failure modes
'''

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

'''
Get Token Auth Header
    get heade from the request
        raise an AuthError if no header is present
    attempt to split bearer and the token
        raise an AuthError if the header is malformer
    return the token part of the header
'''

def get_token_auth_header():
    auth = request.header.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split(' ')
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

'''
Check permissions
@INPUTS
    permission: string permission (i.e. 'get:actor')
    payload: decode jwt payload
raise an AuthError if permissions are not included in the payload
raise an AuthError if the requested permission string is not in 
the payloads permissions array
return true otherwise
'''

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)
    
    return True

'''
Verify Decode JWT
@INPUTS
    token: a json web token (string)
Auth0 token with key id (kid)
verify the token using Auth) /.well-known/jwks.json
decode the payload from the token
validate the claims
return the decoded payload
'''

def verify_decode_jwt(token):
    jsonurl = urlopen('https://' + AUTH0_DOMAIN + '/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issue=('https://' + AUTH0_DOMAIN + '/')
            )

            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and the issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)

'''
Requires Auth
@INPUTS
    permissions: string permission (i.e. 'get:actors')
use get_token_auth_header method to get the token
use the verify_decode_jwt method to decode the jwt
use the check_permissions method validate claims and check
the requested permission
return the decorator which passes the decoded payload to 
the decorated method
'''

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt)
            except Exception:
                raise AuthError({
                    'code': 'invalid_token',
                    'description': 'Invalid token.'
                }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator