import os
from google.cloud import dialogflow


def get_answer(google_cloud_project, chat_id, question, language='ru'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(google_cloud_project, chat_id)
    text_input = dialogflow.TextInput(text=question, language_code=language)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text
