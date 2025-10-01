"""Graph state definition."""
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class MyGraphState(TypedDict):
    """State schema for the multi-agent graph.

    Attributes:
        messages: List of LangChain message objects (HumanMessage, AIMessage, etc.)
                 Messages are appended rather than overwritten via add_messages.
        mode: Controls pipeline execution: "research", "summary", "visualize", or "full"
        table_text: Optional raw text table for visualization
    """

    messages: Annotated[list[AnyMessage], add_messages]
    mode: str
    table_text: str
