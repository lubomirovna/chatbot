from flask import Flask, jsonify, request
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from data_store import customizations, faqs


faq_docs = []
for faq in faqs:
    doc = Document(page_content=faq['question'], metadata={"question_id": faq["id"]})
    faq_docs.append(doc)
faiss_index = FAISS.from_documents(faq_docs, OpenAIEmbeddings())


app = Flask(__name__)


@app.route('/customizations', methods=['GET'])
def get_customizations():
    """
    Retrieves the customizations data.
    Returns:
        A tuple containing the customizations data as JSON and the HTTP status code.
    """
    return jsonify(customizations), 200


@app.route('/faqs', methods=['GET'])
def get_faqs():
    """
    Retrieves frequently asked questions.
    Returns:
        A tuple containing the answer as JSON and the HTTP status code.
    """

    query = request.args.get('question')
    if not query:
        return jsonify({"error": "Question parameter is required"}), 400

    docs = faiss_index.similarity_search(query, k=1)  

    if docs:
        relevant_faq = faqs[docs[0].metadata["question_id"] - 1]
    
    return jsonify({"question": relevant_faq["question"], "answer": relevant_faq["answer"]}), 200


if __name__ == '__main__':
    app.run(debug=True)
    