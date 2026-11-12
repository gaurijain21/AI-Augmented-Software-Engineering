# Assignment 04 Writeup

I put the application’s purpose, file map, setup commands, boundaries, and
change workflow in `AGENTS.md` because that information is broadly useful for
almost every task. An unfamiliar coding agent needs to know what the service
does, where its behavior lives, how to verify it, and which tempting expansions
are out of scope before it edits anything. The guide stays short so it can be
loaded as repository-wide context without competing with task-specific detail.

The scoped instruction is `tests/AGENTS.md`. It activates for tests under the
`tests/` directory and requires public-API assertions, success and failure
coverage, isolated tests, and behavior-focused assertions. I scoped it there
because those rules are important when writing tests but would be distracting
for a change to the API implementation or documentation. The tests discover
the guidance through the directory hierarchy; the repository guide also points
agents to it explicitly.

The reusable workflow is the Agent Skills-style
`.agents/skills/implement-feature/SKILL.md`. It encodes a repeatable sequence:
read guidance, inspect code and tests, state expected behavior, write a failing
behavioral test, implement the smallest compatible change, run `pytest`, and
report risks. In Codex, this file is the selected workflow artifact; other
agents can map it to their native skill or command mechanism.

For the feature, I chose custom aliases. During planning, the important cases
were an available alias, a duplicate alias, invalid URLs, and preserving the
existing generated-code path. The implementation inserts a requested alias
directly into the unique `code` column and converts SQLite uniqueness failures
into a clear `409 Conflict`. It also validates aliases so they remain safe to
use as URL path segments. The new tests verify that an alias is returned and
redirects correctly, and that reusing one is rejected. A temporary database
fixture keeps the tests independent and repeatable.
The dependency versions are pinned to a compatible FastAPI, Starlette, HTTPX,
and pytest set so a fresh setup does not silently change the test runner
underneath the assignment.

In review, I checked the feature against the task, the repository boundaries,
and the existing API behavior. The result was **ACCEPT**: the original tests
and the new custom-alias tests pass, and no new dependency or architectural
surface was needed. The main lesson is that agent-ready structure is less about
adding many files and more about putting the right context at the right scope:
stable orientation at the root, test rules near tests, and a reusable procedure
for the repeated feature loop.
