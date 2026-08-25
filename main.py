import subprocess
import sys
import time
import uvicorn


def main():
    # Start the MCP server as a background subprocess
    mcp_process = subprocess.Popen(
        [sys.executable, "-m", "app.mcp_server.server"],
    )

    # Give it a moment to boot before the agent/API tries to connect
    time.sleep(2)

    try:
        # Run FastAPI in the main process (blocking)
        uvicorn.run("app.api.api:app", host="127.0.0.1", port=9000, reload=False)
    finally:
        mcp_process.terminate()
        mcp_process.wait()


if __name__ == "__main__":
    main()



# .\.venv\Scripts\Activate
# uv run python app/server.py
# uv run uvicorn app.api:app --reload --port 9000