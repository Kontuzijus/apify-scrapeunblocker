<!-- HQ-SESSION-GUARD v1 (managed from ScrapeUnblocker/headquarters - do not remove) -->
# HQ SESSION GUARD (Claude - MANDATORY, READ FIRST)

This repo is part of the ScrapeUnblocker ecosystem. All development on it is governed by the central
`headquarters` repo (`ScrapeUnblocker/headquarters`) - its CLAUDE.md carries the global rules
(branch/push policy, lint gates, credentials handling, worklog, deploy runbooks).

- **If the headquarters CLAUDE.md IS loaded in your context** (the session was started from the local
  `headquarters` folder - you can see its "ScrapeUnblocker - Valdymo pultas (Headquarters)" instructions),
  this guard is satisfied: work normally under those rules.
- **If it is NOT loaded** (Claude was launched directly in this repo or anywhere else): treat this repo as
  **READ-ONLY**. Do NOT edit files, do NOT commit, do NOT push, do NOT create branches or tags, and do NOT
  run deploys from here. Tell the developer: ScrapeUnblocker development sessions must be started from the
  local `headquarters` folder (clone of `ScrapeUnblocker/headquarters`) so the global rules load - then stop.
- Reading, searching, running read-only commands and explaining code is always allowed.
- **Exemption:** sanctioned headless server agents (self-heal / scout / parts-monitor / no-code crawler etc.
  running on our servers) follow their own playbooks and are NOT bound by this guard.

---

## ⚠️ BUMPING `version` DROPS ENV VARS - RE-ADD `SCRAPEUNBLOCKER_KEY` OR THE ACTOR DIES (Claude - MANDATORY)

Apify stores environment variables **per actor VERSION**, and they are baked into the image **at build
time** (a run of an already-built image does NOT pick up a newly added env var - a rebuild is required).
`src/main.py` reads `os.environ["SCRAPEUNBLOCKER_KEY"]` at startup, so if that var is missing the actor
raises `KeyError: 'SCRAPEUNBLOCKER_KEY'` and **every run fails before any API call** (run status FAILED,
exit code 91).

**The trap:** when you change `version` in `.actor/actor.json` and push, Apify creates a **brand-new version
WITHOUT the env vars** from the previous version. The new build becomes `latest`, and the whole actor goes
to ~0% success for everyone (with a country selected or not - the country code is never reached). This is
exactly what happened on 2026-08-28 (v1.5 -> v1.6 for the `proxy_country` feature): 690/694 runs failed the
next day until the env var was restored.

**Rules:**
1. **Prefer NOT bumping `version`** when you only change code - let Apify rebuild the same version, which
   keeps its env vars.
2. **If you DO bump `version`** (or create a version any other way): before treating the deploy as done,
   **verify `SCRAPEUNBLOCKER_KEY` exists on the new version and REBUILD** so the image actually contains it.
   The key value lives in headquarters `credentials.local.md` as `SU_API_KEY_APIFY` (account
   `apify` traffic) - never hardcode it, never commit it.
3. **Env var field name is `name`, not `key`** (Apify API `PUT /v2/acts/<actor>/versions/<v>` with
   `envVars:[{name, value, isSecret:true}]`); a secret's stored value is not readable back (only `valueHash`).
4. **Always confirm with a real run after a version/build change** - trigger one run (with and without
   `proxy_country`) and check status SUCCEEDED / exitCode 0 before calling it fixed.
