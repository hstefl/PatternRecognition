# 🛡️ Project Summary: Fine-Tuning LLMs for Network Attack Detection

## 🎯 Objective

To **learn how to fine-tune large language models (LLMs)** in a practical cybersecurity setting by training a model to **identify and explain specific network-based attacks**, starting with **TCP SYN scans**.

---

## 📌 Key Goals

- Understand the **LLM fine-tuning process** using OpenAI API or Hugging Face.
- Generate and label **structured synthetic traffic data**.
- Focus initially on a **single attack type** (TCP SYN scan) to reduce complexity.
- Train an LLM to:
  - Analyze traffic flow descriptions,
  - Classify them as benign or malicious,
  - Provide short, meaningful explanations.
- Incrementally expand to other attack types (e.g. ICMP ping sweep, UDP scans).

---

## 🔧 Skills Gained

- Fine-tuning workflow for GPT-style models.
- Formatting training data (prompt-completion or chat format).
- Network traffic analysis and simulation (e.g. Nmap, tcpdump).
- Cybersecurity fundamentals (reconnaissance, scanning, TCP/IP stack).
- Automating dataset generation and parsing (e.g. Python scripts).

---

## 🚀 Future Expansion Ideas

- Brute-force login attempt detection (SSH, FTP).
- DNS tunneling identification.
- Application-layer attacks (e.g. HTTP Slowloris).
- Combine LLM output with traditional anomaly detection systems.

---


Ideas to train

| Priority | Attack Type        | Learnability | Simulation Ease | LLM Training Suitability    |
| -------- | ------------------ | ------------ | --------------- | --------------------------- |
| ✅ 1      | TCP SYN Scan       | Easy         | Very Easy       | Excellent                   |
| ✅ 2      | ICMP Ping Sweep    | Easy         | Very Easy       | Excellent                   |
| ✅ 3      | UDP Port Scan      | Medium       | Easy            | Good                        |
| ✅ 4      | TCP Connect Scan   | Medium       | Easy            | Good                        |
| 🔶 5     | Brute-force Logins | Medium       | Moderate        | Excellent                   |
| 🔶 6     | DNS Tunneling      | Harder       | Moderate        | High potential              |
| ⚠️ 7     | Slowloris / DoS    | Harder       | Moderate/Hard   | Tricky (depends on context) |
8 ARP Spoofing / ARP Poisoning

1 TCP SYN Scan https://chatgpt.com/g/g-p-684821ad6c5081919ebfdd204068dbd7-ai-du-3/c/684aa54f-0030-8008-a844-12f5190a691d
| Time       | Src IP    | Dst IP        | Src Port | Dst Port | Flags | Description  |
| ---------- | --------- | ------------- | -------- | -------- | ----- | ------------ |
| 12:00:01.1 | 10.0.0.10 | 192.168.1.100 | 40000    | 22       | SYN   | First probe  |
| 12:00:01.2 | 10.0.0.10 | 192.168.1.100 | 40001    | 80       | SYN   | Second probe |
| 12:00:01.3 | 10.0.0.10 | 192.168.1.100 | 40002    | 443      | SYN   | Third probe  |
| 12:00:01.4 | 10.0.0.10 | 192.168.1.100 | 40003    | 445      | SYN   | Fourth probe |
| 12:00:01.5 | 10.0.0.10 | 192.168.1.100 | 40004    | 8080     | SYN   | Fifth probe  |

Key Characteristics
 * Many SYN packets to different ports.
 * No ACKs follow from source.
 * Short time span (milliseconds between packets).
 * Each probe often uses a new source port.

What to Look for in PCAP (Indicators)
 * If parsing traffic for TCP SYN scan detection:
 * High volume of SYN packets
 * Same source IP, destination IP, and different destination ports
 * Low or no established TCP sessions (no 3-way handshake)
 * No data payloads (pure SYN)
 * Timing: bursts within a few seconds

Note:  What You Can Detect from One Packet
You can classify a single packet as suspicious if it shows:
 * Abnormal TTL or window size (in some evasive scans)
 * Reserved TCP flags (e.g., NULL, FIN, Xmas scan)
 * Use of known scanning tools (some may leave signatures)
 * But this only gives you heuristics, not certainty.


-------------------------------


# 🛡️ LLM-Based Port Scan Detection Pipeline — Summary

## ✅ Overview

A modular pipeline to detect **TCP SYN port scans** using an LLLM. It ingests network packets via Kafka, summarizes behavior over time windows, and uses an LLM to classify and explain suspicious activity.

---

## 🧱 Pipeline Architecture

### 1. **Packet Ingestion**
- **Tool**: `tcpdump`, Zeek, Suricata
- **Storage**: Kafka — one packet per message
- **Format**: JSON with fields like:
  - `timestamp`, `src_ip`, `dst_ip`, `protocol`, `ports`, `flags`, etc.

---

### 2. **Packet Aggregator / Summarizer**
- **Goal**: Aggregate packets into behavioral summaries
- **Method**:
  - Use **sliding windows** (e.g., 5s with 1s step)
  - Group by `(src_ip, dst_ip, protocol)`
  - Extract:
    - SYN/ACK counts
    - Unique destination ports
    - Total packets, payload, flags

- **Tools**:
  - Python, Apache Flink, Kafka Streams

---

### 3. **Pre-Filtering**
- **Purpose**: Reduce LLM load by filtering non-suspicious traffic
- **Method**:
  - Threshold rules (e.g., `syn_count ≥ 5`, `dst_ports ≥ 3`)
  - Optional lightweight ML model for scoring

---

### 4. **LLM Input Formatter**
- **Goal**: Prepare LLM-readable input
- **Structure**:
  - **Structured JSON** (stats)
  - **Text summary** of behavior
- **Prompt Style**:
  - Few-shot examples + clear instructions
  - Example:
    ```json
    {
      "src_ip": "10.0.0.10",
      "dst_ip": "192.168.1.100",
      "syn_count": 12,
      "unique_ports": 5,
      "summary": "Host sent 12 SYN packets to 5 ports with no ACKs."
    }
    ```

---

### 5. **LLM Analysis**
- **Role**: Classify behavior and explain it
- **Tasks**:
  - Is this a scan?
  - What type (e.g., TCP SYN)?
  - Why?
- **Deployment**:
  - OpenAI GPT-4 / Claude / local LLM (LLaMA, Mistral)
  - Use few-shot prompting or fine-tuning

---

### 6. **Post-Processing**
- **Output**:
  - `label`, `confidence`, `explanation`
- **Routing**:
  - Store to DB
  - Trigger alerts
  - Forward to SOC dashboard

---

## 🔧 Key Improvements Over Original Plan

| Area                | Original Idea                      | Improved Plan                                    |
|---------------------|-------------------------------------|--------------------------------------------------|
| Aggregation         | Time-only                          | Sliding window + IP grouping                    |
| LLM Decision        | Every packet summary               | Pre-filtered candidates only                    |
| LLM Input           | Text only                          | Structured + text input                         |
| Training Strategy   | Vague                              | Clear: few-shot or fine-tuning                  |
| Output Usefulness   | Detection                          | + Human-readable explanation                    |

---

## Summary

> You’re building a pipeline where raw packets are ingested via Kafka, grouped and summarized into behavioral patterns over time, then analyzed by an LLM to detect port scans. By combining structured aggregation, intelligent filtering, and text+structured LLM input, you can detect and explain TCP SYN scans effectively. The system is modular, scalable, and LLM-ready with clear decision boundaries.


https://chatgpt.com/c/68497fdd-21dc-8008-8dbe-f92000803e64



----------------------------------------

Prompt for dataset generation
---

Generate a table that includes **all valid permutations** of categorical attributes used to characterize a **TCP SYN scan**.

These attributes describe network traffic summaries over short sliding time windows. Use the categories defined below.

---

## ❗ Exclude Invalid Combinations

Avoid combinations that are logically or behaviorally inconsistent. Specifically:

1. **SYN Rate vs. Port Spread**
   - If `SYN Rate` is `very low` or `low`, do not pair with `many` or `broad sweep` ports in `very-short`, `short`, or `moderate` time windows.

2. **SYN Percentage vs. SYN Rate (Inverse)**
   - If `SYN Rate` is `very low`, do not pair with `dominant` or `overwhelming` SYN percentages.

3. **Port Spread vs. SYN Rate**
   - If `Port Spread` is `broad sweep`, `SYN Rate` must be at least `moderate`, unless the time window is `long`, `extended`, or `prolonged`.

4. **Source Diversity vs. SYN Rate**
   - If `Source Diversity` is `highly distributed`, but `SYN Rate` is `very low`, discard unless `Port Spread` is `broad sweep` (indicating coordinated distributed scanning).

---

## 🔢 Categories

### 1. **Time Window** (duration of the scan window):
- `very-short` (0–1 sec)
- `short` (1–5 sec)
- `moderate` (6–15 sec)
- `long` (16–60 sec)
- `extended` (61–300 sec)
- `prolonged` (301–900 sec)

### 2. **SYN Rate** (SYN packets per second):
- `very low` (1–2)
- `low` (3–9)
- `moderate` (10–49)
- `high` (50–199)
- `very high` (200+)

### 3. **SYN Percentage** (SYNs as a proportion of all packets in the window):
- `minimal` (0–4%)
- `low` (5–24%)
- `moderate` (25–49%)
- `dominant` (50–89%)
- `overwhelming` (90–100%)

### 4. **Port Spread** (number of unique destination ports targeted):
- `a few` (2–4)
- `several` (5–9)
- `many` (10–99)
- `broad sweep` (100–65535)

### 5. **ACK Response Rate** (ACKs received in relation to SYNs sent):
- `no response` (0%)
- `minimal response` (1–9%)
- `partial response` (10–49%)
- `widespread response` (50–84%)
- `broad response` (85–98%)
- `complete response` (99–100%)

### 6. **Source Diversity** (based on source dispersion score = unique source IPs / total SYNs):
- `centralized` (≤ 0.05)
- `moderately distributed` (0.06 – 0.25)
- `highly distributed` (> 0.25)

---

## For Each Valid Combination, Include:

- `Time Window`  
- `SYN Rate`  
- `SYN Percentage`  
- `Port Spread`  
- `ACK Response Rate`  
- `Source Diversity`  
- **Scan Intensity** (None / Low / Moderate / High / Very High)  
- **Risk Assessment** (short sentence in the context of critical infrastructure)  
- **Explanation** (concise logic for the classification)  
- **Suggested Action** (e.g., “Monitor only”, “Alert SOC”, “Throttle source IP”, “Block temporarily”)  
- **Scan Archetype** (`classic`, `stealth`, `distributed`, `obfuscated`, `likely benign`, `ambiguous`)

---

## Defensive Evaluation Policy

- Evaluate scanning risk by combining behavior across SYN rate, percentage, port diversity, source dispersion, and ACK response.
- Only consider `complete response` (99–100% ACK) as confidently non-scan.
- Distributed, low-rate activity must be highlighted — these often evade threshold-based tools.
- Provide interpretability via `Scan Archetype` and `Suggested Action`.
- Format results as a **structured table** suitable for machine learning or expert rule creation.