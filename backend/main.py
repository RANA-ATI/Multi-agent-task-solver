"""Main entry point for the multi-agent task solver."""
import os
import time
from langchain_core.messages import HumanMessage, ToolMessage

from src import create_graph, settings, last_nonempty_ai_message


def main():
    """Run example workflows demonstrating the multi-agent system."""
    # Validate environment variables
    if not settings.validate():
        print("Please set up your environment variables in .env file")
        return

    # Set environment variables (for LangChain/LangGraph to use)
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
    os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
    os.environ["ANTHROPIC_API_KEY"] = settings.ANTHROPIC_API_KEY

    # Create the compiled graph
    app = create_graph()

    # Example 1: Research-only mode
    print("EXAMPLE 1: Research-only mode")
    inputs = {
        "messages": [HumanMessage(content="Find 2 recent stats on EV adoption in Pakistan and summarize.")],
        "mode": "research",
        "table_text": ""
    }
    out = app.invoke(inputs)
    print("\n--- Research-only final ---")
    final = last_nonempty_ai_message(out["messages"])
    print(final.content if final else "(no non-empty AI message)")

    time.sleep(2)  # Delay between runs

    # Example 2: Summary mode (research + summary)
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Summary mode")
    print("=" * 60)
    inputs2 = {
        "messages": [HumanMessage(content="Find 2 recent stats on EV adoption in Pakistan and summarize.")],
        "mode": "summary",
        "table_text": ""
    }
    out2 = app.invoke(inputs2)
    print("\n--- Summary-only final ---")
    final2 = last_nonempty_ai_message(out2["messages"])
    print(final2.content if final2 else "(no non-empty AI message)")

    time.sleep(2)  # Delay between runs

    # Example 3: Visualize mode with CSV data
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Visualize mode")
    print("=" * 60)
    csv_text = "year,ev_count\n2018,1000\n2019,3000\n2020,7000\n2021,15000\n2022,23000\n"
    inputs3 = {
        "messages": [HumanMessage(content="Please visualize the table below.\n\n" + csv_text)],
        "mode": "visualize",
        "table_text": csv_text
    }
    out3 = app.invoke(inputs3)
    print("\n--- Visualize final ---")
    final3 = last_nonempty_ai_message(out3["messages"])
    print(final3.content if final3 else "(no non-empty AI message)")

    # Look for produced ToolMessage(s) with plot output
    for m in out3["messages"]:
        if isinstance(m, ToolMessage) and getattr(m, "name", "") == "plot_table":
            print("Plot produced at:", getattr(m, "content", None))


if __name__ == "__main__":
    main()
