<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/header-light.svg">
  <img alt="Ahmed Mohamed Ebaid — Cloud Security Engineer" src="assets/header-dark.svg" width="100%">
</picture>

I build systems that can **prove they still work** — hybrid architectures that fail over
without anyone watching, and stores that can walk a chain of records back and say exactly
where trust ends.

B.Sc. in Computational Science and Artificial Intelligence from Zewail City, majoring in
Information Technology with a concentration in Networks, Security and Governance.
Graduated July 2026.

**[Portfolio](https://ahmadebaid001.github.io/personal-portfolio/)** ·
[LinkedIn](https://www.linkedin.com/in/ahmed-ebaid-0xc/) ·
[Résumé](https://github.com/AhmadEbaid001/personal-portfolio/raw/main/Ahmed_Mohamed_Ebaid_Resume.pdf) ·
[ahmedebaid0xc@gmail.com](mailto:ahmedebaid0xc@gmail.com)

---

## What I'm doing now

- Building **AURA** with three teammates — a university registration platform that started
  as our graduation project and is now in a pre-incubation programme.
- Preparing for **AWS Certified Security — Specialty** (SCS-C02).
- Open to cloud security and security engineering roles.

---

## Selected work

### AURA — Academic University Registration Architecture

<sub>Private repository · [see it on the portfolio](https://ahmadebaid001.github.io/personal-portfolio/#aura)</sub>

Multi-tenant SaaS for university registration, scheduling and grading. Four-person team at
Zewail City; nominated for the Medal of Excellence in Entrepreneurship. Runs on a
self-hosted server in Egypt and bursts into Azure only when the on-premises node saturates.

I worked in the application and security layer: registration and semester-period scoping,
the professor dashboard, the grade-change workflow with dean approval, multi-tenant
isolation by `university_id`, and remediation of the critical and high findings from code
scanning.

`React 19` `Node 22` `Express 5` `PostgreSQL 17` `Socket.IO` `Redis` `HAProxy` `Cloudflare` `Azure Container Apps` `WireGuard`

> **5,000** concurrent users sustained · **902,246** requests at 100% success ·
> **299.55 ms** p95 · **$3.50/month** total infrastructure · 13 penetration-test findings
> remediated

### EcoForge GEMP — Green Energy Monitoring Platform

<sub>Private repository · [see it on the portfolio](https://ahmadebaid001.github.io/personal-portfolio/#gemp)</sub>

Budget allocator for public-building retrofits, built for RoboDam 2026. Sole engineer on a
two-person team — domain model, telemetry ingestion, optimisation engine, API and front end.

Every meter reading is HMAC-signed and hash-chained on arrival, with chain heads anchored
outside the database volume, so an altered *or* truncated record is detected. RBAC with an
audit log that records denied actions as well as permitted ones. The CI pipeline blocks on
any finding from Bandit, Semgrep, pip-audit, Gitleaks, Hadolint or Trivy, and every security
exception carries an expiry date that fails the build once it lapses.

`Python` `FastAPI` `Docker` `TimescaleDB` `MQTT` `OR-Tools CP-SAT` `nginx`

> **457** automated tests · **50** buildings allocated · exact solver beats the best
> heuristic by **20%** median under district constraints

### [OtterCTF 2018 — Ransomware Memory Forensics](https://github.com/AhmadEbaid001/OtterCTF2018-Forensics)

Four-phase memory forensics investigation of a Windows 7 host compromised by a
torrent-delivered ransomware payload. I led the engagement: kill chain reconstruction,
MITRE ATT&CK mapping, and the prevention write-up.

`Volatility` `Memory forensics` `MITRE ATT&CK`

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/chain-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/chain-light.svg">
  <img alt="A hash chain of six signed records being verified end to end" src="assets/chain-dark.svg" width="100%">
</picture>

### Also built

| Project | What it is |
|---|---|
| [Secure Communication Protocol](https://github.com/AhmadEbaid001/Secure-Communication-with-RSA-and-Symmetric-Encryption) | RSA-2048 key exchange, AES-GCM authenticated encryption, RSA-PSS signatures, HKDF-SHA256 forward secrecy |
| [Backup &amp; Disaster Recovery Framework](https://github.com/AhmadEbaid001/DR-Framework) | Zero-touch backups at a 24-hour RPO, AES-256 at rest, 148 Mbps with zero packet loss |
| [Enterprise Data Center Network](https://github.com/AhmadEbaid001/Green-Datacenter-Design-Project) | Three-tier design for 600+ users, OSPF, dual-ISP redundancy, VLSM, SNMPv2c |
| [Personal portfolio](https://github.com/AhmadEbaid001/personal-portfolio) | Static single-page site — no framework, no build step, three interactive figures |

---

## Toolbox

| | |
|---|---|
| **Cloud &amp; infrastructure** | AWS (IAM, VPC, Security Groups, Load Balancer) · Azure Container Apps · hybrid cloud · Docker · nginx · HAProxy |
| **DevSecOps** | GitHub Actions security gating · Bandit · Semgrep · pip-audit · Gitleaks · Trivy · Hadolint · container image signing |
| **Security domains** | Vulnerability assessment · incident response · SIEM operations · threat modelling (MITRE ATT&amp;CK, STRIDE, PASTA) · encryption &amp; key management · RBAC · audit logging · data integrity (HMAC, hash chaining) |
| **Security tooling** | Nessus · Splunk · Wireshark · Nmap · Snort · Volatility · Autopsy |
| **Networking** | Network design &amp; installation · firewalls · VLANs · OSPF · VLSM · SNMP · MQTT · WireGuard · CCNA/CCNP track |
| **Languages** | Python (FastAPI, pytest) · JavaScript (React, Node, Express) · Bash · SQL · C++ |
| **Data &amp; platforms** | PostgreSQL · TimescaleDB · Redis · Linux (Ubuntu, Kali) · EVE-NG · Cisco Packet Tracer |

---

## Certifications

| Credential | Issuer | Year |
|---|---|---|
| Information Security Analyst — Infrastructure &amp; Security | DEPI · MCIT | 2026 |
| Security Engineer · DevSecOps · Defending AWS *(3 certificates)* | TryHackMe | 2026 |
| Google Cybersecurity Professional Certificate | Coursera | 2023 |
| AWS Certified Security — Specialty (SCS-C02) | AWS | *in progress* |

## Experience

| Role | Organisation | Period |
|---|---|---|
| Security Intern | Commercial International Bank (CIB) | Jul – Aug 2025 |
| Network Intern | Zewail City IT Department | Jul 2024 – Jan 2025 |
| Junior Teaching Assistant — Network Installation &amp; Maintenance | Zewail City | Sep – Dec 2024 |
| IT Representative | Zewail City Student Parliament | Sep 2023 – Sep 2024 |

---

<p align="center">
  <img height="150" alt="GitHub statistics" src="https://github-readme-stats.vercel.app/api?username=AhmadEbaid001&hide_border=true&include_all_commits=true&count_private=true&bg_color=00000000&title_color=22CD6E&text_color=B5B4B3&icon_color=22CD6E&hide_title=true"/>
  <img height="150" alt="Most used languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=AhmadEbaid001&hide_border=true&layout=compact&bg_color=00000000&title_color=22CD6E&text_color=B5B4B3&hide_title=true"/>
</p>

<p align="center">
  <sub><strong>Giza, Egypt</strong> · open to cloud security roles ·
  <a href="mailto:ahmedebaid0xc@gmail.com">ahmedebaid0xc@gmail.com</a></sub>
</p>
