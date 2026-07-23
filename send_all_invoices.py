# from customer_lookup import get_customer_email

# from email_service.send_email import (
#     send_invoice_email
# )

# from database.db import get_connection


# def send_all():

#     conn = get_connection()

#     cursor = conn.cursor(
#         dictionary=True
#     )

#     cursor.execute("""
#         SELECT *
#         FROM invoices
#     """)

#     invoices = cursor.fetchall()

#     for invoice in invoices:

#         customer = get_customer_email(
#             invoice["customer_code"]
#         )

#         if not customer:

#             print(
#                 f"Customer not found : "
#                 f"{invoice['customer_code']}"
#             )

#             continue

#         email = customer["email"]

#         if not email:

#             print(
#                 f"No email : "
#                 f"{invoice['customer_code']}"
#             )

#             continue

#         send_invoice_email(
#             invoice,
#             email
#         )

#     cursor.close()
#     conn.close()

# import time


# from customer_lookup import get_customer_email
# from email_service.send_email import send_invoice_email

# from database.db import get_connection
# from email_service.check_email_status import already_sent, get_pending_invoices

# def send_all():
    
#     conn = get_connection()

#     cursor = conn.cursor(dictionary=True)

#     cursor.execute("""
#         SELECT *
#         FROM invoices
#     """)

#     invoices = cursor.fetchall()
    
#     # Group invoices by customer code and email
#     grouped_invoices = {}
    
#     for invoice in invoices:

#         if already_sent(invoice["id"]):

#             print(
#                 f"Already Sent : "
#                 f"{invoice['customer_code']}"
#             )

#             continue

#         customer = get_customer_email(invoice["customer_code"])
#         # print(f"Customer data for code  {customer}")
        
#         # Check if customer data exists and is returned as a list
#         if isinstance(customer, list) and len(customer) > 0:
#             customer = customer[0]  # Get the first dictionary out of the list
#         print("custoerm data email ",customer)
        
#         if not customer or "customer_email" not in customer:
#             continue
#         # print(f"Customer data for code {invoice['customer_code']}: {customer}")
#         email_address = customer["customer_email"] 
#         print(f"Email address  {invoice['customer_code']}: {email_address}")
#         if not email_address:
#             continue

#         # Group by email address as key
#         if email_address not in grouped_invoices:
#             grouped_invoices[email_address] = []
        
#         grouped_invoices[email_address].append(invoice)
#         # print(f"Grouped invoice for {email_address}: {invoice['invoice_number']}")
#     # Send grouped invoices per customer
#     for email_address, invoices_list in grouped_invoices.items():
#         result = send_invoice_email(invoices_list, email_address)
#         # print(f"Email sent to {email_address} with {len(invoices_list)} invoices. Result: {result}")
        
#         if result:
#             print(f"Email sent to {email_address}")
#             print("Waiting 10 second before next email address...")
#             time.sleep(10)  # Wait for 10 seconds before sending the next email

#     cursor.close()
#     conn.close()
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
        FROM invoices i
        JOIN customers c
            ON i.customer_code = c.customer_code
        AND i.invoice_month = c.Invoice_Month
        AND i.net_amount = c.balance
        WHERE c.balance > 0 
    """)
    invoices = cursor.fetchall()
    # print("=Fetch all invoices page=" * 90)
    print(f"invoices fetched from database: {len(invoices)}")    

    grouped_invoices = {}
    customer_cache = {}

    # -----------------------------
    # Group invoices per customer send email one by one to customer
    # -----------------------------
    # for invoice in invoices:

    #     if already_sent(invoice["id"]):
    #         continue

    #     customer_code = invoice["customer_code"]
        
    #     # Load customer emails only once
    #     if customer_code not in customer_cache:
    #         customer_cache[customer_code] = get_customer_email(customer_code)

    #     customer = customer_cache[customer_code]

    #     if customer_code not in grouped_invoices:
    #         grouped_invoices[customer_code] = {
    #             "emails": customer["emails"] if customer else None,
    #             "invoices": []
    #         }
    #         # print("group email is ",grouped_invoices[customer_code]["emails"])
    #     grouped_invoices[customer_code]["invoices"].append(invoice)

    # print("Grouped invoices Completed")

    # ==============================
    # End of the code snippet. The rest of the code is unchanged and continues with sending emails to customers based on the grouped invoices.
    # ==============================
    
    
    # ==============================
    # Start sending emails to customers based on the email grouped invoices.
    # ==============================

    # Get the email directly from this database row
    for invoice in invoices:
        if already_sent(invoice["id"]):
            continue

        row_email = invoice.get("customer_email")
        if not row_email:
            continue
            
        # Clean up any accidental leading/trailing spaces
        clean_email_key = row_email.strip()

        # Group solely by this specific email string
        if clean_email_key not in grouped_invoices:
            grouped_invoices[clean_email_key] = {
                "customer_codes": set(),
                "invoices": []
            }

        grouped_invoices[clean_email_key]["customer_codes"].add(invoice["customer_code"])
        grouped_invoices[clean_email_key]["invoices"].append(invoice)

    print("Grouped invoices completed in send_all invoices function")
    
    # for invoice in invoices:

    #     # if already_sent(invoice["id"]):
    #     #     continue

    #     customer_code = invoice["customer_code"]

    #     # Load emails only once
    #     if customer_code not in customer_cache:
    #         customer_cache[customer_code] = get_customer_email(customer_code)

    #     customer = customer_cache[customer_code]

    #     if not customer:
    #         continue

    #     # customer["emails"] is a list
    #     for email in customer["emails"]:

    #         if email not in grouped_invoices:
    #             grouped_invoices[email] = {
    #                 "customer_codes": set(),
    #                 "invoices": []
    #             }

    #         grouped_invoices[email]["customer_codes"].add(customer_code)
    #         grouped_invoices[email]["invoices"].append(invoice)

    # print("Grouped invoices completed in send_all invoices function")
    
   
    # ==============================
    # end sending emails to customers based on the email grouped invoices.
    # ========================




    # -----------------------------
    # Send one email per customer
    # -----------------------------
    for email, data in grouped_invoices.items():
        # print("groupup item customer code",customer_code)
        print("Invoices :", len(data["invoices"]))
        # print("groupup item",email)
        # print("groupup item",data)
        # email = customer_code  # Here, customer_code is actually the email address in the grouped

        print("=" * 60)
        # print("Customer code from Send All invoices :", customer_code)
        # print("Emails   :", data["emails"])
        
        # print(data["emails"])
        # print(type(data["emails"]))
        # print(type(data["emails"][0]))

        # result = send_invoice_email(
        #     data["invoices"],
        #     data["emails"]
        # )

        # if result:
        #     print(f"Email sent for {customer_code}")
        # print("Email :", email)
        # print("Customers :", list(data["customer_codes"]))
        # print("Invoices :", len(data["invoices"]))

        # print("data",data["invoices"])
        # print("data",data["customer_codes"])
        # print("email",email)
        
        
        result = send_invoice_email(
            data["invoices"],
            email
        )
        if result:
            print(f"Email sent to {email}")
            print("Waiting 10 seconds before next email address...")
            time.sleep(10)
            # print("=End Send all invoices page=" * 90)
            print("=" * 60)
    cursor.close()
    conn.close()