# Create a behaviour for the SpaceType class
from abc import ABC, abstractmethod

class DesignBehaviourBase(ABC):
    def __init__(self, graphqlClient):
        self.graphqlClient = graphqlClient
        self.subscription = None

    # When this changes
    @abstractmethod
    def GetSubscriptionQuery(self):
        """
        Abstract method to get subscription query.
        This method must be overridden by the subclass.
        """
        pass

    @abstractmethod
    def CanRunBehaviour(self):
        """
        Abstract method to execute a certain behavior.
        This method must be overridden by the subclass.
        """
        pass

    # Do this
    @abstractmethod
    async def RunBehaviour(self, eventResult):
        """
        Abstract method to execute a certain behavior.
        This method must be overridden by the subclass.
        """
        pass

    async def Start(self):
        """
        Concrete implementation of RunBehaviour.
        This is specific to space type behavior.
        """
        print("Running space type specific behaviour...")
        # Implement the behavior logic here
        subQuery = self.GetSubscriptionQuery()
        print(f"Executing subscription query: {subQuery}")

        self.subscription = self.graphqlClient.SubscribeAsync(subQuery)

        async for event in self.subscription:
            await self.RunBehaviour(event)
        
        return True
    
    async def Stop(self):
        self.subscription.close()
        