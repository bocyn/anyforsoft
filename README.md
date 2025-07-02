# High-Performance Daily Commission Engine for MLM Network

## 📌 Project Overview
This project implements a high-performance Python engine to compute daily commissions for a multi-level marketing (MLM) partner network. Each partner earns a 5% commission on the daily gross profit of every partner in their downline (i.e., direct or indirect referrals).

The engine is optimized to handle:
- **50,000+ partners**
- **15+ hierarchy levels**
- **Full computation in under 2 seconds**


## ✅ Functional Summary
- **Input**: JSON file with partner hierarchy and monthly revenues.
- **Output**: JSON file mapping each `partner_id` to their earned commission.
- **Computation Rule**: 
  ```
  commission_p = 0.05 × sum(daily_profit_d for all descendants d of p)
  daily_profit = monthly_revenue / days_in_month
  ```
- **Rooted Tree Assumption**: Data must form a valid, connected, acyclic tree with one root node.
- **Cycle Detection**: DFS traversal detects and raises errors on invalid graphs.


## ⚙️ How to Run
```bash
python main.py --input dataset.json --output commissions.json
```


## 💡 Algorithmic Approach
We use a **bottom-up post-order DFS traversal** to compute commissions efficiently:

1. **Build Tree**: Create an adjacency list from the input.
2. **Cycle Check**: Perform DFS to ensure the graph is a tree.
3. **Daily Profits**: Precompute each partner's daily profit.
4. **DFS Traversal**:
    - For each node, recursively compute the total descendant profit.
    - Multiply it by `0.05` and assign to that node's commission.
    - Avoids repeated computation by visiting each node once.


### Example:
```
Partner 1
├── Partner 2
│   └── Partner 3

- Partner 3 earns 0 (no descendants)
- Partner 2 earns 5% of Partner 3's daily profit
- Partner 1 earns 5% of (Partner 2 + Partner 3)'s daily profits
```


## 🧠 Complexity Analysis
| Operation            | Complexity     |
|---------------------|----------------|
| Build tree          | O(n)           |
| DFS with memoization| O(n)           |
| Cycle detection     | O(n)           |
| Total               | **O(n)**       |
| Space complexity    | O(n)           |

Where **n** is the number of partners.


## 🧪 Testing Strategy
- Covered edge cases like:
  - Trees with one node
  - Cycles in hierarchy
  - Multiple root candidates
  - Deep tree structures (max depth)
- Used `pytest` for unit testing


## 🚀 Benchmark
Run:
```bash
python benchmark.py
```

Results:
- **50,000 partners**
- **Execution time**: ~1.4s on 4-core 3.0 GHz CPU
- **Memory use**: < 2× input size


## 📁 Project Structure
```
mlm/
├── engine.py       # Core commission logic
main.py             # CLI entry point
benchmark.py        # Performance test
README.md           # This file
tests/
├── test_engine.py  # Unit tests
```


## 📎 Dependencies
- Python 3.11+
- Standard library only (`argparse`, `json`, `collections`, `datetime`)
- `pytest` (for testing only)
