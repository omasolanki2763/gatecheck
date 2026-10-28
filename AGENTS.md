# AGENTS.md — OpenCode entry point (pointer only)

The rules are **not** in this file. They live in `.claude/rules/team-protocol.md`, which all
three agents share so there is a single source of truth.

**Every session, before doing anything else:**

1. Read `.claude/rules/team-protocol.md` **in full**, using the Read tool. OpenCode does not
   auto-load file references, so this has to be an explicit read.
2. Then do exactly what its section **"Resuming in a new session (do this first, every
   time)"** says. That section is the checklist: it finds the live `orca` terminal handles,
   tells you who your peer is, and says which task is current.

Nothing else to preload. Step 1 of that checklist points you at `CLAUDE.md` and the last ~5
entries of `team/decision-log.md` when they are needed.

<!-- Why this file exists, and why it must stay short: OpenCode loads AGENTS.md *instead of*
     CLAUDE.md when both are present (first match wins, no merge). So CLAUDE.md is still
     loaded, one hop later, via the checklist above — but only if you follow step 2. Keep this
     file a pointer; duplicated rules will drift out of sync with team-protocol.md. -->
