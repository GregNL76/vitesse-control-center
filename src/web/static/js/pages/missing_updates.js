async function loadGrid() {
    const response = await fetch("/api/missing-updates");
    const data = await response.json();

    const gridOptions = {
        theme: "legacy",
        rowData: data,

        defaultColDef: {
            sortable: true,
            filter: true,
            resizable: true
        },

        columnDefs: [
            {
                field: "name",
                headerName: "Game",
                flex: 3
            },
            {
                field: "installed",
                headerName: "Installed",
                width: 170
            },
            {
                field: "latest",
                headerName: "Latest",
                width: 170
            },
            {
                field: "title_id",
                headerName: "Title ID",
                width: 180
            },
            {
                headerName: "Links",
                width: 150,
                cellRenderer: params => {
                    const links = params.data;

                    return `
                        <a class="btn btn-sm btn-outline-secondary" href="${links.url}" target="_blank">
                            Open
                        </a>
                        <a class="btn btn-sm btn-outline-secondary" href="${links.search_url}" target="_blank">
                            Search
                        </a>
                    `;
                },
                sortable: false,
                filter: false
            }
        ]
    };

    const gridApi = agGrid.createGrid(
        document.getElementById("games-grid"),
        gridOptions
    );

    document
        .getElementById("quickFilter")
        .addEventListener("input", function () {
            gridApi.setQuickFilter(this.value);
        });
}

window.addEventListener("load", loadGrid);
