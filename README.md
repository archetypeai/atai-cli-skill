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

## Update

```bash
claude plugin marketplace update atai-cli-skill
claude plugin update atai-cli@atai-cli-skill
```

## Use

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
