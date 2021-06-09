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
    print(response)
    return response.query_result

response = detect_intent_from_text("Hey", 12314)
print(response.fulfillment_text)
print(f"Intent : {response.intent.display_name}")