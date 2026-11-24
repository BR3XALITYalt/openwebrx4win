# Repository instructions

## Project

MultiV is a multi-source, multi-stream client for virtual radio simulators. The desktop app uses Tkinter and accepts microphone, desktop-audio, and playlist input. See [ROADMAP.md](ROADMAP.md) for provider support and integration status. `web_gui.py` serves a password-protected control panel on the local network.

Call the application **MultiV**. Use **TXITY** for the service, website, station directory, and remote protocol.

## Product behavior

- MultiV is a provider-agnostic, multi-broadcast system. It is not exclusive to TXITY; treat TXITY as one output provider alongside Icecast and other supported providers.
- Output providers must operate independently. Each output has its own enable/disable control, and disabling or disconnecting one provider must not disable, block, or otherwise affect other enabled providers.
- Route the selected audio source to every enabled output concurrently. Do not make Icecast transmission depend on a TXITY connection or authentication session, or make TXITY transmission depend on Icecast availability.
- Keep provider-specific configuration and connection state separate. Shared audio capture may feed multiple outputs, but each output's lifecycle and failure handling must remain isolated.
- In the Transmit page, present TXITY and Icecast as separate collapsible output rows. Each row has an independent enable toggle and a draggable handle for pointer-based reordering. Support Up and Down keys when the handle has focus. Persist the enabled state and order.
- Remove Stations from the main navigation. Put Station directory in the TXITY menu and open it in a separate window containing the searchable live station list. Station details must provide a route back to that window.

## Before editing

- Read [DESIGN.md](DESIGN.md) before changing either interface.
- Read [PRODUCT.md](PRODUCT.md) before changing product positioning or marketing copy.
- Use [ROADMAP.md](ROADMAP.md) as the source of truth for provider support. Do not maintain separate provider lists.
- Inspect the relevant implementation and nearby tests before changing behavior.
- Keep changes within the requested scope. Do not replace working code to impose a personal style.
- After Python changes, run `python -m compileall -q .` and `python -m unittest discover -s tests -v`.
- When a runtime is available, launch the interface you changed. Passing tests do not prove that a GUI works.

## Interface rules

- Use ttkbootstrap for standard interface widgets and its themed Tk equivalents for the scroll canvas, listboxes, multiline text editor, menus, and secondary windows. Keep the existing Sun Valley-compatible light/dark color values in the custom MultiV themes. Use classic Tk widgets only where ttkbootstrap has no compatible equivalent.
- Keep the browser panel consistent with its current layout. Add gradients, animation, activity indicators, or panels only when they serve a documented purpose.
- Follow the ENERGY, RHYTHM, and MOTION dials in [DESIGN.md](DESIGN.md). Record the reason for any major visual change.
- Make controls keyboard-accessible. Give each input a visible label, keep focus visible, and maintain readable contrast. Do not use color as the only status indicator.
- Use semantic HTML and native controls in the browser panel. Expose status changes through accessible status regions.

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
