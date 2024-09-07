from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from datetime import datetime

def create_invoice(invoice_data, filename="invoice.pdf"):
    # Create PDF document
    pdf = SimpleDocTemplate(filename, pagesize=A4)
    
    # Set up styles
    styles = getSampleStyleSheet()
    elements = []
    
    # Invoice Title
    title = Paragraph("INVOICE", styles['Title'])
    elements.append(title)
    
    # Invoice Info (Date, Invoice Number, etc.)
    invoice_info = f"""
    <br/><br/>
    Invoice Number: {invoice_data['invoice_number']}<br/>
    Date: {datetime.now().strftime('%Y-%m-%d')}<br/>
    Bill To: {invoice_data['client_name']}<br/>
    Bill from: {invoice_data['my_name']}<br/>
    Bank name: {invoice_data['bank_name']}<br/>
    Account type: {invoice_data['account_type']}<br/>
    Account number: {invoice_data['account_number']}<br/>
    Account holder: {invoice_data['account_holder']}<br/>
    Reference: {invoice_data['ref']}<br/>
    <br/>
    """
    elements.append(Paragraph(invoice_info, styles['Normal']))

    # Table Header and Data
    table_data = [['Item', 'Description', 'Quantity', 'Unit Price', 'Total']]
    total_price = 0

    # Add each item to the table
    for item in invoice_data['items']:
        row = [item['name'], item['description'], item['quantity'], f"R{item['unit_price']:.2f}", f"R{item['total']:.2f}"]
        table_data.append(row)
        total_price += item['total']
    
    # Table Styling
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    
    # Total Amount
    total = f"<br/><br/><b>Total: R{total_price:.2f}</b>"
    elements.append(Paragraph(total, styles['Normal']))

    # Build the PDF
    pdf.build(elements)
    print(f"Invoice saved as {filename}")

# Example invoice data
invoice_data = {
    'invoice_number': 'INV-80085',
    'client_name': '',
    'my_name': '',
    'bank_name': '',
    'account_type': '',
    'account_number': '',
    'account_holder': '',
    'ref': '',
    'items': [
        {'name': 'Product 1', 'description': 'Description for product 1', 'quantity': 2, 'unit_price': 50, 'total': 100},
        {'name': 'Service 1', 'description': 'Description for service 1', 'quantity': 5, 'unit_price': 20, 'total': 100},
    ]
}

# Generate the invoice PDF
create_invoice(invoice_data)
