
import os
import time
import mysql.connector

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "faker_db"),
}

LOCALE = "en_US"
SEED = 42
BATCH_INDEX = 0
BATCH_SIZES = [10, 100, 500, 1000]
REPEATS = 3

connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor()

try:
    # Warm-up: initialize the connection and stored procedure.
    cursor.callproc(
        "generate_users",
        (SEED, LOCALE, 0, 1)
    )
    for result in cursor.stored_results():
        result.fetchall()

    print("Locale:", LOCALE)
    print("Seed:", SEED)
    print("Repeats per batch size:", REPEATS)
    print()

    for batch_size in BATCH_SIZES:
        elapsed_times = []

        for repeat in range(REPEATS):
            start = time.perf_counter()

            cursor.callproc(
                "generate_users",
                (SEED, LOCALE, BATCH_INDEX, batch_size)
            )

            rows = []
            for result in cursor.stored_results():
                rows.extend(result.fetchall())

            elapsed = time.perf_counter() - start

            if len(rows) != batch_size:
                raise RuntimeError(
                    f"Expected {batch_size} rows, got {len(rows)}"
                )

            elapsed_times.append(elapsed)

        average_seconds = sum(elapsed_times) / len(elapsed_times)
        users_per_second = batch_size / average_seconds

        print(
            f"Batch size: {batch_size:4d} | "
            f"Average time: {average_seconds:.4f} s | "
            f"Throughput: {users_per_second:.2f} users/s"
        )

finally:
    cursor.close()
    connection.close()
