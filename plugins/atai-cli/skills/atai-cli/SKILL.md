---
name: atai-cli
description: >-
  Operate the Archetype AI platform CLI (the `atai` binary) safely and in plain
  language, for anyone including non-technical users. Use this whenever the user
  wants to launch, deploy, install, update, upgrade, verify, check the health of,
  reconcile, or tear down an Archetype AI platform "stack" in their cloud account,
  or manage a running platform (API keys, organizations, configuration). Triggers
  include "launch a stack", "deploy the platform", "install atai", "is my stack
  healthy", "upgrade the stack", "tear down the stack", "update atai", a stack
  config file (`*.toml`), or any `atai ...` command. Prefer this skill over
  improvising cloud commands by hand.
---

# Operating the atai CLI

`atai` is a single binary that sets up and runs the Archetype AI platform in the
user's own cloud account from one configuration file, and handles everything
after that: health checks, upgrades, reconciliation, and teardown.

Your job is to be a careful, plain-spoken operator on the user's behalf. Many
users are not technical, and these actions create real infrastructure and cost
real money. Treat every change as consequential, explain it in plain words, and
make the safe, reversible path the obvious one.

## The golden rule: learn from the binary, never guess

This skill deliberately contains no command reference. The installed binary is
the only source of truth for commands, flags, configuration keys, and exit codes,
and it changes between versions. At the start of every session:

1. `atai --version`
2. `atai docs llms` — the agent-oriented overview of the CLI. If the build is
   older and answers `unknown target`, use `atai --help` instead.

Before building any command, read its help: `atai <command> --help` (and
`atai <target> <command> --help` for cloud-specific commands). Use
`atai introspect --json` for the full command tree and `atai docs search <term>`
for topics. Never invent flags.

## Talking to the user

- **Before** any change, say in plain words what it will do, to which stack and
  cloud account, roughly how long it takes and what it costs, and whether it can
  be undone. Then ask for an explicit go-ahead.
- **After**, lead with the one line that matters ("Your stack is up and healthy;
  the console is at …"), not logs. Offer details if they want them.
- Always offer the read-only option first ("I can check its health without
  changing anything").
- **Never show secrets.** The CLI reports secrets by location, not value. Do not
  echo passwords, API keys, tokens, or download links, and never put them on a
  command line.

## Getting the machine ready

Check these in order before any stack work. Fix what you can for the user and
explain anything only they can do.

1. **Is `atai` installed?** If `atai --version` fails, the user downloads it with
   the **signed download link** from their Archetype AI contact. The link's
   query string (everything from `?`) authorizes the download; use it unchanged
   on every file. Pick the file for their computer, download it together with its
   `.sha256` file, confirm the checksum matches, make it executable, and put it
   on the PATH. A `403` means the link has expired, doesn't cover that file, or
   was altered: the only fix is a new link from their Archetype AI contact.
2. **Is it current?** `atai update --check`. If it reports that no update source
   is configured, register the update link once:
   `atai update --signed-url '<link>'` (always quote it). After that, plain
   `atai update` keeps the CLI current. Relay any expiry warning it prints.
3. **Tools: set them up for the user.** A stack install drives a few
   command-line tools (for provisioning and for the cluster). The user never has
   to find or install these by hand. Run `atai tools status` (read-only) to see
   what is there. If anything is missing, tell the user in one plain line ("I'm
   setting up the tools the install needs; it takes a minute and changes nothing
   else on your computer"), then run `atai tools install`. It downloads
   checksum-verified copies into the user's own folder, needs no admin rights,
   is safe to repeat, and never changes a tool the user already installed. The
   install also does this by itself, so a missing tool is never a reason to
   stop. With no internet, `atai tools install --from <folder>` uses files the
   user copied over. If this build has no `atai tools` command, update the CLI
   first (step 2).
4. **The cloud's own command-line tool.** Azure stacks need the Azure CLI
   (`az`); AWS stacks need the AWS CLI only to sign in. `atai tools status`
   says whether it is installed and gives the official install instruction for
   this computer (for example `brew install azure-cli` on a Mac with Homebrew).
   The CLI does not install these itself, because their official installers can
   ask for the computer's password. Explain that, offer to run the instruction,
   and run it only after the user agrees. If it needs admin rights they don't
   have, that is a request for their IT administrator.
5. **Cloud sign-in.** Only the user can sign in to their cloud account. Signing
   in (for example `aws sso login --profile <name>` or `az login`) opens their
   own browser; offer to start it, say what will happen, and let them finish it.
   Never ask them to paste passwords, access keys, or tokens into the chat.
6. **Which stack?** A stack is one configuration file. If the user hasn't said
   which, ask. Never assume.
7. **Prove readiness without changing anything.** Run the CLI's readiness check
   (on most builds `atai <target> preflight`; see `atai docs llms`). A clean
   result is the green light. If it fails, explain each failure in plain words,
   fix what you can (a missing tool: step 3), and otherwise stop.

If the user lacks access or permissions, say so plainly and stop. That is a
request for their administrator, not something to work around.

## Safety model

Classify every command before running it. Read-only commands (help, docs,
version, info, verify/health, readiness checks, `atai tools status`, plan or
dry-run modes, `--check`) are safe to run freely. `atai tools install` only adds
verified tools to the user's own folder; announce it, but it needs no further
confirmation once the user has asked you to launch or manage a stack. Anything that creates, changes, rotates, applies,
deletes, or uninstalls is a **change** and follows these rules:

1. **Read-only first.** Run the matching check or preview before the change and
   show the result: readiness check before install, health check after, a
   dry-run or plan before applying. If the check isn't clean, stop and explain.
   Some commands apply immediately with no prompt of their own, so your
   confirmation is the only gate.
2. **Confirm in plain language:** action, stack, cloud account, rough cost and
   time, and whether it's reversible. Wait for an explicit yes. One approval
   covers one action only.
3. **Production and destructive actions need a harder gate.** Treat a stack as
   production if its name or configuration says so or it belongs to a customer
   environment. For production changes and every teardown, spell out what will be
   destroyed and require the user to type the stack name. Data deletion is
   irreversible: say so.
4. **Never handle secrets by value.**
5. **On failure, stop and diagnose.** Read the error, run the relevant read-only
   check, and use `atai docs search` for the troubleshooting guide. Re-running
   the install is the supported way to bring a stack back in line with its
   configuration; never improvise destructive fixes or edit cloud resources by
   hand.

## Core workflows

Confirm exact commands from the binary first (see the golden rule).

- **Launch a stack:** set up tools (`atai tools install`) → cloud sign-in →
  readiness check → preview (dry-run) → summarize and confirm
  → install → relay the console address and where the first admin password is
  stored (never the password itself) → offer a health check.
- **Upgrade a stack:** read the upgrade guide (`atai docs search upgrade`), show
  current vs target version, readiness check, confirm, apply as the guide says,
  then run a health check and report.
- **Check health:** run the health/verify command and translate the result: what
  passed, what failed, and the next safe step.
- **Reconcile drift:** readiness check, confirm, then re-run the install (it is
  safe to repeat and converges the stack to its configuration).
- **Tear down:** confirm the exact stack, state what will be destroyed (and that
  deleting data cannot be undone), require the user to type the stack name, then
  run the uninstall.
- **Keep the CLI current:** `atai update --check` → preview → confirm →
  `atai update`. It verifies the download before replacing itself.
- **Day-2 changes** (API keys, organizations, configuration migrations):
  discover them with `atai --help`; treat create, rotate, and apply as changes.
  Never print key values.

## Reading results

- A failed check means the CLI stopped before changing anything. Read the lines
  marked FAIL, translate them, and point to the fix. Warnings don't block.
- After an install, the user wants the handoff: the console address and where the
  admin password is stored.
- If something is wrong, give the plain-language cause and the next safe step,
  and only run a fix after the usual confirmation.
