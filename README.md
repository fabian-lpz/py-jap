# Pyjap
This repository contains a JSON API serialize to parse custom objects into custom JSON API document.

### Example of the custom object to be parsed into JSON API document:
```javascript
data = [
    {
        "object_id":"firstobject"
        "first_attr": "1"
        "second_attr": "2"
	// "object_type":"object1"
    },
    {
        "object_id":"secondobject"
        "first_attr": "3"
        "second_attr": "4"
	// "object_type":"object1"
    }
]
```

### Python Function
```python
from pyjap import json_api_serializer
serializer = json_api_serializer.JASerializer()

parsedData = serializer.serializeJADataColumnSetID("object1", data, [{"column":"first_attr", "alias":"first"},{"column":"second_attr", "alias":"second"}], "object_id")
```

### Example of the custom JSON API document that was parsed:
```javascript
parsedData = {
    "data": [
        {
	    "id":"firstobject",
	    "type":"object1",
	    "attributes": {
		"first_attr":"1",
		"second_attr":"2"
	    }
	},
        {
	    "id":"firstobject",
	    "type":"object1",
	    "attributes": {
		"first_attr":"1",
		"second_attr":"2"
	    }
	}
    ]
} 
```
