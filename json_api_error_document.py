from json_api_serializer import json_api_documents

class JAErrorDocument(json_api_documents.JADocuments):
    def __init__(self):
        errorDocument = {"errors":[]}
        super(JAErrorDocument, self).__init__(errorDocument)
    def createErrorElement(self, status, title, detail):
        errorElement = {}
        errorElement['status'] = status
        errorElement['title'] = title
        errorElement['detail'] = detail
        return errorElement