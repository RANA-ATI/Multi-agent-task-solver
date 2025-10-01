"""Helper utility functions."""
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage


def _flatten_messages(raw_messages):
    """
    Yield message objects in a flat sequence from possibly nested lists.

    Args:
        raw_messages: List of messages (possibly nested)

    Yields:
        Individual message objects
    """
    stack = list(raw_messages)
    while stack:
        m = stack.pop(0)
        if m is None:
            continue
        if isinstance(m, (list, tuple)):
            stack = list(m) + stack
            continue
        yield m


def last_nonempty_ai_message(messages):
    """
    Find last AIMessage with non-empty textual content.

    Handles nested lists and ToolMessage content that might be non-string.

    Args:
        messages: List of messages (possibly nested)

    Returns:
        Last AIMessage with non-empty content, or None
    """
    last_found = None
    for m in _flatten_messages(messages):
        # Skip unexpected types
        if not isinstance(m, (AIMessage, ToolMessage, HumanMessage)):
            continue

        if isinstance(m, AIMessage):
            content = m.content or ""
            if isinstance(content, (list, tuple)):
                # Flatten if AIMessage.content is a list of strings
                text = " ".join(str(x) for x in content if x)
            else:
                text = str(content)
            if text.strip():
                last_found = m

    return last_found


def try_draw_graph(app):
    """
    Attempt to draw and display the graph using mermaid.

    Works in Jupyter/IPython environments.

    Args:
        app: Compiled LangGraph application
    """
    try:
        png = app.get_graph().draw_mermaid_png()
        from IPython.display import Image, display
        display(Image(png))
    except Exception:
        pass
