document.getElementById('mergeBtn').addEventListener('click', async () => {
    const file1 = document.getElementById('pdf1').files[0];
    const file2 = document.getElementById('pdf2').files[0];

    if (!file1 || !file2) {
        alert('Por favor selecciona ambos archivos PDF.');
        return;
    }

    const pdf1Bytes = await file1.arrayBuffer();
    const pdf2Bytes = await file2.arrayBuffer();

    const pdf1 = await PDFLib.PDFDocument.load(pdf1Bytes);
    const pdf2 = await PDFLib.PDFDocument.load(pdf2Bytes);

    const mergedPdf = await PDFLib.PDFDocument.create();

    const maxPages = Math.max(pdf1.getPageCount(), pdf2.getPageCount());

    for (let i = 0; i < maxPages; i++) {
        let [page1] = i < pdf1.getPageCount() ? await mergedPdf.copyPages(pdf1, [i]) : [];
        let [page2] = i < pdf2.getPageCount() ? await mergedPdf.copyPages(pdf2, [i]) : [];

        if (page1 && page2) {
            const { width, height } = page1.getSize();
            const page = mergedPdf.addPage([width, height]);
            page.drawPage(page1);
            page.drawPage(page2);
        } else if (page1) {
            mergedPdf.addPage(page1);
        } else if (page2) {
            mergedPdf.addPage(page2);
        }
    }

    const mergedPdfBytes = await mergedPdf.save();

    const blob = new Blob([mergedPdfBytes], { type: 'application/pdf' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'PDF_superpuesto.pdf';
    link.click();
});
