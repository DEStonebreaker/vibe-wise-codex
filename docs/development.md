# Development

VibeWise for Codex 0.1.0 adapts upstream VibeWise 0.1.43 at commit
`1135f4ae8205da78404a71e85f567d5911da4e4d`. The initial port preserves the
learning workflow and Markdown state format. Python 3.10+ and the standard
library are sufficient; no service, MCP server, or dependency installation is needed.

## Components

| Path | Responsibility |
| --- | --- |
| `plugin.json` | Portable identity and OpenAI presentation/hook configuration |
| `.agents/plugins/marketplace.json` | Repository marketplace; `./` points at the plugin root |
| `skills/vibe-wise/` | Onboarding, teaching, checkpoint flow, and state templates |
| `skills/vibe-wise-reset/` | Explicit preview/confirmation and backup/reset helper |
| `hooks/hooks.json` | SessionStart for startup, resume, clear, and compact |
| `hooks/session_start.py` | Read-only state discovery and bounded restoration instructions |

The hook tells the agent where to read notes, search the entire progress file,
and restore the pending stage. It stays silent for uninitialized or paused projects.
Its command receives `PLUGIN_ROOT` from Codex; the reset skill instead resolves
its helper from its installed file path because ordinary shell tools need not
receive hook variables.

Checkpoints are behavioral instructions, not a security boundary. No PreToolUse
gate or transcript parser is included. The agent saves meaningful state as it goes;
SessionStart reloads it after compaction. Both skills disable implicit invocation
through `agents/openai.yaml`.

## Local checks

```sh
python3 -B -m unittest discover -s tests -v
git diff --check
```

Tests execute the registered hook with JSON stdin in isolated projects and installed
copies whose paths contain spaces. They cover activation, pending restoration,
pause, incomplete onboarding, legacy names, repo/worktree boundaries, symlinks,
malformed input, read-only execution, and bounded context. Reset regressions
cover snapshots, stale confirmation, partial state, backups, failed writes, and
source isolation. Packaging checks verify manifest paths, the marketplace,
skill names, metadata, and absence of Claude runtime dependencies. CI runs Python
3.10, 3.12, and 3.14.

These checks do not prove the installed Codex client follows the teaching instructions.
Complete the live smoke tests below before tagging a release. Record the Codex
version and actual results, including failures or tests not run.

## Install a development checkout

Follow [the README](../README.md#get-started), substituting a local marketplace:

```sh
codex plugin marketplace add /absolute/path/to/vibe-wise-codex
```

Open `/plugins` in Codex CLI, install/enable the marketplace entry, start a new
session, and use `/hooks` to review and trust its current SessionStart definition.
After editing, refresh the marketplace and reinstall/refresh the installed copy
using the plugin browser; verify that the cached files are current. Review changed
hooks again. Do not bypass hook trust during normal testing.

## Conversation smoke tests

Use disposable projects. The [notes-app walkthrough](demos/notion-dupe.md)
provides example learner responses.

| Scenario | Action | Expected result |
| --- | --- | --- |
| Fresh activation | Invoke `$vibe-wise` in an empty project | One setup question at a time; three notes created; no application code before approval |
| Existing repo | Select Existing repo | Inspect source; save a map with evidence and unknowns; no invented stack |
| Requirements | Request a meaningful feature | Build checkpoint invites the learner's approach before supplying architecture |
| Partial reasoning | Give a tentative preference | Follow up on implications; no invented rationale or mastery |
| Explanation | Ask what an unfamiliar term means | Explain directly; leave the project decision open |
| Design confirmation | Reply Confirm and continue | Record the presented design and continue planning without code edits |
| Discussion | Reply Discuss | Keep implementation paused while discussing the proposal |
| Implementation | Reply Implement this step | Edit only the presented scope, verify, and report actual results |
| Pending compaction | Reach implementation approval, run `/compact`, then say continue | Restore the pending stage; continue alone does not authorize implementation |
| Restart/resume | Start another session with active state | Restore preferences and decisions without repeating completed onboarding |
| Pause | Say Pause learning, restart | Hook stays silent; explicit `$vibe-wise` resumes |
| Picker unavailable | Use a surface without a suitable picker | Ask the same choices in chat; no answer never means approval |
| Cancel reset | Invoke `$vibe-wise-reset`, reply Cancel | Read-only preview; state and source unchanged |
| Confirm reset | Preview, reply Reset learning | Back up originals; fresh onboarding; discard old preferences |
| Stale reset | Change a note after preview | Reject old token; preview and confirm again |
| Explicit skip | Say Just implement this one | Honor that scope; preserve learning preferences for later |

Onboarding uses optional `request_user_input` choices only where its tool contract
permits them. Required checkpoint/reset confirmations use chat on optional-only
surfaces. Tool execution permission never substitutes for learner confirmation.

## Upstream maintenance

Preserve the MIT license and Noah Kim attribution. Keep state/reset algorithms
close to upstream; isolate host changes to packaging, paths, interaction instructions,
and documentation. Review upstream changes semantically before replacing provider
names. Do not migrate existing state or reintroduce Claude tool assumptions.

```sh
git remote add upstream https://github.com/nykooi1/vibe-wise.git
git fetch upstream
git log main..upstream/main
```

Reference contracts:

- [Portable packaging and marketplaces](https://developers.openai.com/plugins/build/plugins)
- [Codex hooks and trust](https://developers.openai.com/codex/hooks)
- [Skills](https://developers.openai.com/codex/skills)
- [Plugin installation surfaces](https://developers.openai.com/codex/plugins)
