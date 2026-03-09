import random
from datetime import datetime, timedelta

from app.database import get_connection, init_db

MACHINES = ["filler_01", "capper_01", "labeler_01"]
STATES = ["RUNNING", "IDLE", "DOWN", "CHANGEOVER"]
DOWN_REASONS = ["Jam", "Sensor Fault", "Material Shortage", "Operator Stop"]


def weighted_state() -> str:
    return random.choices(
        population=STATES,
        weights=[70, 12, 10, 8],
        k=1,
    )[0]


def generate_events(num_events_per_machine: int = 150) -> None:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM machine_events")
    conn.commit()

    now = datetime.now()
    start_time = now - timedelta(hours=8)

    for machine in MACHINES:
        current_time = start_time
        total_parts = 0

        for _ in range(num_events_per_machine):
            state = weighted_state()
            downtime_reason = None

            if state == "RUNNING":
                produced = random.randint(5, 25)
                total_parts += produced
            elif state == "DOWN":
                downtime_reason = random.choice(DOWN_REASONS)

            cursor.execute(
                """
                INSERT INTO machine_events (
                    machine_id,
                    timestamp,
                    state,
                    part_count,
                    downtime_reason
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    machine,
                    current_time.isoformat(),
                    state,
                    total_parts,
                    downtime_reason,
                ),
            )

            current_time += timedelta(minutes=random.randint(1, 8))

    conn.commit()
    conn.close()
    print("Sample industrial events generated successfully.")


if __name__ == "__main__":
    generate_events()