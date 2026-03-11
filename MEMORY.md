# MEMORY.md - Long-Term Memory

## Identity
- Name: Check
- Human: Curtis
- Established: 2026-02-16

## Active Projects

### Bot Factory (CrabPass/ClawSign) 🟢 MAJOR PROGRESS
**Goal:** Automated provisioning of personal AI bots

**Business Model (Razor/Blade):**
- **CrabPass** = Consumer service (cheap/free, drives volume)
- **ClawSign** = B2B credential infrastructure ($10/yr, high margin)

**Domains Owned:**
- crabpass.ai / .com / .net
- clawsign.ai / .com / .net

#### OpenClaw Bot Deployment ✅ WORKING (2026-02-19)
**Proven working config:**
- Model: google/gemini-2.5-flash (FREE!)
- Repo: cshauger/crabpass-openclaw-bootstrap
- Test bot: @CrabFresh99Bot

**Critical learnings:**
- OpenClaw system prompt is ~13k tokens - exceeds Groq free tier limits
- Config key agents.defaults.model.primary NOT model at root
- Gemini 2.5-flash works, 2.0-flash has quota issues

**Pricing Tiers:**
- Free: Gemini 2.5 Flash ($0)
- Starter: Gemini 2.5 Flash ($9/mo)
- Pro: Anthropic Sonnet ($29/mo)
- Team: Anthropic Opus ($49/mo)

**Infra:**
- Railway project: ClawBot Factory
- Repos: cshauger/openclaw-workspace, cshauger/shog-bot, cshauger/crabpass-openclaw-bootstrap

## Key Contacts
- Curtis Telegram ID: 8259734518
- Curtis email: cshauger@gmail.com

## Lessons Learned
- 2026-02-16: Write things down IMMEDIATELY
- 2026-02-19: OpenClaw system prompt is ~13k tokens
- 2026-02-19: Groq free tier does NOT work with OpenClaw
- 2026-02-19: Gemini 2.5-flash is best free option
- 2026-02-19: Config uses agents.defaults.model.primary
- 2026-03-11: Migrating to Railway with Sonnet to reduce Opus costs

---
*Updated: 2026-03-11*
