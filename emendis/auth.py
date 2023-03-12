from fastapi_auth_middleware import FastAPIUser
from jose import JWTError, jwt
from starlette.authentication import AuthenticationError


def verify_authorization_header(headers) -> tuple[list[str], FastAPIUser]:
    # TODO verify_token_or_abort(headers)

    user = FastAPIUser(first_name="Google", last_name="PubSub", user_id=1)
    scopes = []  # restrict access to specific scopes, not used here
    return scopes, user


def verify_token_or_abort(headers):
    # TODO: incomplete code from
    # https://cloud.google.com/python/docs/getting-started/authenticate-users

    if not (token := headers.get("X-Goog-IAP-JWT-Assertion")):
        raise AuthenticationError("No token found in the request")

    certs = ...  # TODO: get google certs and cache them
    try:
        info = jwt.decode(token, certs, algorithms=["ES256"])
    except JWTError:
        # TODO: log exception
        raise AuthenticationError("Invalid token")

    return info
