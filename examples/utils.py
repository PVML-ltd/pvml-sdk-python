import json

import pandas as pd

from pvml import View, Workspace


async def get_pandas_from_execute(execute_async_iterator) -> pd.DataFrame:
    data_chunks = []
    async for row in execute_async_iterator:
        data_chunks.append(row.decode('utf-8'))

    complete_json = ''.join(data_chunks)

    parsed_data = json.loads(complete_json)

    columns = parsed_data[0]
    data_rows = parsed_data[1:]

    df = pd.DataFrame(data_rows, columns=columns)
    return df


def get_view_mcp(workspace: Workspace, view: View):
    _view_name = view.name
    """Retrieve the MCP created with the same name as the view"""
    print(f"Retrieving MCP associated with view '{_view_name}'...")

    # Get all MCPs in the workspace
    all_mcps = workspace.get_mcps()
    print(f"Found {len(all_mcps)} MCPs in workspace")

    # Look for MCP with the same name as the view
    view_mcp = None
    for mcp_id, mcp in all_mcps.items():
        # print(f"  MCP: {mcp.name} (ID: {mcp_id})")
        if mcp.name == _view_name:
            view_mcp = mcp
            print(f"    -> Found matching MCP for view!")
            break

    if not view_mcp:
        print(f"No MCP found with name '{_view_name}'")
        print("Available MCPs:")
        for mcp_id, mcp in all_mcps.items():
            print(f"  - {mcp.name} (ID: {mcp_id})")
        raise ValueError(f"MCP with name '{_view_name}' not found")

    print(f"\nRetrieved MCP: {view_mcp.name}")
    print(f"MCP ID: {view_mcp.id}")
    print(f"MCP Type: {view_mcp.type}")
    print(f"Created by: {view_mcp.created_by}")

    return view_mcp