# Fake Contact Information Generator

**Author:** Sitora Bakhronova

A Python web application that generates reproducible synthetic contact information using MySQL stored procedures. The application uses Streamlit as its user interface and supports two locales: `en_US` and `de_DE`.

## Live Demo

- **Streamlit Application:** https://itransitiontask6-mgqwzfbnktyivrybv46czx.streamlit.app/
- **Video Demonstration:** https://youtu.be/WcHmjVtxIFs?si=wXQc2bYfSPH5Qo0A

## Features

- Supports English (United States) and German (Germany) locales.
- Uses a random seed to ensure reproducible data generation.
- Supports batch generation with configurable batch index and batch size.
- Generates names, addresses, geographic coordinates, physical attributes, eye colors, phone numbers, and email addresses.
- Displays generated records in a table.
- Allows users to download generated records as a CSV file.
- Performs data generation directly in MySQL using stored procedures and functions rather than Python.

## Technologies

- Python 3
- MySQL 8
- Streamlit
- mysql-connector-python
- Pandas

## Generated Data

Each generated record contains the following fields:

| Field | Description |
|---|---|
| `user_position` | Position of the record in the generated sequence |
| `locale` | Selected locale |
| `gender` | Generated gender category |
| `full_name` | Generated full name |
| `address` | Generated address |
| `latitude` | Geographic latitude |
| `longitude` | Geographic longitude |
| `height_cm` | Height generated using a normal distribution (mean: 170 cm, standard deviation: 10 cm) |
| `weight_kg` | Weight generated using a normal distribution (mean: 70 kg, standard deviation: 15 kg) |
| `eye_color` | Eye color selected according to configured probabilities |
| `phone` | Phone number generated using locale-specific formatting |
| `email` | Generated email address |

## Database Design and Stored Procedures

The project uses a MySQL database with lookup tables containing locale-specific data, including names, cities, streets, email domains, phone formats, address formats, and eye colors.

### Main Stored Procedure

The main procedure is:

```sql
CALL generate_users(seed, locale, batch_index, batch_size);
```

Parameters:

- `seed` — integer used to initialize deterministic pseudo-random generation.
- `locale` — supported locale (`en_US` or `de_DE`).
- `batch_index` — index of the requested batch, starting from zero.
- `batch_size` — number of records to generate.

Example:

```sql
CALL generate_users(42, 'en_US', 0, 100);
```

This generates the first batch of 100 users.

### Helper Functions

| Function | Responsibility |
|---|---|
| `gen_gender` | Selects a gender category deterministically |
| `gen_name` | Generates a full name |
| `gen_address` | Generates a formatted address |
| `gen_phone` | Generates a locale-specific phone number |
| `gen_email` | Generates an email address |
| `rand_unit` | Produces a deterministic pseudo-random value |
| `rand_int` | Generates deterministic integer values within a specified range |
| `pick_value` | Selects an entry from lookup tables |
| `rand_normal` | Generates normally distributed values using the Box–Muller transform |
| `rand_lat` | Generates geographic latitude |
| `rand_lon` | Generates geographic longitude |
| `rand_eye_color` | Selects an eye color according to configured probabilities |
| `slugify` | Converts text into a suitable email-address component |

## Reproducibility and Batch Generation

The generator uses the seed, locale, record position, and helper-specific salt to determine generated values.

Using the same seed, locale, batch index, and batch size produces the same results, provided that the lookup data and stored procedure definitions remain unchanged.

Batch generation allows records to be generated in separate groups.

For example:

```sql
CALL generate_users(42, 'en_US', 0, 100);
CALL generate_users(42, 'en_US', 1, 100);
```

The first call generates records with positions 0–99, while the second generates positions 100–199.

## Installation and Configuration

### Requirements

- Python 3
- MySQL Server 8
- Project database, lookup data, stored functions, and stored procedure

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Database Connection

Set the following environment variables according to your MySQL configuration:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

Example for a local MySQL installation:

```bash
export DB_HOST='127.0.0.1'
export DB_PORT='3306'
export DB_USER='root'
export DB_PASSWORD='YOUR_MYSQL_PASSWORD'
export DB_NAME='faker_db'
```

For deployment, configure the corresponding database credentials securely in the hosting platform's secrets or environment settings.

**Never commit real database credentials to GitHub.**

### Run the Application Locally

```bash
python -m streamlit run app.py
```

Open the local URL provided by Streamlit, usually:

```text
http://localhost:8501
```

## Benchmark

The benchmark measures the end-to-end performance of generating fake user records using the remote Aiven MySQL database.

### Test Configuration

- Database: Aiven MySQL
- Locale: `en_US`
- Seed: `42`
- Batch size: `1,000` users
- Number of measured runs: `3`
- Warm-up: `100` users (excluded from measurements)
- Measurement tool: Python `time.perf_counter()`

### Results

| Metric | Result |
|---|---:|
| Users per run | 1,000 |
| Number of runs | 3 |
| Average execution time | 8.367 seconds |
| Average generation speed | **119.52 users/second** |
| Median generation speed | 120.07 users/second |

Generation speed is calculated as:

```text
Generation speed = Number of generated users / Execution time
```

The measurement includes stored procedure execution and fetching the generated records from the remote database. Therefore, it represents end-to-end throughput, including network transfer.

## Limitations

- Output quality depends on the lookup data available for each locale.
- Reproducibility depends on keeping lookup tables and stored procedure definitions unchanged.
- Generated contact details are synthetic and should not be treated as verified real-world information.

## Project Links

- **GitHub Repository:** https://github.com/sitorb/itransitiontask6
- **Live Application:** https://itransitiontask6-mgqwzfbnktyivrybv46czx.streamlit.app/
- **Video Demonstration:** https://youtu.be/WcHmjVtxIFs?si=wXQc2bYfSPH5Qo0A

## Author

**Sitora Bakhronova**
