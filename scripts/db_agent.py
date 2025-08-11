"""AI assistant for database connection issues using Ollama."""
# ruff: noqa: S603, S607
import subprocess


def troubleshoot_connection(issue: str, model: str = "openllama") -> str:
    """
    Uses the Ollama AI model to provide troubleshooting guidance for a database connection issue.
    
    Args:
        issue: Description of the connection problem.
        model: Name of the Ollama model to use (default is "openllama").
    
    Returns:
        The output from the Ollama tool with troubleshooting advice, or an error message if the tool fails to run.
    """
    try:
        result = subprocess.run(  # noqa: S603,S607
            ["ollama", "run", model, issue],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout

        return f"Failed to run ollama: {err}"

