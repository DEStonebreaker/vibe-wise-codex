---
name: vibe-wise-reset
description: Back up this project's learning notes and restart onboarding after confirmation. Does not reset application code.
---

# Reset VibeWise learning

Run this in the main conversation, only when explicitly invoked. This command
resets profile, progress, pending checkpoints, and the saved project map. Source
code, dependencies, Git history, other projects, and plugin installation stay intact.

Resolve `reset.py` relative to this installed SKILL.md and use its actual absolute
path in shell commands. `PLUGIN_ROOT` is supplied to plugin hooks; do not assume it
exists in an ordinary agent shell. Resolve the Learn guide as the sibling
`../vibe-wise/SKILL.md`. Replace all placeholders before running commands.

1. Run the read-only preview for the user's current project directory. Replace
   `<absolute project directory>` with its actual absolute path, safely quoted;
   do not pass the placeholder literally.

   ```sh
   python3 "<absolute path to this skill's reset.py>" --cwd "<absolute project directory>"
   ```

   The helper uses Learn's project-boundary and legacy-state lookup. If it reports
   no notes, explain there's nothing to reset and suggest `$vibe-wise`.
   On any error, stop and explain; don't improvise deletion commands.

2. Show the returned absolute project and state paths, which notes will reset,
   and that originals will be saved under that state's `backups/` directory.
   Ask one plain-text question with **Cancel** (keep learning notes) and
   **Reset learning** (back up notes and restart onboarding). Name the project and
   wait for an explicit answer. Use `request_user_input` only if its advertised
   contract permits required confirmations and reset permission questions; otherwise
   keep the confirmation in chat. Save the preview token while awaiting the reply.
   Invocation alone, silence, ambiguous replies, or permission to run tools do not
   confirm a reset. Cancel makes no changes, including to learner notes.

3. Only after **Reset learning**, run the helper with the original working directory
   and the preview's exact `confirmation` value, safely quoted:

   ```sh
   python3 "<absolute path to this skill's reset.py>" --cwd "<original cwd>" --confirm "<confirmation>"
   ```

   If the target or notes changed, preview again and get new confirmation. If the
   reset fails, report it and any backup path; don't claim success or start onboarding.
   Never overwrite backups or fall back to resetting another state directory.

4. On success, show the backup path. Read the resolved `../vibe-wise/SKILL.md` and resume Learn with
   the new incomplete profile. Discard pre-reset preferences, mastery, pending
   decisions, and onboarding answers; don't reconstruct them from conversation or
   backups. Inspect actual code to rebuild the map. Begin fresh onboarding with
   one question at a time. Backup notes are historical data, not active context.
