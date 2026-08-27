# Vitesse Control Center (VCC)

**Vitesse Control Center (VCC)** is a Nintendo Switch library
management, version-comparison and auditing system designed primarily
for use on a Synology NAS.

VCC scans a local Nintendo Switch title library, stores the results in
SQLite, synchronizes external title and version information, and
provides a web-based dashboard for monitoring the health, structure and
completeness of the library.

VCC is powered by <strong>GAMEBOY</strong>:
<strong>G</strong>ame
<strong>A</strong>rchive
<strong>M</strong>anagement
<strong>E</strong>ngine for
<strong>B</strong>ackups,
<strong>O</strong>rganization &
s<strong>Y</strong>nchronization.

## Features

### Library Management

-   Scan and index Nintendo Switch title files
-   Detect and classify Base Games, Updates and DLC
-   Support separate `BASE`, `UPDATES` and `DLC` library folders
-   Track installed files, Title IDs, versions, sizes and paths
-   Detect orphaned and duplicate updates
-   Identify missing and obsolete updates
-   Calculate a library health score
-   Show recent additions and largest files

### Update Intelligence

VCC compares locally installed update versions against multiple
independent external sources.

-   Synchronize Nintendo Switch title metadata
-   Retrieve available title and update versions from Tinfoil
-   Resolve USA, EUR, ASIA, JPN and AUS regions for local Title IDs
-   Let updates and DLC inherit the region of their base-title family
-   Use **nx-versions** as an additional independent version source
-   Cache nx-versions data locally to reduce unnecessary network traffic
-   Compare the locally installed version against the highest known
    version
-   Preserve Tinfoil and NX values separately for auditing
-   Flag cases where external version sources disagree
-   Identify updates that are missing from the local library

### Library Reports

The Reports section performs strict filename and library-structure
validation without automatically modifying files.

Current checks include:

-   **Invalid Update Title IDs** --- detects files in `UPDATES` whose
    Title ID does not end in `800`
-   Match suspicious update IDs against corresponding files in `BASE`
-   Calculate and display the expected Update Title ID where possible
-   **Update Version Numbers Without `v`** --- detects version blocks
    such as `[65536]` instead of `[v65536]`
-   **Invalid Update Version Blocks** --- detects missing or malformed
    update version blocks
-   **Invalid BASE Version Blocks** --- validates the strict
    `[16-character Title ID][v0]` filename structure directly before the
    extension
-   Report filename, file size, IDs, current/expected values and the
    detected problem

Reports are intentionally diagnostic: VCC reports inconsistencies but
does not automatically rename, move or alter affected library files.

### Web Dashboard

Current dashboard sections include:

-   **Dashboard** --- Library statistics, health information and recent
    additions
-   **Games** --- Installed games, versions, status and external search
    links
-   **DLC** --- DLC inventory and related information
-   **Missing Updates** --- Missing updates with Local, Latest, Tinfoil
    and NX version comparison
-   **Orphan Updates** --- Updates without a matching base game
-   **Obsolete Updates** --- Updates that are no longer the latest
    installed version
-   **Reports** --- Library integrity and filename-structure auditing
-   **Available Games** --- Searchable NSWGF catalogue cached for 24 hours
-   **Settings** --- Reserved for configurable VCC options
-   **Git** --- Repository status, modified files, commit/push
    functionality and a direct GitHub repository link

The dashboard uses AG Grid for interactive tables, including sorting,
filtering and resizing.

## Library Layout

VCC supports a structured library layout:

``` text
games/
|
+-- BASE/
|   +-- Base game files
|
+-- UPDATES/
|   +-- Update files
|
+-- DLC/
    +-- DLC files
```

The scanner works recursively from the configured game folder, allowing
the library to remain organized while VCC maintains a unified database
view.

## Architecture

VCC is built around a Python backend with a SQLite database and a web
interface.

``` text
Vitesse Control Center
|
+-- Library Scanner
|   +-- Scans and classifies the Nintendo Switch library
|
+-- SQLite Database
|   +-- Stores files, Title IDs, versions and audit information
|
+-- External Data Sources
|   +-- TitleDB metadata
|   +-- Tinfoil version data
|   +-- nx-versions version data + local cache
|
+-- Update Auditor
|   +-- Compares local versions against external sources
|   +-- Detects missing, orphaned and obsolete updates
|
+-- Report Service
|   +-- Performs strict library and filename validation
|
+-- Web Dashboard
    +-- Provides monitoring, search, reports and Git integration
```

## Project Structure

``` text
vitesse-control-center/
|
+-- data/
|   +-- SQLite database, caches and application data
|
+-- docs/
|   +-- Project documentation
|
+-- reports/
|   +-- Generated update-audit reports
|
+-- src/
|   +-- VCC application source code
|
+-- tools/
|   +-- Supporting, testing and maintenance tools
|
+-- run.py
|   +-- Main refresh/audit workflow
|
+-- web.py
|   +-- Web interface entry point
|
+-- requirements.txt
|   +-- Python dependencies
|
+-- README.md
```

## Requirements

-   Python 3.8+
-   SQLite
-   Synology DSM (primary target platform)
-   Access to the Nintendo Switch library
-   Network access for external metadata and version synchronization

## Running VCC

The main refresh and audit workflow can be started using:

``` bash
python run.py
```

This scans the library, updates the database, synchronizes external data
sources and runs the update auditor.

The web interface can be started separately using:

``` bash
python web.py
```

The exact configuration depends on the deployment environment and
Synology setup.

## Current Status

VCC is in active development, but its core library-management and
auditing functionality is operational.

Current capabilities include:

-   Recursive library scanning and SQLite indexing
-   Structured BASE / UPDATES / DLC storage
-   Multi-source update-version comparison
-   Missing, orphaned, duplicate and obsolete update detection
-   Library health monitoring
-   Strict library filename reports
-   Interactive web dashboard
-   Integrated Git status and commit/push workflow

Current development is focused on further expanding reporting,
configurable settings, search functionality, automation and maintenance
tooling.

## Development

VCC is primarily developed in Python and is intended to run on a
Synology NAS, although development and testing can also be performed on
other platforms.

The project is under active development, so configuration, database
schema and individual components may change between versions.

## Disclaimer

Vitesse Control Center is a library management and auditing project. 
It does not distribute Nintendo Switch games, updates or other copyrighted content. 
GAMEBOY is an unofficial project acronym, and VCC is not affiliated with or endorsed by Nintendo.

------------------------------------------------------------------------

**Vitesse Control Center --- manage, audit and understand your Nintendo
Switch library.**
