"""
Vitesse Control Center

Report writer.
"""

from __future__ import annotations

from csv import writer
from datetime import datetime
from pathlib import Path
from src.vcc.url_validator import UrlValidator


class ReportWriter:

    def __init__(self, output_dir: str = "reports"):

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write(self, report):

        for game in report:

            game["available"] = UrlValidator.exists(game["url"])

        self.write_text(report)
        self.write_csv(report)
        self.write_html(report)

    def write_text(self, report):

        filename = self.output_dir / "missing_updates.txt"

        with filename.open("w", encoding="utf-8") as f:

            f.write("=" * 60 + "\n")
            f.write("Vitesse Control Center\n")
            f.write("Missing Updates Report\n")
            f.write("=" * 60 + "\n\n")

            f.write(f"Generated : {datetime.now():%Y-%m-%d %H:%M:%S}\n")
            f.write(f"Missing   : {len(report)}\n\n")

            for game in report:

                f.write("-" * 60 + "\n")
                f.write(f"Name      : {game['name']}\n")
                f.write(f"Installed : {game['installed']}\n")
                f.write(f"Latest    : {game['latest']}\n")
                f.write(f"Title ID  : {game['title_id']}\n")
                f.write(f"Direct URL : {game['url']}\n")
                f.write(f"Search URL : {game['search_url']}\n\n")

    def write_csv(self, report):

        filename = self.output_dir / "missing_updates.csv"

        with filename.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as f:

            csv = writer(f)

            csv.writerow(
                [
                    "Name",
                    "Installed",
                    "Latest",
                    "TitleID",
                    "DirectURL",
                    "SearchURL",
                ]
            )

            for game in report:

                csv.writerow(
                    [
                        game["name"],
                        game["installed"],
                        game["latest"],
                        game["title_id"],
                        game["url"],
                        game["search_url"],
                    ]
                )

    def write_html(self, report):

        filename = self.output_dir / "missing_updates.html"

        rows = []

        for game in report:

            rows.append(
                f"""
<tr>
<td>{game["name"]}</td>
<td>{game["installed"]}</td>
<td>{game["latest"]}</td>
<td>{game["title_id"]}</td>
<td>
    <a class="button" href="{game["url"]}" target="_blank">Open</a>
    <a class="button" href="{game["search_url"]}" target="_blank">Search</a>
</td>
</tr>
"""
            )

        html = f"""<!DOCTYPE html>
    <html lang="en">

    <head>

    <meta charset="UTF-8">

    <title>Vitesse Control Center</title>

    <style>

    body {{
        font-family: Arial, Helvetica, sans-serif;
        background: #f5f5f5;
        margin: 40px;
    }}

    h1 {{
        margin-bottom: 5px;
    }}

    .stats {{
        margin-bottom: 20px;
    }}

    .search {{
        width: 350px;
        padding: 8px;
        margin-bottom: 20px;
        font-size: 15px;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        background: white;
    }}

    th {{
        background: #222;
        color: white;
        padding: 10px;
        text-align: left;
    }}

    td {{
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }}

    tr:nth-child(even) {{
        background: #f7f7f7;
    }}

    tr:hover {{
        background: #ffffdd;
    }}

    .button {{
        text-decoration: none;
        background: #1976d2;
        color: white;
        padding: 5px 10px;
        border-radius: 4px;
        margin-right: 5px;
    }}

    .button:hover {{
        background: #125699;
    }}

    </style>

    </head>

    <body>

    <h1>Vitesse Control Center</h1>

    <h2>Missing Updates Report</h2>

    <div class="stats">

    <b>Missing updates:</b> {len(report)}

    </div>

    <input
    class="search"
    type="text"
    id="search"
    placeholder="Search..."
    onkeyup="filterTable()">

    <table id="games">

    <thead>

    <tr>

    <th>Name</th>
    <th>Installed</th>
    <th>Latest</th>
    <th>Title ID</th>
    <th>Links</th>

    </tr>

    </thead>

    <tbody>

    {''.join(rows)}

    </tbody>

    </table>

    <script>

    function filterTable() {{

        let input = document.getElementById("search");
        let filter = input.value.toUpperCase();
        let table = document.getElementById("games");
        let tr = table.getElementsByTagName("tr");

        for (let i = 1; i < tr.length; i++) {{

            let td = tr[i].getElementsByTagName("td")[0];

            if (td) {{

                let txt = td.textContent;

                tr[i].style.display =
                    txt.toUpperCase().indexOf(filter) > -1
                    ? ""
                    : "none";
            }}
        }}
    }}

    </script>

    </body>

    </html>
    """

        with filename.open("w", encoding="utf-8") as f:
            f.write(html)