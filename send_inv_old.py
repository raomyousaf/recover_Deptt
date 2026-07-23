import time


from customer_lookup import get_customer_email
from email_service.send_email import send_invoice_email

from database.db import get_connection
from email_service.check_email_status import already_sent, get_pending_invoices

def send_all():
    
    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM invoices
    """)

    invoices = cursor.fetchall()
    
    # Group invoices by customer code and email
    grouped_invoices = {}

    for invoice in invoices:

        if already_sent(invoice["id"]):
            continue

        customer_code = invoice["customer_code"]

        # Create the group only once
        if customer_code not in grouped_invoices:

            customer = get_customer_email(customer_code)

            if not customer:
                continue

            # Get unique email(s)
            emails = sorted({
                row["customer_email"].strip()
                for row in customer
                if row.get("customer_email")
            })
            print("email is ",emails[0])
            grouped_invoices[customer_code] = {
                "emails": emails[0],
                "invoices": []
            }

        # Add every invoice to that customer
        grouped_invoices[customer_code]["invoices"].append(invoice)
        # print(f"Email sent to {emails}")
        # print("Waiting 10 second before next email address...")
                                    
        for customer_code, data in grouped_invoices.items():

            # print("customer data:", customer_code)
            print("emails:", data["emails"])
            # print("invoices:", data["invoices"])

            result = send_invoice_email(
                data["invoices"],
                data["emails"]
            )

            time.sleep(10)        
                # if result:
                #     time.sleep(10)  # Wait for 10 seconds before sending the next email

    cursor.close()
    conn.close()

