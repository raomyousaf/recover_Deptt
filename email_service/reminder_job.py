from datetime import datetime
from datetime import timedelta

from database.db import get_connection
from email_service.send_email import send_reminder_email

def process_reminders():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""

    SELECT *
    FROM invoices i
    JOIN customers c
    ON i.customer_code=c.customer_code

    WHERE c.balance > 0

    """)

    rows = cursor.fetchall()

    for row in rows:

        if row["last_reminder"]:

            diff = (
                datetime.now()
                - row["last_reminder"]
            )

            if diff.days < 1:
                continue

        send_reminder_email(
            row,
            row["email"]
        )

        cursor.execute("""

        UPDATE invoices

        SET
        reminder_count=
        reminder_count+1,

        last_reminder=NOW()

        WHERE id=%s

        """, (row["id"],))

        conn.commit()

    cursor.close()
    conn.close()