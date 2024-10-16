
class Utils:
    @staticmethod
    def getIdByName(entity_types, name):
        for entity in entity_types:
            if entity['Name'] == name:
                return entity['Id']
