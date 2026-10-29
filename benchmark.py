
import time
import statistics
import mysql.connector
from getpass import getpass

# Aiven database connection
config = {
    "host": "mysql-3480df3-sitorb.i.aivencloud.com",
    "port": 25780,
    "user": "avnadmin",
    "password": getpass("Enter your Aiven password: "),
    "database": "defaultdb",
    "ssl_disabled": False,
}

BATCH_SIZE = 1000
REPEATS = 3
SEED = 42
LOCALE = "en_US"

connection = mysql.connector.connect(**config)
cursor = connection.cursor()

def generate_and_measure(batch_size, batch_index=0):
    start = time.perf_counter()

    cursor.callproc(
        "generate_users",
        [SEED, LOCALE, batch_index, batch_size]
    )

    # Fetch all generated records
    for result in cursor.stored_results():
        result.fetchall()

    elapsed = time.perf_counter() - start
    return elapsed

try:
    # Warm-up: not included in the benchmark
    print("Running warm-up...")
    generate_and_measure(100)

    # Actual measurements
    times = []

    for i in range(REPEATS):
        elapsed = generate_and_measure(BATCH_SIZE)
        times.append(elapsed)

        speed = BATCH_SIZE / elapsed
        print(
            f"Run {i + 1}: {elapsed:.3f} seconds "
            f"({speed:.2f} users/second)"
        )

    average_time = statistics.mean(times)
    average_speed = BATCH_SIZE / average_time
    median_time = statistics.median(times)
    median_speed = BATCH_SIZE / median_time

    print("\n--- BENCHMARK RESULTS ---")
    print(f"Users per run: {BATCH_SIZE}")
    print(f"Number of runs: {REPEATS}")
    print(f"Average time: {average_time:.3f} seconds")
    print(f"Average speed: {average_speed:.2f} users/second")
    print(f"Median speed: {median_speed:.2f} users/second")

finally:
    cursor.close()
    connection.close()
