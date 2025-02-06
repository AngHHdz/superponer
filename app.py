from PyPDF2 import PdfReader, PdfWriter
import streamlit as st
import base64

def superponer_pdf(pdf_base, pdf_superpuesto, salida):
    # Leer los archivos PDF
    reader_base = PdfReader(pdf_base)
    reader_superpuesto = PdfReader(pdf_superpuesto)
    writer = PdfWriter()
    
    # Iterar sobre las páginas y superponerlas
    for i in range(len(reader_base.pages)):
        page_base = reader_base.pages[i]
        if i < len(reader_superpuesto.pages):  # Verificar que haya páginas suficientes en el superpuesto
            page_superpuesto = reader_superpuesto.pages[i]
            page_base.merge_page(page_superpuesto)  # Superponer
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
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    set_background()
    st.title("🔮 Superposición de PDFs - Estilo Futurista")
    st.markdown("**Sube dos PDFs y obtén una versión combinada con un diseño moderno.**")
    
    pdf_base = st.file_uploader("📄 Sube el PDF base", type="pdf")
    pdf_superpuesto = st.file_uploader("📄 Sube el PDF a superponer", type="pdf")
    
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
