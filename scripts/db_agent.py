"""AI assistant for database connection issues using Ollama."""
# ruff: noqa: S603, S607
import subprocess


def troubleshoot_connection(issue: str, model: str = "openllama") -> str:
    """Use Ollama to get help troubleshooting a connection issue.

    Parameters
    ----------
    issue: str
        Description of the connection problem.
    model: str
        Name of the ollama model to use.
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

