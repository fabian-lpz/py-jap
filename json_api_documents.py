class JADocuments(object):
    def __init__(self, document):
        self.document = document
    def appendObjectInDocument(self, objectToAppend, attribute):
        attr = self.document.get(attribute, {})
        if not attr:
            self.document[attribute] = objectToAppend
        else:
            if isinstance(self.document[attribute] ,list):
                self.document[attribute].append(objectToAppend)
            else:
                tempData = self.document[attribute]
                self.document[attribute] = []
                self.document[attribute].append(tempData)
                self.document[attribute].append(objectToAppend)
    def getJSONResponse(self):
        return self.document