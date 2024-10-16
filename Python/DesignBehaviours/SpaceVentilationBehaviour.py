
from .DesignBehaviour import DesignBehaviourBase
from Client.OriginQueries import Query
from Client.OriginMutations import Mutate
from Utils import Utils

class SpaceVentilationBehaviour(DesignBehaviourBase):
    def __init__(self, graphqlClient):
        self.graphqlClient = graphqlClient
        self.subscription = None

    def GetSubscriptionQuery(self):
        return """
subscription SpaceUpdated {
  spaceUpdated {
    previousState {
      Space_Ventilation_Strategy
    }
    updatedSpace {
      Id
      Space_Ventilation_Strategy
    }
    event
  }
}
"""

    def CanRunBehaviour(self, eventResult):
        
        return True
    
    async def runForTypeName(self, varName, mvhrTypeName, eventResult):
        try:
          value_prv = eventResult["spaceUpdated"]["previousState"][varName]
          value_new = eventResult["spaceUpdated"]["updatedSpace"][varName]
          spaceId = eventResult["spaceUpdated"]["updatedSpace"]["Id"]
            
          projectId = await Query.GetProjectIdForSpaceId(spaceId, self.graphqlClient)
          entityTypes = await Query.GetMVHRTypesForProject(projectId, self.graphqlClient)

          # We're only going to create an mvhr if needed, not delete them
          if (value_prv != value_new):

            mvhrTypeId = Utils.getIdByName(entityTypes, mvhrTypeName)          
            allmvhrUnits = await Query.GetMVHRUnitsInSpace(spaceId, mvhrTypeId, self.graphqlClient)
            countmvhrUnits = len(allmvhrUnits)

            numberOfmvhrNeeded = 0
            if value_new == "MVHR" : numberOfmvhrNeeded = 1

            print(f"Count of MVHR units in space: {countmvhrUnits}")

            numberOfmvhrToCreate = numberOfmvhrNeeded - countmvhrUnits
            
            if (numberOfmvhrToCreate <= 0): return False

            print(f"Creating {numberOfmvhrToCreate} of {mvhrTypeName} with type Id {mvhrTypeId} in space {spaceId}")

            # create an array of items to numberOf230v_needed
            for i in range(numberOfmvhrToCreate):
              print(f"Creating {mvhrTypeName} {i + 1} in space {spaceId}")
              mutResult = await Mutate.AddMVHRToSpace(spaceId, mvhrTypeId, f"MVHR {countmvhrUnits + i + 1}", self.graphqlClient)
              
        except Exception as e:
          print(e)

        return True

    async def RunBehaviour(self, eventResult):        
        await self.runForTypeName("Space_Ventilation_Strategy", "MVHR Generic", eventResult)
        return True

    def GetSocketTypes(self):
  
        return ""