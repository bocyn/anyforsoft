from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass
class Partner:
    id: int
    parent_id: Optional[int]
    monthly_revenue: float


def detect_cycle(
    graph: Dict[int, List[int]],
    node: int,
    visited: Set[int],
    visiting: Set[int],
) -> bool:
    visiting.add(node)
    for neighbor in graph.get(node, []):
        if neighbor in visiting:
            return True  # cycle found
        if neighbor not in visited:
            if detect_cycle(graph, neighbor, visited, visiting):
                return True
    visiting.remove(node)
    visited.add(node)
    return False


def compute_commissions(
    partners: List[Partner], days_in_month: int = 30
) -> Dict[int, float]:
    # Build ID → Partner map
    partner_map = {p.id: p for p in partners}

    # Build tree: parent → list of children
    tree = defaultdict(list)
    root_candidates = set(partner_map.keys())

    for partner in partners:
        if partner.parent_id is not None:
            tree[partner.parent_id].append(partner.id)
            root_candidates.discard(partner.id)

    if len(root_candidates) != 1:
        raise ValueError("Invalid tree: must have exactly one root")
    root_id = root_candidates.pop()

    # Detect cycles
    visited = set()
    if detect_cycle(tree, root_id, visited, set()):
        raise ValueError("Cycle detected in partner hierarchy")

    commissions: Dict[int, float] = {}
    daily_profits: Dict[int, float] = {
        p.id: round(p.monthly_revenue / days_in_month, 2) for p in partners
    }

    def dfs(node_id: int) -> float:
        total_descendant_profit = 0.0
        for child_id in tree.get(node_id, []):
            descendant_sum = dfs(child_id)
            total_descendant_profit += daily_profits[child_id] + descendant_sum
        commissions[node_id] = round(0.05 * total_descendant_profit, 2)
        return total_descendant_profit

    dfs(root_id)
    return commissions
