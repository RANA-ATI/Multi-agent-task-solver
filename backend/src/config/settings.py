"""Configuration and environment settings."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings and configuration."""

    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # LLM Configuration
    LLM_PROVIDER = "anthropic"
    LLM_MODEL = "claude-3-5-sonnet-latest"
    # Alternate: "google_genai:gemini-2.5-flash"

    # Tavily Search Configuration
    TAVILY_MAX_RESULTS = 2

    # Visualization Configuration
    PLOT_OUTPUT_DIR = "outputs"  # Changed to local directory for Windows compatibility
    PLOT_FIGURE_SIZE = (8, 4.5)
    PLOT_DPI = 150

    @classmethod
    def validate(cls):
        """Validate required environment variables are set."""
        missing = []
        if not cls.GOOGLE_API_KEY:
            missing.append("GOOGLE_API_KEY")
        if not cls.TAVILY_API_KEY:
            missing.append("TAVILY_API_KEY")
        if not cls.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")

        if missing:
            print(f"WARNING: Missing environment variables: {', '.join(missing)}")

        return len(missing) == 0


# Initialize settings
settings = Settings()
