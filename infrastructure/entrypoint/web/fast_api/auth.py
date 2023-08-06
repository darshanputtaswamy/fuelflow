import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta, timezone
import time
class AuthHandler():
    security = HTTPBearer()
    secret = 'SECRET'

    def encode_token(self, payload):
        return jwt.encode({
            'payload':payload,
            'exp':datetime.now(tz=timezone.utc) + timedelta(seconds=60*60*8),
            'iat':datetime.now(tz=timezone.utc)
            },
            self.secret,
            algorithm='HS256'
        )
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)