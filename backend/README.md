# Multi-Agent Task Solver

A sophisticated multi-agent system built with **LangGraph** that orchestrates specialized AI agents to research, summarize, and visualize data autonomously.

## 🎯 Overview

This system demonstrates a production-ready implementation of LangGraph's multi-agent orchestration capabilities, featuring:

- **4 Specialized Agents** working in coordinated pipeline
- **Real-time Web Search** integration via Tavily API
- **Automatic Tool Selection** based on task requirements
- **Dynamic Data Visualization** from multiple table formats
- **Conditional Routing** for optimized execution paths

---

## 🏗️ Architecture

### Agent Pipeline

```
START → Planner → Researcher → Summarizer → Visualizer → END
                     ↓↑ (tools: web_search)
```

### Specialized Agents

1. **Planner Agent**
   - Analyzes user requests and creates execution plan
   - Identifies missing information
   - Generates structured approach (2-6 steps)

2. **Researcher Agent**
   - Gathers facts using web search tool (Tavily)
   - Synthesizes information from multiple sources
   - Provides cited evidence with provenance
   - **Tool Access:** `web_search`

3. **Summarizer Agent**
   - Produces concise bullet-point summaries
   - Formats with bold headers and structured content
   - Generates actionable recommendations
   - Limits output to 180 words for clarity

4. **Visualizer Agent**
   - Automatically detects table data in messages
   - Creates professional charts (line, bar, scatter)
   - Supports multiple table formats (CSV, Markdown, whitespace)
   - **Tool Access:** `plot_table`

### Tools

- **`web_search`**: Real-time web search via Tavily API (max 2 results)
- **`plot_table`**: Data visualization engine supporting CSV, Markdown, and whitespace-separated tables

---

## 📁 Project Structure

```
backend/
├── src/
│   ├── agents/              # Agent orchestration
│   │   ├── nodes.py         # Agent implementations (planner, researcher, summarizer, visualizer)
│   │   ├── routing.py       # Conditional routing logic based on mode and tool calls
│   │   └── graph.py         # LangGraph workflow definition and compilation
│   ├── config/              # Configuration management
│   │   ├── settings.py      # Environment variables, API keys, app settings
│   │   └── state.py         # Graph state schema (TypedDict)
│   ├── prompts/             # Agent system prompts
│   │   └── templates.py     # ChatPromptTemplate for each agent
│   ├── tools/               # Agent tools
│   │   ├── search.py        # Tavily web search integration
│   │   └── visualization.py # Matplotlib plotting engine
│   └── utils/               # Utility functions
│       └── helpers.py       # Message handling and graph visualization
├── main.py                  # Entry point with 3 example workflows
├── examples.py              # Comprehensive test suite (10 test cases)
├── outputs/                 # Generated visualizations (gitignored)
├── pyproject.toml           # Dependencies (uv/pip)
├── .env                     # API keys (gitignored)
├── .env.example             # Environment template
└── README.md                # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

### Installation

```bash
# 1. Install dependencies
uv sync
# or
pip install -e .

# 2. Set up environment variables
cp .env.example .env

# 3. Edit .env with your API keys
# GOOGLE_API_KEY=your_google_api_key
# TAVILY_API_KEY=your_tavily_api_key
# ANTHROPIC_API_KEY=your_anthropic_api_key
```

### Required API Keys

| Service | Purpose | Get Key From |
|---------|---------|--------------|
| **Anthropic** | Claude 3.5 Sonnet (primary LLM) | https://console.anthropic.com/ |
| **Tavily** | Real-time web search | https://tavily.com/ |
| **Google** | Gemini (optional alternative LLM) | https://makersuite.google.com/app/apikey |

---

## 🧪 Running Tests

### Basic Examples (3 tests, ~30 seconds)
```bash
python main.py
```

Runs:
- **Test 1:** Research mode - EV adoption query with web search
- **Test 2:** Summary mode - Research + structured summary
- **Test 3:** Visualize mode - Chart generation from CSV data

### Comprehensive Test Suite (10 tests, ~3-4 minutes)
```bash
python examples.py
```

Covers:
- ✓ Research queries (no tables) - 4 tests
- ✓ Data visualization (CSV, Markdown, whitespace) - 6 tests
- ✓ Large datasets (16+ data points)
- ✓ Complex multi-step analysis

**Expected Results:**
- ✅ 10/10 tests pass (100% success rate)
- 📊 6 charts generated in `outputs/` folder
- ⏱️ ~3-4 minutes total runtime

---

## 💻 Usage Examples

### Example 1: Basic Research Query
```python
from src import create_graph, last_nonempty_ai_message
from langchain_core.messages import HumanMessage

app = create_graph()

inputs = {
    "messages": [HumanMessage(content="What are the latest renewable energy trends?")],
    "mode": "full",
    "table_text": ""
}

output = app.invoke(inputs)
final = last_nonempty_ai_message(output["messages"])
print(final.content)
```

### Example 2: Data Visualization
```python
from src import create_graph
from langchain_core.messages import HumanMessage

app = create_graph()

csv_data = """month,revenue
Jan,50000
Feb,62000
Mar,78000
Apr,85000"""

inputs = {
    "messages": [HumanMessage(content="Create a chart showing revenue growth")],
    "mode": "visualize",
    "table_text": csv_data
}

output = app.invoke(inputs)
# Chart saved in outputs/plot_*.png
```

### Example 3: Research-Only Mode
```python
inputs = {
    "messages": [HumanMessage(content="Find statistics on global EV adoption")],
    "mode": "research",  # Stops after research, skips summary/visualization
    "table_text": ""
}
output = app.invoke(inputs)
```

---

## 🎛️ Execution Modes

| Mode | Pipeline | Duration | Use Case |
|------|----------|----------|----------|
| `research` | Planner → Researcher | ~10s | Quick fact-finding with synthesis |
| `summary` | Planner → Researcher → Summarizer | ~15s | Structured summaries with action items |
| `visualize` | Full pipeline + chart generation | ~20s | When table data is provided |
| `full` | All agents (default) | ~25s | Comprehensive analysis |

**Note:** Modes currently require manual specification. See "Future Enhancements" for automatic mode detection.

---

## ⚙️ Configuration

### LLM Settings

Edit `src/config/settings.py`:

```python
# Current: Anthropic Claude 3.5 Sonnet
LLM_PROVIDER = "anthropic"
LLM_MODEL = "claude-3-5-sonnet-latest"

# Alternative: Google Gemini
# LLM_PROVIDER = "google_genai"
# LLM_MODEL = "gemini-2.5-flash"
```

### Visualization Settings

```python
PLOT_OUTPUT_DIR = "outputs"      # Chart output directory
PLOT_FIGURE_SIZE = (8, 4.5)      # Figure dimensions (inches)
PLOT_DPI = 150                   # Resolution
```

### Search Settings

```python
TAVILY_MAX_RESULTS = 2           # Max search results per query
```

---

## 🎨 Design Decisions

### 1. **LangGraph for Orchestration**
**Why:** Built-in conditional routing, state management, and tool calling support.

**Trade-offs:**
- ✅ Robust agent coordination with minimal boilerplate
- ✅ Built-in support for tool loops and conditional edges
- ⚠️ Learning curve for LangGraph-specific concepts
- ⚠️ More heavyweight than simple LangChain chains

### 2. **Modular Agent Architecture**
**Why:** Separation of concerns, testability, maintainability.

**Structure:**
- Agents (nodes) separated from routing logic
- Prompts isolated in templates
- Tools as standalone modules
- Configuration centralized

**Benefits:**
- Easy to add new agents/tools
- Each component independently testable
- Clear responsibility boundaries

### 3. **Manual Mode Selection (Current Implementation)**
**Why:** Simplicity and predictability for initial implementation.

**Trade-offs:**
- ✅ Explicit control over pipeline execution
- ✅ Predictable behavior and easier debugging
- ❌ Requires user to specify mode for each query
- ❌ Not fully autonomous

**Future:** See "Enhancements" section for automatic mode detection.

### 4. **Matplotlib for Visualization**
**Why:** Lightweight, well-documented, good enough for MVP.

**Trade-offs:**
- ✅ Simple API, fast rendering
- ✅ Good for basic charts (line, bar, scatter)
- ❌ Less interactive than Plotly
- ❌ Limited customization vs Seaborn

**Future:** Planned migration to Plotly/Seaborn for richer visualizations.

### 5. **State Schema Design**
**Current state:**
```python
class MyGraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    mode: str              # Required field
    table_text: str        # Required field
```

**Trade-offs:**
- ✅ Simple and explicit
- ❌ Requires boilerplate (empty strings for unused fields)
- ❌ Mode must be manually specified

**Future:** Optional fields with intelligent defaults.

---

## 🚀 Future Enhancements

### High Priority

#### 1. **Automatic Mode Detection**
**Current:** Manual mode specification required.

**Enhancement:** Intelligent router agent that analyzes query and selects mode:
```python
# Future API
inputs = {
    "messages": [HumanMessage(content="Show me a chart of Q1 sales")]
    # No mode/table_text needed - automatically detected
}
```

**Implementation:**
- Add Router Agent before Planner
- Analyze query for keywords ("chart", "visualize", "summarize", "find")
- Detect table data in message content
- Set mode and extract table_text automatically

**Benefits:**
- Fully autonomous operation
- Better user experience
- More intelligent than hardcoded modes

---

#### 2. **Enhanced Visualization with Plotly/Seaborn**
**Current:** Basic Matplotlib charts (line, bar, scatter).

**Enhancement:**
- **Plotly:** Interactive charts with zoom, pan, hover tooltips
- **Seaborn:** Statistical visualizations (heatmaps, distributions, pair plots)
- **Chart Types:** Add histograms, box plots, violin plots, treemaps

**Example:**
```python
# Plotly interactive chart
import plotly.graph_objects as go

fig = go.Figure(data=go.Scatter(x=df['year'], y=df['revenue']))
fig.write_html('outputs/chart.html')  # Interactive HTML output
```

**Benefits:**
- Richer, more professional visualizations
- Better for data exploration
- Export to multiple formats (PNG, SVG, HTML)

---

#### 3. **Markdown/Rich Text Output**
**Current:** Plain text summaries.

**Enhancement:**
- Proper markdown formatting in outputs
- Tables, lists, code blocks
- Better structure and readability

**Example Output:**
```markdown
## Key Findings

| Metric | 2023 | 2024 | Change |
|--------|------|------|--------|
| EV Sales | 1.2M | 1.8M | +50% |

### Recommendations
1. **Market Expansion:** Focus on emerging markets...
2. **Product Development:** Invest in battery technology...
```

---

#### 4. **Additional Tools**

| Tool | Purpose | Priority |
|------|---------|----------|
| **`code_executor`** | Run Python/SQL code snippets | High |
| **`file_reader`** | Read CSV/Excel/PDF files | High |
| **`data_processor`** | Clean, transform, aggregate data | Medium |
| **`api_caller`** | Call external REST APIs | Medium |
| **`sql_query`** | Query databases | Medium |
| **`web_scraper`** | Extract structured data from websites | Low |

**Example - Code Executor:**
```python
@tool
def code_executor(code: str, language: str = "python") -> str:
    """Execute code safely in sandboxed environment."""
    # Use RestrictedPython or Docker sandbox
    return execution_result
```

---

#### 5. **State Persistence & Conversation Memory**
**Current:** Each invocation is stateless.

**Enhancement:**
- Save conversation history to database
- Resume previous analysis sessions
- Reference earlier findings

**Implementation:**
```python
# Add checkpoint system
from langgraph.checkpoint import MemorySaver

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Resume conversation
output = app.invoke(inputs, config={"thread_id": "session_123"})
```

---

#### 6. **Streaming Responses**
**Current:** Wait for full completion before output.

**Enhancement:** Stream agent outputs in real-time.

**Example:**
```python
for chunk in app.stream(inputs):
    print(chunk)  # Real-time agent outputs
```

**Benefits:**
- Better UX for long-running queries
- See progress as agents work
- Early feedback

---

### Medium Priority

- **Error Recovery:** Retry logic for failed tool calls
- **Caching:** Cache web search results to reduce API calls
- **Parallel Tool Calls:** Execute multiple searches simultaneously
- **Custom Visualization Themes:** Brand-specific chart styling
- **Export Formats:** PDF reports, Excel spreadsheets
- **Multi-language Support:** I18n for prompts and outputs
- **Metrics & Logging:** Track performance, costs, success rates

---

### Lower Priority

- **Web UI:** Gradio/Streamlit interface
- **API Server:** FastAPI REST endpoint
- **Webhooks:** Notify on completion
- **Scheduled Runs:** Cron-like automation
- **Team Collaboration:** Share analyses

---

## 🔧 Development

### Adding a New Agent

1. **Create agent function** (`src/agents/nodes.py`):
```python
def my_agent(state: MyGraphState):
    """My custom agent."""
    ai = my_runnable.invoke(state)
    return {"messages": [ai]}
```

2. **Add prompt template** (`src/prompts/templates.py`):
```python
my_agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are MyAgent. Your task is to..."),
    MessagesPlaceholder("messages"),
])
```

3. **Update graph** (`src/agents/graph.py`):
```python
workflow.add_node("my_agent", my_agent)
workflow.add_edge("previous_agent", "my_agent")
```

### Adding a New Tool

1. **Create tool** (`src/tools/my_tool.py`):
```python
from langchain_core.tools import tool

@tool
def my_tool(input: str) -> str:
    """Tool description for LLM."""
    # Implementation
    return result
```

2. **Bind to agent** (`src/agents/nodes.py`):
```python
my_agent_llm = llm.bind_tools([my_tool])
tools_node = ToolNode([web_search, plot_table, my_tool])
```

---

## 📊 Test Results

**Last Run:** October 1, 2025

| Test | Description | Status |
|------|-------------|--------|
| 1 | Research mode (renewable energy) | ✅ PASS |
| 2 | Summary mode (AI breakthroughs) | ✅ PASS |
| 3 | CSV visualization (revenue growth) | ✅ PASS |
| 4 | Markdown table (temperature data) | ✅ PASS |
| 5 | Whitespace table (sales data) | ✅ PASS |
| 6 | Full pipeline (quantum computing) | ✅ PASS |
| 7 | Product comparison chart | ✅ PASS |
| 8 | Specific data request (EV stats) | ✅ PASS |
| 9 | Large dataset (16 quarters) | ✅ PASS |
| 10 | Complex analysis (climate + agriculture) | ✅ PASS |

**Success Rate:** 100% (10/10)

See `TEST_RESULTS.md` for detailed analysis.

---

## ⚠️ Known Limitations

### Current Constraints (24-Hour Development)

1. **Manual Mode Selection**
   - User must specify `mode` parameter
   - No automatic query analysis
   - **Impact:** Less autonomous than ideal
   - **Mitigation:** Clear documentation, easy-to-use modes

2. **Basic Visualization**
   - Only Matplotlib (not Plotly/Seaborn)
   - Limited chart types (line, bar, scatter)
   - Static PNG outputs only
   - **Impact:** Less interactive/rich visualizations
   - **Mitigation:** Clean, professional charts; easy to extend

3. **Table Format Parsing**
   - Markdown tables sometimes have numeric detection issues
   - No support for Excel/Google Sheets files
   - **Impact:** May require manual CSV conversion
   - **Mitigation:** Supports 3 formats (CSV, Markdown, whitespace)

4. **No Conversation Memory**
   - Each invocation is independent
   - Cannot reference previous queries
   - **Impact:** Must repeat context in each query
   - **Mitigation:** Full context in single query

5. **Limited Error Recovery**
   - Tool failures stop pipeline
   - No automatic retry logic
   - **Impact:** Single point of failure
   - **Mitigation:** Good error messages, graceful degradation

### Minor Issues

- **Pandas FutureWarning:** Non-critical warning in `visualization.py:95`
- **Bar Chart Detection:** Requested bar charts sometimes render as line charts
- **Windows Path Handling:** Output directory uses forward slashes (works but inconsistent)

---

## 📝 Design Trade-offs (24h Constraint)

| Feature | Ideal | Implemented | Reason |
|---------|-------|-------------|--------|
| Mode selection | Automatic | Manual | Simplicity; focused on core pipeline |
| Visualization | Plotly/Seaborn | Matplotlib | Faster implementation, good enough for MVP |
| State fields | Optional | Required | Avoided complex TypedDict with Optional handling |
| Error handling | Retry + recovery | Fail fast | Clearer debugging, less complexity |
| Memory | Persistent | Stateless | Avoided database dependency |
| Streaming | Real-time | Batch | Simpler implementation |
| File upload | Direct file handling | Text paste | No file server setup needed |

**Philosophy:** Build a solid, working foundation that can be enhanced incrementally rather than a feature-rich but buggy prototype.

---

## 🐛 Troubleshooting

### Missing API Keys
```bash
WARNING: Missing environment variables: TAVILY_API_KEY
```
**Solution:** Check `.env` file has all required keys set.

### Import Errors
```bash
ModuleNotFoundError: No module named 'langchain'
```
**Solution:** Install dependencies: `uv sync` or `pip install -e .`

### No Charts Generated
```bash
# outputs/ folder is empty
```
**Solution:**
1. Check `outputs/` directory exists: `mkdir outputs`
2. Verify mode is set to "visualize" or "full"
3. Ensure `table_text` contains valid data

### Unicode Errors (Windows)
```bash
UnicodeEncodeError: 'charmap' codec can't encode character
```
**Solution:** Already fixed in latest version (emojis removed).

---

## 📚 Documentation

- **README.md** (this file) - Overview, setup, usage
- **QUICK_START.md** - Quick reference guide
- **TEST_RESULTS.md** - Detailed test analysis
- **Docstrings** - Inline documentation in all modules

---

## 🤝 Contributing

This is a demonstration project showcasing LangGraph capabilities. Future enhancements welcome!

**Areas for contribution:**
1. Automatic mode detection (router agent)
2. Plotly/Seaborn visualization
3. Additional tools (file reader, code executor, etc.)
4. Markdown output formatting
5. Conversation memory/state persistence

---

## 📄 License

[Your License Here]

---

## 🙏 Acknowledgments

- **LangGraph** - Multi-agent orchestration framework
- **Anthropic Claude** - Primary LLM (Claude 3.5 Sonnet)
- **Tavily** - Real-time web search API
- **LangChain** - Agent tooling and integrations

---

## 📧 Contact

[Your Contact Information]

---

**Built with LangGraph | Powered by Claude 3.5 Sonnet**
