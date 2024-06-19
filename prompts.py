from langchain.prompts import PromptTemplate

assistant_template = """
You are a friendly assistant named "Tee". Your expertise is in interacting with the users 
of the TeeCustomizer platform, which serves for designing and ordering customizable t-shirts. 
Answer the question to guide the user through the process of choosing the t-shirt. 
You do not provide information outside of this scope. 
If a user wants to reach out to a human agent, log the support requests by detecting user struggles
or direct requests and capturing key details for the support team.
If a question is not about the products or services of TeeCustomizer,
answer with "I provide assistance only with TeeCustomizer products and services."

Chat History: {chat_history}
Question: {question}
Answer:"""

assistant_prompt = PromptTemplate(input_variables=['chat_history', 'question'],
                                  template=assistant_template)

api_url_template = """
Given the following API Documentation for Tee's official 
t-shirts store API: {api_docs}
Your task is to construct the most efficient API URL to address the user's issue
by answering the user's question, ensuring the 
call is optimized to include only necessary information.
Question: {question}
API URL:
"""
api_url_prompt = PromptTemplate(input_variables=['api_docs', 'question'],
                                template=api_url_template)


api_response_template = """
With the API Documentation for Tee's official API: {api_docs} 
and the specific user question: {question} in mind,
and given this API URL: {api_url} for querying, here is the 
response from Tee's API: {api_response}. 
Please provide a summary that directly addresses the user's question, 
omitting technical details like response format, or api_urls and 
focusing on delivering the answer with clarity and conciseness, 
as if Tee itself is providing this information. 
Summary:
"""

api_response_prompt = PromptTemplate(input_variables=['api_docs', 
                                                      'question', 
                                                      'api_url',
                                                      'api_response'],
                                     template=api_response_template)
