from json_api_serializer import json_api_documents

class JADataDocument(json_api_documents.JADocuments):
    def __init__(self):
        dataDocument = {"data": {}}
        super(JADataDocument, self).__init__(dataDocument)
    def createDataElement(self, idValue, dataType, attributes = {}, relationships = {}, links = {}, meta = {}):
        dataElement = {}
        if len(attributes) != 0:
        	dataElement['attributes'] = attributes
        if len(relationships) != 0:
        	dataElement['relationships'] = relationships
        if len(links) != 0:
        	dataElement['links'] = links
        if len(meta) != 0:
        	dataElement['meta'] = meta
        dataElement['id'] = idValue
        dataElement['type'] = dataType
        return dataElement
    def createMetaElement(self, idValue, metaAttributes = [], attributes = {}, relationships = {}, links = {}, meta = {}):
        metaElement = {}
        if len(metaAttributes) != 0:
        	for metaNode in metaAttributes:
        		metaElement[metaNode['attribute']] = metaNode['value']
        if len(attributes) != 0:
        	metaElement['attributes'] = attributes
        if len(relationships) != 0:
        	metaElement['relationships'] = relationships
        if len(links) != 0:
        	metaElement['links'] = links
        if len(meta) != 0:
        	metaElement['meta'] = meta
        return {idValue:metaElement}