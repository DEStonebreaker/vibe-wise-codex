<img src="assets/vibewise-icon.png" alt="VibeWise icon" width="96" height="96">

# VibeWise for Codex

**You design. Codex writes.**

An unofficial Codex adaptation of [VibeWise by Noah Kim](https://github.com/nykooi1/vibe-wise),
based on upstream 0.1.43. Codex asks for your approach first, helps you examine
tradeoffs, and explains unfamiliar concepts. You shape the design and decide when
it's ready to implement; Codex writes the agreed code and explains the result.

For developers who want to learn while building, from a first project to an
unfamiliar stack. The three Markdown state files remain compatible with upstream.

## Get started

The initial target is **Codex CLI on macOS or Linux**, with Python 3.10+ available
as `python3`. No extra Python packages, account, backend, or MCP server are needed.
Use a current Codex build that supports portable plugins and SessionStart hooks.

In your terminal, add this repository's marketplace:

```sh
codex plugin marketplace add DEStonebreaker/vibe-wise-codex
```

For a local checkout instead:

```sh
codex plugin marketplace add /absolute/path/to/vibe-wise-codex
```

Then:

1. Start Codex and open `/plugins`.
2. Select the **VibeWise for Codex** marketplace, install **vibe-wise-codex**, and enable it.
3. Start a new session in the project you want to learn in.
4. Open `/hooks`, review the VibeWise SessionStart command, and trust the current definition.
5. Invoke the learning skill:

```text
$vibe-wise
```

Installing a plugin does not automatically trust its hooks. Without hook trust,
explicit invocation can work while automatic restoration does not. Review hooks
again when their definition changes. If your client lacks these commands, update
Codex before attempting the plugin flow.

Setup asks one question at a time; choose **Use defaults** to skip preference
customization. Choice pickers are used when available and permitted, with ordinary
chat as the fallback. Reasoning questions and required confirmations stay in chat
on surfaces with optional-only pickers. No reply never counts as approval.

An existing repository is inspected to create a small project map. Nothing activates
in other projects just because you installed the plugin. Ask for a feature after
setup, or include the task alongside `$vibe-wise`.

## What it feels like

You're building a Notion-style notes app: users sign in, create and edit private
notes, and organize them into folders. Here, you're working through how notes and
folders relate—and what should happen when someone deletes a folder.

This condensed example adapts an upstream Claude learning session for Codex. Later implementation
steps are illustrative; intervening design discussions are omitted.

**You:**

```text
A note can be in several folders. Deleting a folder should delete its notes.
```

**Codex:**

```text
✦ Build checkpoint: Deleting a shared note

"Trip ideas" is in both Travel and Summer. Deleting it removes it from both.

When someone deletes Travel, what should happen to that note in Summer?
```

**You:**

```text
Keep it in Summer. If it has no folders left, keep the note outside any folder.
```

**Codex:**

```text
That separates deleting a folder from deleting a note.

✦ Build checkpoint: Connecting notes and folders

How would you represent which folders a note belongs to, without copying the note?
```

**You:**

```text
A links table with note_id and folder_id. Deleting a folder removes its links,
not the notes.
```

**Codex:**

```text
Each link records one membership. Several links can point to the same note;
a note with no links is unfiled.

notes ← folder links → folders

✦ Design checkpoint: Folder membership

Proposed: store notes once and track folder membership in a links table.
Deleting a folder removes its links and keeps the notes. This supports multiple
folders per note; loading a folder's notes needs a lookup through those links.

Confirming records this design. We still need to work through access rules
and technology choices before writing code.

❯ 1. Confirm and continue
     This approach makes sense to me; move to the next piece.
  2. Discuss
     Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Confirm and continue.
```

*Later, after the remaining choices for this step are worked through...*

**Codex:**

```text
✦ Implementation checkpoint: Folder membership

I'll add the agreed tables and folder-deletion operation, then test that deleting
a folder preserves its notes and their membership in other folders.
This step builds storage behavior; the UI comes later.

❯ 1. Implement this step
     This approach makes sense to me; write the code for this step.
  2. Discuss
     Ask questions or clarify anything that doesn't make sense before deciding.
```

**You:**

```text
Implement this step.
```

*Codex writes the code and runs the tests.*

**Codex:**

```text
✦ Implementation report: Folder membership

- Added the schema migration: each membership references one note and one folder.
- Added folder deletion: removes the folder and its links, preserving note content.
- Added and ran tests for shared notes and notes left without a folder; both passed.
```

You don't need to know the answer already. Codex can explain unfamiliar concepts, sketch the relevant pieces, and help you tackle a smaller question. You stay involved in forming the plan. Answer in plain English; ask for more help or say “skip” whenever you want.

Describing what you want sets the requirements. Build Checkpoints ask you to work
out how it should function; a feature preference doesn't approve an architecture.

| Checkpoint | What happens |
| --- | --- |
| **Build** | You reason through how to approach the problem with Codex. |
| **Design** | Review the design. **Confirm and continue** records it and continues planning; no code yet. |
| **Implementation** | Review the specific code changes. **Implement this step** authorizes Codex to make them. |

These aren't three mandatory stops. When ready to code, the Implementation
checkpoint also confirms the design, skipping a separate Design checkpoint.
Both confirmations offer **Discuss** to ask questions, clarify anything confusing,
or explore alternatives before deciding.

When Codex proposes additional implementation details, it separates them from your
decisions in a short list or table explaining each addition and why it matters.
You can question or change any item before proceeding.

After implementation, Codex briefly explains what changed, how the key code works,
why it fits your decision, any tests it added or updated and what they cover, and
which checks ran with their results. Ask to dig deeper anywhere it's unclear.

Small diagrams help you trace data, understand relationships, and see how the system fits together.

## Make it yours

Experience changes the support you get, not your ownership of decisions:

| Level | Teaching approach |
| --- | --- |
| Beginner | Explain unfamiliar pieces, use diagrams, ask smaller reasoning questions. |
| Intermediate | Less introductory context; explore interactions and tradeoffs. |
| Advanced | Probe difficult constraints, failure modes, and design assumptions. |

Everyone reasons first. Codex adapts to what you demonstrate and how familiar you
are with the stack. Checkpoint frequency—Light, Normal, or Frequent—is separate.

- “Use fewer checkpoints.”
- “Focus on backend architecture.”
- “Use multiple-choice questions.”
- “Just implement this one.”
- “Pause learning.” Resume with `$vibe-wise`.

Preferences, learning notes, and a project map live in `.vibe-wise/` in your project. Learning mode resumes in future sessions and after compaction. Add `.vibe-wise/` to your `.gitignore` to keep your notes out of Git; the plugin won't change it silently.

No extra account, backend, or telemetry. Saved notes are included in Codex's context, so your normal Codex data settings still apply.

To start learning this project from scratch, run `$vibe-wise-reset`. It shows the
project and asks **Cancel / Reset learning**. After confirmation, it backs up your
profile, progress, and project map inside the notes directory's `backups/` folder,
then restarts onboarding. Source code and other projects stay untouched. To change
your experience level or preferences, just tell Codex; no reset is needed.

## Updating

Refresh this marketplace from your terminal:

```sh
codex plugin marketplace upgrade vibe-wise-codex
```

Use `/plugins` to refresh/reinstall the installed plugin if needed, then start a new
session and verify the current files are loaded. Review any changed hook definition
in `/hooks`. Updating does not reset project notes.

## Compatibility and limits

This is an initial Codex port, version 0.1.0. The automated suite covers packaging,
the hook command, and state/reset behavior; live Codex installation and conversation
smoke tests must still be completed before a release. See
[development and smoke tests](docs/development.md).

- Codex CLI on macOS/Linux is the primary target.
- Other local Codex clients may load the skills, but have not been smoke-tested.
- The Codex IDE extension does not provide plugin installation.
- Ordinary ChatGPT chats and Claude Code are not supported by this fork.
- Windows is not yet verified; hook execution currently expects `python3`.
- Checkpoints are instructions to the agent, not a hard tool gate.

The SessionStart hook only reads activation state and returns file-reading
instructions. It does not modify notes, parse transcripts, or perform network calls.
The agent maintains the three state files during meaningful learning events.
A paused profile stays paused across restart and compaction. Legacy
`.sensible-vibes/` directories are reused in place; no migration is performed.

Official contracts:
[plugins and marketplaces](https://developers.openai.com/plugins/build/plugins),
[Codex hooks](https://developers.openai.com/codex/hooks),
[skills](https://developers.openai.com/codex/skills), and
[plugin surfaces](https://developers.openai.com/codex/plugins).

## License

Based on VibeWise by Noah Kim. The original copyright and MIT license are retained.

[MIT](LICENSE). You can use, modify, and share this software, including commercially. Keep the license notice with copies. The software comes without a warranty.
