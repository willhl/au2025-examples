from msal import ConfidentialClientApplication 
from .Authenticator import AuthenticatorBase

class MsalClientAuthenticator(AuthenticatorBase):
    def __init__(self, client_id, tenant_id, secret, scopes):
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.scopes = scopes
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.clientapp = ConfidentialClientApplication(self.client_id, authority=self.authority, client_credential=secret)

    def acquire_token(self):
        # Attempt to acquire token silently from cached accounts
        token = self.clientapp.acquire_token_for_client(scopes=self.scopes)
        return token

    def GetAuthtoken(self):
        result = self.acquire_token()
        if 'access_token' in result:
            return result['access_token']
        else:
            raise Exception(f"Failed to acquire token: {result.get('error')}, {result.get('error_description')}")



