from google.auth.transport import requests
from google.oauth2 import id_token


class Google:
    """A Google class to fetch user infor and return it"""

    @staticmethod
    def validate(auth_token):
        """
        Validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try: 
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())
            if 'accounts.google.com' in idinfo['iss']: #to check if the issuer of the token is a google server
                return idinfo

        except:
            return "The token is either invalid or it has expired."
             