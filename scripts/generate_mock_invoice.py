from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path

out = Path("data/raw/mock_invoice_01.pdf")
out.parent.mkdir(parents=True, exist_ok=True)

c = canvas.Canvas(str(out), pagesize=A4)
c.setFont("Helvetica-Bold", 14)
c.drawString(50, 800, "Invoice #INV-2025-001")
c.setFont("Helvetica", 10)
c.drawString(50, 785, "Date: 11/11/2025")
c.drawString(50, 770, "Bill To: Acme Corporation")
c.drawString(50, 740, "Description")
c.drawString(300, 740, "Qty")
c.drawString(360, 740, "Unit Price")
c.drawString(460, 740, "Line Total")

# table rows
items = [
    ("Widget A", "2", "1,000.00", "2,000.00"),
    ("Widget B", "1", "500.00", "500.00"),
    ("Service C", "3", "250.00", "750.00"),
]
y = 720
for desc, qty, up, lt in items:
    c.drawString(50, y, desc)
    c.drawString(300, y, qty)
    c.drawString(360, y, up)
    c.drawString(460, y, lt)
    y -= 20

c.drawString(400, 640, "Total: 3,250.00")
c.save()

print(f"Generated {out}")
