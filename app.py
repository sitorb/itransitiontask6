
import os

import mysql.connector
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Fake Contact Generator",
    page_icon="👤",
    layout="wide",
)

st.title("Fake Contact Information Generator")
st.write(
    "Generate reproducible fake contact information "
    "using MySQL stored procedures."
)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "faker_db"),
}

with st.form("generator_form"):
    locale = st.selectbox(
        "Locale",
        options=["en_US", "de_DE"],
    )

    seed = st.number_input(
        "Seed",
        min_value=0,
        max_value=2147483647,
        value=42,
        step=1,
    )

    batch_index = st.number_input(
        "Batch index",
        min_value=0,
        max_value=1000000,
        value=0,
        step=1,
    )

    batch_size = st.number_input(
        "Number of users",
        min_value=1,
        max_value=1000,
        value=10,
        step=1,
    )

    submitted = st.form_submit_button("Generate users")

if submitted:
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        cursor.callproc(
            "generate_users",
            (
                int(seed),
                locale,
                int(batch_index),
                int(batch_size),
            ),
        )

        rows = []
        for result in cursor.stored_results():
            rows.extend(result.fetchall())

        if rows:
            df = pd.DataFrame(rows)

            st.success(f"Generated {len(df)} users.")
            st.dataframe(df, use_container_width=True)

            csv_data = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "Download CSV",
                data=csv_data,
                file_name=f"fake_users_{locale}.csv",
                mime="text/csv",
            )
        else:
            st.warning("The procedure returned no users.")

    except mysql.connector.Error as error:
        st.error(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
