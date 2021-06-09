import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "whatsappbot-kfpj-ac8fd20ea504.json"


import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "whatsappbot-kfpj"

def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)

    result = ""

    if response.query_result.parameters.fields:
        option = response.query_result.parameters.fields
        all = str(option).split(":")
        getVals = list([val for val in all[len(all)-1] if val.isalnum()]) 
        result = "".join(getVals) 
        print(result)

    return response.query_result, result

def fetch_reply(query, session_id):
    response , option = detect_intent_from_text(query, session_id)
    return response.fulfillment_text, option