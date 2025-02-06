from PyPDF2 import PdfReader, PdfWriter
import streamlit as st

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

def main():
    st.title("Superponer PDFs")
    pdf_base = st.file_uploader("Sube el PDF base", type="pdf")
    pdf_superpuesto = st.file_uploader("Sube el PDF a superponer", type="pdf")
    
    if pdf_base and pdf_superpuesto:
        with open("base.pdf", "wb") as f:
            f.write(pdf_base.read())
        with open("superpuesto.pdf", "wb") as f:
            f.write(pdf_superpuesto.read())
        
        salida_pdf = superponer_pdf("base.pdf", "superpuesto.pdf", "salida.pdf")
        
        with open(salida_pdf, "rb") as f:
            st.download_button("Descargar PDF resultante", f, file_name="salida.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
