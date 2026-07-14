<!--
UDAY OJHA — resume content

Edit this file from the GitHub mobile app.
Every commit rebuilds Uday_Ojha_Resume.pdf + .docx and posts to
github.com/OJ-Uday/uday-docs/releases/latest within ~2 minutes.

Schema (obvious once you see it):

  # NAME              — one-line H1 at the top
  contact-line        — pipe-separated line under name; supports [text](url)
  ## Section          — section heading (uppercased in output)
  ### Role — Org · Date
                      — a job / education entry header
    - a bullet under that role
    - another bullet
  - Label: value      — a skills-line if it is under "## Technical Skills"
  **bold text**       — inside any line for emphasis

Anything inside a HTML comment block is ignored by the generator.
-->

# UDAY OJHA

Chandigarh, India | +91 8360493330 | [udayojha129@gmail.com](mailto:udayojha129@gmail.com) | [oj-uday.github.io](https://oj-uday.github.io/) | [github.com/OJ-Uday](https://github.com/OJ-Uday) | [linkedin.com/in/uday-o](https://www.linkedin.com/in/uday-o/)

## Summary

Software engineer (B.Tech CS '26). At Eli Lilly, designed and shipped a production telemetry platform end-to-end — TypeScript browser SDK, Go + ClickHouse analytics backend, React dashboard, zero-touch Kubernetes/GitOps delivery. Independently authored vetlock, an open-source npm supply-chain scanner (17 detectors, 375 tests, 12/13 historical attacks caught) with a live browser demo on Cloudflare Workers + GitHub Actions. CTF reverse-engineering lead; two prior cybersecurity internships.

## Technical Skills

- Languages: TypeScript, JavaScript, Go (Golang), Python, Java, C, C#, SQL, Bash
- Backend & Data: Node.js, REST APIs, microservices, event pipelines, ClickHouse, MySQL, PL/SQL
- Frontend: React, micro-frontends (Module Federation), Jest, React Testing Library, HTML, CSS
- Cloud & DevOps: AWS, Kubernetes, Docker, GitOps (Argo CD), GitHub Actions, Cloudflare Workers, CI/CD, Git, npm
- Security: SAST, supply-chain security, static analysis, AST parsing (Babel), lockfile analysis, Ghidra, IDA Pro, GDB, x86/ARM Assembly, Wazuh (SIEM), Burp Suite, Nmap, Wireshark, penetration testing

## Experience

### Software Engineering Intern — Eli Lilly and Company — Bangalore, India (On-site) · Jan 2026 – Jul 2026

- Designed and shipped an end-to-end product-telemetry platform — TypeScript browser SDK, Go + ClickHouse backend, React dashboard — adopted across a federated micro-frontend estate of 5+ internal applications.
- Invented a two-tier UI element-identity scheme and capture-time causality protocol powering an inference engine that auto-names UI elements for one-click approval; new apps onboard with two HTML attributes, zero code changes.
- Built a release-audit service in Go on ClickHouse (append-only deploy ledger + before/after behavior diffs), backtested over 1,648 deploys / 90 days; its first live run flagged a same-day API regression (53% error rate) with session-level evidence.
- Automated develop→Kubernetes delivery with GitHub Actions + GitOps (CI-authored image bumps, programmatic approval, merge queue), cutting deploy lead time from ~1 day of manual coordination to under 15 minutes with zero human steps.
- Worked in an AI-augmented workflow (LLM pair-programming, multi-agent orchestration), landing 25+ production pull requests across SDK, backend, and dashboard in the final two weeks.

### Cybersecurity Intern — CyberRange (Remote) · Jul 2024 – Nov 2024

- Tested and hardened penetration-testing challenges for a security-training platform; performed reconnaissance, mobile-security, and vulnerability analysis across the challenge pipeline.

### Cybersecurity Intern — PGI-Data (Jakarta, Indonesia) · May 2024 – Jul 2024

- Deployed Wazuh SIEM on production servers for threat detection; implemented ZTNA (Zero Trust Network Access), VPN, and PAM (Privileged Access Management) solutions.

### Head of Reverse Engineering — Cryptonite, MIT Manipal CTF Team · Nov 2022 – Present

- Lead the reverse-engineering division — training, research, and strategy across x86/ARM binary analysis and vulnerability research — competing in national and international CTFs.

## Projects

- **vetlock** (TypeScript / Node, github.com/OJ-Uday/vetlock, Apache-2.0) — open-source npm supply-chain scanner: behavioral diff between two lockfiles, static analysis over extracted tarballs, 17 detectors (install-script injection, env-token harvest, exfil endpoints, obfuscation jumps, typosquat detection, GHSA correlation). Ships CLI, GitHub Action (SARIF), and a live in-browser demo backed by Cloudflare Workers + GitHub Actions. 375 tests; caught 12 of 13 real historical npm attacks.
- **docsforge** (GitHub Actions / Node / Python, github.com/OJ-Uday/docsforge, MIT) — reusable GitHub Actions workflow that auto-builds documents (LaTeX, Word-via-docx, Markdown-via-pandoc) on every push and publishes to a rolling GitHub Release. Discovers a .docmeta.yml in each doc folder, dispatches by builder type, runs the matrix in parallel, auto-heals lockfiles that point at private registries. Consumed by my own docs hub; anyone can adopt it in three lines of YAML.
- **telemetry-sdk-patterns** (TypeScript, github.com/OJ-Uday/telemetry-sdk-patterns) — zero-dependency browser-telemetry SDK: batching queue with retry/beacon drain, micro-frontend event bridge, pluggable MSAL-style auth adapter, delegated auto-capture; 24 tests, matrix CI, live demo.
- **ratelimit** (Go, github.com/OJ-Uday/ratelimit) — goroutine-safe token-bucket and sliding-window rate limiters: stdlib-only, zero background goroutines, injectable clocks, net/http middleware; 0 allocs/op on the hot path.
- **react-hooks-kit** (React + TypeScript, github.com/OJ-Uday/react-hooks-kit) — five strictly-typed hooks: cross-tab localStorage sync, churn-free event listeners, undo/redo with history forking, debounced values; 13 tests.
- **NiteCTF Challenge Author** (Reverse Engineering) — authored challenges for an international CTF: .NET + SQLCipher database forensics, a PIE binary requiring Z3 SMT solving, and a custom AES-XTS cipher in Go.

## Education

### B.Tech, Computer Science and Engineering — Manipal Institute of Technology · 2022 – 2026

- CGPA 7.81/10 · Coursework: Algorithms, Data Structures, Operating Systems, Computer Networks, OOP
