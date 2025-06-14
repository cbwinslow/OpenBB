"""AI assistant for database connection issues using Ollama."""
# ruff: noqa: S603, S607
import subprocess


def troubleshoot_connection(issue: str, model: str = "openllama") -> str:
    """
    Uses the Ollama tool to provide troubleshooting assistance for a database connection issue.
    
    Args:
        issue: Description of the connection problem.
        model: Optional; name of the Ollama model to use (default is "openllama").
    
    Returns:
        The output from the Ollama tool if successful, or an error message if the command fails.
    """
    try:
        result = subprocess.run(  # noqa: S603,S607
            ["ollama", "run", model, issue],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
    except Exception as err:  # pragma: no cover - external dependency
        return f"Failed to run ollama: {err}"

