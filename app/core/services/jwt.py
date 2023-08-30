import time
from datetime import datetime
from app.core.errors.exceptions import InvalidTokenException
from app.core.settings.config import Settings
from pydantic import ValidationError

import jwt


settings = Settings()

JWT_ALGORITHM = settings.JWT_ALGORITHM
SECRET_KEY = settings.SECRET_KEY


def get_id_from_token(token: str) -> int:
    try:
        decoded_payload = jwt.decode(token, str(SECRET_KEY), algorithms=[JWT_ALGORITHM])
        if decoded_payload["exp"] <= datetime.now().timestamp():
            raise InvalidTokenException(detail="token has expired.")
        return decoded_payload["id"]
    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except KeyError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error
    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
