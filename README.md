# atai CLI skill for Claude

A Claude skill that lets anyone, including non-technical users, launch and
manage the Archetype AI platform in their own cloud account by asking Claude in
plain English. Claude runs the `atai` CLI for you, checks readiness first, shows
what a change will do, and asks before creating or deleting anything.

The skill contains only instructions for Claude. It needs the `atai` CLI, which
your Archetype AI contact provides along with a signed download link.

## Install

**Claude Code** (CLI or desktop app):

```
/plugin marketplace add archetypeai/atai-cli-skill
/plugin install atai-cli@atai-cli-skill
```

or from a terminal:

```bash
claude plugin marketplace add archetypeai/atai-cli-skill
claude plugin install atai-cli@atai-cli-skill
```

**Claude.ai or Claude Desktop:** download this repository, zip the
`plugins/atai-cli/skills/atai-cli` folder, and upload it as a custom skill in
Claude's settings. On Team and Enterprise plans an admin can enable it for the
whole organization.

## Verify it's installed

In Claude Code, run `/plugin` and check that **atai CLI operator** is listed and
enabled. That's all — the skill turns on automatically when you ask Claude about
your platform, and there's no restart.

## Update

```bash
claude plugin marketplace update atai-cli-skill
claude plugin update atai-cli@atai-cli-skill
```

## Use

The first time you ask Claude to work with your platform, it offers to set up the
`atai` CLI for you — downloading it from the secure link your Archetype AI contact
gave you — before doing anything else. That's expected. After that, just ask in
plain English: Claude checks readiness first, shows what a change will do, and
asks before it creates or deletes anything.

Ask Claude, for example:

- "Set up the atai CLI on my machine."
- "Is our production stack healthy?"
- "Preview what launching `stacks/demo/config.toml` would create."
- "Upgrade the staging stack to the latest version."
- "Tear down the test stack I made yesterday."

## Support and security

For help, contact your Archetype AI representative. To report a security issue,
see [SECURITY.md](SECURITY.md).

## License

Licensed under the [Apache License 2.0](LICENSE).
