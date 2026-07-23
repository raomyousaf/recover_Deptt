
import os
import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import time
import time

from database.email_log import save_email_log
from config import SMTP_CONFIG

# from check_email_status import already_sent

from database.db import get_connection

def send_invoice_email(invoices, email_addresses):
    """
    Send all invoices for a customer in a single email.
    invoices: list of invoice dictionaries or a single invoice dictionary
    """
    conn = None
    cursor = None
    ph_no = None
    # rec_off = None
    # print("Email address:", email_address)
    
    
    # Handle both single invoice and list of invoices
    if not isinstance(invoices, list):
        invoices = [invoices]
        print(f"Single invoice provided. Converted to list: {invoices}")
    
    if not invoices:
        return False

    try:
        # print(f"send email page Preparing to send email to {email_addresses} for {len(invoices)} invoices.")

      
      
        msg = MIMEMultipart()
        if isinstance(email_addresses, list):
            msg["To"] = ", ".join(email_addresses)
        else:
             msg["To"] = email_addresses
        email_addresses = email_addresses
        # print(f"Email addresses: {email_addresses}")
        # print("msg [to]:", msg["To"])



        msg["From"] = SMTP_CONFIG["sender"]
        # msg["To"] = email_address
        msg["Cc"] = "farooq.siddiqui@sospakistan.net,callcenter@sospakistan.com,recovery@sospakistan.net"  # CC to the same address for record
        
        # Create subject with customer name and months
        months = ", ".join([inv['invoice_month'] for inv in invoices])
        customer_name = invoices[0]['customer_name']
        msg["Subject"] = f"Invoices - {customer_name} - {months}"

        # Create alternative part for text and HTML
        msg_alternative = MIMEMultipart("alternative")
        msg.attach(msg_alternative)

        # Plain text version
        plain_text = f"""
Dear Sir/Madam,

Please find attached invoices for {customer_name}:

"""
        for inv in invoices:
            plain_text += f"\n- {inv['invoice_month']}: PKR {inv.get('balance', 0)}"
        
        plain_text += """

Kindly arrange payment at the earliest.

If payment has already been made, please share the payment evidence.

While making payment kindly mention your Branch Code in the memo/reference.

Regards,

Nadia Zafar
Recovery Officer
Credit & Collection Department
"""
               # 1. Establish connection and cursor FIRST
        conn = get_connection()
        if conn is None:
            print("FAILED: Database connection could not be established.")
            return

        cursor = conn.cursor(dictionary=True)
        # print("First invoice:")
        # print(invoices[0])
        myrec_off = invoices[0].get('Rec_off', '').strip()
        # myrec_off = invoices[0].get('Rec_off', '') 
        # customer_name = invoices[0].get('customer_name', '') if invoices else "Valued Customer"
        # print(f"Recovery Officers: {myrec_off}")
        # print(invoices[0].keys())
        officer_contacts = {
            "Nadia Zafar": {
                "contact": "0307-5556089",
                "Email": "callcenter@sospakistan.com",
            },
            "Iqra Tauheed": {
                "contact": "0307-5554282",
                "Email": "callcenter@sospakistan.com"
            },
            "Fareeha Mushtaq": {
                "contact": "061-4480713",
                "Email": "callcenter@sospakistan.com"
            }
        }
        # print("contact list:", officer_contacts)
        contact_info = officer_contacts.get(myrec_off, {"contact": "N/A", "Email": "N/A"})
        # print("contact_info", contact_info)
        contact = contact_info["contact"]
        email = contact_info["Email"]
        
        # print(f"Officer: {myrec_off} | Phone: {contact} | Email: {email}")

        
        
        # myrec_off = officer_contacts.get(
        #     myrec_off
        #      # {"Contact": "", "Email": ""}
        # )
        # contact  = contact["contact"]
        # email = contact["Email"]
           
        
        # print(f"Contact details for {myrec_off}: {contact}")
                # landline_no = contact["landline"]
        
        # print(f"Contact: {contact}")

        # print("Invoices count:", len(invoices))

        # for inv in invoices:
        #     print(
        #         inv["customer_code"],
        #         inv["customer_name"],
        #         repr(inv.get("Rec_off"))
        #     )

        # print("Selected officer:", repr(myrec_off))
        # print("Lookup result:", officer_contacts.get(myrec_off))

        # Build table rows for all invoices
        table_rows = ""
        customer_codes = list(set(invoice["customer_code"]
            for invoice in invoices
        ))

        # placeholders = ",".join(["%s"] * len(customer_codes))
        
       
        for invoice in invoices:
            # print(f"Processing invoice for customer Name: {invoice['customer_name']}, Month: {invoice['invoice_month']}, rec_off: {invoice.get('Rec_off', '')}")
            # print(f"Invoice: {invoice['invoice_month']}")
            # Format net_amount with commas and two decimal places
            net_amount_raw = invoice.get('net_amount', '')
            try:
                net_amount_formatted = f"{float(net_amount_raw):,.2f}"
            except (ValueError, TypeError):
                net_amount_formatted = net_amount_raw
            table_rows += f"""<tr>
            
            <td>{invoice.get('invoice_month', '')}</td>
            <td>{invoice.get('customer_code', '')}</td>
            <td>{invoice.get('customer_name', '')}</td>
            <td>PKR {net_amount_formatted}</td>
          
</tr>
"""

        # HTML version
        html_body = f"""
<html>
<body style="font-family:Calibri,Arial,sans-serif;background-color:#f5f5f5;padding:20px;">

<table width="700" align="center" cellpadding="0" cellspacing="0"
       style="background:#ffffff;border:1px solid #dcdcdc;">

<tr>
    <td style="background:#003366;color:white;padding:15px;">
        <h2 style="margin:0;">Reminder Invoice Submission</h2>
    </td>
</tr>

<tr>
<td style="padding:20px;">

<p>Dear Sir/Madam,</p>

<p>
Please find attached invoices for <strong>{customer_name}</strong>.
</p>

<p>
You are requested to please pay the attached invoices at your earliest convenience. 
If the payment has already been made, kindly share the payment advice/evidence for our records.
</p>

<p>
While making payment Please mention your
<strong>Branch Code</strong>
in the memo/reference to facilitate reconciliation..
</p>
<br>
<p>
<table border="1" cellpadding="10" cellspacing="0" style="border-collapse:collapse;width:100%;">
<tr>
<td style="background:#e0e0e0;padding:10px;"><strong>Invoice Month</strong></td>
<td style="background:#e0e0e0;padding:10px;"><strong>Branch Code</strong></td>
<td style="background:#e0e0e0;padding:10px;"><strong>Customer Name</strong></td>
<td style="background:#e0e0e0;padding:10px;"><strong>Amount</strong></td>
</tr>
{table_rows}
</table>
</p>

<br>

<p>Regards,</p>

<p>
<strong> {myrec_off} </strong>  <br>
Contact No. {contact}<br>
Email: {email}<br>
Recovery Officer<br>
Credit & Collection Department
</p>

</td>
</tr>

<tr>
<td style="background:#f0f0f0;padding:10px;text-align:center;font-size:12px;color:#666;">
This is a system generated email (Rao).
</td>
</tr>

</table>

</body>
</html>
"""

        msg_alternative.attach(MIMEText(plain_text, "plain"))
        msg_alternative.attach(MIMEText(html_body, "html"))

        # Attach all invoice PDFs
        for invoice in invoices:
            # print(f"Attaching file: {invoice['pdf_file']}")
            file_path = invoice["pdf_file"]
            # print(f"Checking if file exists: {os.path.exists(file_path)}")

            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(file_path)}"
                )
                msg.attach(part)

        server = smtplib.SMTP_SSL(
            SMTP_CONFIG["smtp_server"],
            SMTP_CONFIG["smtp_port"]
        )

        server.login(
            SMTP_CONFIG["sender"],
            SMTP_CONFIG["password"]
        )

        
        server.send_message(msg)
        server.quit()
        
        
        
        
        
        # print(f"Sleeping for {EMAIL_DELAY} seconds...")
        # time.sleep(EMAIL_DELAY)

        # Log all invoices as sent successfully
        # print("email log", invoice["customer_code"],
        #         invoice["customer_name"],
        #         email_address,
        #         invoice["invoice_month"],
        #         invoice["pdf_file"],)
        
        for invoice in invoices:
            save_email_log(
                invoice["customer_code"],
                invoice["customer_name"],
                email_addresses,
                invoice["invoice_month"],
                invoice["pdf_file"],
                "SUCCESS"
            )

        print(
            f"SUCCESS : {email_addresses,} - {len(invoices)} invoices sent"
        )
        # import msvcrt

        # print("Press any key to continue...")
        # msvcrt.getch()
        
        return True
        
    except Exception as e:

        # Log all invoices as failed
        for invoice in invoices:
            save_email_log(
                invoice["customer_code"],
                invoice["customer_name"],
                email_addresses,
                invoice["invoice_month"],
                invoice["pdf_file"],
                "FAILED",
                str(e)
            )

        print(
            f"FAILED : {email_addresses} - Error: {str(e)}"
        )

        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




