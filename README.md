# COM732 AE2 – SSH Authentication Monitoring and Automated Network Enforcement

## My Contribution (Member B)

This repository is my working copy of **Component B: the Authentication Log Preprocessor**, built as part of a six-person group project at Solent University. The same work is pushed to the team repository.

I am responsible for:

- Reading multiple Linux authentication log files, including compressed `.gz` files.
- Parsing authentication records into structured event data (usernames, source IPs, source ports).
- Identifying failed and successful SSH login attempts.
- Grouping failed attempts by host, source IP address and configurable time windows.
- Applying alert thresholds based on the business criticality of the affected asset.
- Producing structured summaries as JSON Lines (JSONL) or forwarding them over HTTPS to the downstream components.

The other components (asset inventory and policy engine, enforcement API, Cisco network driver, and testing and security) are built by my teammates. They are described below for context, so the preprocessor can be understood as part of the whole system.

### Component Status

| Capability                                                        | Status                       |
| ----------------------------------------------------------------- | ---------------------------- |
| Read authentication logs and parse into structured events         | Working                      |
| Identify failed and successful logins (user, source IP and port)  | Working                      |
| Read compressed `.gz` logs                                        | [update: Done] |
| Aggregate failed logins by host, source IP and time window        | [update: Done] |
| Asset-based alert thresholds                                      | [update: Done] |
| JSONL output                                                      | [update: Done] |
| HTTPS output to the downstream components                         | [update: Done] |

## Project Overview

This project is a Python-based cybersecurity solution for detecting suspicious remote login activity, aggregating authentication events, and enforcing automated network security controls.

It focuses on identifying potentially hostile SSH login attempts against Linux systems by analysing authentication logs. Rather than forwarding every individual event to a Security Information and Event Management (SIEM) system, the solution aggregates related events, assesses their significance, and generates meaningful security alerts.

Where predefined security conditions are met, the system is designed to trigger network controls on Cisco IOS XE devices through an automated enforcement mechanism.

The project is part of the **COM732 – Computer Fundamentals** assessment at Solent University.

## Project Objectives

The primary objectives are to:

- Detect suspicious remote login activity from Linux authentication logs.
- Aggregate and enrich authentication events to reduce unnecessary SIEM processing and associated costs.
- Identify repeated failed login attempts using configurable time windows and asset-based thresholds.
- Maintain an asset inventory to support risk assessment and informed security decisions.
- Apply automated, reversible network controls to appropriate Cisco network devices.
- Maintain secure communication, reliable processing, auditability and accountability across the system.

## System Architecture

The solution has three principal functional areas. **Area 1 is my component.**

### 1. Authentication Log Preprocessor (Member B – my component)

The preprocessor analyses Linux authentication logs and identifies relevant SSH authentication events.

Its responsibilities include:

- Reading multiple authentication log files, including compressed `.gz` files.
- Parsing authentication records into structured event data.
- Identifying failed and successful login attempts.
- Grouping failed login attempts by host, source IP address and configurable time windows.
- Applying alert thresholds based on the business criticality of the affected asset.
- Generating structured summaries in JSON Lines (JSONL) format or forwarding them through an HTTPS interface.

This component minimises unnecessary event forwarding by identifying potentially significant activity before it reaches downstream security services.

### 2. Asset Inventory and Policy Engine (teammates)

The asset inventory maintains information about monitored systems, including:

- Hostname and primary IP address.
- Environment and system owner.
- Business function.
- Business criticality.

The policy engine uses this information alongside predefined allowlists and risk modifiers to decide whether an alert warrants further action. It also determines the appropriate network control point for a potential enforcement action.

### 3. Policy Enforcement and Cisco Network Integration (teammates)

The enforcement component receives alerts and determines whether an automated network response is authorised.

The intended workflow includes:

- Validating incoming alert requests.
- Checking authentication and replay-protection requirements.
- Preventing duplicate enforcement actions.
- Communicating with Cisco IOS XE devices through a secure configuration interface.
- Applying network controls, such as access-control restrictions or sinkhole routes.
- Recording enforcement actions and their outcomes.
- Applying time-to-live (TTL) values so temporary controls can be removed.
- Supporting rollback and recovery.

## High-Level Data Flow

My component covers the first four stages of the flow below, down to the security event summary.

```text
Linux Authentication Logs
          |
          v
Authentication Log Preprocessor        <-- Member B (this repository)
          |
          v
Event Parsing and Aggregation          <-- Member B
          |
          v
Asset-Based Threshold Evaluation       <-- Member B
          |
          v
Security Event Summary                 <-- Member B
       /       \
      v         v
    JSONL      HTTPS
      \         /
       v       v
   Asset Inventory
          |
          v
     Policy Engine
          |
          v
   Enforcement API
          |
          v
   Cisco Network Driver
          |
          v
    Cisco IOS XE Device
          |
          v
  Network Security Control
          |
          v
 Audit Logging and TTL/Rollback
```

## Technology and Development Approach

| Technology / Concept            | Application                               |
| ------------------------------- | ----------------------------------------- |
| Python                          | Core application development              |
| Linux authentication logs       | Source of authentication events           |
| Python file handling            | Reading authentication log files          |
| Gzip                            | Processing compressed authentication logs |
| Regular expressions and parsing | Extracting structured event information   |
| JSON / JSONL                    | Structured event and alert representation |
| HTTPS                           | Secure communication between components   |
| Cisco IOS XE                    | Target network infrastructure             |
| RESTCONF                        | Network device configuration interface    |
| HMAC                            | Request authentication and integrity      |
| Git and GitHub                  | Version control and collaboration         |
| Python testing tools            | Functional and integration testing        |

The application uses a modular design, so individual components can be developed, tested and integrated independently.

## Team Responsibilities

The project is divided among six team members. **I am Member B.**

| Member    | Primary Responsibility             | Main Contribution                                                                                  |
| --------- | ---------------------------------- | -------------------------------------------------------------------------------------------------- |
| A         | Project management and integration | Repository management, shared configuration, logging, CI skeleton and end-to-end integration       |
| **B (me)** | **Authentication log preprocessor** | **Log reading, parsing, event aggregation, threshold evaluation, JSONL and HTTPS output**          |
| C         | Asset inventory and policy engine  | CSV inventory, HTTP inventory endpoint, allowlists, risk modifiers and control-point selection     |
| D         | Enforcement API                    | HMAC authentication, timestamp and nonce replay protection, deduplication and schema validation    |
| E         | Cisco network driver               | RESTCONF communication, read-before-write, retries, TTL expiry and rollback                        |
| F         | Testing and security               | Unit and integration testing, performance testing, Bandit, pip-audit, Gitleaks, SBOM and checksums |

Separating responsibilities allows parallel development while the components are integrated into one application.

## Current Development Progress

Development is incremental, with each component implemented and tested before integration.

The preprocessor has a working foundation that reads Linux authentication log entries and parses them into structured Python data. Test outputs show it identifying both failed and successful login events, including usernames, source IP addresses and source ports.

The next steps for my component are event aggregation, time-window evaluation, asset-based thresholds and structured output for the other components. Progress is recorded through repository commits, test results and project documentation.

## Security Considerations

Security is a central consideration throughout development. The solution is designed around these requirements:

- **Encrypted communication:** Network communication between components and devices must use secure transport.
- **Input validation:** Incoming data, file paths, IP addresses and configuration parameters must be validated.
- **Secure secrets management:** Credentials and sensitive configuration values must not be hardcoded.
- **Least privilege:** Application and network device accounts should have only the permissions they need.
- **Request authentication:** Enforcement requests must be authenticated and protected against replay attacks.
- **Duplicate prevention:** Repeated alerts should not cause unnecessary or duplicated network changes.
- **Auditability:** Processing and enforcement activities should be recorded without exposing sensitive information.
- **Reversibility:** Automated network controls should have defined expiry periods and rollback mechanisms.

In the preprocessor, the most relevant requirements are input validation of log files and paths, safe handling of untrusted log content, and secure transport when forwarding summaries over HTTPS.

## Testing and Quality Assurance

The project testing strategy includes:

**Functional testing**

- Authentication log reading and parsing.
- Recognition of relevant login events.
- Event aggregation and threshold evaluation.
- JSONL output generation.
- Validation of application inputs.

**Integration testing**

- Communication between the preprocessor and enforcement components.
- Inventory and policy engine interactions.
- Mocked external services and network device interfaces.
- Verification of the overall event-to-enforcement workflow.

**Performance testing**

- Assessment of log-processing performance.
- Evaluation of event aggregation under increased workloads.
- Measurement of enforcement response times.

**Security testing**

- Static code analysis.
- Dependency vulnerability assessment.
- Secret scanning.
- Input validation and secure communication checks.

The intended testing and security tools include Bandit, pip-audit and Gitleaks, alongside the team's automated and manual testing.

## Repository Organisation

My preprocessor code lives under:

```text
preprocessor/
```

Shared configuration and logging (Member A) are part of the wider team repository structure under:

```text
common/
```

Other component directories, test files and documentation are maintained in the team repository as each module and the integration work progress. The `Northmen-SOC-project` submodule links to the team repository.

## Development Environment

The assessment requires a Python-based application using Python 3.6 or above. A virtual environment is recommended to keep project dependencies separate from the system Python installation.

Component-specific execution and testing instructions will be added as the application entry points and shared test framework are finalised.

## Project Scope and Limitations

This project is an academic software development exercise demonstrating computer systems, cybersecurity principles, Python programming, network automation and collaborative software development.

The automated enforcement functionality is intended to operate in a controlled and authorised testing environment. Sample authentication logs, mocked external services and simulated network devices can be used to validate behaviour without affecting production infrastructure.

The project is not intended to replace a full enterprise SIEM, network access-control platform or dedicated threat detection system.

## Academic Context

**Institution:** Solent University
**Module:** COM732 – Computer Fundamentals
**Assessment:** AE2 – Group Software Project
**Academic Year:** 2026–2027

This repository provides evidence of my individual contribution as Member B, supported by Git commits and project documentation, within the wider collaborative project.
Individual contributions are supported through Git commits and accompanying project documentation.
