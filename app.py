import os
import chainlit as cl
from chainlit.playground.config import add_llm_provider
from chainlit.playground.providers.langchain import LangchainGenericProvider
from langchain_huggingface.llms import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# Zet de model ID en API token
model_id = "openai-community/gpt2-medium"
api_token = os.environ.get('HUGGINGFACEHUB_API_TOKEN')

# Print de API-token voor testdoeleinden
if api_token:
    print(f"HuggingFace API Token: {api_token}")
else:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in the environment variables.")

# Configureer het model met de bijgewerkte klasse
conv_model = HuggingFaceEndpoint(
    huggingfacehub_api_token=api_token,
    repo_id=model_id,
    max_new_tokens=150  # Voeg de parameter hier expliciet toe
)

# Voeg de LLM provider toe
add_llm_provider(
    LangchainGenericProvider(
        # Zorg ervoor dat de id van de provider overeenkomt met de _llm_type
        id=conv_model._llm_type,
        # De naam is niet belangrijk. Het wordt weergegeven in de UI.
        name="HuggingFaceEndpoint",
        # Dit moet altijd een Langchain LLM-instantie zijn (correct geconfigureerd)
        llm=conv_model,
        # Als de LLM werkt met berichten, stel dit dan in op True
        is_chat=False
    )
)

template = """My name is {query} and I am"""

@cl.on_chat_start
def on_chat_start():
    prompt = PromptTemplate(template=template, input_variables=['query'])
    conv_chain = LLMChain(llm=conv_model, prompt=prompt, verbose=True)
    cl.user_session.set("llm_chain", conv_chain)

@cl.on_message
async def handle_message(message: str):
    llm_chain = cl.user_session.get("llm_chain")

    # Assuming 'message' is already the correct text to be processed
    # If 'message' is a Message object, we need to extract the text or content from it
    if isinstance(message, cl.message.Message):
        message_text = message.content  # Adjust this according to the actual structure of your Message class
    else:
        message_text = message  # It's already a string

    res = await llm_chain.acall(message_text, callbacks=[cl.AsyncLangchainCallbackHandler()])

    # Prepare the response text
    response_text = res.get("text", "Error processing your request")
    await cl.Message(content=response_text).send()
