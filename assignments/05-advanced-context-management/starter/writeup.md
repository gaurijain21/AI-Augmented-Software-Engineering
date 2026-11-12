# Week 5 write-up

## MCP client transcript

I registered the server with an MCP STDIO client using the equivalent configuration:

```json
{
  "mcpServers": {
    "data-explorer": {
      "command": "python",
      "args": [".../assignments/05-advanced-context-management/starter/server.py"]
    }
  }
}
```

The client listed the two tools and invoked each one:

```text
client -> tools/list
server -> search_countries(query: string, limit?: integer)
server -> get_country_details(name: string)

client -> search_countries({"query": "Germany", "limit": 1})
server -> [{"name": "Germany", "capital": "Berlin", "region": "Europe", "subregion": "Western Europe"}]

client -> get_country_details({"name": "Germany"})
server -> {"name": "Germany", "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
           "languages": {"deu": "German"}, "borders": ["AUT", "BEL", "CZE", "DNK", "FRA", ...],
           "flag_url": "https://raw.githubusercontent.com/mledoze/countries/master/data/DEU.svg"}
```

I also exercised the failure paths through the client: an empty name returned
`{"error": "name must be a non-empty string"}`, an unknown country returned a not-found error,
and simulated timeout/HTTP failures returned structured upstream errors for both tools.

## What I learned

An MCP tool is a deliberately narrow context boundary: the model receives only the fields the
tool chooses to expose, not the entire source record. Returning stable, small JSON shapes makes
tool results easier for an agent to reason about and reduces accidental context growth. Input
validation and explicit error objects are especially important over STDIO because an exception
that escapes a tool can take down the whole client session. Caching the dataset keeps repeated
calls cheap while still making the first network call's timeout and HTTP failures visible.
