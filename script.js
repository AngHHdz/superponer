document.getElementById('superponer').addEventListener('click', async () => {
    const pdf1File = document.getElementById('pdf1').files[0];
    const pdf2File = document.getElementById('pdf2').files[0];

    if (!pdf1File || !pdf2File) {
        alert('Por favor, selecciona ambos archivos PDF.');
        return;
    }

    const pdf1Bytes = await pdf1File.arrayBuffer();
    const pdf2Bytes = await pdf2File.arrayBuffer();

    const pdf1Doc = await PDFLib.PDFDocument.load(pdf1Bytes);
    const pdf2Doc = await PDFLib.PDFDocument.load(pdf2Bytes);

    const mergedPdf = await PDFLib.PDFDocument.create();

    const [pdf1Pages] = await mergedPdf.copyPages(pdf1Doc, pdf1Doc.getPageIndices());
    const [pdf2Pages] = await mergedPdf.copyPages(pdf2Doc, pdf2Doc.getPageIndices());

    for (let i = 0; i < pdf1Pages.length; i++) {
        const page = mergedPdf.addPage(pdf1Pages[i]);
        page.drawPage(pdf2Pages[i], {
            x: 0,
            y: 0,
            width: page.getWidth(),
            height: page.getHeight(),
        });
    }

    const mergedPdfBytes = await mergedPdf.save();

    const blob = new Blob([mergedPdfBytes], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);

    // Visualizar el PDF
    document.getElementById('visor').innerHTML = `<iframe src="${url}" width="100%" height="100%"></iframe>`;

    // Habilitar el botón de descarga
    document.getElementById('descargar').disabled = false;
    document.getElementById('descargar').onclick = () => {
        const a = document.createElement('a');
        a.href = url;
        a.download = 'superpuesto.pdf';
        a.click();
    };
});