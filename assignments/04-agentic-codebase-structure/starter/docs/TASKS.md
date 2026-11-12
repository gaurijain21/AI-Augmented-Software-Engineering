# Tasks

Complete one task and add behavioral tests for the successful behavior plus at
least one failure or edge case.

1. **Custom alias** — allow `POST /shorten` to accept an optional `alias`; use
   it as the code if it is available, otherwise return `409`. *(Completed.)*
2. **Click counter** — track visits and expose `GET /stats/{code}`.
3. **Expiry** — accept an optional positive `expires_in_days` and return `410`
   for expired links.
