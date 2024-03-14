function exportToPDF() {
    var doc = new jsPDF();

    // Add title
    doc.setFontSize(20);
    doc.text("Grocery Tracking Summary", 15, 15);

    // Add grocery items table
    var groceriesTable = document.getElementById("groceriesTable");
    doc.autoTable({ html: groceriesTable });

    // Add expense summary
    var expenseSummary = document.getElementById("expenseSummary").innerText;
    doc.setFontSize(14);
    doc.text(15, doc.lastAutoTable.finalY + 10, "Expense Summary:");
    doc.text(15, doc.lastAutoTable.finalY + 20, expenseSummary);

    // Add category chart
    var categoryChartCanvas = document.getElementById("categoryChart");
    var categoryChartImg = categoryChartCanvas.toDataURL("image/png");
    doc.addImage(
        categoryChartImg,
        "PNG",
        15,
        doc.lastAutoTable.finalY + 40,
        180,
        100
    );

    // Save the PDF
    doc.save("grocery_summary.pdf");
}