"""Graph definition and compilation."""
from langgraph.graph import StateGraph, START, END
from ..config.state import MyGraphState
from .nodes import (
    planner_agent,
    researcher_agent,
    summarizer_agent,
    visualizer_agent,
    tools_node,
)
from .routing import (
    route_from_researcher,
    route_from_summarizer,
    route_from_visualizer,
)


def create_graph():
    """
    Create and compile the multi-agent workflow graph.

    The graph follows this flow:
    START -> planner -> researcher -> summarizer -> visualizer -> END

    With conditional routing based on mode and tool calls.

    Returns:
        Compiled LangGraph application
    """
    workflow = StateGraph(MyGraphState)

    # Add nodes
    workflow.add_node("planner_agent", planner_agent)
    workflow.add_node("researcher_agent", researcher_agent)
    workflow.add_node("summarizer_agent", summarizer_agent)
    workflow.add_node("visualizer_agent", visualizer_agent)
    workflow.add_node("tools", tools_node)

    # Add edges
    workflow.add_edge(START, "planner_agent")
    workflow.add_edge("planner_agent", "researcher_agent")

    # Conditional routing from researcher
    workflow.add_conditional_edges(
        "researcher_agent",
        route_from_researcher,
        {
            "tools": "tools",
            "summarizer_agent": "summarizer_agent",
            str(END): str(END)
        }
    )

    # Tools loop back to researcher (research loop)
    workflow.add_conditional_edges(
        "tools",
        lambda state: "researcher_agent",
        {"researcher_agent": "researcher_agent"}
    )

    # Conditional routing from summarizer
    workflow.add_conditional_edges(
        "summarizer_agent",
        route_from_summarizer,
        {
            "visualizer_agent": "visualizer_agent",
            str(END): str(END)
        }
    )

    # Conditional routing from visualizer
    workflow.add_conditional_edges(
        "visualizer_agent",
        route_from_visualizer,
        {
            str(END): str(END)
        }
    )

    return workflow.compile()
