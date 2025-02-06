from PyPDF2 import PdfReader, PdfWriter
import streamlit as st
import base64

def superponer_pdf(pdf_base, pdf_superpuesto, salida):
    # Leer los archivos PDF
    reader_base = PdfReader(pdf_base)
    reader_superpuesto = PdfReader(pdf_superpuesto)
    writer = PdfWriter()
    

    for i in range(len(reader_base.pages)):
        page_base = reader_base.pages[i]
        if i < len(reader_superpuesto.pages):
            page_superpuesto = reader_superpuesto.pages[i]
            page_base.merge_page(page_superpuesto)
        writer.add_page(page_base)
    
    # Guardar el nuevo PDF
    with open(salida, "wb") as output_pdf:
        writer.write(output_pdf)
    return salida

def set_background():
    st.markdown(
        """
        <style>
            body {
                background-color: #0e1117;
                color: #ffffff;
                font-family: 'Arial', sans-serif;
            }
            .stButton>button {
                background: linear-gradient(135deg, #ff00ff, #00ffff);
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            .stFileUploader>div>div>button {
                background: linear-gradient(135deg, #00ffff, #ff00ff);
                color: white;
                border-radius: 10px;
            }
            .title {
                text-align: center;
                font-size: 32px;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    set_background()
    st.markdown("<h1 class='title'>🔮 Superposición de PDFs - Miguelito 👽</h1>", unsafe_allow_html=True)
    st.markdown("**El uso de esta app merece una coca cola bien fría.**")
    
    pdf_base = st.file_uploader("📄 Carga el primer PDF 1️⃣", type="pdf")
    pdf_superpuesto = st.file_uploader("📄 Carga el segundo PDF 2️⃣", type="pdf")
    
    if pdf_base and pdf_superpuesto:
        with open("base.pdf", "wb") as f:
            f.write(pdf_base.read())
        with open("superpuesto.pdf", "wb") as f:
            f.write(pdf_superpuesto.read())
        
        salida_pdf = superponer_pdf("base.pdf", "superpuesto.pdf", "salida.pdf")
        
        with open(salida_pdf, "rb") as f:
            st.download_button("🚀 Descargar PDF resultante", f, file_name="salida.pdf", mime="application/pdf")
    
if __name__ == "__main__":
    main()
