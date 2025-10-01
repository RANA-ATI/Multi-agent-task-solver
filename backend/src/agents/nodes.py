"""Agent node implementations."""
from uuid import uuid4
from langchain_core.messages import AIMessage, ToolMessage
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode

from ..config import settings
from ..config.state import MyGraphState
from ..tools import web_search, plot_table
from ..prompts import (
    planner_prompt,
    researcher_prompt,
    summarizer_prompt,
    visualizer_prompt,
)


# Initialize LLM
llm = init_chat_model(f"{settings.LLM_PROVIDER}:{settings.LLM_MODEL}")

# Bind tools to specific agents
# Researcher should only be able to call web_search
researcher_llm = llm.bind_tools([web_search])
# Visualizer should only be able to call plot_table
visualizer_llm = llm.bind_tools([plot_table])

# ToolNode knows how to run either tool when asked
tools_node = ToolNode([web_search, plot_table])

# Create runnables by chaining prompts with LLMs
planner_runnable = planner_prompt | llm
researcher_runnable = researcher_prompt | researcher_llm
summarizer_runnable = summarizer_prompt | llm
visualizer_runnable = visualizer_prompt | visualizer_llm


def planner_agent(state: MyGraphState):
    """
    Planner agent node.

    Reads user request and produces a short plan with numbered steps.
    """
    ai = planner_runnable.invoke(state)
    return {"messages": [ai]}


def researcher_agent(state: MyGraphState):
    """
    Researcher agent node.

    Gathers facts using web_search tool and synthesizes findings.
    """
    ai = researcher_runnable.invoke(state)
    return {"messages": [ai]}


def summarizer_agent(state: MyGraphState):
    """
    Summarizer agent node.

    Produces bullet-point summary with action items.
    """
    ai = summarizer_runnable.invoke(state)
    return {"messages": [ai]}


def visualizer_agent(state: MyGraphState):
    """
    Visualizer agent node.

    Creates visualizations from table data. If the model emits a tool call,
    returns the AIMessage for ToolNode to handle. Otherwise, auto-invokes
    plot_table if table_text exists.
    """
    ai = visualizer_runnable.invoke(state)

    # If the model already requested a tool, return only the AIMessage
    tool_calls = getattr(ai, "tool_calls", None)
    if tool_calls and len(tool_calls) > 0:
        return {"messages": [ai]}

    # No tool call present. If table_text exists, auto-plot.
    out_messages = [ai]
    if state.get("table_text"):
        try:
            chart_type = "line"
            content_lower = (ai.content or "").lower()
            if "bar chart" in content_lower or ("bar" in content_lower and "line" not in content_lower):
                chart_type = "bar"
            elif "scatter" in content_lower:
                chart_type = "scatter"

            file_path = plot_table.invoke({"table_text": state["table_text"], "chart_type": chart_type})

            # Return a ToolMessage so downstream consumers see the tool result
            tm = ToolMessage(tool_call_id=str(uuid4()), name="plot_table", content=file_path)
            out_messages.append(tm)

            # Optionally add a follow-up AIMessage
            follow_up = AIMessage(
                content=f"Automatically plotted table as a {chart_type} chart. File saved at: {file_path}"
            )
            out_messages.append(follow_up)
        except Exception as e:
            out_messages.append(AIMessage(content=f"Failed to auto-plot the table: {e}"))

    return {"messages": out_messages}
