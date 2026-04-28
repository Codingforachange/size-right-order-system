from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

app = FastAPI()

# Enable CORS for Angular communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 1. DATA MODELS ---

class FSItem(BaseModel):
    fsOrderType: str
    description: str
    productCode: str
    billingMethod: str
    price: float
    abusEnabled: bool
    abusName: Optional[str] = ""
    abusEmpNum: Optional[str] = ""
    systematicReplace: bool
    replacePercent: Optional[float] = 0
    replaceRate: Optional[float] = 0
    orderMethod: str
    soilCounted: str
    circulatingQty: int
    deliveryScheme: str
    deliveryVarEnabled: bool
    deliveryVarType: str

class Product(BaseModel):
    wearerFunction: str
    productCode: str
    size: str
    issueQty: int
    price: float
    emblemId: Optional[str] = ""

class Wearer(BaseModel):
    lkr: str
    firstName: str
    lastName: str
    products: List[Product]

class OrderData(BaseModel):
    customerNumber: str
    customerName: str
    location: str
    date: str
    facilityItems: List[FSItem]
    wearers: List[Wearer]

# --- 2. PDF GENERATION ---

@app.post("/generate-pdf")
async def generate_pdf(data: OrderData):
    buffer = io.BytesIO()
    # Adjusted margins to maximize space
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    elements = []
    unifirst_green = colors.HexColor('#008a4e')
    
    # Track the running total
    grand_total = 0.0

    # Header
    elements.append(Paragraph(f"UniFirst Order Form - {data.customerName}", styles['Title']))
    elements.append(Paragraph(f"Customer #: {data.customerNumber} | Location: {data.location} | Date: {data.date}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Facility Services Section
    if data.facilityItems:
        elements.append(Paragraph("FACILITY SERVICES / FS ORDER", styles['Heading2']))
        
        fs_data = [['Type', 'Description', 'Product Code', 'Billing Method', 'Price', 'Order Method', 'Soil Count', 'Freq', 'Inv']]
        span_rows = []

        for item in data.facilityItems:
            grand_total += item.price # Add item price to total
            
            desc_p = Paragraph(item.description or "", styles['Normal'])
            method_p = Paragraph(item.orderMethod or "", styles['Normal'])
            
            fs_data.append([
                item.fsOrderType, desc_p, item.productCode,
                item.billingMethod.replace('Based On ', 'B.O. '),
                f"${item.price:.2f}", method_p, item.soilCounted,
                item.deliveryScheme, item.circulatingQty
            ])
            
            # Sub-row notes (Joined with '|' to save space)
            notes_list = []
            if item.abusEnabled:
                notes_list.append(f"ABUS: {item.abusName} ({item.abusEmpNum})")
            if item.systematicReplace:
                notes_list.append(f"Sysematic Replacement: {item.replacePercent}% @ ${item.replaceRate:.2f}")
            if item.deliveryVarEnabled:
                notes_list.append(f"Delivery Variation: {item.deliveryVarType}")
            
            if notes_list:
                combined_notes = " | ".join(notes_list)
                note_para = Paragraph(f"<i>{combined_notes}</i>", styles['Italic'])
                fs_data.append([note_para, '', '', '', '', '', '', '', ''])
                span_rows.append(len(fs_data) - 1) # Bookmark for spanning

        fs_table = Table(fs_data, colWidths=[55, 80, 65, 75, 45, 85, 50, 50, 35])
        
        fs_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), unifirst_green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])

        # Apply spanning to note rows
        for row_idx in span_rows:
            fs_style.add('SPAN', (0, row_idx), (-1, row_idx))

        fs_table.setStyle(fs_style)
        elements.append(fs_table)
        elements.append(Spacer(1, 20))

    # Wearer Section
    for wearer in data.wearers:
        elements.append(Paragraph(f"Wearer: {wearer.firstName} {wearer.lastName} (LKR: {wearer.lkr})", styles['Heading3']))
        
        p_data = [['Function', 'Product Code', 'Size', 'Qty', 'Price']]
        span_wearer_rows = []
        
        for prod in wearer.products:
            # Add (Price * Qty) to grand total
            grand_total += (prod.price * prod.issueQty)
            
            p_data.append([prod.wearerFunction, prod.productCode, prod.size, prod.issueQty, f"${prod.price:.2f}"])
            if prod.emblemId:
                emb_p = Paragraph(f"<b>Emblem Template:</b> {prod.emblemId}", styles['Normal'])
                p_data.append([emb_p, '', '', '', ''])
                span_wearer_rows.append(len(p_data) - 1)

        p_table = Table(p_data, colWidths=[120, 100, 80, 60, 80])
        p_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), unifirst_green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])

        for row_idx in span_wearer_rows:
            p_style.add('SPAN', (0, row_idx), (-1, row_idx))
        
        p_table.setStyle(p_style)
        elements.append(p_table)
        elements.append(Spacer(1, 15))

    # --- GRAND TOTAL SECTION ---
    elements.append(Spacer(1, 10))
    total_data = [[f"ORDER GRAND TOTAL: ${grand_total:.2f}"]]
    total_table = Table(total_data, colWidths=[545])
    total_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 2, unifirst_green),
        ('ALIGN', (0,0), (-1,0), 'RIGHT'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
    ]))
    elements.append(total_table)

    doc.build(elements)
    buffer.seek(0)
    
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=UniFirst_Order_{data.customerNumber}.pdf"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)