from io import BytesIO
from datetime import datetime
from fpdf import FPDF


class ReportPDF(FPDF):
    """Simple PDF builder for ESG analysis and recommendations."""

    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Data Centre ESG Report", ln=1)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        page_text = f"Page {self.page_no()}"
        self.cell(0, 10, page_text, align="C")


def _wrap_words(text: str, max_word_len: int = 40) -> str:
    """Hard-wrap any word longer than max_word_len to avoid overflow in PDF."""
    wrapped_tokens = []
    for token in text.split():
        if len(token) > max_word_len:
            # Break long token into chunks of max_word_len
            for i in range(0, len(token), max_word_len):
                wrapped_tokens.append(token[i : i + max_word_len])
        else:
            wrapped_tokens.append(token)
    return " ".join(wrapped_tokens)


def _add_section(pdf: ReportPDF, title: str, body: str, max_word_len: int = 20):
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, title, ln=1)
    pdf.set_font("Arial", "", 10)
    effective_width = getattr(pdf, "epw", pdf.w - pdf.l_margin - pdf.r_margin)
    if effective_width <= 0:
        effective_width = 100  # fallback width
    for line in body.splitlines():
        if line.strip() == "":
            pdf.ln(4)
        else:
            safe_line = _wrap_words(line, max_word_len=max_word_len)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(effective_width, 7, safe_line, align="L")
    pdf.ln(4)


def create_pdf_report(analysis_text: str, recommendations_text: str, selected_year: int, prev_year=None) -> bytes:
    """
    Build a PDF report combining AI analysis and recommendations.

    Returns PDF bytes suitable for Streamlit download_button.
    """
    pdf = ReportPDF()
    # Set roomier margins to prevent text hugging the edges
    margin = 20
    pdf.set_left_margin(margin)
    pdf.set_right_margin(margin)
    pdf.set_auto_page_break(auto=True, margin=margin)
    pdf.add_page()

    # Cover details
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"ESG Analysis & Recommendations - {selected_year}", ln=1)
    pdf.set_font("Arial", "", 11)
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M")
    prev_text = f" vs {prev_year}" if prev_year is not None else ""
    pdf.cell(0, 8, f"Generated: {generated_on}", ln=1)
    pdf.cell(0, 8, f"Period: {selected_year}{prev_text}", ln=1)
    pdf.ln(6)

    _add_section(pdf, "Analysis", analysis_text or "(No analysis available)", max_word_len=20)
    _add_section(pdf, "Recommendations", recommendations_text or "(No recommendations available)", max_word_len=20)

    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
