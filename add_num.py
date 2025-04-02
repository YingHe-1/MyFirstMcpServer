import os
from pathlib import Path
from mcp.server import FastMCP
import httpx
from typing import Any

# 创建 MCP Server
mcp = FastMCP("桌面 TXT 文件统计器")

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
def count_desktop_txt_files() -> int:
    """Count the number of .txt files on the desktop."""
    # Get the desktop path
    #username = os.getenv("USER") or os.getenv("USERNAME")
    desktop_path = Path(f"D:/tmp")

    # Count .txt files
    txt_files = list(desktop_path.glob("*.txt"))
    return len(txt_files)

@mcp.tool()
def list_desktop_txt_files() -> str:
    """Get a list of all .txt filenames on the desktop."""
    # Get the desktop path
    #username = os.getenv("USER") or os.getenv("USERNAME")
    desktop_path = Path(f"D:/tmp")

    # Get all .txt files
    txt_files = list(desktop_path.glob("*.txt"))

    # Return the filenames
    if not txt_files:
        return "No .txt files found on desktop."

    # Format the list of filenames
    file_list = "\n".join([f"- {file.name}" for file in txt_files])
    return f"Found .txt files on desktop:\n{file_list}"
    
@mcp.tool()
def create_desktop_txt_file(filename: str, content: str = "") -> str:
    """Create a new .txt file on the desktop using shell command.
    
    Args:
        filename: The name of the file to create (without .txt extension)
        content: Optional content to write to the file
        ctx: MCP Context object for user interaction
    
    Returns:
        A message indicating success or failure
    """
    import subprocess
    
    # Get the desktop path
    # username = os.getenv("USER") or os.getenv("USERNAME")
    desktop_path = Path(f"D:/tmp")
    
    # Ensure filename has .txt extension
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    
    # Full path to the file
    file_path = desktop_path / filename
    
    try:
        # Create file using echo command
        if content:
            # 使用PowerShell创建带内容的文件
            cmd = f'powershell -Command "Set-Content -Path \'{file_path}\' -Value \'{content}\'"'
        else:
            # 创建空文件
            cmd = f'powershell -Command "New-Item -Path \'{file_path}\' -ItemType File -Force"'
        
        subprocess.run(cmd, shell=True, check=True)
        return f"成功在桌面创建文件 {filename}"
    except Exception:
        return f"创建文件 {filename} 失败"
    
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)
def main():
    mcp.run(transport='stdio')
    
if __name__ == "__main__":
    main()