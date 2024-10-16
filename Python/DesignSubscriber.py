import graphql
import gql

class DesignSubscriber:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def subscribe(self, design_behaviour):
        query = design_behaviour.GetSubscriptionQuery()


        self.graphql_client.subscribe(query, self.handle_update)

    def handle_update(self, update):
        self.design_behaviour.process_update(update)

# Example usage
# design_behaviour = DesignBehaviour()
# graphql_client = GraphQLClient(endpoint="your_graphql_endpoint")
# subscriber = DesignSubscriber(design_behaviour, graphql_client)
# subscriber.subscribe()