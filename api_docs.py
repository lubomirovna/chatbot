import json

tee_api_docs = {
    "base_url": "https://patient-river-7277.ploomberapp.io/",
    "endpoints": {
        "/customizations": {
            "method": "GET",
            "description": "Retrieve available t-shirts customizations.",
            "parameters": None,
            "response": {
                "description": "A JSON object listing available \
                                customizations like size and color \
                                options.",
                "content_type": "application/json"
            }
        },
        "/faqs": {
            "method": "GET",
            "description": "Retrieve a list of questions relevant to the user's query.",
            "parameters": {
                "name": "question",
                "description": "A string containing user question for answer retrieval.",
                "content_type": "string"
            },
            "response": {
                "description": "A JSON array of FAQ objects, each containing a question and its corresponding answer.",
                "content_type": "application/json"
            }
        },
    }
}

# Convert the dictionary to a JSON string
tee_api_docs = json.dumps(tee_api_docs, indent=2)