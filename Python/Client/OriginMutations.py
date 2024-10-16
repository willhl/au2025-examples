
class Mutate:
    @staticmethod
    async def AddSocketToSpace(spaceId, socketTypeId, name, client):
        mutation = """
mutation UpdateSpaces ($spaceId: ID!, $typeId: ID!, $name: String ) {
  updateSpaces(
    where: { Id: $spaceId }
    update: {
      ElectricalOutlets: {
        ElectricalSocket: [
          {
            create: [
              {
                node: {
                  EquipmentType: {
                    connect: {
                      where: {
                        node: { Id: $typeId }
                      }
                    }
                  }
                  Name: $name
                }
              }
            ]
          }
        ]
      }
    }
  ) {
    info {
      nodesCreated
      relationshipsCreated
    }
  }
}
"""
        variables = { "spaceId": spaceId, "typeId": socketTypeId, "name": name }
        result = await client.MutateAsync(mutation, variables)
        types = result["updateSpaces"]["info"]
        return types


    @staticmethod
    async def AddMVHRToSpace(spaceId, mvhrTypeId, name, client):
        mutation = """
mutation UpdateSpaces ($spaceId: ID!, $typeId: ID!, $name: String ) {
  updateSpaces(
    where: { Id: $spaceId }
    update: {
      MechanicalEquipment: {
        MVHRUnit: [
          {
            create: [
              {
                node: {
                  EquipmentType: {
                    connect: {
                      where: {
                        node: { Id: $typeId }
                      }
                    }
                  }
                  Name: $name
                }
              }
            ]
          }
        ]
      }
    }
  ) {
    info {
      nodesCreated
      relationshipsCreated
    }
  }
}
"""
        variables = { "spaceId": spaceId, "typeId": mvhrTypeId, "name": name }
        result = await client.MutateAsync(mutation, variables)
        types = result["updateSpaces"]["info"]
        return types