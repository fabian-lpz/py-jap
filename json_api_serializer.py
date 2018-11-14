from json_api_serializer import json_api_error_document, json_api_data_document
from collections import defaultdict
import json

__author__ = "Fabian Lopez Verdugo"
__version__ = "0.1"
__maintainer__ = "Fabian Lopez"
__email__ = "fabian.lopez@enova.mx"
__status__ = "Development"

class JASerializer():
    def __init__(self):
        print("__init__ JASerializer")
    def createDataDocument(self):
        self.document = json_api_data_document.JADataDocument()
    def createErrorDocument(self):
        self.document = json_api_error_document.JAErrorDocument()
    def serializeJAError(self, status, title, detail):
        """
        :param status: The HTTP status of the error.
        :param title: The HTTP title of the error.
        :param detail: A more descriptive detail descrition of the error.
        :returns: JSON API error document
        """
        self.createErrorDocument()
        errorElement = self.document.createErrorElement(status, title, detail)
        self.document.appendObjectInDocument(errorElement, "errors")
        return json.dumps(self.document.getJSONResponse(), default=str)

    def serializeJADataColumnSetID(self, dataType, data, attributes, idColumn = "id", relationships = [], links = {}, meta = {}):
        """
        :param dataType: The JSON API  attribute type of the data document.
        :param data: The data that will be parsed into JSON API document.
        :param attributes: An array of strings, that will be the attributes of the data that will be .
        :param idValue: A more descriptive detail descrition of the error.
        :returns: JSON API error document
        """
        self.createDataDocument()
        if isinstance(data ,list):
            for index in data:
                dataAttributes = self.getAttributesFromDataSet(index, attributes)
                idValue = self.getIdFromDataSet(index, idColumn)
                if len(relationships) != 0:
                    if isinstance(relationships ,dict):
                        relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(index, relationships)
                        if len(relationshipsIncludes) == 0:
                            return self.serializeJAError(400, "Bad Request", "La relación dada no cumple con las especificaciones de objeto de data")
                    else:
                        for rel in relationships:
                            relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(index, rel)
                            if len(relationshipsIncludes) == 0:
                                return self.serializeJAError(400, "Bad Request", "La relación dada no cumple con las especificaciones de objeto de data")
                else:
                    relationshipsIncludes = {"included":[],"relationship":[]}
                if len(meta) != 0:
                    if isinstance(meta ,dict):
                        metasIncludes = self.getMetaIncludesFromDataSet(index, meta)
                        if len(metasIncludes) == 0:
                            return self.serializeJAError(400, "Bad Request", "La metadata dada no cumple con las especificaciones de objeto de metadata")
                    else:
                        for rel in meta:
                            metasIncludes = self.getMetaIncludesFromDataSet(index, rel)
                            if len(metasIncludes) == 0:
                                return self.serializeJAError(400, "Bad Request", "La metadata dada no cumple con las especificaciones de objeto de metadata")
                else:
                    metasIncludes = {"included":[],"metas":[]}
                dataElement = self.document.createDataElement(idValue, dataType, dataAttributes, relationshipsIncludes["relationship"], links, metasIncludes["metas"])
                self.document.appendObjectInDocument(dataElement, "data")
                if len(metasIncludes["included"]) > 0:
                    self.document.appendObjectInDocument(metasIncludes["included"], "included")
                if len(relationshipsIncludes["included"]) > 0:
                    self.document.appendObjectInDocument(relationshipsIncludes["included"], "included")
        elif isinstance(data ,dict):
            dataAttributes = self.getAttributesFromDataSet(data, attributes)
            idValue = self.getIdFromDataSet(data, idColumn)
            if len(relationships) != 0:
                if isinstance(relationships ,dict):
                    relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(data, relationships)
                    if len(relationshipsIncludes) == 0:
                        return self.serializeJAError(400, "Bad Request", "La relación dada no cumple con las especificaciones de objeto de data")
                else:
                    for rel in relationships:
                        relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(data, rel)
                        if len(relationshipsIncludes) == 0:
                            return self.serializeJAError(400, "Bad Request", "La relación dada no cumple con las especificaciones de objeto de data")
            else:
                relationshipsIncludes = {"included":[],"relationship":[]}
            if len(meta) != 0:
                if isinstance(meta ,dict):
                    metasIncludes = self.getMetaIncludesFromDataSet(data, meta)
                    if len(metasIncludes) == 0:
                        return self.serializeJAError(400, "Bad Request", "La metadata dada no cumple con las especificaciones de objeto de metadata")
                else:
                    for rel in meta:
                        metasIncludes = self.getMetaIncludesFromDataSet(data, rel)
                        if len(metasIncludes) == 0:
                            return self.serializeJAError(400, "Bad Request", "La metadata dada no cumple con las especificaciones de objeto de metadata")
            else:
                metasIncludes = {"included":[],"metas":[]}
            dataElement = self.document.createDataElement(idValue, dataType, dataAttributes, relationshipsIncludes["relationship"], links, metasIncludes["metas"])
            self.document.appendObjectInDocument(dataElement, "data")
            if len(metasIncludes["included"]) > 0:
                self.document.appendObjectInDocument(metasIncludes["included"], "included")
            if len(relationshipsIncludes["included"]) > 0:
                self.document.appendObjectInDocument(relationshipsIncludes["included"], "included") 
        else:
            return self.serializeJAError(400, "Bad Request", "No se puede serializar la data ingresada porque no es un objeto dict o list.")
        return json.dumps(self.document.getJSONResponse(), default=str)

    def getAttributesFromDataSet(self, data, attributes):
        parsedAttributes = defaultdict(dict)
        for attr in attributes:
            if isinstance(attr ,dict):
                if "." in attr["column"]:
                    splitColumn = [x.strip() for x in attr["column"].split('.')]
                    loopData = data
                    cicleAttributes = {}
                    lastAttr = ""
                    for c in splitColumn:
                        cicleAttributes = loopData[c]
                        loopData = loopData[c]
                        lastAttr = c
                    if "group" in attr:
                        parsedAttributes[attr["group"]][attr["alias"]] = self.solveAttribute(cicleAttributes, attr.get('solved',{}))
                    else:
                        parsedAttributes[attr["alias"]] = self.solveAttribute(cicleAttributes, attr.get('solved',{}))

                else:
                    if attr["column"] in data:
                        if "group" in attr:
                            parsedAttributes[attr["group"]][attr["alias"]] = self.solveAttribute(data[attr["column"]], attr.get('solved',{}))
                        else:
                            parsedAttributes[attr["alias"]] = self.solveAttribute(data[attr["column"]], attr.get('solved',{}))
            elif "." in attr:
                splitColumn = [x.strip() for x in attr.split('.')]
                loopData = data
                cicleAttributes = {}
                lastAttr = ""
                for c in splitColumn:
                    cicleAttributes = loopData[c]
                    loopData = loopData[c]
                    lastAttr = c
                parsedAttributes[lastAttr] = cicleAttributes
            else:
                if attr in data:
                    parsedAttributes[attr] = data[attr]
        return parsedAttributes

    def solveAttribute(self, pivotArray, solvedArray):
        if len(solvedArray) == 0:
            return pivotArray
        else:
            for i, k in enumerate(pivotArray):
                if k not in solvedArray:
                    pivotArray[i] = solvedArray[int(k)]
        return pivotArray

    def getMetaAttributesFromDataSet(self, data, attributes):
        parsedAttributes = []
        for attr in attributes:
            if "." in attr:
                splitColumn = [x.strip() for x in attr.split('.')]
                loopData = data
                cicleAttributes = {}
                lastAttr = ""
                for c in splitColumn:
                    cicleAttributes = loopData[c]
                    loopData = loopData[c]
                    lastAttr = c
                parsedAttributes.append({"attribute":lastAttr,"value":cicleAttributes})
            else:
                if attr in data:
                    parsedAttributes.append({"attribute":attr,"value":data[attr]})
        return parsedAttributes

    def getIdFromDataSet(self, data, idColumn):
        if "." in idColumn:
            splitColumn = [x.strip() for x in idColumn.split('.')]
            loopData = data
            for c in splitColumn:
                parsedId = loopData[c]
                loopData = loopData[c]
        else:
            if idColumn in data:
                parsedId = data[idColumn]
            else:
                parsedId = 1
        return parsedId

    def getRelationshipsIncludesFromDataSet(self, data, relationships):
        includeElement = []
        relationshipElement = []
        if "." in relationships['column_relation']:
            splitColumn = [x.strip() for x in relationships['column_relation'].split('.')]
            for c in splitColumn:
                if c in json.dumps(data, default=str):
                    data = data[c]
            relationData = data
            for relda in relationData:
                relrel = {}
                idValue = self.getIdFromDataSet(relda, relationships['id'])
                dataAttributes = self.getAttributesFromDataSet(relda, relationships['attributes'])
                relationshipsRelationships = relationships.get('relationships', {})
                if len(relationshipsRelationships) != 0:
                    if isinstance(relationships['relationships'] ,dict):
                        relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(relda, relationships['relationships'])
                        if len(relationshipsIncludes) != 0:
                            relrel = relationshipsIncludes["relationship"]
                            for included in relationshipsIncludes["included"]:
                                includeElement = self.appendInclude(includeElement, included)
                        else:
                            relationshipsIncludes = {"included":[],"relationship":[]}
                    else:
                        for j in relationships['relationships']:
                            relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(relda, j)
                            if len(relationshipsIncludes) != 0:
                                if len(relrel) != 0:
                                    relrel.extend(relationshipsIncludes["relationship"])
                                else:
                                    relrel = relationshipsIncludes["relationship"]
                                for included in relationshipsIncludes["included"]:
                                    includeElement = self.appendInclude(includeElement, included)
                            else:
                                relationshipsIncludes = {"included":[],"relationship":[]}
                else:
                    relationshipsIncludes = {"included":[],"relationship":[]}
                relationshipElement = self.appendInclude(relationshipElement, self.document.createDataElement(idValue, relationships['type'],[],relrel))
                includeElement = self.appendInclude(includeElement, self.document.createDataElement(idValue, relationships['type'], dataAttributes))
        else:
            if(not self.validateRelationship(relationships)):
                return {}
            if relationships['column_relation'] in json.dumps(data, default=str):
                relationData = data[relationships['column_relation']]
                for relda in relationData:
                    relrel = {}
                    idValue = self.getIdFromDataSet(relda, relationships['id'])
                    dataAttributes = self.getAttributesFromDataSet(relda, relationships['attributes'])
                    relationshipsRelationships = relationships.get('relationships', {})
                    if len(relationshipsRelationships) != 0:
                        if isinstance(relationships['relationships'] ,dict):
                            relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(relda, relationships['relationships'])
                            if len(relationshipsIncludes) != 0:
                                relrel = relationshipsIncludes["relationship"]
                                for included in relationshipsIncludes["included"]:
                                    includeElement = self.appendInclude(includeElement, included)
                        else:
                            for j in relationships['relationships']:
                                relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(relda, j)
                                if len(relationshipsIncludes) != 0:
                                    if len(relrel) != 0:
                                        relrel.extend(relationshipsIncludes["relationship"])
                                    else:
                                        relrel = relationshipsIncludes["relationship"]
                                    for included in relationshipsIncludes["included"]:
                                        includeElement = self.appendInclude(includeElement, included)
                                else:
                                    relationshipsIncludes = {"included":[],"relationship":[]}
                    else:
                        relationshipsIncludes = {"included":[],"relationship":[]}
                    relationshipElement = self.appendInclude(relationshipElement, self.document.createDataElement(idValue, relationships['type'],[],relrel))
                    includeElement = self.appendInclude(includeElement, self.document.createDataElement(idValue, relationships['type'], dataAttributes))
        return {"included":includeElement,"relationship":relationshipElement}

    def getMetaIncludesFromDataSet(self, data, meta):
        includeElement = []
        metadataElement = {}
        if "." in meta['column_relation']:
            splitColumn = [x.strip() for x in meta['column_relation'].split('.')]
            for c in splitColumn:
                if c in json.dumps(data, default=str):
                    data = data[c]
            relationData = data
            for relda in relationData:
                # Metadata
                relrel = []
                idValue = self.getIdFromDataSet(relda, meta['id'])
                dataAttributes = self.getAttributesFromDataSet(relda, meta['attributes'])
                meta_attributes = meta.get('meta_attributes', [])
                metaDataAttributes = self.getMetaAttributesFromDataSet(relda, meta_attributes)
                metaRelationshipsRelationships = meta.get('meta_relationships', {})
                if len(metaRelationshipsRelationships) != 0:
                    if isinstance(meta['meta_relationships'] ,dict):
                        relationshipsIncludes = self.getMetaIncludesFromDataSet(relda, meta['meta_relationships'])
                        if len(relationshipsIncludes) != 0:
                            relrel = relationshipsIncludes["metas"]
                            for included in relationshipsIncludes["included"]:
                                includeElement = self.appendInclude(includeElement, included)
                        else:
                            relationshipsIncludes = {"included":[],"metas":[]}
                    else:
                        for j in meta['meta_relationships']:
                            relationshipsIncludes = self.getMetaIncludesFromDataSet(relda, j)
                            if len(relationshipsIncludes) != 0:
                                if len(relrel) != 0:
                                    relrel.extend(relationshipsIncludes["metas"])
                                else:
                                    relrel = relationshipsIncludes["metas"]
                                for included in relationshipsIncludes["included"]:
                                    includeElement = self.appendInclude(includeElement, included)
                            else:
                                relationshipsIncludes = {"included":[],"metas":[]}
                else:
                        relationshipsIncludes = {"included":[],"metas":[]}
                metadataElement = self.insertObjectInDictAsAttributes(self.document.createMetaElement(idValue, metaDataAttributes,[],relrel), metadataElement)
                # Relationships
                relationshipsRelationships = meta.get('relationships', {})
                relrel = []
                relation = {}
                relType = ""
                if len(relationshipsRelationships) != 0:
                    if isinstance(meta['relationships'] ,dict):
                        relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(relda, meta['relationships'])
                        relType = j['type']
                        if len(relationshipsIncludes) != 0:
                            relrel = relationshipsIncludes["relationship"]
                            for included in relationshipsIncludes["included"]:
                                includeElement = self.appendInclude(includeElement, included)
                    else:
                        for j in meta['relationships']:
                            relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(relda, j)
                            relType = j['type']
                            if len(relationshipsIncludes) != 0:
                                if len(relrel) != 0:
                                    relrel.extend(relationshipsIncludes["relationship"])
                                else:
                                    relrel = relationshipsIncludes["relationship"]
                                for included in relationshipsIncludes["included"]:
                                    includeElement = self.appendInclude(includeElement, included)
                            else:
                                relationshipsIncludes = {"included":[],"relationship":[]}
                    relation = self.createRelationShipElement(relrel,relType)
                else:
                    relationshipsIncludes = {"included":[],"relationship":[]}
                includeElement = self.appendInclude(includeElement, self.document.createDataElement(idValue, meta['type'], dataAttributes,relation))
        else:
            if(not self.validateRelationship(meta)):
                return {}
            if meta['column_relation'] in json.dumps(data, default=str):
                relationData = data[meta['column_relation']]
                for relda in relationData:
                    # Metadata
                    relrel = []
                    idValue = self.getIdFromDataSet(relda, meta['id'])
                    dataAttributes = self.getAttributesFromDataSet(relda, meta['attributes'])
                    meta_attributes = meta.get('meta_attributes', [])
                    metaDataAttributes = self.getMetaAttributesFromDataSet(relda, meta_attributes)
                    metaRelationshipsRelationships = meta.get('meta_relationships', {})
                    if len(metaRelationshipsRelationships) != 0:
                        if isinstance(meta['meta_relationships'] ,dict):
                            relationshipsIncludes = self.getMetaIncludesFromDataSet(relda, meta['meta_relationships'])
                            if len(relationshipsIncludes) != 0:
                                relrel = relationshipsIncludes["metas"]
                                for included in relationshipsIncludes["included"]:
                                    includeElement = self.appendInclude(includeElement, included)
                        else:
                            for j in meta['meta_relationships']:
                                relationshipsIncludes = self.getMetaIncludesFromDataSet(relda, j)
                                if len(relationshipsIncludes) != 0:
                                    if len(relrel) != 0:
                                        relrel.extend(relationshipsIncludes["metas"])
                                    else:
                                        relrel = relationshipsIncludes["metas"]
                                    for included in relationshipsIncludes["included"]:
                                        includeElement = self.appendInclude(includeElement, included)
                                else:
                                    relationshipsIncludes = {"included":[],"metas":[]}
                    else:
                        relationshipsIncludes = {"included":[],"metas":[]}
                    metadataElement = self.insertObjectInDictAsAttributes(self.document.createMetaElement(idValue, metaDataAttributes,[],relrel), metadataElement)
                    # Relatonships
                    relationshipsRelationships = meta.get('relationships', {})
                    relrel = []
                    relation = {}
                    if len(relationshipsRelationships) != 0:
                        relType = "";
                        if isinstance(meta['relationships'] ,dict):
                            relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(relda, meta['relationships'])
                            relType = meta['relationships']['type']
                            if len(relationshipsIncludes) != 0:
                                relrel = relationshipsIncludes["relationship"]
                                for included in relationshipsIncludes["included"]:
                                    includeElement = self.appendInclude(includeElement, included)
                        else:
                            for j in meta['relationships']:
                                relationshipsIncludes = self.getRelationshipsIncludesFromDataSet(relda, j)
                                relType = j['type']
                                if len(relationshipsIncludes) != 0:
                                    if len(relrel) != 0:
                                        relrel.extend(relationshipsIncludes["relationship"])
                                    else:
                                        relrel = relationshipsIncludes["relationship"]
                                    for included in relationshipsIncludes["included"]:
                                        includeElement = self.appendInclude(includeElement, included)
                                else:
                                    relationshipsIncludes = {"included":[],"relationship":[]}
                        relation = self.createRelationShipElement(relrel,relType)
                    else:
                        relationshipsIncludes = {"included":[],"relationship":[]}
                    includeElement = self.appendInclude(includeElement, self.document.createDataElement(idValue, meta['type'], dataAttributes,relation))
        return {"included":includeElement,"metas":metadataElement}

    def validateRelationship(self, relationship):
        if 'column_relation' not in json.dumps(relationship, default=str):
            return False
        if 'id' not in json.dumps(relationship, default=str):
            return False
        if 'type' not in json.dumps(relationship, default=str):
            return False
        if 'attributes' not in json.dumps(relationship, default=str):
            return False
        if 'relationships' in json.dumps(relationship, default=str):
            if isinstance(relationship['relationships'] ,dict):
                self.validateRelationship(relationship['relationships']) 
            else:
                for rela in relationship:
                    self.validateRelationship(rela) 
        return True

    def appendInclude(self, includeArray, itemToInclude):
        for item in includeArray:
            if item['id'] == itemToInclude['id'] and item['type'] == itemToInclude['type']:
                if len(item.keys()) != len(itemToInclude.keys()):
                    item.update(itemToInclude)
                return includeArray
        includeArray.append(itemToInclude)
        return includeArray

    def insertObjectInDictAsAttributes(self, objectToInsert, dictionary):
        for key in objectToInsert.keys():
            dictionary[key] = objectToInsert[key]
        return dictionary

    def createRelationShipElement(self, relation, relationType):
        if(relationType[-1:]!='s'):
            relationType = relationType + "s"
        relationship = {relationType:{"data":relation}}
        return relationship