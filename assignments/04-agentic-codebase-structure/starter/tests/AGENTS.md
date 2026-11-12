# Test-Specific Guidance

These tests exercise the public route handlers at the API boundary. If an
HTTP-level client is available, it may be used, but do not test private helper
functions in place of endpoint behavior.

- Cover both successful behavior and at least one failure or edge case.
- Use the `client` fixture so each test receives an isolated temporary SQLite
  database; tests must not rely on execution order.
- Assert status codes and response behavior, not private implementation details.
- Keep tests independent and use distinct input values when the behavior calls
  for multiple resources.
