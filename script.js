document.getElementById('superponer').addEventListener('click', async () => {
    const pdf1File = document.getElementById('pdf1').files[0];
    const pdf2File = document.getElementById('pdf2').files[0];

    if (!pdf1File || !pdf2File) {
        alert('Por favor, selecciona ambos archivos PDF.');
        return;
    }

    try {
        // Cargar los PDFs
        const pdf1Bytes = await pdf1File.arrayBuffer();
        const pdf2Bytes = await pdf2File.arrayBuffer();

        const pdf1Doc = await PDFLib.PDFDocument.load(pdf1Bytes);
        const pdf2Doc = await PDFLib.PDFDocument.load(pdf2Bytes);

        // Crear un nuevo PDF
        const mergedPdf = await PDFLib.PDFDocument.create();

        // Copiar las páginas del primer PDF
        const pdf1Pages = await mergedPdf.copyPages(pdf1Doc, pdf1Doc.getPageIndices());

        // Copiar las páginas del segundo PDF
        const pdf2Pages = await mergedPdf.copyPages(pdf2Doc, pdf2Doc.getPageIndices());

        // Superponer las páginas
        for (let i = 0; i < pdf1Pages.length; i++) {
            const page = mergedPdf.addPage(pdf1Pages[i]);
            const { width, height } = page.getSize();
            page.drawPage(pdf2Pages[i], {
                x: 0,
                y: 0,
                width,
                height,
            });
        }

        // Guardar el PDF resultante
        const mergedPdfBytes = await mergedPdf.save();

        // Crear un Blob y una URL para el PDF resultante
        const blob = new Blob([mergedPdfBytes], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);

        // Mostrar el PDF en el visor
        document.getElementById('visor').innerHTML = `<iframe src="${url}" width="100%" height="100%"></iframe>`;

        // Habilitar el botón de descarga
        document.getElementById('descargar').disabled = false;
        document.getElementById('descargar').onclick = () => {
            const a = document.createElement('a');
            a.href = url;
            a.download = 'superpuesto.pdf';
            a.click();
        };
    } catch (error) {
        console.error('Error al superponer los PDFs:', error);
        alert('Ocurrió un error al superponer los PDFs. Por favor, verifica que los archivos sean válidos.');
    }
});
