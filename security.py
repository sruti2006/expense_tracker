from passlib.context import CryptContext
from jose import jwt
SECRET_KEY="mysecurity"
ALGORITHM="HS256"
pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


def create_access_token(data:dict):
    return jwt.encode(
        data,SECRET_KEY,algorithm=ALGORITHM
    )

def verify_token(token):
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    user_id=payload.get("user_id")
    return user_id














#from jose import jwt
#from fastapi.security import OAuth2PasswordBearer
#SECRET_KEY="mysecretkey"
#ALGORITHM="HS256"
#oauth2_scheme=OAuth2PasswordBearer(tokenUrl="")