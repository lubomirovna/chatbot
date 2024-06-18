import chainlit as cl
from literalai import LiteralClient
from langchain_openai import OpenAI
from langchain.chains import LLMChain, APIChain
from langchain.memory.buffer import ConversationBufferMemory
from prompts import api_response_prompt, api_url_prompt, assistant_prompt
from api_docs import tee_api_docs
from data_store import keywords

from dotenv import load_dotenv


load_dotenv()


client = LiteralClient()


@cl.on_chat_start
def setup_multiple_chains():
    llm = OpenAI(model='gpt-3.5-turbo-instruct', temperature=0)
    conversation_memory = ConversationBufferMemory(memory_key="chat_history", max_len=200, return_messages=True)
    
    # LLM Chain for general conversations
    llm_chain = LLMChain(llm=llm, prompt=assistant_prompt, memory=conversation_memory)
    cl.user_session.set("llm_chain", llm_chain)

    # API Chain for API interactions
    api_chain = APIChain.from_llm_and_api_docs(
        llm=llm,
        api_docs=tee_api_docs,
        api_url_prompt=api_url_prompt,
        api_response_prompt=api_response_prompt,
        verbose=True,
        limit_to_domains=None
    )
    cl.user_session.set("api_chain", api_chain)



@cl.on_message
async def handle_message(message: cl.Message):
    user_message = message.content.lower()
    llm_chain = cl.user_session.get("llm_chain")
    api_chain = cl.user_session.get("api_chain")

    cb = client.langchain_callback()
    
    if any(keyword in user_message for keyword in keywords):
        # If any of the keywords are in the user_message, use api_chain
        response = await api_chain.acall(user_message, callbacks=[cb])
    else:
        # Default to llm_chain for handling general queries 
        response = await llm_chain.acall(user_message, callbacks=[cb])

    
    response_key = "output" if "output" in response else "text"
    
    await cl.Message(response.get(response_key, "")).send()
