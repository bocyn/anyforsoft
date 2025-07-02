import random
import time
from mlm.engine import Partner, compute_commissions


def generate_fake_partners(n: int) -> list:
    partners = [Partner(id=1, parent_id=None, monthly_revenue=1000)]
    for i in range(2, n + 1):
        parent_id = random.randint(1, i - 1)
        partners.append(
            Partner(
                id=i,
                parent_id=parent_id,
                monthly_revenue=random.uniform(500, 2000),
            )
        )
    return partners


def benchmark():
    print("Generating 50,000 partners...")
    partners = generate_fake_partners(50_000)
    print("Starting commission computation...")

    start = time.time()
    compute_commissions(partners)
    duration = time.time() - start

    print(f"✅ Finished in {duration:.3f} seconds.")


if __name__ == "__main__":
    benchmark()
