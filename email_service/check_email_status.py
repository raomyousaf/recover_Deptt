from database.db import get_connection

def already_sent(invoice_id):
    

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM email_logs
        WHERE invoice_id=%s
        AND status='SUCCESS'
        LIMIT 1
    """, (invoice_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row is not None



def get_pending_invoices():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
        SELECT *
        FROM customers c
        JOIN invoices i
        ON c.customer_code=i.customer_code
        WHERE c.balance > 0
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows