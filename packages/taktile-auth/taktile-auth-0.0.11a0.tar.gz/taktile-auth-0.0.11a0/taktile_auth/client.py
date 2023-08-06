import json
import typing as t

import jwt
import requests
from jwt.algorithms import RSAAlgorithm
from pydantic import ValidationError

from taktile_auth.exceptions import InvalidAuthException
from taktile_auth.schemas.session import SessionState
from taktile_auth.schemas.token import TaktileIdToken
from taktile_auth.settings import settings

ALGORITHM = "RS256"


class AuthClient:
    def __init__(
        self,
        *,
        url: str,
        key: t.Optional[str] = None,
    ) -> None:
        self.public_key_url = f"{url}/.well-known/jwks.json"
        self.access_token_url = f"{url}/api/v1/login/access-token"
        self.public_key = self.get_public_key(key=key)

    def get_public_key(
        self,
        *,
        key: t.Optional[str] = None,
        kid: str = "taktile-service",
    ) -> t.Any:
        jwk = (
            json.loads(key)
            if key
            else requests.get(self.public_key_url).json()
        )
        for k in jwk["keys"]:
            if k["kid"] == kid:
                return RSAAlgorithm.from_jwk(k)  # type: ignore
        raise InvalidAuthException("invalid-public-key")

    def decode_id_token(
        self,
        *,
        token: t.Optional[str] = None,
    ) -> TaktileIdToken:
        if not token:
            raise InvalidAuthException("no-auth-provided")
        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=[ALGORITHM],
                audience=settings.ENV,
            )
            return TaktileIdToken(**payload)
        except jwt.ExpiredSignatureError as exc:
            raise InvalidAuthException("signature-expired") from exc
        except (jwt.PyJWTError, ValidationError) as exc:
            raise InvalidAuthException("could-not-validate") from exc

    def get_access(
        self,
        *,
        session_state: SessionState,
    ) -> t.Tuple[TaktileIdToken, SessionState]:
        if not session_state.api_key and not session_state.jwt:
            raise InvalidAuthException("no-auth-proved")
        if not session_state.jwt:
            res = requests.post(
                self.access_token_url,
                headers=session_state.to_auth_headers(),
            )
            res.raise_for_status()
            session_state.jwt = res.json()["id_token"]
        return (
            self.decode_id_token(token=session_state.jwt),
            session_state,
        )
