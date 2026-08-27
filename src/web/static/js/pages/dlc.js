document.addEventListener("DOMContentLoaded", async () => {

    const response = await fetch("/api/dlc");
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
                headerName: "DLC",
                width: 480
            },

            {
                field: "title_id",
                headerName: "Title ID",
                width: 135
            },

            {
                field: "region",
                headerName: "Region",
                width: 95
            },

            {
                field: "version",
                headerName: "Version",
                width: 100,
                valueFormatter: params => {
                    if (
                        params.value === null ||
                        params.value === undefined ||
                        params.value === ""
                    ) {
                        return "-";
                    }

                    return `v${params.value}`;
                },
                comparator: (valueA, valueB) => {
                    return Number(valueA || 0) - Number(valueB || 0);
                }
            },

            {
                field: "size_display",
                headerName: "Size",
                width: 100
            },

            {
                field: "filename",
                headerName: "Filename",
                flex: 2,
                minWidth: 300
            }
        ]
    };

    const gridApi = agGrid.createGrid(
        document.getElementById("dlc-grid"),
        gridOptions
    );

    document
        .getElementById("quickFilter")
        .addEventListener("input", function () {
            gridApi.setGridOption(
                "quickFilterText",
                this.value
            );
        });

});
