"""Visualization tool for plotting tables."""
import os
import io
import re
from uuid import uuid4
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from langchain_core.tools import tool
from ..config import settings


@tool
def plot_table(table_text: str, chart_type: str = "line") -> str:
    """
    Parse table_text into a DataFrame, plot it, save as PNG, and return file path.

    Accepts CSV, markdown-style table, or whitespace-separated table.

    Args:
        table_text: Raw table data as string (CSV/markdown/whitespace-separated)
        chart_type: Type of chart to create ("line", "bar", or "scatter")

    Returns:
        File path to the saved PNG plot

    Raises:
        ValueError: If table_text is empty, unparseable, or has no numeric columns
    """
    txt = (table_text or "").strip()
    if not txt:
        raise ValueError("plot_table: table_text is empty")

    df = None

    # 1) Try markdown pipe table
    try:
        if '|' in txt and re.search(r'\|[-\s:]+\|', txt):
            # Remove separator line and outer pipes, keep header + rows
            lines = []
            for line in txt.splitlines():
                if re.match(r'^\s*\|?\s*-{2,}\s*\|?', line):
                    continue
                lines.append(line.strip().strip('|'))
            csv_txt = "\n".join(lines)
            df = pd.read_csv(io.StringIO(csv_txt))
        # 2) Try plain CSV
        elif '\n' in txt and ',' in txt:
            df = pd.read_csv(io.StringIO(txt))
    except Exception:
        df = None

    # 3) Try whitespace separated
    if df is None:
        try:
            df = pd.read_csv(io.StringIO(txt), sep=r'\s+')
        except Exception:
            df = None

    if df is None:
        raise ValueError(
            "plot_table: Unable to parse table_text into a DataFrame. "
            "Provide CSV or markdown table with header row."
        )

    # Choose x and y columns
    x_col = None
    for c in df.columns:
        if c.lower() in ("date", "year", "time") or re.search(r'date|year|time', c.lower()):
            x_col = c
            break
    if x_col is None:
        x_col = df.columns[0]

    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and c != x_col]
    y_col = numeric_cols[0] if numeric_cols else (df.columns[1] if len(df.columns) > 1 else None)

    if y_col is None:
        # Try to convert second column to numeric
        if len(df.columns) >= 2:
            try:
                df[df.columns[1]] = pd.to_numeric(df[df.columns[1]], errors='coerce')
                y_col = df.columns[1]
            except Exception:
                y_col = None

    if y_col is None:
        raise ValueError(
            "plot_table: No numeric column found to plot. "
            "Provide at least one numeric column."
        )

    # Attempt date parsing for x column
    try:
        df[x_col] = pd.to_datetime(df[x_col], errors='ignore')
    except Exception:
        pass

    # Create plot
    plt.figure(figsize=settings.PLOT_FIGURE_SIZE)
    if chart_type == "line":
        plt.plot(df[x_col], df[y_col], marker='o')
    elif chart_type == "bar":
        plt.bar(df[x_col].astype(str), df[y_col])
    elif chart_type == "scatter":
        plt.scatter(df[x_col], df[y_col])
    else:
        raise ValueError(f"plot_table: Unsupported chart_type: {chart_type}")

    plt.title(f"{y_col} vs {x_col}")
    plt.xlabel(str(x_col))
    plt.ylabel(str(y_col))
    plt.tight_layout()

    # Save plot
    out_dir = settings.PLOT_OUTPUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    fname = f"plot_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid4().hex[:6]}.png"
    out_path = os.path.join(out_dir, fname)
    plt.savefig(out_path, dpi=settings.PLOT_DPI)
    plt.close()

    return out_path
