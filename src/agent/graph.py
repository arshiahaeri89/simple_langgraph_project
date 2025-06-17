from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import TypedDict

from langgraph.graph import StateGraph


@dataclass
class InputState(TypedDict):
    """
       This is the input state that shows the structure of user input.
    """
    today_sales: float
    today_costs: float
    today_customers: int

    yesterday_sales: float
    yesterday_costs: float
    yesterday_customers: int


@dataclass
class ProcessingState(InputState):
    """
        This is just a passing state to send data from input node to processing node.
    """


@dataclass
class ProcessedState(TypedDict):
    """
        This is the state that stores processed data from processing node
        and sends the data to recommendation node.
    """
    today_profit: float
    today_cac: float

    yesterday_profit: float
    yesterday_cac: float

    sales_growth: float
    costs_growth: float
    cac_growth: float


@dataclass
class OutputState(TypedDict):
    """
        This is the final state that stores the recommendations for sending it to user.
    """
    status: str
    warnings: list[str]
    recommendations: list[str]


async def input_node(state: InputState) -> ProcessingState:
    """
        This is the input node that receives user's data and just sends it to prcessing node.
    """
    return {
        "today_sales": state["today_sales"],
        "today_costs": state["today_costs"],
        "today_customers": state["today_customers"],

        "yesterday_sales": state["yesterday_sales"],
        "yesterday_costs": state["yesterday_costs"],
        "yesterday_customers": state["yesterday_customers"]
    }


async def processing_node(state: ProcessingState) -> ProcessedState:
    """
        This is the processing node that gets its data 
        from input node and processes it to thease fields:

        today_profit: today's profit
        yesterday_profit: yesterday's profit
        today_cac: today's CAC (Customer Acquisition Cost)
        yesterday_cac: yesterday's CAC (Customer Acquisition Cost)

        Profit:
        profit = sales - costs

        Customer Acquisition Cost (CAC):
        cac = costs / number_of_customers
    """
    today_profit = state['today_sales'] - state['today_costs']
    today_cac = state['today_costs'] / state['today_customers']
    yesterday_profit = state['yesterday_sales'] - state['yesterday_costs']
    yesterday_cac = state['yesterday_costs'] / state['yesterday_customers']
    # Note: All growth rates are in percentage
    sales_growth = (
        (state['today_sales'] - state['yesterday_sales']) / state["yesterday_sales"]) * 100
    costs_growth = (
        (state['today_costs'] - state['yesterday_costs']) / state["yesterday_costs"]) * 100
    cac_growth = ((today_cac - yesterday_cac) / yesterday_cac) * 100

    return {
        "today_profit": today_profit,
        "today_cac": today_cac,
        "yesterday_profit": yesterday_profit,
        "yesterday_cac": yesterday_cac,
        "sales_growth": sales_growth,
        "costs_growth": costs_growth,
        "cac_growth": cac_growth
    }


async def recommendation_node(state: ProcessedState) -> OutputState:
    """
        This is the recommendattion node that receives
        processed data and gives decision-making suggestions 
        and warnings to the user.

        Warnings:
        - CAC increased compared to yesterday.

        Recommendations:
        - if sales are growing, suggests increasing advertising budget.
        - if user is in loss today, suggests reducing costs.
        - if CAC is growing significanttly, suggests reviewing marketting campaigns.
    """
    if state['today_profit'] > 0:
        status = 'profit'
    elif state['today_profit'] == 0:
        status = 'no profit, no loss'
    else:
        status = 'loss'

    warnings = []
    if state['cac_growth'] > 0:
        warnings.append('cac is increased!')

    recommendations = []
    if state["sales_growth"] > 0:
        recommendations.append(
            'Your sales are growing. Consider increase advertising budget.')
    if state['today_profit'] < 0:
        recommendations.append('You are in loss! Reduce costs.')
    if state["cac_growth"] > 20:
        recommendations.append(
            'CAC is growing significantly! Review marketing campaigns.')

    return {
        "status": status,
        "warnings": warnings,
        "recommendations": recommendations
    }


# Define the graph
graph = (
    StateGraph(ProcessingState, input=InputState, output=OutputState)
    .add_node(input_node)
    .add_node(processing_node)
    .add_node(recommendation_node)
    .add_edge("__start__", "input_node")
    .add_edge("input_node", "processing_node")
    .add_edge("processing_node", "recommendation_node")
    .compile(name="Graph")
)


async def main():
    resp = await graph.ainvoke({
        "today_sales": 800,
        "today_costs": 400,
        "today_customers": 20,

        "yesterday_sales": 500,
        "yesterday_costs": 600,
        "yesterday_customers": 10
    })
    print(resp)


if __name__ == '__main__':
    asyncio.run(main())
