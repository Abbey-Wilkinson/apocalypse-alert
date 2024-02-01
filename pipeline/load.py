from os import environ

from dotenv import load_dotenv

import snowflake.connector

LOCAL_FILE_PATH = "mock_air_reading.csv"
# Table's stage
STAGE_NAME = "@%AIR_READING"


def get_connection() -> snowflake.connector.connection:
    """
    Returns a connection to the specified snowflake database.
    """
    try:
        conn = snowflake.connector.connect(
            user=environ["USERNAME"],
            password=environ["PASSWORD"],
            account=environ["ACCOUNT_NAME"],
            database=environ["DATABASE"],
            warehouse=environ["WAREHOUSE"],
            schema=environ["SCHEMA"]
        )
        return conn

    except Exception as e:
        print("An unexpected error occurred:", str(e))


def load_data(conn: snowflake.connector.connection) -> None:
    """
    Loads csv data from the local machine and uploads it to the database
    """
    try:
        cur = conn.cursor()
        put_command = f"PUT file://{LOCAL_FILE_PATH} {STAGE_NAME} auto_compress=true"
        cur.execute(put_command)

        copy_command = f"""
            COPY INTO APOCALYPSE_ALERT.PUBLIC.AIR_READING (AT, COUNTRY, GENERAL_AQI)
            FROM {STAGE_NAME}/mock_air_reading.csv
            FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
            ON_ERROR = 'CONTINUE';
        """
        cur.execute(copy_command)
        conn.commit()

    except Exception as e:
        print(e)

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    load_data(conn)
