"""Comprehensive test cases for the multi-agent task solver."""
import os
import time
from langchain_core.messages import HumanMessage, ToolMessage

from src import create_graph, settings, last_nonempty_ai_message


def print_separator(title):
    """Print a formatted separator."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def run_test_case(app, test_name, inputs, show_all_messages=False):
    """Run a single test case and display results."""
    print_separator(test_name)
    print(f"Mode: {inputs['mode']}")
    print(f"Query: {inputs['messages'][0].content[:100]}...")
    print("\n" + "-" * 70)

    try:
        output = app.invoke(inputs)

        if show_all_messages:
            print("\nAll Messages:")
            for i, msg in enumerate(output["messages"]):
                print(f"\n[{i}] {type(msg).__name__}:")
                print(f"  {str(msg.content)[:200]}...")

        print("\n--- Final Output ---")
        final = last_nonempty_ai_message(output["messages"])
        if final:
            print(final.content)
        else:
            print("(no non-empty AI message)")

        # Check for generated plots
        for m in output["messages"]:
            if isinstance(m, ToolMessage) and getattr(m, "name", "") == "plot_table":
                print(f"\n[PLOT] Plot saved: {getattr(m, 'content', None)}")

        print("\n[PASS] Test completed successfully")
        return True

    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {str(e)}")
        return False


def main():
    """Run all test cases."""
    # Validate environment
    if not settings.validate():
        print("⚠️  Please set up your environment variables in .env file")
        return

    # Set environment variables
    os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
    os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
    os.environ["ANTHROPIC_API_KEY"] = settings.ANTHROPIC_API_KEY

    # Create the graph
    app = create_graph()

    results = []

    # =========================================================================
    # TEST CASE 1: Research Mode - No Tables
    # =========================================================================
    results.append(run_test_case(
        app,
        "TEST 1: Research Mode - General Query (No Tables)",
        {
            "messages": [HumanMessage(content="What are the latest developments in renewable energy in 2024?")],
            "mode": "research",
            "table_text": ""
        }
    ))
    time.sleep(2)

    # =========================================================================
    # TEST CASE 2: Summary Mode - No Tables
    # =========================================================================
    results.append(run_test_case(
        app,
        "TEST 2: Summary Mode - Tech Trends (No Tables)",
        {
            "messages": [HumanMessage(content="Summarize the key AI breakthroughs in the last 6 months")],
            "mode": "summary",
            "table_text": ""
        }
    ))
    time.sleep(2)

    # =========================================================================
    # TEST CASE 3: Visualize Mode - CSV Format
    # =========================================================================
    csv_data = """year,revenue
2019,1000000
2020,1500000
2021,2200000
2022,3100000
2023,4500000"""

    results.append(run_test_case(
        app,
        "TEST 3: Visualize Mode - CSV Table (Revenue Growth)",
        {
            "messages": [HumanMessage(content="Please create a line chart showing our revenue growth over the years.")],
            "mode": "visualize",
            "table_text": csv_data
        }
    ))
    time.sleep(2)

    # =========================================================================
    # TEST CASE 4: Visualize Mode - Markdown Table
    # =========================================================================
    markdown_table = """| Month | Temperature |
|-------|-------------|
| Jan   | 5           |
| Feb   | 7           |
| Mar   | 12          |
| Apr   | 18          |
| May   | 23          |
| Jun   | 28          |"""

    results.append(run_test_case(
        app,
        "TEST 4: Visualize Mode - Markdown Table (Temperature)",
        {
            "messages": [HumanMessage(content="Show me a visualization of this temperature data.")],
            "mode": "visualize",
            "table_text": markdown_table
        }
    ))
    time.sleep(2)

    # =========================================================================
    # TEST CASE 5: Visualize Mode - Whitespace Separated
    # =========================================================================
    whitespace_table = """date        sales
2024-01     450
2024-02     520
2024-03     610
2024-04     580
2024-05     690
2024-06     750"""

    results.append(run_test_case(
        app,
        "TEST 5: Visualize Mode - Whitespace Table (Sales Data)",
        {
            "messages": [HumanMessage(content="Create a chart from this sales data.")],
            "mode": "visualize",
            "table_text": whitespace_table
        }
    ))
    time.sleep(2)

    # =========================================================================
    # TEST CASE 6: Full Mode - No Tables (End-to-End)
    # =========================================================================
    results.append(run_test_case(
        app,
        "TEST 6: Full Mode - Complete Pipeline (No Tables)",
        {
            "messages": [HumanMessage(content="What is the current state of quantum computing research?")],
            "mode": "full",
            "table_text": ""
        }
    ))
    time.sleep(2)

    # =========================================================================
    # TEST CASE 7: Visualize Mode - Bar Chart Request
    # =========================================================================
    product_data = """product,units_sold
Product A,1200
Product B,850
Product C,1500
Product D,920
Product E,1100"""

    results.append(run_test_case(
        app,
        "TEST 7: Visualize Mode - Bar Chart (Product Sales)",
        {
            "messages": [HumanMessage(content="Create a bar chart comparing product sales.")],
            "mode": "visualize",
            "table_text": product_data
        }
    ))
    time.sleep(2)

    # =========================================================================
    # TEST CASE 8: Research Mode - Specific Facts
    # =========================================================================
    results.append(run_test_case(
        app,
        "TEST 8: Research Mode - Specific Data Request",
        {
            "messages": [HumanMessage(content="Find the latest global EV market share statistics for 2024")],
            "mode": "research",
            "table_text": ""
        }
    ))
    time.sleep(2)

    # =========================================================================
    # TEST CASE 9: Visualize Mode - Large Dataset
    # =========================================================================
    large_dataset = """quarter,profit
Q1-2020,25000
Q2-2020,28000
Q3-2020,31000
Q4-2020,35000
Q1-2021,38000
Q2-2021,42000
Q3-2021,45000
Q4-2021,50000
Q1-2022,53000
Q2-2022,58000
Q3-2022,62000
Q4-2022,67000
Q1-2023,71000
Q2-2023,76000
Q3-2023,82000
Q4-2023,88000"""

    results.append(run_test_case(
        app,
        "TEST 9: Visualize Mode - Large Dataset (Quarterly Profits)",
        {
            "messages": [HumanMessage(content="Visualize our quarterly profit trends.")],
            "mode": "visualize",
            "table_text": large_dataset
        }
    ))
    time.sleep(2)

    # =========================================================================
    # TEST CASE 10: Summary Mode - Complex Topic
    # =========================================================================
    results.append(run_test_case(
        app,
        "TEST 10: Summary Mode - Complex Analysis",
        {
            "messages": [HumanMessage(content="Analyze the impact of climate change on global agriculture and provide key recommendations")],
            "mode": "summary",
            "table_text": ""
        }
    ))

    # =========================================================================
    # RESULTS SUMMARY
    # =========================================================================
    print_separator("TEST RESULTS SUMMARY")
    passed = sum(results)
    total = len(results)
    print(f"\n[PASS] Passed: {passed}/{total}")
    print(f"[FAIL] Failed: {total - passed}/{total}")
    print(f"\nSuccess Rate: {(passed/total)*100:.1f}%")

    # List generated plots
    print("\n" + "=" * 70)
    print(" Generated Visualizations")
    print("=" * 70)
    import glob
    plots = glob.glob("outputs/*.png")
    if plots:
        for i, plot in enumerate(sorted(plots), 1):
            print(f"{i}. {plot}")
    else:
        print("No plots generated")

    print("\n" + "=" * 70)
    print(" Test Suite Completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
