from workflow.state import llmState,product_structural
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import requests
import os
load_dotenv(override=True)

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def comapany_detail(state:llmState):
    question=state['question']  
    prompt = f""" your name is Sara 
    You are sale analyst working in the company name Highlet

    #intial_conversation :
    welcome then and greet them for contact us


    # Company details 
    company_name : highlet
    company_location : America
    company_number:0987654321
    comapny_email : contact@highlet.com

    # answer the user question
    answer specific to the user question
    {question}
    """
    results=model.invoke(prompt).content
    state['answer']=results

    return {"answer":state['answer']}


def product_node(state:llmState):
    question=state['question']
    prompt= f"find the product name in singular from the user question: {question}"
    llm=model.with_structured_output(product_structural)
    result = llm.invoke(prompt)
    state['product'] = result.product
    product=state['product']
    response = requests.get(f"{os.getenv('HOST')}/api/products/?search={product}")
    if response.status_code == 200:
        products = response.json()
        return {"product":products}
    else:
        return {"error":"Error fetching products"}


def product_answer_node(state:llmState):
    products=state['product']
    prompt=f""" given the product list : {products}
    answer the user question : {state['question']}

    # provide a concise answer based on the product list with price and availability
    """
    answer=model.invoke(prompt).content
    state['answer']=answer

    return {"answer":state['answer']}
