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

## Categories

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