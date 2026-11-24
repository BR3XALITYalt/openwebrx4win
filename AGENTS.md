# Repository instructions

## Writing standard

Apply these rules to the README, developer documentation, design notes, code comments, docstrings, CLI help, dialogs, notifications, logs shown to users, desktop controls, and browser controls.

### General copy

- State the action, fact, result, or limitation directly. Use concrete nouns and specific verbs.
- Remove filler introductions, canned summaries, empty praise, unsupported claims, and sentences that only announce the next section.
- Avoid formulaic contrasts, forced groups of three, slogan-like endings, rhetorical questions, dramatic fragments, and repeated sentence patterns.
- Use active voice when it identifies the actor. Use passive voice when the actor is unknown or does not matter.
- Remove vague terms such as "high quality", "robust", "seamless", and "intuitive" unless a relevant measure explains the claim.
- Keep every claim verifiable. State supported formats, frequency ranges, defaults, limits, and prerequisites instead of promising untested behavior.
- Distinguish audio-source choices from concurrent streams. Multiple input options do not mean that MultiV mixes or transmits several sources at once.
- Distinguish a working simulator backend from one under development. Do not claim concurrent connections or multiple destinations until the code supports and tests them.
- Vary sentence structure naturally. Do not force a tone, sentence length, or checklist score to make prose appear human.
- Do not mention AI, language models, prompts, or the writing process in user-facing content.

### Documentation

- Organize user instructions around tasks: prerequisites, steps, expected result, and relevant limits.
- Keep [README.md](README.md) as the user-facing entry page. It should cover installation, first use, core controls, important limitations, and safety-critical warnings without becoming a full technical manual.
- Put detailed user reference material in [wiki/](wiki/Home.md): mode parameters and transport behavior, audio-format exceptions, encoder prerequisites, browser-panel configuration, storage paths, and command-line options.
- Keep architecture, internal module notes, unfinished implementation details, and test commands in [DEVELOPMENT.md](DEVELOPMENT.md). Do not put these details in the user-facing README.
- Keep [ROADMAP.md](ROADMAP.md) limited to concise provider and feature status. Link to the reference pages for technical explanations.
- Use runnable examples. Match the actual command, option, path, control label, unit, and supported format.
- Describe current behavior. Label experimental features and unverified signal paths. Do not present planned or partial work as usable.
- Include implementation history only when it explains a current compatibility requirement.
- Preserve third-party license and attribution notices beside the code or components they cover.

### Interface copy

- Use the same name for each control and feature in the app and its documentation.
- Use sentence case and short, specific labels. Name the action on buttons, such as "Start transmission" or "Save station profile".
- Report only the state the app has reached. Do not report a connection, save, upload, or transmission as successful before it succeeds.
- For errors, name the failed operation and give the next useful action when one exists.
- Put explanations beside the controls they describe. Keep release notes, developer instructions, and implementation details out of the UI.
- Write from the user's point of view. Refer to controls by their visible labels, not by their widget or component type.

### Code comments and docstrings

- Explain non-obvious intent: protocol requirements, invariants, units, lifecycle rules, concurrency constraints, or the reason for a workaround.
- Do not narrate obvious control flow or restate the next line of code.
- Document a function's contract: return value, important inputs or units, side effects, and relevant errors when the signature does not make them clear.
- Keep comments accurate as code changes. Remove comments about deleted behavior, old implementations, or development history.
- Preserve required license and SPDX notices.

### Code quality

- Optimize for correctness, readability, and straightforward control flow. Remove complexity only when behavior stays the same.
- Avoid abstractions for one-off cases, speculative frameworks, unnecessary dependencies, dead code, and compatibility branches without a supported use case.
- Add or update tests for changed behavior, especially error paths and boundary conditions.
- Review changes for correctness, readability, architecture, security, and performance.
- Do not claim that tests, builds, receiver checks, or GUI launches passed unless they ran and passed.

## Source guidelines

These sources informed the repository rules. Apply the relevant principles to MultiV's stack rather than copying general advice mechanically.

- [Stop Slop by Hardik Pandya](https://github.com/hardikpandya/stop-slop) (MIT): remove filler, vague claims, canned structures, and artificial prose patterns.
- [Writing a good CLAUDE.md, HumanLayer](https://www.humanlayer.dev/blog/writing-a-good-claude-md): keep agent instructions concise and link to task-specific documentation.
- [GitHub: How to write a great AGENTS.md](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/): provide project context, commands, tests, examples, and boundaries.
- [Anthropic: Best practices for Claude Code](https://code.claude.com/docs/en/best-practices): give agents useful repository context and concrete constraints.
- [Addy Osmani: Agentic Code Quality](https://addyosmani.com/blog/agentic-code-quality/): review correctness, readability, architecture, security, performance, and maintainability.
- [Addy Osmani's Code Review and Quality skill](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): avoid unnecessary abstractions and review the changed code.
- [Google Material communication principles](https://codelabs.developers.google.com/codelabs/material-communication-guidance): keep interface copy direct and limited to the information needed for the current task.
- [W3C Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/): check text alternatives, keyboard operation, focus, and contrast.

## Windows port scope

This repository is a platform-compatibility port of upstream OpenWebRX+. Preserve upstream receiver behavior, web interface, settings, configuration semantics, decoders, and supported SDR types.

- Change code only where required for Windows compatibility or to test that compatibility.
- Do not add application features, receiver features, decoders, plugins, custom desktop interfaces, or interface redesigns.
- Do not remove existing functionality to make a Windows build pass. Record unsupported dependencies and port them.
- Keep Linux behavior and defaults unchanged.
- Do not use WSL2, Docker, virtual machines, or an embedded Linux installation as the Windows runtime.
- Keep platform-specific code isolated where practical and test Windows changes on Windows as well as Linux regression behavior.
