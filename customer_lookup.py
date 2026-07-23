from database.db import get_connection


def get_customer_email(customer_code):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM customers
        WHERE customer_code=%s
    """, (customer_code,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return{
        "customer_code": customer_code,
        "emails": sorted({
            row["customer_email"].strip()
            for row in rows
        })
    }