import urllib
from urllib.request import Request
from urllib.error import HTTPError

import json
import logging

from IAMPASS.config import IAMPASS_SERVER
from IAMPASS.session import Session
from IAMPASS.hmac import make_authentication_headers
from IAMPASS.authentication_method import AuthenticationMethod

logger = logging.getLogger("IAMPASS")


class AuthenticationAPI:
    """
        Wrapper class for the IAMPASS REST API.

        Attributes:
            application_id (str): The application id of the IAMPASS application.
            application_secret (str): The application secret of the IAMPASS application.
    """

    def __init__(self, application_id: str, application_secret: str):
        """
            The constructor for IAMPASS class.

            Parameters:
                application_id (str): The application id of the IAMPASS application.
                application_secret (str): The application secret of the IAMPASS application.
        """

        self.application_id = application_id
        self.application_secret = application_secret

    def authenticate_user(self, user_id, authentication_methods=None, duration_seconds=None):
        """
            Authenticates a user.

            Calls the IAMPASS service to authenticate a user.

            Parameters:
            user_id (str): The id of the user to authenticate. This is the value used when adding the user.
            authentication_methods (AuthenticationMethod[]):    The authentication methods to use. If this value is None
                                                                IAMPASS will choose the authentication methods.
            duration_seconds:                                   The maximum length the session is valid. The default
                                                                value is 3600 seconds.

            Returns:
            Session: The session information or None if the request fails.

            """

        if user_id is None:
            logger.debug("user_id is None.")
            raise ValueError("user_id cannot be None")

        encoded_user_id = urllib.parse.quote_plus(user_id)

        param_values = []
        # If we have authentication methods, check they are valid and build the query string.
        if authentication_methods is not None and len(authentication_methods) > 0:
            if not all(type(n) is AuthenticationMethod for n in authentication_methods):
                logger.debug("authentication_methods contains invalid values {}".format(authentication_methods))
                raise TypeError("authentication_methods must be an array of AuthenticationMethod or None.")

            methods = "methods=" + ",".join(method.name for method in authentication_methods)
            param_values.append("methods=" + ",".join(method.name for method in authentication_methods))

        if duration_seconds is not None:
            if not isinstance(duration_seconds, int):
                logger.debug("duration_seconds must be an integer {}".format(authentication_methods))
                raise TypeError("duration_seconds must be an integer or None.")

            param_values.append("duration_seconds=" + str(duration_seconds))

        param_string = ""
        if param_values:
            param_string = "?" + "&".join(p for p in param_values)

        url = "{}/authentication/authenticate_user/{}/{}{}".format(
            IAMPASS_SERVER, self.application_id, encoded_user_id, param_string)

        headers = make_authentication_headers(client_id=self.application_id,
                                              client_shared_secret=self.application_secret,
                                              request_uri=url)
        headers["Content-Type"] = "application/json"

        data = json.dumps({}).encode('UTF-8')

        req = urllib.request.Request(url, headers=headers, data=data)

        try:
            auth_response = urllib.request.urlopen(req)
            if 200 <= auth_response.code < 300:
                d = auth_response.read()
                response_data = json.loads(d)
                return Session.from_authentication_response(response_data)
        except HTTPError as ex:
            logger.warn("authenticate_user failed {}".format(ex))
            return None

        return None
