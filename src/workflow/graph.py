from langgraph.graph import StateGraph,START,END
from typing import Literal
from workflow.state import llmState
from workflow.node import comapany_detail,product_node,product_answer_node
from workflow.edge import question_conditional_edge


graph=StateGraph(llmState)

graph.add_node("company_detail",comapany_detail)
graph.add_node("product_node",product_node)
graph.add_node("product_answer_node",product_answer_node)

graph.add_conditional_edges(START,question_conditional_edge)
graph.add_edge("product_node","product_answer_node")
graph.add_edge("product_answer_node",END)
graph.add_edge("company_detail",END)

workflow = graph.compile()