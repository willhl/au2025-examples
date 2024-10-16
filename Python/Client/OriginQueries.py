
class Query:
    @staticmethod
    async def GetProjectIdForSpaceId(spaceId, client):

        query = """
query GetProjectForSpace ( $spaceID: ID!){
    projects(
        where: {
            Models_SOME: {
                Spaces_SOME: { Id: $spaceID }
            }
        }
    ) {
        Id
    }
}
        """  
        variables = { "spaceID": spaceId }
        result = await client.QueryAsync(query, variables)
        id = result["projects"][0]["Id"]
        return id
    
    @staticmethod
    async def GetSocketTypesForProject(projectId, client):
        query = """
query GetSocketTypes ($projectID: ID!) {
  projects(where: { Id: $projectID }) {
    EntityTypes(where: { typename_IN: [ElectricalOutletType] }) {
      Name
      Id
    }
  }
}
"""
        variables = { "projectID": projectId }
        result = await client.QueryAsync(query, variables)
        types = result["projects"][0]["EntityTypes"]
        return types
    
    @staticmethod
    async def GetMVHRTypesForProject(projectId, client):
        query = """
query GetMVHRTypes ($projectID: ID!) {
  projects(where: { Id: $projectID }) {
    EntityTypes(where: { typename_IN: [MVHRUnitType] }) {
      Name
      Id
    }
  }
}
"""
        variables = { "projectID": projectId }
        result = await client.QueryAsync(query, variables)
        types = result["projects"][0]["EntityTypes"]
        return types

    async def GetCountEquipmentTypesInSpace(spaceId, typeID, client):

        query = """
query GetEquipmentInSpace ($spaceId: ID!, $typeId: ID!) {
  spaces(where: { Id: $spaceId }) {
    AllEquipmentAggregate(
      where: { Id: $typeId }
    ) {
      count
    }
  }
}
        """  
        variables = { "spaceId": spaceId, "typeId": typeID }
        result = await client.QueryAsync(query, variables)
        id = result["spaces"][0]["AllEquipmentAggregate"]["count"]
        return id

    async def GetSocketsInSpace(spaceId, socketTypeId, client):
        query = """
query GetSocketsInSpace ($spaceId: ID!, $typeId: ID! ) {
  spaces(where: { Id: $spaceId }) {
    ElectricalOutlets(
      where: {
        ElectricalSocket: {
          EntityType: { Id: $typeId }
        }
      }
    ) {
      ... on ElectricalSocket {
        Id
        Name
      }
    }
  }
}
"""
        variables = { "spaceId": spaceId, "typeId": socketTypeId }
        result = await client.QueryAsync(query, variables)
        sockets = result["spaces"][0]["ElectricalOutlets"]
        return sockets
    

    async def GetMVHRUnitsInSpace(spaceId, typeId, client):
        query = """
query GetMVHRsInSpace ($spaceId: ID!, $typeId: ID! ) {
  spaces(where: { Id: $spaceId }) {
    MechanicalEquipment(
      where: {
        MVHRUnit: {
          EntityType: { Id: $typeId }
        }
      }
    ) {
      ... on MVHRUnit {
        Id
        Name
      }
    }
  }
}
"""
        variables = { "spaceId": spaceId, "typeId": typeId }
        result = await client.QueryAsync(query, variables)
        sockets = result["spaces"][0]["MechanicalEquipment"]
        return sockets