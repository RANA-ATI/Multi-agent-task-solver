"""Routing logic for conditional edges in the graph."""
from langgraph.graph import END
from ..config.state import MyGraphState


def route_from_researcher(state: MyGraphState):
    """
    Route from researcher agent based on mode and tool calls.

    Returns:
        - "tools" if researcher requested a tool call
        - END if mode is "research"
        - "summarizer_agent" otherwise
    """
    mode = state.get("mode", "full")
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    if mode == "research":
        return END
    return "summarizer_agent"


def route_from_summarizer(state: MyGraphState):
    """
    Route from summarizer agent based on mode and tool calls.

    Returns:
        - "tools" if summarizer requested a tool call (rare)
        - END if mode is "summary"
        - "visualizer_agent" otherwise
    """
    mode = state.get("mode", "full")
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    if mode == "summary":
        return END
    return "visualizer_agent"


def route_from_visualizer(state: MyGraphState):
    """
    Route from visualizer agent based on tool calls.

    Returns:
        - "tools" if visualizer requested a tool call
        - END otherwise
    """
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END
