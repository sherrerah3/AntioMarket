from datetime import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from .interfaces import ComprobantePagoStrategy
from ..models import Pedido

class GeneradorFacturaPDF(ComprobantePagoStrategy):
    """
    Implementación concreta que genera un PDF con formato de factura tradicional.
    """
    
    def generar_comprobante(self, pedido: Pedido) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        factura_style = ParagraphStyle(
            'FacturaStyle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1 
        )
        
        elements.append(Paragraph("FACTURA", factura_style))
        elements.append(Paragraph(f"Pedido #{pedido.id}", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", styles['Normal']))
        elements.append(Paragraph(f"Cliente: {pedido.cliente.usuario.username}", styles['Normal']))
        elements.append(Spacer(1, 0.5*inch))
        
        data = [['Producto', 'Cantidad', 'Precio Unit.', 'Subtotal']]
        for detalle in pedido.detalles.all():
            data.append([
                detalle.producto.nombre,
                str(detalle.cantidad),
                f"${detalle.precio_unitario:,.2f}",
                f"${detalle.subtotal:,.2f}"
            ])
        
        subtotal = self._calcular_subtotal(pedido)
        iva = self._calcular_iva(pedido)
        
        data.append(['', '', 'Subtotal:', f"${subtotal:,.2f}"])
        data.append(['', '', 'IVA (19%):', f"${iva:,.2f}"])
        data.append(['', '', 'TOTAL:', f"${pedido.total:,.2f}"])
        
        table = Table(data, colWidths=[4*inch, 1*inch, 1.25*inch, 1.25*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -3), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, -3), (-1, -1), colors.black),
            ('FONTNAME', (-2, -3), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        doc.build(elements)
        
        return buffer.getvalue()
        
    def _calcular_subtotal(self, pedido: Pedido) -> float:
        """Calcula el subtotal del pedido sin IVA"""
        return float(pedido.total) / 1.19  # Asumiendo IVA del 19%
    
    def _calcular_iva(self, pedido: Pedido) -> float:
        """Calcula el IVA del pedido"""
        return float(pedido.total) - self._calcular_subtotal(pedido)