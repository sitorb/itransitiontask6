# Fake Contact Information Generator

**Author:** Sitora Bakhronova

## Overview

A Python web application that generates reproducible fake contact information using MySQL stored procedures. The application uses Streamlit for its user interface and allows users to generate data for two locales: `en_US` and `de_DE`.

## Features

- Supports English (United States) and German (Germany) locales.
- Accepts a random seed to make generated records reproducible.
- Supports batch generation with a batch index and batch size.
- Generates names, addresses, geographic coordinates, physical attributes, eye colors, phone numbers, and email addresses.
- Displays generated records in a table.
- Allows users to download generated records as a CSV file.
- Performs data generation in MySQL stored procedures rather than Python.

## Technologies

- Python
- MySQL 8
- Streamlit
- `mysql-connector-python`
- Pandas

## Generated Data

Each generated record contains:

| Field | Description |
|---|---|
| `user_position` | Position of the record in the generated sequence |
| `locale` | Selected locale |
| `gender` | Generated gender category used for name and email generation |
| `full_name` | Generated full name with variations |
| `address` | Generated address |
| `latitude` | Geographic latitude |
| `longitude` | Geographic longitude |
| `height_cm` | Normally distributed height, with mean 170 cm and standard deviation 10 cm |
| `weight_kg` | Normally distributed weight, with mean 70 kg and standard deviation 15 kg |
| `eye_color` | Eye color selected according to configured probabilities |
| `phone` | Generated phone number using locale-specific formatting |
| `email` | Generated email address |

## Database Design and Stored Procedures

The project uses the `faker_db` MySQL database. Lookup tables store locale-specific names, cities, streets, email domains, phone formats, address formats, and eye colors.

The main procedure is `generate_users(seed, locale, batch_index, batch_size)`. It validates the inputs, generates each record by calling helper routines, and returns the requested batch.

Helper routines divide the work into smaller tasks:

- `gen_gender` — selects the gender category deterministically.
- `gen_name` — generates a full name with variations.
- `gen_address` — formats an address from locale-specific data.
- `gen_phone` — generates a formatted phone number.
- `gen_email` — generates an email address.
- `rand_unit` — produces a deterministic pseudo-random value.
- `rand_int` and `pick_value` — select integer values and lookup entries.
- `rand_normal` — generates normally distributed values using the Box–Muller transform.
- `rand_lat` and `rand_lon` — generate geographic coordinates.
- `rand_eye_color` — selects an eye color according to configured probabilities.
- `slugify` — converts text into a suitable email-address component.

## Reproducibility and Batches

The seed, locale, record position, and helper-specific salt determine the generated values. Using the same seed, locale, batch index, and batch size produces the same results, provided the database lookup data and stored procedure definitions remain unchanged.

The batch index and batch size determine the starting record position and the number of records returned.

## Installation and Configuration

### Requirements

- Python 3
- MySQL Server 8
- The project database, lookup data, functions, and stored procedures

### Install Python dependencies

```bash
pip install -r requirements.txt
```

### Configure the database connection

Set these environment variables to match your MySQL installation:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

For example, in Bash:

```bash
export DB_HOST='127.0.0.1'
export DB_PORT='3306'
export DB_USER='root'
export DB_PASSWORD='YOUR_MYSQL_PASSWORD'
export DB_NAME='faker_db'
```

Do not commit your real database password to the repository.

### Run the application

```bash
python -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Benchmark

**Environment:** Complete this with your operating system, CPU, RAM, and MySQL/Python versions.

**Test configuration:** Record the locale, seed, and batch size used for each measurement.

**Measured performance:** Add the actual number of records generated per second. See the Benchmark section in this README's preparation notes before submitting.

## Limitations

- Output quality depends on the lookup data provided for each locale.
- Reproducibility depends on keeping the lookup tables and stored procedure definitions unchanged.
- Generated contact details are synthetic and should not be treated as verified real-world information.

## Submission

- **Author:** Sitora Bakhronova
- **Source code:** Add your repository URL.
- **Documentation:** Add the URL to this README after publishing it.
- **Demo video:** Add your recording URL.
- **Deployed application:** Add the URL if deployment is required and completed.
