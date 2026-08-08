async function loadGrid() {

    const response = await fetch("/api/games");
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
				field: "title_id",
				headerName: "Title ID",
				width: 160
			},

            {
                field: "installed_display",
                headerName: "Installed",
                width: 100,

                comparator: (valueA, valueB, nodeA, nodeB) => {
                    return nodeA.data.installed - nodeB.data.installed;
                }
            },

            {
                field: "latest_display",
                headerName: "Latest",
                width: 100,

                comparator: (valueA, valueB, nodeA, nodeB) => {
                    return nodeA.data.latest - nodeB.data.latest;
                }
            },

            {
                field: "status",
                headerName: "Status",
                width: 110,

                comparator: (valueA, valueB) => {

                    const order = {
                        "Update": 0,
                        "Unknown": 1,
                        "Current": 2
                    };

                    return order[valueA.text] - order[valueB.text];
                },

                cellRenderer: params => {

                    const status = params.value;

                    return `
                        <span style="
                            display:inline-flex;
                            align-items:center;
                            justify-content:center;
                            vertical-align:middle;
                            min-width:90px;
                            text-align:center;
                            padding:2px 10px;
                            border-radius:999px;
                            background:${status.color};
                            color:white;
                            font-size:12px;
                            line-height:12px;
                            font-weight:600;
                        ">
                            ${status.text}
                        </span>
                    `;
                }
            },

            {
                headerName: "Links",
                width: 150,

                cellRenderer: params => {

                    const links = params.data.external_links;

                    return `
                    <a class="btn btn-sm btn-outline-secondary"
                       href="${links.game_page}"
                       target="_blank"
                       rel="noopener noreferrer">
                        Open
                    </a>

                    <a class="btn btn-sm btn-outline-secondary"
                       href="${links.search}"
                       target="_blank"
                       rel="noopener noreferrer">
                        S1
                    </a>

                    <a class="btn btn-sm btn-outline-secondary"
                       href="${links.search2}"
                       target="_blank"
                       rel="noopener noreferrer">
                        S2
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