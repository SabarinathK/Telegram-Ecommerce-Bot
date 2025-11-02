from typing import Literal
from workflow.state import llmState,question_conditional
from langchain_google_genai import ChatGoogleGenerativeAI 

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def question_conditional_edge(state:llmState) -> Literal["product_node", "company_detail"]:
    question=state['question']
    prompt= f"""classify the user question is about product or about general , it about your or company detail:

    # if the question is about product then respond with product
    # if the question is about company or your detail then respond with company

    example :
    question : what is the price of iphone 14 pro max
    answer : product
    question : where is your company located
    answer : company
    question : what is your name
    answer : company
    question : {question}
    
    """
    llm=model.with_structured_output(question_conditional)
    result = llm.invoke(prompt)

    if "product" in result.result:
        return "product_node"
    elif "company" in result.result:
        return "company_detail"
    else:
        return "company_detail"
