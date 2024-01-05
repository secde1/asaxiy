from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

JWT_SECRET = "cairocoders$§%§$Ednalan"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000

pwd_contex = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/signin")
COOKIE_NAME = "Authorization"


def create_access_token(user):
    try:
        payload = {
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
            "active": user.is_active,
        }
        return jwt.encode(payload, key=JWT_SECRET, algorithm=ALGORITHM)
    except Exception as ex:
        print(str(ex))
        raise ex


# create verify Token
def verify_token(token):
    try:
        payload = jwt.decode(token, key=JWT_SECRET)
        return payload
    except Exception as ex:
        print(str(ex))
        return ex


# password hash
def get_password_hash(password):
    return pwd_contex.hash(password)


# password verify
def verify_password(plain_password, hashed_password):
    return pwd_contex.verify(plain_password, hashed_password)
