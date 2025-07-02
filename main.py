import argparse
import json
from mlm.engine import Partner, compute_commissions


def load_partners(file_path: str) -> list[Partner]:
    with open(file_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [
        Partner(
            id=entry["id"],
            parent_id=entry.get("parent_id"),
            monthly_revenue=entry["monthly_revenue"],
        )
        for entry in raw
    ]


def save_commissions(file_path: str, commissions: dict[int, float]) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            {str(k): round(v, 2) for k, v in commissions.items()}, f, indent=2
        )


def main():
    parser = argparse.ArgumentParser(description="Compute MLM commissions")
    parser.add_argument(
        "--input", required=True, help="Input JSON file with partner data"
    )
    parser.add_argument(
        "--output", required=True, help="Output JSON file for commissions"
    )
    args = parser.parse_args()

    partners = load_partners(args.input)
    commissions = compute_commissions(partners)
    save_commissions(args.output, commissions)


if __name__ == "__main__":
    main()
