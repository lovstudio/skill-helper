# lovstudio-skill-helper

CLI helper for Lovstudio license keys — activate a license on this machine,
bind it to your Lovstudio account, and call cloud-split Skill handlers.

Paid Lovstudio Skills are no longer encrypted. Owning a Skill (a Credits
purchase or an activated license bound to your account) only controls whether
you can download it; `npx lovstudio skills add <name>` checks that on
lovstudio.ai and installs the Skill as plain files.

## Install

The canonical way is via [`uv`](https://docs.astral.sh/uv/) — no install step needed, runs on first use:

```bash
uvx lovstudio-skill-helper login
```

Or install it persistently:

```bash
pipx install lovstudio-skill-helper
```

## Usage

```bash
# account login (the npm CLI can start this flow automatically)
lovstudio-skill-helper login

# activate a license key once per device; it is bound to the signed-in account
lovstudio-skill-helper activate <license-key>

lovstudio-skill-helper status           # show current activation
lovstudio-skill-helper heartbeat        # refresh last-seen and entitled Skills
lovstudio-skill-helper deactivate       # wipe local license

# invoke a cloud-split Skill's server-side handler
lovstudio-skill-helper call <skill-name> --op <operation> --input '{"key": "value"}'
```

After activation, install paid Skills with `npx lovstudio skills add <name>`.
Versions before 0.10.0 also decrypted encrypted Skill bundles; reinstalling a
paid Skill with the command above replaces an old encrypted install.

License keys are sold via the 手工川 (ShougongChuan) WeChat official account.

## License

MIT.
