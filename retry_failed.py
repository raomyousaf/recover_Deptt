from database.db import get_connection


def get_failed_emails():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT *
        FROM email_logs
        WHERE status='FAILED'
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows