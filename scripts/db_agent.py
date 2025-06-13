"""AI assistant for database connection issues using Ollama."""
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
        result = subprocess.run(
            ["ollama", "run", model, issue],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
    except Exception as err:  # pragma: no cover - external dependency
        return f"Failed to run ollama: {err}"

