from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")


def passwd_hash(password: str):
    return pwd_context.hash(password)

def passwd_verify(plain_passwd, hashed_passwd ):
    return pwd_context.verify(plain_passwd,hashed_passwd)
