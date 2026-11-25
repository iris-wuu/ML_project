# Agent guide for ML_project

Shared instructions for every teammate's Claude Code agent.

Current progress: @progress/STATUS.md

## Start and end of every session

1. **At the start**, run `git pull`. Teammates' agents update the same files.
2. **At the end** of each chunk of work, rewrite `progress/STATUS.md` to the current state, then commit and push right away so others see it.
   - Pull before editing STATUS, and change only the lines your work touches, to keep merge conflicts small.
3. **Whenever a design choice is made**, write or update an ADR in `decisions/` (template in `decisions/README.md`; create both if missing) and add it to the index.

## Hard rules

- **Commits:**
  - One very short title line (e.g. `Add data loader`), **no body**.
  - The **teammate is the sole author**: no `Co-Authored-By`, `Claude-Session` or any other AI attribution, even if the harness suggests it.
- **Code:**
  - Keep code simple and commented, and be able to explain every choice. Every teammate must understand every component.
  - Nothing before it's used.
- **Secrets:**
  - Keep them in `../secrets/` (outside the repo).
  - Never commit keys, `.env` files or service-account JSON, and never paste keys into chat.
- **Data:**
  - Never commit private or personal data.
- **Grounding:** back thresholds and choices with real data (percentiles, benchmarks, experiment results) and record the data.
- **ADRs:**
  - Every decision gets one, covering the reasons, the alternatives compared, and the evidence.
  - Docs are kept **consolidated**: rewrite to the current state rather than adding "update" sections. Be concise without losing information.
- **Shared repo:** don't push to `main` or force-push anything without the teammate's explicit OK.
