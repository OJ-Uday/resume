const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat,
  ExternalHyperlink, TabStopType, TabStopPosition, BorderStyle,
} = require("docx");

// ── palette / metrics ────────────────────────────────────────────────────
const FONT = "Calibri";
const BODY = 20;      // 10pt (half-points)
const SMALL = 19;     // 9.5pt
const NAME = 31;      // 16.5pt
const HEAD = 21;      // 10.5pt
const ACCENT = "1F4E79";

const sectionHeading = (text) =>
  new Paragraph({
    spacing: { before: 70, after: 30 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACCENT, space: 2 } },
    children: [new TextRun({ text, bold: true, size: HEAD, color: ACCENT, font: FONT, allCaps: true })],
  });

const roleLine = (title, org, date) =>
  new Paragraph({
    spacing: { before: 40, after: 12 },
    tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
    children: [
      new TextRun({ text: title, bold: true, size: BODY, font: FONT }),
      new TextRun({ text: ` — ${org}`, size: BODY, font: FONT }),
      new TextRun({ text: `\t${date}`, bold: true, size: SMALL, font: FONT }),
    ],
  });

// runs: array of {text, bold?} — real w:numPr bullets, never unicode chars
const bullet = (runs) =>
  new Paragraph({
    numbering: { reference: "b", level: 0 },
    spacing: { after: 10 },
    children: runs.map((r) => new TextRun({ font: FONT, size: BODY, ...r })),
  });

const link = (text, url) =>
  new ExternalHyperlink({
    children: [new TextRun({ text, style: "Hyperlink", size: SMALL, font: FONT })],
    link: url,
  });

const skills = (label, items) =>
  new Paragraph({
    spacing: { after: 12 },
    children: [
      new TextRun({ text: `${label}: `, bold: true, size: BODY, font: FONT }),
      new TextRun({ text: items, size: BODY, font: FONT }),
    ],
  });

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: BODY } } } },
  numbering: {
    config: [{
      reference: "b",
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 260, hanging: 160 } } },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 560, right: 700, bottom: 420, left: 700 },
      },
    },
    children: [
      // ── header (in BODY — Workday-class parsers skip real headers/footers)
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 20 },
        children: [new TextRun({ text: "UDAY OJHA", bold: true, size: NAME, font: FONT, color: ACCENT })],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 2 },
        children: [
          new TextRun({ text: "Chandigarh, India  |  +91 8360493330  |  ", size: SMALL, font: FONT }),
          link("udayojha129@gmail.com", "mailto:udayojha129@gmail.com"),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 40 },
        children: [
          link("oj-uday.github.io", "https://oj-uday.github.io/"),
          new TextRun({ text: "  |  ", size: SMALL, font: FONT }),
          link("github.com/OJ-Uday", "https://github.com/OJ-Uday"),
          new TextRun({ text: "  |  ", size: SMALL, font: FONT }),
          link("linkedin.com/in/uday-o", "https://www.linkedin.com/in/uday-o/"),
        ],
      }),

      // ── summary ────────────────────────────────────────────────────────
      sectionHeading("Summary"),
      new Paragraph({
        spacing: { after: 20 },
        children: [new TextRun({
          font: FONT, size: BODY,
          text: "Software engineer (B.Tech CS ’26). At Eli Lilly, designed and shipped a production telemetry platform end-to-end — TypeScript browser SDK, Go + ClickHouse analytics backend, React dashboard, zero-touch Kubernetes/GitOps delivery. Independently authored vetlock, an open-source npm supply-chain scanner (17 detectors, 375 tests, 12/13 historical attacks caught, 31 red-team exploits closed) with a live browser demo on Cloudflare Workers + GitHub Actions. CTF reverse-engineering lead; two prior cybersecurity internships.",
        })],
      }),

      // ── skills ─────────────────────────────────────────────────────────
      sectionHeading("Technical Skills"),
      skills("Languages", "TypeScript, JavaScript, Go (Golang), Python, Java, C, C#, SQL, Bash"),
      skills("Backend & Data", "Node.js, REST APIs, microservices, event pipelines, ClickHouse, MySQL, PL/SQL"),
      skills("Frontend", "React, micro-frontends (Module Federation), Jest, React Testing Library, HTML, CSS"),
      skills("Cloud & DevOps", "AWS, Kubernetes, Docker, GitOps (Argo CD), GitHub Actions, Cloudflare Workers, CI/CD, Git, npm"),
      skills("Security", "SAST, supply-chain security, static analysis, AST parsing (Babel), lockfile analysis, Ghidra, IDA Pro, GDB, x86/ARM Assembly, Wazuh (SIEM), Burp Suite, Nmap, Wireshark, penetration testing"),

      // ── experience ─────────────────────────────────────────────────────
      sectionHeading("Experience"),
      roleLine("Software Engineering Intern", "Eli Lilly and Company — Bangalore, India (On-site)", "Jan 2026 – Jul 2026"),
      bullet([{ text: "Designed and shipped an end-to-end product-telemetry platform — TypeScript browser SDK, Go + ClickHouse backend, React dashboard — adopted across a federated micro-frontend estate of 5+ internal applications." }]),
      bullet([{ text: "Invented a two-tier UI element-identity scheme and capture-time causality protocol powering an inference engine that auto-names UI elements for one-click approval; new apps onboard with two HTML attributes, zero code changes." }]),
      bullet([{ text: "Built a release-audit service in Go on ClickHouse (append-only deploy ledger + before/after behavior diffs), backtested over 1,648 deploys / 90 days; its first live run flagged a same-day API regression (53% error rate) with session-level evidence." }]),
      bullet([{ text: "Automated develop→Kubernetes delivery with GitHub Actions + GitOps (CI-authored image bumps, programmatic approval, merge queue), cutting deploy lead time from ~1 day of manual coordination to under 15 minutes with zero human steps." }]),
      bullet([{ text: "Root-caused a React render loop that was OOM-killing CI runners — took a 962-test suite from 60+ min to 35 s; published the SDK to a private npm registry with semantic versioning and property-based tests." }]),
      bullet([{ text: "Worked in an AI-augmented workflow (LLM pair-programming, multi-agent orchestration), landing 25+ production pull requests across SDK, backend, and dashboard in the final two weeks." }]),

      roleLine("Cybersecurity Intern", "CyberRange (Remote)", "Jul 2024 – Nov 2024"),
      bullet([{ text: "Tested and hardened penetration-testing challenges for a security-training platform; performed reconnaissance, mobile-security, and vulnerability analysis across the challenge pipeline." }]),

      roleLine("Cybersecurity Intern", "PGI-Data (Jakarta, Indonesia)", "May 2024 – Jul 2024"),
      bullet([{ text: "Deployed Wazuh SIEM on production servers for threat detection; implemented ZTNA (Zero Trust Network Access), VPN, and PAM (Privileged Access Management) solutions." }]),

      roleLine("Head of Reverse Engineering", "Cryptonite, MIT Manipal CTF Team", "Nov 2022 – Present"),
      bullet([{ text: "Lead the reverse-engineering division — training, research, and strategy across x86/ARM binary analysis and vulnerability research — competing in national and international CTFs." }]),

      // ── projects ───────────────────────────────────────────────────────
      sectionHeading("Projects"),
      bullet([
        { text: "vetlock", bold: true },
        { text: " (TypeScript / Node, github.com/OJ-Uday/vetlock, Apache-2.0) — open-source npm supply-chain scanner: behavioral diff between two lockfiles, static analysis over extracted tarballs, 17 detectors (install-script injection, env-token harvest, exfil endpoints, obfuscation jumps, typosquat detection, GHSA correlation). Ships CLI, GitHub Action (SARIF), and a live in-browser demo backed by Cloudflare Workers + GitHub Actions. 375 tests; caught 12 of 13 real historical npm attacks; closed 31 of 35 exploits from a six-agent adversarial red-team review. NEVER-EXECUTE canary invariant." },
      ]),
      bullet([
        { text: "telemetry-sdk-patterns", bold: true },
        { text: " (TypeScript, github.com/OJ-Uday/telemetry-sdk-patterns) — zero-dependency browser-telemetry SDK: batching queue with retry/beacon drain, micro-frontend event bridge, pluggable MSAL-style auth adapter, delegated auto-capture; 24 tests, matrix CI, live demo." },
      ]),
      bullet([
        { text: "ratelimit", bold: true },
        { text: " (Go, github.com/OJ-Uday/ratelimit) — goroutine-safe token-bucket and sliding-window rate limiters: stdlib-only, zero background goroutines, injectable clocks, net/http middleware; 0 allocs/op on the hot path." },
      ]),
      bullet([
        { text: "react-hooks-kit", bold: true },
        { text: " (React + TypeScript, github.com/OJ-Uday/react-hooks-kit) — five strictly-typed hooks: cross-tab localStorage sync, churn-free event listeners, undo/redo with history forking, debounced values; 13 tests." },
      ]),
      bullet([
        { text: "NiteCTF Challenge Author", bold: true },
        { text: " (Reverse Engineering) — authored challenges for an international CTF: .NET + SQLCipher database forensics, a PIE binary requiring Z3 SMT solving, and a custom AES-XTS cipher in Go." },
      ]),

      // ── education ──────────────────────────────────────────────────────
      sectionHeading("Education"),
      roleLine("B.Tech, Computer Science and Engineering", "Manipal Institute of Technology", "2022 – 2026"),
      new Paragraph({
        spacing: { after: 0 },
        indent: { left: 260 },
        children: [new TextRun({
          font: FONT, size: SMALL,
          text: "CGPA 7.81/10 · Coursework: Algorithms, Data Structures, Operating Systems, Computer Networks, OOP",
        })],
      }),
    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("Uday_Ojha_Resume.docx", buf);
  console.log("written", buf.length, "bytes");
});
