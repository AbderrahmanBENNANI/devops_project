from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.units import mm
from xml.sax.saxutils import escape

def build_cv(data):
    out = BytesIO()
    doc = SimpleDocTemplate(out, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
                            topMargin=16*mm, bottomMargin=16*mm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Name", parent=styles["Title"], alignment=TA_CENTER,
                              textColor=colors.HexColor("#17324d"), spaceAfter=4))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"],
                              textColor=colors.HexColor("#176b87"), spaceBefore=10, spaceAfter=4))
    story = [Paragraph(escape(data.full_name), styles["Name"])]
    contact = " · ".join(x for x in [data.email, data.phone, data.city] if x)
    story += [Paragraph(escape(contact), styles["Normal"]), Spacer(1, 8)]
    if data.title:
        story.append(Paragraph(escape(data.title), styles["Heading2"]))
    if data.summary:
        story += [Paragraph("PROFIL", styles["Section"]), Paragraph(escape(data.summary), styles["BodyText"])]
    if data.skills:
        story += [Paragraph("COMPÉTENCES", styles["Section"]),
                  Paragraph(" · ".join(escape(x) for x in data.skills), styles["BodyText"])]
    for heading, items in [("EXPÉRIENCES", data.experience), ("FORMATION", data.education)]:
        if items:
            story.append(Paragraph(heading, styles["Section"]))
            for item in items:
                title = escape(str(item.get("title", ""))[:150])
                org = escape(str(item.get("organization", ""))[:150])
                dates = escape(str(item.get("dates", ""))[:80])
                desc = escape(str(item.get("description", ""))[:1200])
                story.append(Paragraph(f"<b>{title}</b> — {org} <font color='#666666'>{dates}</font>", styles["BodyText"]))
                if desc: story.append(Paragraph(desc, styles["BodyText"]))
                story.append(Spacer(1, 5))
    doc.build(story)
    return out.getvalue()

def build_letter(data):
    out = BytesIO()
    doc = SimpleDocTemplate(out, pagesize=A4, rightMargin=23*mm, leftMargin=23*mm,
                            topMargin=24*mm, bottomMargin=24*mm)
    styles = getSampleStyleSheet()
    story = [Paragraph(escape(data.full_name), styles["Heading2"]), Spacer(1, 16),
             Paragraph(escape(data.recipient), styles["BodyText"])]
    if data.company: story.append(Paragraph(escape(data.company), styles["BodyText"]))
    story += [Spacer(1, 18), Paragraph(f"<b>Objet : Candidature au poste de {escape(data.role)}</b>", styles["BodyText"]),
              Spacer(1, 14)]
    for paragraph in data.paragraphs:
        story += [Paragraph(escape(paragraph), styles["BodyText"]), Spacer(1, 10)]
    story.append(Paragraph("Je vous prie d’agréer, Madame, Monsieur, l’expression de mes salutations distinguées.", styles["BodyText"]))
    doc.build(story)
    return out.getvalue()
