# from email.mime import text

# import fitz
# import re
# import os

# OUTPUT_FOLDER = "generated_invoices"

# os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# def split_invoices(pdf_file):

#     pdf = fitz.open(pdf_file)

#     invoices = []
#     page_groups = {}  # Group pages by customer_code + month
#     page_info = []    # Store info for each page

#     # First pass: extract info from all pages
#     for page_no in range(len(pdf)):

#         page = pdf[page_no]
#         text = page.get_text()

#         print("=" * 50)
#         print(f"Processing page {page_no + 1}")
        
#         # Extract customer name - handle flexible whitespace
#         customer_match = re.search(
#             r'Customer\s+Name\s*:\s*(.*?)(?=SALES TAX|Invoice|$)',
#             text,
#             re.IGNORECASE | re.DOTALL
#         )

#         # Extract month - look after "Invoice Month" label
#         month_match = re.search(
#             r'Invoice\s+Month\s*:\s*\n?\s*((?:January|February|March|April|May|June|July|August|September|October|November|December)\s*-\s*\d{4})',
#             text,
#             re.IGNORECASE
#         )
#         # Fallback: look for month-year pattern if label not found
#         if not month_match:
#             month_match = re.search(
#                 r'\n\s*((?:January|February|March|April|May|June|July|August|September|October|November|December)\s*-\s*\d{4})',
#                 text,
#                 re.IGNORECASE
#             )

#         # Extract invoice number
#         invoice_match = re.search(
#             r'Invoice\s+#\s*:\s*([\w\-]*)',
#             text,
#             re.IGNORECASE
#         )

#         # Extract net amount - look for "Net Amount" followed by digits
#         amount_match = re.search(
#             r'Net Amount\s*[\n\s]*([\d,]+)',
#             text,
#             re.IGNORECASE
#         )

#         if not customer_match:
#             continue

#         customer_name = customer_match.group(1).strip()

#         # Extract any customer code (NBP-, SOS-, etc.)
#         code_match = re.search(
#             r'([A-Z]+\-\d+)',
#             customer_name
#         )

#         if not code_match:
#             continue

#         customer_code = code_match.group(1)
        
#         # Extract region name - get the last location/city name
#         # Example: "NBP-5315 - NBP IBB Wapda Town Multan" -> "Multan"
#         region_match = re.search(
#             r'(?:NBP|SOS)\s+[A-Z]+\s+(.+)\s+(\w+)$',
#             customer_name
#         )
#         region_name = region_match.group(2) if region_match else "Unknown"

#         invoice_month = (
#             month_match.group(1).strip()
#             if month_match else "Unknown"
#         )
        
#         # Convert month to short format (April-2026 -> April-26)
#         if '-' in invoice_month and invoice_month != "Unknown":
#             parts = invoice_month.split('-')
#             month_short = f"{parts[0].strip()}-{parts[1].strip()[-2:]}"
#         else:
#             month_short = invoice_month



        
#         # invoice_number = (
#         #     invoice_match.group(1).strip()
#         #     if invoice_match else ""
#         # )
#         # fix inoice number 
#         invoice_match = re.search(
#             r'Invoice\s*#\s*:\s*([\s\S]*?)\n([A-Z0-9\/\-]+)',
#             text,
#             re.IGNORECASE
#         )

#         invoice_number = (
#             invoice_match.group(2).strip()
#             if invoice_match else ""
#         )
        
        
#         # net_amount = (
#         #     amount_match.group(1).replace(",", "")
#         #     if amount_match else "0"
#         # )
        
        
        
#         # If net amount not found on current page, look on the last page of the group
#         last_page = 0
#         last_text = 0
#         pages = [page_no]
        
        
#         last_page = pdf[pages[-1]]
#         last_text = last_page.get_text()

#         amount_match = re.search(
#             r'Net\s+Amount\s+([\d,]+)',
#             last_text,
#             re.IGNORECASE
#         )

#         net_amount = (
#             amount_match.group(1).replace(",", "")
#             if amount_match else "0"
#         )
        
#         print(f"Extracted info - Customer Code: {customer_code}, Customer Name: {customer_name}, Region: {region_name}, Invoice Month: {invoice_month}, Invoice Number: {invoice_number}, Net Amount: {net_amount}")
#         # Create grouping key
#         group_key = f"{customer_code}_{month_short}"
        
#         # Store page info
#         page_info.append({
#             "page_no": page_no,
#             "customer_code": customer_code,
#             "customer_name": customer_name,
#             "region_name": region_name,
#             "invoice_month": invoice_month,
#             "month_short": month_short,
#             "invoice_number": invoice_number,
#             "net_amount": net_amount,
#             "group_key": group_key
#         })
#         print(f"page store Extracted info on  - Customer Code: {customer_code}, Customer Name: {customer_name}, Region: {region_name}, Invoice Month: {invoice_month}, Invoice Number: {invoice_number}, Net Amount: {net_amount}")
#         # Group pages by customer_code + month
#         if group_key not in page_groups:
#             page_groups[group_key] = {
#                 "pages": [],
#                 "first_info": {
#                     "customer_code": customer_code,
#                     "customer_name": customer_name,
#                     "region_name": region_name,
#                     "invoice_month": invoice_month,
#                     "month_short": month_short,
#                     "invoice_number": None,
#                     "net_amount": None
#                 }
#             }
        
#         page_groups[group_key]["pages"].append(page_no)

#     # Second pass: create single PDF for each group
#     for group_key, group_data in page_groups.items():
#         pages = group_data["pages"]
#         last_page_no = pages[-1]
#         last_text = pdf[last_page_no].get_text()
#         info = group_data["first_info"]
        
#         # Create filename with region name
#         filename = (
#     f"{info.get('customer_code', 'UNKNOWN')}-"
#     f"{info.get('month_short', 'UNKNOWN')}.pdf"
# )

#         output_pdf = os.path.join(
#             OUTPUT_FOLDER,
#             filename
#         )

#         # Create new PDF with all pages for this group
#         new_pdf = fitz.open()
#         for page_no in pages:
#             new_pdf.insert_pdf(
#                 pdf,
#                 from_page=page_no,
#                 to_page=page_no
#             )

#         new_pdf.save(output_pdf)
#         new_pdf.close()
        
        
        
#         amount_match = re.search(
#                 r'Net\s+Amount\s+([\d,]+)',
#                 last_text,
#                 re.IGNORECASE
#             )

#     net_amount = (
#                 amount_match.group(1).replace(",", "")
#                 if amount_match else "0"
#             )

#     info["net_amount"] = net_amount

# # Then when creat

#     invoices.append({
#             "customer_code": info['customer_code'],
#             "customer_name": info['customer_name'],
#             "region_name": info['region_name'],
#             "invoice_month": info['invoice_month'],
#             "invoice_number": info['invoice_number'],
#             "net_amount": info['net_amount'],
#             "pdf_file": output_pdf,
#             "page_count": len(pages)
#         })
#     print(f"invoices.append - Customer Code: {info['customer_code']}, Customer Name: {info['customer_name']}, Region: {info['region_name']}, Invoice Month: {info['invoice_month']}, Invoice Number: {info['invoice_number']}, Net Amount: {info['net_amount']}")
#     print(f"Created: {output_pdf} (pages: {len(pages)})")

#     pdf.close()

#     return invoices

from email.mime import text
import fitz
import re
import os

OUTPUT_FOLDER = "generated_invoices"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def split_invoices(pdf_file):
    pdf = fitz.open(pdf_file)
    invoices = []
    page_groups = {}  # Group pages by customer_code + month
    page_info = []    # Store info for each page

    # Regex to find all matching months on a page
    month_pattern = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s*-\s*\d{4}'

    # First pass: extract info from all pages
    for page_no in range(len(pdf)):
        page = pdf[page_no]
        text = page.get_text()

        print("=" * 50)
        print(f"Processing page {page_no + 1}")
        
        # matches = list(re.finditer(month_pattern, text, re.IGNORECASE))

        # for m in matches:
        #     # print(
        #     #     m.group(0),
        #     #     "position:",
        #     #     m.start()
        #     # )
        #     print(f"Found month: {m.group(0)} at position: {m.start()} on page {page_no + 1}")
        #     # print("matches:", matches)        
        
        # Extract customer name - handle flexible whitespace
        customer_match = re.search(
            r'Customer\s+Name\s*:\s*(.*?)(?=SALES TAX|Invoice|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )
    
        if not customer_match:
            continue

        customer_name = customer_match.group(1).strip()

        # Extract any customer code (NBP-, SOS-, etc.)
        code_match = re.search(r'([A-Z]+\-\d+)', customer_name)
        if not code_match:
            continue

        customer_code = code_match.group(1)
        
        # Extract region name
        region_match = re.search(r'(?:NBP|SOS)\s+[A-Z]+\s+(.+)\s+(\w+)$', customer_name)
        region_name = region_match.group(2) if region_match else "Unknown"
# ================================================================================================
        # # --- FIX: Only save the last month value ---
        all_months = re.findall(month_pattern, text, re.IGNORECASE)
        if all_months:
            invoice_month = all_months[-1].strip()  # Selects the absolute last match (e.g., May)
        else:
            invoice_month = "Unknown"
        
        # ==========================================
# Extract Invoice Month using Coordinates
# ==========================================

        # MONTH_X1 = 96
        # MONTH_Y1 = 710
        # MONTH_X2 = 211
        # MONTH_Y2 = 724

        # words = page.get_text("words")

        # text_in_box = []

        # for word in words:

        #     x0, y0, x1, y1, txt, *_ = word

        #     if (
        #         x0 >= MONTH_X1 and
        #         x1 <= MONTH_X2 and
        #         y0 >= MONTH_Y1 and
        #         y1 <= MONTH_Y2
        #     ):
        #         text_in_box.append(txt)

        # invoice_text = " ".join(text_in_box).strip()

        # print("Invoice Box Text:", invoice_text)

        # month_pattern = (
        #     r"(January|February|March|April|May|June|July|August|September|"
        #     r"October|November|December)\s*-\s*\d{4}"
        # )

        # match = re.search(month_pattern, invoice_text, re.IGNORECASE)

        # if match:
        #     invoice_month = match.group(0).title()
        # else:
        #     invoice_month = "Unknown"

        # print("Invoice Month:", invoice_month)
# ================================================================================================
        # Convert month to short format (April-2026 -> April-26)
        if '-' in invoice_month and invoice_month != "Unknown":
            parts = invoice_month.split('-')
            month_short = f"{parts[0].strip()}-{parts[1].strip()[-2:]}"
        else:
            month_short = invoice_month

        # Fix invoice number 
        invoice_match = re.search(
            r'Invoice\s*#\s*:\s*([\s\S]*?)\n([A-Z0-9\/\-]+)',
            text,
            re.IGNORECASE
        )
        invoice_number = invoice_match.group(2).strip() if invoice_match else ""
        
        # Net amount extraction for current page
        amount_match = re.search(r'Net\s+Amount\s+([\d,]+)', text, re.IGNORECASE)
        net_amount = amount_match.group(1).replace(",", "") if amount_match else "0"
        
        # print(f"Extracted info - Customer Code: {customer_code}, Customer Name: {customer_name}, Region: {region_name}, Invoice Month: {invoice_month}, Invoice Number: {invoice_number}, Net Amount: {net_amount}")
        
        # Create grouping key
        
        
        
        group_key = f"{customer_code}_{month_short}"
        
        # print(f"Page {page_no + 1}"
        # )

        # print(
        #     f"Invoice Month : {invoice_month}"
        # )

        # print(
        #     f"Group Key : {group_key}"
        # )
                
        
        # Store page info
        page_info.append({
            "page_no": page_no,
            "customer_code": customer_code,
            "customer_name": customer_name,
            "region_name": region_name,
            "invoice_month": invoice_month,
            "month_short": month_short,
            "invoice_number": invoice_number,
            "net_amount": net_amount,
            "group_key": group_key
        })

        # Group pages by customer_code + month
        if group_key not in page_groups:
            page_groups[group_key] = {
                "pages": [],
                "first_info": {
                    "customer_code": customer_code,
                    "customer_name": customer_name,
                    "region_name": region_name,
                    "invoice_month": invoice_month,
                    "month_short": month_short,
                    "invoice_number": invoice_number,
                    "net_amount": None
                }
            }
        
        page_groups[group_key]["pages"].append(page_no)
        
        # print("\n========== GROUP SUMMARY ==========")

        # for key, value in page_groups.items():
        #     print(key, "->", value["pages"])

        # print("=============A======================")


    print("\n--- Phase 2: Generating Split Invoice PDFs ---")
    # Second pass: create single PDF for each group
    for group_key, group_data in page_groups.items():
        pages = group_data["pages"]
        last_page_no = pages[-1]
        last_text = pdf[last_page_no].get_text()
        info = group_data["first_info"]
        
        # Create filename
        filename = f"{info.get('customer_code', 'UNKNOWN')}-{info.get('month_short', 'UNKNOWN')}.pdf"
        output_pdf = os.path.join(OUTPUT_FOLDER, filename)

        # Create new PDF with all pages for this group
        new_pdf = fitz.open()
        for page_no in pages:
            new_pdf.insert_pdf(pdf, from_page=page_no, to_page=page_no)

        new_pdf.save(output_pdf)
        new_pdf.close()
        
        # Recalculate net amount from the last page of the group
        final_amount_match = re.search(r'Net\s+Amount\s+([\d,]+)', last_text, re.IGNORECASE)
        info["net_amount"] = final_amount_match.group(1).replace(",", "") if final_amount_match else "0"

        invoices.append({
            "customer_code": info['customer_code'],
            "customer_name": info['customer_name'],
            "region_name": info['region_name'],
            "invoice_month": info['invoice_month'],
            "invoice_number": info['invoice_number'],
            "net_amount": info['net_amount'],
            "pdf_file": output_pdf,
            "page_count": len(pages)
        })
        
        print(f"invoices.append - Customer Code: {info['customer_code']}, Customer Name: {info['customer_name']}, Region: {info['region_name']}, Invoice Month: {info['invoice_month']}, Invoice Number: {info['invoice_number']}, Net Amount: {info['net_amount']}")
        print(f"Created: {output_pdf} (pages: {len(pages)})")

    pdf.close()
    return invoices
