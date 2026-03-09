from fastapi import FastAPI, HTTPException

from app.database import get_connection, init_db

app = FastAPI(
    title="Industrial Event Stream Simulator",
    description="Simulated industrial machine events with API access.",
)

init_db()


@app.get("/")
def root():
    return {"message": "Industrial Event Stream Simulator API"}


@app.get("/events")
def get_events(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT machine_id, timestamp, state, part_count, downtime_reason
        FROM machine_events
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/machines/{machine_id}/status")
def get_machine_status(machine_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT machine_id, timestamp, state, part_count, downtime_reason
        FROM machine_events
        WHERE machine_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        (machine_id,),
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Machine not found")

    return dict(row)


@app.get("/metrics/downtime")
def get_downtime_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT machine_id, downtime_reason, COUNT(*) as event_count
        FROM machine_events
        WHERE state = 'DOWN'
        GROUP BY machine_id, downtime_reason
        ORDER BY machine_id, event_count DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/metrics/summary")
def get_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            machine_id,
            SUM(CASE WHEN state = 'RUNNING' THEN 1 ELSE 0 END) as running_events,
            SUM(CASE WHEN state = 'DOWN' THEN 1 ELSE 0 END) as down_events,
            SUM(CASE WHEN state = 'IDLE' THEN 1 ELSE 0 END) as idle_events,
            SUM(CASE WHEN state = 'CHANGEOVER' THEN 1 ELSE 0 END) as changeover_events,
            MAX(part_count) as total_parts
        FROM machine_events
        GROUP BY machine_id
        ORDER BY machine_id
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/metrics/oee")
def get_oee_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            machine_id,
            COUNT(*) as total_events,
            SUM(CASE WHEN state = 'RUNNING' THEN 1 ELSE 0 END) as running_events,
            SUM(CASE WHEN state = 'DOWN' THEN 1 ELSE 0 END) as down_events,
            MAX(part_count) as total_parts
        FROM machine_events
        GROUP BY machine_id
        ORDER BY machine_id
        """
    )

    rows = cursor.fetchall()
    conn.close()

    results = []

    for row in rows:
        machine_id = row["machine_id"]
        total_events = row["total_events"] or 0
        running_events = row["running_events"] or 0
        down_events = row["down_events"] or 0
        total_parts = row["total_parts"] or 0

        availability = round(running_events / total_events, 3) if total_events else 0.0

        performance_raw = (total_parts / running_events) if running_events else 0.0
        performance = round(min(performance_raw / 25, 1.0), 3) if running_events else 0.0

        quality = 1.0
        oee = round(availability * performance * quality, 3)

        results.append(
            {
                "machine_id": machine_id,
                "total_events": total_events,
                "running_events": running_events,
                "down_events": down_events,
                "total_parts": total_parts,
                "availability": availability,
                "performance": performance,
                "quality": quality,
                "oee": oee,
            }
        )

    return results