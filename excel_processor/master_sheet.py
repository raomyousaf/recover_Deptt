import pandas as pd
import numpy as np
from database.db import get_connection

def import_master_sheet(file_path):

    df = pd.read_excel(file_path)
    print(f"Master sheet loaded with {len(df)} records.")
    print("df",df)
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():

        invoice_month = row['Invoice Month']
        # print("invoice_month",invoice_month)

        try:
            invoice_month = pd.to_datetime(invoice_month).strftime('%B-%Y')
        except:
            invoice_month = str(invoice_month).strip()
        Invoice_Month = invoice_month
        customer_code = str(row['Customer Code']).strip() if pd.notna(row['Customer Code']) else None
        customer_name = str(row['Customer']).strip() if pd.notna(row['Customer']) else None
        station = str(row['Station']).strip() if pd.notna(row['Station']) else None
        balance = row['Balance'] if pd.notna(row['Balance']) else None
        customer_email = str(row['customer_email']).strip() if pd.notna(row['customer_email']) else None
        rec_off = str(row['Collection Person']).strip() if pd.notna(row['Collection Person']) else None
        # print("recover person",rec_off)
        sql = """
        INSERT INTO customers
        (Invoice_Month,customer_code, customer_name, station, customer_email, balance, rec_off)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
        customer_name=VALUES(customer_name),
        station=VALUES(station),
        customer_email=VALUES(customer_email),
        balance=VALUES(balance),
        rec_off=VALUES(rec_off),
        Invoice_Month=VALUES(Invoice_Month)
        """

        cursor.execute(sql, (
            Invoice_Month,
            customer_code,
            customer_name,
            station,
            customer_email,
            balance,
            rec_off
        ))

    conn.commit()
    cursor.close()
    conn.close()

    print("Master sheet imported.")