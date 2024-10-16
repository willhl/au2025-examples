
from .DesignBehaviour import DesignBehaviourBase
from Client.OriginQueries import Query
from Client.OriginMutations import Mutate
from Utils import Utils

class SpaceOutletsBehaviour(DesignBehaviourBase):
    def __init__(self, graphqlClient):
        self.graphqlClient = graphqlClient
        self.subscription = None

    def GetSubscriptionQuery(self):
        return """
subscription SpaceUpdated {
  spaceUpdated {
    previousState {
      Number_of_Fused_Connection_Units_Non_Essential     
      Number_of_230V_Single_Sockets_Non_Essential
      Number_of_230V_Twin_Sockets_Non_Essential
      Number_of_Cleaners_Sockets_Non_Essential
    }
    updatedSpace {
      Id
      Number_of_Fused_Connection_Units_Non_Essential     
      Number_of_230V_Single_Sockets_Non_Essential
      Number_of_230V_Twin_Sockets_Non_Essential
      Number_of_Cleaners_Sockets_Non_Essential
    }
    event
  }
}
"""

    def CanRunBehaviour(self, eventResult):
        
        return True
    
    async def runForSocketTypeName(self, varName, socketType, eventResult):
        try:
          #numberOf230v_prv = eventResult["spaceUpdated"]["previousState"][varName]
          numberOf230v_new = eventResult["spaceUpdated"]["updatedSpace"][varName]
          spaceId = eventResult["spaceUpdated"]["updatedSpace"]["Id"]
            
          projectId = await Query.GetProjectIdForSpaceId(spaceId, self.graphqlClient)
          entityTypes = await Query.GetSocketTypesForProject(projectId, self.graphqlClient)

          # We're only going to create sockets if needed, not delete them
          if (True):#numberOf230v_prv != numberOf230v_new):
            typeId_230vsocket = Utils.getIdByName(entityTypes, socketType)          
            all30vSockets = await Query.GetSocketsInSpace(spaceId, typeId_230vsocket, self.graphqlClient)
            countOf230vSockets = len(all30vSockets)

            numberOf230v_needed = numberOf230v_new - countOf230vSockets
            
            if (numberOf230v_needed <= 0): return False

            print(f"Creating {numberOf230v_needed} of {socketType} with type Id {typeId_230vsocket} in space {spaceId}")

            # create an array of items to numberOf230v_needed
            for i in range(numberOf230v_needed):
              print(f"Creating {socketType} {i + 1} in space {spaceId}")
              mutResult = await Mutate.AddSocketToSpace(spaceId, typeId_230vsocket, f"Socket {countOf230vSockets + i + 1}", self.graphqlClient)

        except Exception as e:
          print(e)

        return True

    async def RunBehaviour(self, eventResult):        
        await self.runForSocketTypeName("Number_of_230V_Single_Sockets_Non_Essential", "230v Single Socket Non Essential", eventResult)
        await self.runForSocketTypeName("Number_of_230V_Twin_Sockets_Non_Essential", "230v Double Socket Non Essential", eventResult)
        await self.runForSocketTypeName("Number_of_Cleaners_Sockets_Non_Essential", "230v Cleaners Socket", eventResult)
        await self.runForSocketTypeName("Number_of_Fused_Connection_Units_Non_Essential", "230v Fused Connection Unit", eventResult)
        return True

    def GetSocketTypes(self):
  
        return ""