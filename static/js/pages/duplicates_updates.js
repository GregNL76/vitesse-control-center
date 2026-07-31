async function loadGrid() {

    const response = await fetch("/api/duplicate-updates");
    const data = await response.json();

    if (!data.length) {

        document.getElementById("empty-state").classList.remove("d-none");
        document.getElementById("games-grid").style.display = "none";
        document.getElementById("quickFilter").style.display = "none";
        return;
    }

    const columnDefs = Object.keys(data[0]).map(key => ({
        field: key,
        headerName: key.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase()),
        sortable: true,
        filter: true,
        resizable: true,
        flex: 1
    }));

    const gridApi = agGrid.createGrid(
        document.getElementById("games-grid"),
        {
            theme: "legacy",
            rowData: data,
            defaultColDef: {
                sortable: true,
                filter: true,
                resizable: true
            },
            columnDefs
        }
    );

    document
        .getElementById("quickFilter")
        .addEventListener("input", function () {
            gridApi.setQuickFilter(this.value);
        });
}

window.addEventListener("load", loadGrid);