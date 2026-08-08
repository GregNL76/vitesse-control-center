async function loadGrid() {

    const response = await fetch("/api/duplicate-updates");
    const data = await response.json();

    if (!data.length) {

        document.getElementById("empty-state").classList.remove("d-none");
        document.getElementById("games-grid").style.display = "none";
        document.getElementById("quickFilter").style.display = "none";
        return;
    }

    const columnDefs = [

		{
			field: "name",

			headerName: "Game",

			flex: 2,

			minWidth: 420

		},

		{
			field: "latest_version",

			headerName: "Latest",

			width: 110,

			valueFormatter: params => {

				return params.value
					? "v" + params.value
					: "-";

			}

		},

		{
			field: "installed_version",

			headerName: "Installed",

			width: 110,

			valueFormatter: params => {

				return params.value
					? "v" + params.value
					: "-";

			}

		},

		{
			field: "obsolete",

			headerName: "Remove",

			flex: 1,

			sortable: false,

			valueGetter: params => {

				return params.data.obsolete
					.map(item => "v" + item.version)
					.join(", ");

			}

		},

		{
			field: "space_to_free",

			headerName: "Space to free",

			width: 140,

			valueFormatter: params => {

				const mb = params.value / 1024 / 1024;

				if (mb >= 1024) {

					return (mb / 1024).toFixed(2) + " GB";

				}

				return mb.toFixed(1) + " MB";

			}

		}

	];


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