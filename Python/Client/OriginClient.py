from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport

class OriginClient:
    def __init__(self, endpoint, ws_endpoint, authenticator):
        self.transport = AIOHTTPTransport(url=endpoint)
        self.wstransport = WebsocketsTransport(url=ws_endpoint)
        self.authenticator = authenticator

    def GetClient(self):
        token = self.authenticator.GetAuthtoken()
        tclient = Client(transport=self.transport, fetch_schema_from_transport=False)
        tclient.transport.headers = {
              "Authorization": "Bearer " + token
        }
        return tclient
    
    def GetWSClient(self):
        token = self.authenticator.GetAuthtoken()
        tclient = Client(transport=self.wstransport, fetch_schema_from_transport=False)
        tclient.transport.headers = {
              "Authorization": "Bearer " + token
        }
        return tclient
    
    async def Close(self):
        await self.wstransport.close()

    def QueryAsync(self, query, variables=None):
        gqlQuery = gql(query)
        oclient = self.GetClient()
        return oclient.execute_async(gqlQuery, variable_values=variables)
    
    def MutateAsync(self, query, variables=None):
        gqlQuery = gql(query)
        oclient = self.GetClient()
        return oclient.execute_async(gqlQuery, variable_values=variables)
    

    async def SubscribeAsync(self, query):
        token = self.authenticator.GetAuthtoken()
        wsclient = self.GetWSClient()
        wsclient.transport.headers = {
              "Authorization": "Bearer " + token
        }
        gqlQuery = gql(query)
        async for result in wsclient.subscribe_async(gqlQuery):
            yield result