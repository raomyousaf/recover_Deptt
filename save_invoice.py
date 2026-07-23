import mysql

from database.db import get_connection
import pandas as pd

def save_invoice(invoice):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    print(f"Saving invoice {invoice['invoice_number']} for customer {invoice['customer_name']} and invoice month: {invoice['invoice_month']} and net amount: {invoice['net_amount']} and invoice: {invoice['invoice_number']} to the database.")    
    
    # Get rec_off from customers table based on customer_code
    rec_off = None
    balance = None
    customer_code = None
    # cursor.execute("SELECT rec_off FROM customers WHERE customer_code = %s", (invoice.get("customer_code"),))
    # cursor.execute(""" select * from customers where customer_code = %s """, (invoice.get("customer_code"),))
    # customer = cursor.fetchall()
    
    cursor.execute("""
    SELECT customer_code,rec_off, balance, Invoice_Month
    FROM customers
    WHERE customer_code = %s
    AND Invoice_Month = %s
""", (
    invoice.get("customer_code"),
    invoice.get("invoice_month")
))

    customer = cursor.fetchall()
    
    if customer:
        rec_off = customer[0].get("rec_off")
        balance = customer[0].get("balance")
        customer_code = customer[0].get("customer_code")

    print(f"rec_off: {rec_off}, balance: {balance}, my customer_code: {customer_code}")

    # print("Customer fetch result:", customer)
    if customer:
        rec_off = customer[0].get("rec_off")
        # print(f"Found customer for code: {customer[0].get('customer_code')}, rec_off: {rec_off}")
    else:
        rec_off = None
        print(f"No customer found for code: {invoice.get('customer_code')}")

    if balance is None or float(balance) <= 0:
        print(
            f"Skipping invoice {invoice.get('invoice_number')} "
            f"- zero or negative balance for month {invoice.get('invoice_month')}"
        )
        return    
        
    try:
        sql = """
    INSERT INTO invoices
    (
        customer_code,
        customer_name,
        invoice_month,
        invoice_number,
        net_amount,
        pdf_file,
        rec_off
        
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

        cursor.execute(sql, (
            # invoice["customer_code"] if pd.notna(invoice.get("customer_code")) else None,
            customer_code if pd.notna(customer_code) else None,
            invoice["customer_name"] if pd.notna(invoice.get("customer_name")) else None,
            invoice["invoice_month"] if pd.notna(invoice.get("invoice_month")) else None,
            invoice["invoice_number"] if pd.notna(invoice.get("invoice_number")) else None,
            invoice["net_amount"] if pd.notna(invoice.get("net_amount")) else None,
            invoice["pdf_file"] if pd.notna(invoice.get("pdf_file")) else None,
            rec_off
        ))
        conn.commit()

        # print(
        #     f"Saved invoice {invoice['invoice_number']} "
        #     f"for customer {invoice['customer_name']} "
        #     f"with rec_off: {rec_off} "
        #     f"and net_amount: {invoice['net_amount']} "
        #     f"to the database."
        # )

    except mysql.connector.IntegrityError as e:
        conn.rollback()
        print(f"Failed to save invoice {invoice['invoice_number']} for customer {invoice['customer_name']} due to integrity error.")
        print("IntegrityError:", e)

    except mysql.connector.DataError as e:
        conn.rollback()
        print(f"Failed to save invoice {invoice['invoice_number']} for customer {invoice['customer_name']} due to data error.")
        print("DataError:", e)

    except mysql.connector.ProgrammingError as e:
        conn.rollback()
        print(f"Failed to save invoice {invoice['invoice_number']} for customer {invoice['customer_name']} due to programming error.")
        print("ProgrammingError:", e)

    except mysql.connector.DatabaseError as e:
        conn.rollback()
        print(f"Failed to save invoice {invoice['invoice_number']} for customer {invoice['customer_name']} due to database error.")
        print("DatabaseError:", e)

    except Exception as e:
        conn.rollback()
        print("Unexpected Error:", e)

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()
    # except mysql.connector.DataError as e:
    #     conn.rollback()
    # print("DataError:", e)

    
    
   
