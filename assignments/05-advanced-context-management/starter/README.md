# Data Explorer MCP Server

This Week 5 submission exposes the open [mledoze/countries](https://github.com/mledoze/countries)
dataset as two model-friendly tools over MCP's STDIO transport. The dataset is fetched lazily
from GitHub and cached for the lifetime of the server process.

## Install and run

```bash
cd assignments/05-advanced-context-management/starter
python -m pip install -r requirements.txt
python server.py
```

The server intentionally prints nothing to the terminal: it waits for an MCP client on STDIO.

## Register in an MCP client

For Claude Desktop or another MCP-aware client, add an entry like this to its MCP configuration.
Use an absolute path to this repository on your machine:

```json
{
  "mcpServers": {
    "data-explorer": {
      "command": "python",
      "args": ["/absolute/path/to/assignments/05-advanced-context-management/starter/server.py"]
    }
  }
}
```

Restart the client after saving the configuration. The transcript in `writeup.md` records calls
to both tools and representative validation and network failures.

## Tool reference

### `search_countries(query, limit=5)`

Searches common and official country names. `query` must be a non-empty string and `limit` must
be an integer from 1 through 20. No matches return `[]`.

Example input:

```json
{"query": "united", "limit": 2}
```

Example output:

```json
[
  {
    "name": "United States",
    "capital": "Washington, D.C.",
    "region": "Americas",
    "subregion": "North America"
  }
]
```

### `get_country_details(name)`

Looks up an exact common or official country name. The result contains the country name,
currencies, languages, border `cca3` codes, and a flag URL.

Example input:

```json
{"name": "Germany"}
```

Example output:

```json
{
  "name": "Germany",
  "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
  "languages": {"deu": "German"},
  "borders": ["AUT", "BEL", "CZE"],
  "flag_url": "https://raw.githubusercontent.com/mledoze/countries/master/data/DEU.svg"
}
```

Both tools return a structured `{ "error": "..." }` item when input is invalid or the upstream
dataset cannot be loaded. Timeouts, HTTP status failures, malformed responses, and missing
countries do not crash the server.
