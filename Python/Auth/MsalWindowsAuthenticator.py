from msal import PublicClientApplication
from .Authenticator import AuthenticatorBase

class MsalWindowsAuthenticator(AuthenticatorBase):
    def __init__(self, client_id, tenant_id, scopes):
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.scopes = scopes
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.app = PublicClientApplication(self.client_id, authority=self.authority, enable_broker_on_windows=True)
        #self.app = PublicClientApplication(self.client_id, authority=self.authority)

    def acquire_token(self):
        # Attempt to acquire token silently from cached accounts
        accounts = self.app.get_accounts()
        if accounts:
            result = self.app.acquire_token_silent(self.scopes, account=accounts[0])
            if result:
                return result

        # Attempt Integrated Windows Authentication
        result = self.app.acquire_token_interactive(self.scopes, port=3001, parent_window_handle=self.app.CONSOLE_WINDOW_HANDLE)
        return result

    def GetAuthtoken(self):
        result = self.acquire_token()
        if 'access_token' in result:
            return result['access_token']
        else:
            raise Exception(f"Failed to acquire token: {result.get('error')}, {result.get('error_description')}")

# Usage
if __name__ == "__main__":
    CLIENT_ID = 'your-client-id'
    TENANT_ID = 'your-tenant-id'
    SCOPES = ["User.Read"]  # Define the required scopes

    authenticator = MsalWindowsAuthenticator(CLIENT_ID, TENANT_ID, SCOPES)
    try:
        token = authenticator.GetAuthtoken()
        print("Token acquired:", token)
    except Exception as e:
        print(str(e))
