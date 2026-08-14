function formatSize(bytes) {
    if (bytes == null || isNaN(bytes)) return "";

    const units = ["B", "KB", "MB", "GB", "TB"];
    let size = Number(bytes);
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    return size.toFixed(unitIndex === 0 ? 0 : 2) + " " + units[unitIndex];
}

async function loadGrid() {

    const response = await fetch("/api/orphan-updates");
    const data = await response.json();

    if (!data.length) {

        document.getElementById("empty-state").classList.remove("d-none");
        document.getElementById("games-grid").style.display = "none";
        document.getElementById("quickFilter").style.display = "none";
        return;
    }

    const visibleColumns = [
    "filename",
    "size",
    "title_id",
    "version",
    "version_display"
];

const columnDefs = visibleColumns
    .filter(key => key in data[0])
    .map(key => ({
        field: key,
        headerName: key.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase()),
        sortable: true,
        filter: true,
        resizable: true,
        flex: key === "filename" ? 3 : 1,
        cellStyle: {
            userSelect: "text",
            WebkitUserSelect: "text"
        },
        valueFormatter: key === "size"
            ? params => formatSize(params.value)
            : undefined
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