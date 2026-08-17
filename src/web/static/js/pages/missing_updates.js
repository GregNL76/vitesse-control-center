async function loadGrid() {
    const response = await fetch("/api/missing-updates");
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
            },            {
                field: "installed",
                headerName: "Installed",
                width: 100
            },
            {
                field: "latest",
                headerName: "Latest",
                width: 100
            },
{
    headerName: "🔍",
    width: 60,

    cellRenderer: params => {

        const links = params.data;

        const dropdownWrapper = document.createElement("div");

        dropdownWrapper.setAttribute("data-missing-search-popup", "1");

        dropdownWrapper.style.position = "relative";
        dropdownWrapper.style.display = "flex";
        dropdownWrapper.style.alignItems = "center";
        dropdownWrapper.style.justifyContent = "center";
        dropdownWrapper.style.height = "100%";

        const button = document.createElement("button");

        button.type = "button";
        button.className = "btn btn-sm btn-outline-secondary";
        button.textContent = "🔍";
        button.title = "Search";

        button.style.width = "42px";
        button.style.padding = "4px 0";
        button.style.textAlign = "center";

function buildMenu() {

    const menu = document.createElement("div");

    menu.style.position = "fixed";
    menu.style.zIndex = "999999";
    menu.style.width = "160px";

    menu.style.background = "#252b33";
    menu.style.border = "1px solid #3d4652";
    menu.style.borderRadius = "6px";

    menu.style.padding = "4px";
    menu.style.margin = "0";

    menu.style.boxSizing = "border-box";

    menu.style.boxShadow =
        "0 6px 18px rgba(0,0,0,0.45)";

const sites = [
    {
        name: "NSWGF",
        url: links.search_url
    },
    {
        name: "RomsLab",
        url: links.search2_url
    },
    {
        name: "EggNS Emulator",
        url: links.search3_url
    },
    {
        name: "Ziperto",
        url: links.search4_url
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
        item.style.width = "100%";
        item.style.boxSizing = "border-box";

        item.style.padding = "7px 10px";

        item.style.color = "#ffffff";
        item.style.textDecoration = "none";

        item.style.fontSize = "13px";
        item.style.lineHeight = "18px";

        item.style.borderRadius = "4px";

        item.style.whiteSpace = "nowrap";

        item.addEventListener(
            "mouseenter",
            () => {
                item.style.background = "#343c47";
            }
        );

        item.addEventListener(
            "mouseleave",
            () => {
                item.style.background = "transparent";
            }
        );

        item.addEventListener(
            "mousedown",
            event => event.stopPropagation()
        );

        item.addEventListener(
            "click",
            event => event.stopPropagation()
        );

        menu.appendChild(item);
    });

    return menu;
}

 dropdownWrapper._popup = null;
 dropdownWrapper._hideTimer = null;

 function cancelHidePopup() {
     if (dropdownWrapper._hideTimer) {
         clearTimeout(dropdownWrapper._hideTimer);
         dropdownWrapper._hideTimer = null;
     }
 }

 function scheduleHidePopup() {
     cancelHidePopup();

     // Kleine vertraging zodat je van de knop naar de popup kunt bewegen
     // zonder dat de popup tussendoor verdwijnt.
     dropdownWrapper._hideTimer = setTimeout(() => {
         hidePopup();
     }, 180);
 }

 function showPopup() {

     cancelHidePopup();

     if (dropdownWrapper._popup) {
         return;
     }

     const menuEl = buildMenu();

     // Popup buiten AG Grid plaatsen zodat deze niet wordt afgeknipt
     document.body.appendChild(menuEl);

     // Positioneren ten opzichte van de zoekknop
     const btnRect = button.getBoundingClientRect();

     menuEl.style.position = "fixed";
     menuEl.style.display = "block";
     menuEl.style.visibility = "visible";

// ---------------------------------------------------------
// Popup binnen het scherm houden
// ---------------------------------------------------------

const menuWidth = menuEl.offsetWidth;
const menuHeight = menuEl.offsetHeight;
const margin = 8;

let left = btnRect.right - menuWidth;
let top = btnRect.bottom + 4;

// Niet buiten de rechterkant van het scherm
if (left + menuWidth > window.innerWidth - margin) {
    left = window.innerWidth - menuWidth - margin;
}

// Niet buiten de linkerkant van het scherm
if (left < margin) {
    left = margin;
}

// Als er onder de knop niet genoeg ruimte is,
// plaats de popup boven de knop.
if (top + menuHeight > window.innerHeight - margin) {
    top = btnRect.top - menuHeight - 4;
}

// Ook boven de bovenrand blijven
if (top < margin) {
    top = margin;
}

menuEl.style.left = `${left}px`;
menuEl.style.top = `${top}px`;

     menuEl.style.zIndex = "999999";

     // Popup open houden zolang de muis erboven staat
     menuEl.addEventListener(
         "mouseenter",
         cancelHidePopup
     );

     menuEl.addEventListener(
         "mouseleave",
         scheduleHidePopup
     );

     dropdownWrapper._popup = menuEl;
 }

 function hidePopup() {

     cancelHidePopup();

     if (!dropdownWrapper._popup) {
         return;
     }

     const el = dropdownWrapper._popup;

     if (el.parentNode) {
         el.parentNode.removeChild(el);
     }

     dropdownWrapper._popup = null;
 }


 // ---------------------------------------------------------
 // Click
 // ---------------------------------------------------------

 button.addEventListener(
     "click",
     event => {

         event.stopPropagation();

         if (dropdownWrapper._popup) {

             hidePopup();

         } else {

             closeAllMissingSearchPopups();
             showPopup();
         }
     }
 );


 // ---------------------------------------------------------
 // Hover
 // ---------------------------------------------------------

 button.addEventListener(
     "mouseenter",
     () => {

         cancelHidePopup();
         closeAllMissingSearchPopups();
         showPopup();
     }
 );

 button.addEventListener(
     "mouseleave",
     () => {

         scheduleHidePopup();
     }
);

        // ---------------------------------------------------------
        // Expose close function
        // ---------------------------------------------------------

        dropdownWrapper.closeDropdown = hidePopup;

        dropdownWrapper.appendChild(button);

        return dropdownWrapper;
    },

    suppressMovable: true,
    suppressSizeToFit: true,

    sortable: false,
    filter: false
}
        ]
    };

    const gridApi = agGrid.createGrid(
        document.getElementById("games-grid"),
        gridOptions
    );


        const searchInput =
	        document.getElementById("quickFilter");

	    searchInput.addEventListener("input", event => {

	        gridApi.setFilterModel({
	            name: {
	                filterType: "text",
	                type: "contains",
	                filter: event.target.value
	            }
	        });

    });


}

function closeAllMissingSearchPopups() {

    const dropdowns = document.querySelectorAll(
        '[data-missing-search-popup]'
    );

    dropdowns.forEach(dropdown => {

        if (dropdown.closeDropdown) {
            dropdown.closeDropdown();
        }

    });
}

window.addEventListener("load", loadGrid);