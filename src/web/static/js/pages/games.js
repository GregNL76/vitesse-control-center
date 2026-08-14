async function loadGrid() {

    const response = await fetch("/api/games");
    const data = await response.json();

    const gridOptions = {
        theme: "legacy",
        rowData: data,

		defaultColDef: {
			sortable: true,
			filter: true,
			resizable: true,

			cellStyle: {
				userSelect: "text",
				WebkitUserSelect: "text"
			}
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
    width: 110,

    cellRenderer: params => {

        const links = params.data.external_links;

        const wrapper = document.createElement("div");

        wrapper.style.display = "flex";
        wrapper.style.alignItems = "center";
        wrapper.style.justifyContent = "flex-start";
        wrapper.style.gap = "4px";
        wrapper.style.height = "100%";

        // ---------------------------------------------------------
        // Open button
        // ---------------------------------------------------------

        const openButton = document.createElement("a");

        openButton.className = "btn btn-sm btn-outline-secondary";
        openButton.href = links.game_page;
        openButton.target = "_blank";
        openButton.rel = "noopener noreferrer";
        openButton.textContent = "Open";

        // ---------------------------------------------------------
        // Search button
        // ---------------------------------------------------------

        const searchButton = document.createElement("button");

        searchButton.type = "button";
        searchButton.className = "btn btn-sm btn-outline-secondary";
		searchButton.textContent = "🔍";
		searchButton.setAttribute("aria-label", "Search");
		searchButton.title = "Search";
        searchButton.style.whiteSpace = "nowrap";

        // ---------------------------------------------------------
        // Search popup
        // ---------------------------------------------------------

        let menu = null;
        let hideTimer = null;

        function hideMenu() {

            if (!menu) {
                return;
            }

            menu.remove();
            menu = null;
        }

        function scheduleHide() {

            clearTimeout(hideTimer);

            hideTimer = setTimeout(() => {
                hideMenu();
            }, 250);
        }

        function showMenu() {

            clearTimeout(hideTimer);

            if (menu) {
                return;
            }

            menu = document.createElement("div");

            menu.style.position = "fixed";
            menu.style.zIndex = "999999";
            menu.style.minWidth = "160px";

            menu.style.background = "#252b33";
            menu.style.border = "1px solid #3d4652";
            menu.style.borderRadius = "6px";

            menu.style.padding = "4px";
            menu.style.boxShadow = "0 6px 18px rgba(0,0,0,0.45)";

            const sites = [
                {
                    name: "NSWGF",
                    url: links.search
                },
                {
                    name: "RomsLab",
                    url: links.search2
                },
                {
                    name: "EggNS Emulator",
                    url: links.search3
                },
                {
                    name: "Ziperto",
                    url: links.search4
                }
            ];

            sites.forEach(site => {

                if (!site.url) {
                    return;
                }

                const item = document.createElement("a");

                item.href = site.url;
                item.target = "_blank";
                item.rel = "noopener noreferrer";

                item.textContent = site.name;

                item.style.display = "block";
                item.style.padding = "7px 10px";

                item.style.color = "#ffffff";
                item.style.textDecoration = "none";

                item.style.borderRadius = "4px";
                item.style.whiteSpace = "nowrap";

                item.addEventListener("mouseenter", () => {
                    item.style.background = "#343c47";
                    clearTimeout(hideTimer);
                });

                item.addEventListener("mouseleave", () => {
                    item.style.background = "transparent";
                    scheduleHide();
                });

                menu.appendChild(item);
            });

            document.body.appendChild(menu);

            // Position the popup directly below the Search button
            const rect = searchButton.getBoundingClientRect();

            menu.style.left = `${rect.left}px`;
            menu.style.top = `${rect.bottom + 4}px`;

            menu.addEventListener("mouseenter", () => {
                clearTimeout(hideTimer);
            });

            menu.addEventListener("mouseleave", () => {
                scheduleHide();
            });
        }

        // Hover
        searchButton.addEventListener("mouseenter", () => {
            showMenu();
        });

        searchButton.addEventListener("mouseleave", () => {
            scheduleHide();
        });

        // Click
        searchButton.addEventListener("click", event => {

            event.stopPropagation();

            if (menu) {
                hideMenu();
            } else {
                showMenu();
            }
        });

        wrapper.appendChild(openButton);
        wrapper.appendChild(searchButton);

        return wrapper;
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