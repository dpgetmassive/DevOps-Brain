---
description: Git and SSH configuration rules for this repository
globs:
alwaysApply: true
---

# Git & SSH Rules for DevOps Brain

## SSH Key Policy

**Always use the `getmassive` SSH key (`id_ed25519_dpgetmassive`) for this repository.**

- Remote: `git@github.com:dpgetmassive/DevOps-Brain.git`
- The `github.com` host maps to the `getmassive` key via `~/.ssh/config`
- Do NOT use the `github-cyberpeople` SSH alias or the `id_ed25519_cyberpeople` key for this repo
- If a push fails with "Repository not found" or permission denied, do NOT switch to the cyberpeople key -- escalate to the user instead

## Git Conventions

- Default branch: `main`
- Commit style: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`)
- No force pushes to `main`
- Do not modify git config (user.name, user.email)
