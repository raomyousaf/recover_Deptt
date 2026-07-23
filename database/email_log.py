from database.db import get_connection
from datetime import datetime


def save_email_log(
        customer_code,
        customer_name,
        email_address,
        invoice_month,
        pdf_file,
        status,
        error_message="",
        retry_count=0
        
        
):
    # print("Saving email log for customer_code:", customer_code, email_address, invoice_month, pdf_file, status, error_message)
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO email_logs
    (
        customer_code,
        customer_name,
        email,
        invoice_month,
        pdf_file,
        status,
        error_message,
        sent_time,
        retry_count
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (
        customer_code,
        customer_name,
        email_address,
        invoice_month,
        pdf_file,
        status,
        error_message,
        datetime.now(),
        retry_count
    ))

    conn.commit()

    cursor.close()
    conn.close()
    
    
    