function highlightTableRow(row) {
    // Remove highlight from previously selected row, if any
    const previouslySelectedRow = document.querySelector('tr.selected');
    if (previouslySelectedRow) {
    previouslySelectedRow.classList.remove('selected');
    }
    // Highlight the clicked row
    row.classList.add('selected');
    //var value=row.find('td:first').html();
    //alert(value);   
    document.getElementById('invoice').src = "/static/assets/invoices/"+row.cells[0].innerText+".pdf#navpanes=0";
    //alert("url('/static/assets/"+row.cells[0].innerText+".pdf')");
}

const rows = document.querySelectorAll('table tr');
for (let i = 0; i < rows.length; i++) {
    rows[i].onclick = function() {
    highlightTableRow(this);
    
    };
}