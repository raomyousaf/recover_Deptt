from pdf_processor.split_pdf import split_invoices
from excel_processor.master_sheet import import_master_sheet
from save_invoice import save_invoice
from send_all_invoices import send_all

MASTER_SHEET = "Master_sheet_23july.xlsx"
PDF_FILE = "invoices.pdf"

import_master_sheet(MASTER_SHEET)

invoices = split_invoices(PDF_FILE)
print(f"Extracted {len(invoices)} invoices from PDF.")
for invoice in invoices:
    save_invoice(invoice)
print("All invoices saved to the database.",invoices)
print("Phase 1 Completed")
# import msvcrt

# print("Press any key to continue...")
# msvcrt.getch()
        
send_all()
print("Phase 2 Completed")

