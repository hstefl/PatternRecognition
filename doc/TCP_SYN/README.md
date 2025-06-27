# Prompt for Dataset Generation: TCP SYN Scan Detection

--------------------------------------------------------

## 🧠 What is a TCP SYN Scan?

A **TCP SYN scan** is a common reconnaissance technique used by attackers to identify open ports on target machines. The scanner sends **TCP SYN (synchronize)** packets to multiple ports without completing the three-way handshake. If a port is open, the target responds with a **SYN-ACK**; if it is closed, it responds with a **RST**.

The scanner typically does **not complete the handshake**, meaning it does not send back an ACK to the SYN-ACK. This behavior allows the scanner to:
- Probe many ports quickly,
- Avoid full connections (reducing detection footprint),
- Identify services listening on specific ports.

Such scans can be:
- **Aggressive and centralized** (e.g., thousands of ports in seconds from one IP),
- **Slow and distributed** (e.g., low-rate scans from many IPs across hours),
- **Noisy or stealthy**, depending on SYN volume, diversity of sources, and responses received.

This dataset aims to simulate **sliding time-window summaries** of such behavior, suitable for detection models — especially LLMs — by generating realistic permutations of scan features and their context-aware classifications.

---

## 📊 Generate

Generate a table (into downloadable CSV file) that includes **all valid permutations** of categorical attributes used to characterize a **TCP SYN scan**.

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

5. **Port spread vs. Source Diversity**
   - If `Port Spread` is `one`, then `Source Diversity` must be only `centralized`.
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
- `one` (1)
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

## 📈 Evaluation Dimensions

### 7. **Scan Intensity**
- Qualitative severity of the observed scan pattern.
- Values: `None`, `Low`, `Moderate`, `High`, `Very High`

### 8. **Risk Assessment**
- A categorized risk level associated with the pattern, especially in the context of critical infrastructure.
- Values: `none`, `low`, `moderate`, `elevated`, `critical`

### 9. **Scan Archetype**
- Classification of the likely scanning behavior type:
  - `classic`: fast, centralized, brute-force scans
  - `stealth`: slow or low-volume scans attempting to evade detection
  - `distributed`: sourced from many IPs, coordinated across nodes
  - `obfuscated`: hidden among normal traffic, or noisy but disguised
  - `likely benign`: pattern resembles normal application behavior
  - `ambiguous`: inconclusive or borderline cases

### 10. **Suggested Action**
- Operational guidance based on risk level:
  - Examples: `Monitor only`, `Alert SOC`, `Throttle source IP`, `Block temporarily`

### 11. **Explanation**
- A short, structured justification describing **why** the classification, archetype, and action were chosen (e.g., “High SYN rate and no responses over short time from single source = classic scan”).

---

## ✅ For Each Valid Combination, Include:

- `Time Window`  
- `SYN Rate`  
- `SYN Percentage`  
- `Port Spread`  
- `ACK Response Rate`  
- `Source Diversity`  
- `Scan Intensity`  
- `Risk Assessment`  
- `Scan Archetype`  
- `Suggested Action`  
- `Explanation`

---

## 🛡️ Defensive Evaluation Policy

- Evaluate scanning risk by combining behavior across SYN rate, percentage, port diversity, source dispersion, and ACK response.
- Only consider `complete response` (99–100% ACK) as confidently non-scan.
- Distributed, low-rate activity must be highlighted — these often evade threshold-based tools.
- Provide interpretability via `Scan Archetype` and `Suggested Action`.
- Format results as a **structured table** suitable for machine learning or expert rule creation.
