# Vitesse Control Center (VCC)

**Vitesse Control Center (VCC)** is a Nintendo Switch library management and auditing system designed primarily for use on a Synology NAS.

VCC scans a local Nintendo Switch game library, stores the results in SQLite, synchronizes title and update information from Tinfoil, and provides a web-based dashboard for monitoring the health and completeness of the library.

## Features

### Library Management

* Scan and index Nintendo Switch game files
* Detect Base Games, Updates and DLC
* Track installed files and their versions
* Detect orphaned updates
* Detect duplicate updates
* Identify missing updates
* Identify obsolete updates
* Calculate a library health score

### Tinfoil Integration

* Synchronize Nintendo Switch title information
* Retrieve available title and update versions
* Compare locally installed versions against known Tinfoil data
* Identify updates that are missing from the local library

### Web Dashboard

VCC includes a web-based dashboard for monitoring and managing the library.

Current dashboard sections include:

* **Dashboard** — Library statistics, health information and recent additions
* **Games** — Installed games, versions, status and external search links
* **DLC** — DLC inventory and related information
* **Missing Updates** — Updates available according to Tinfoil but missing locally
* **Orphan Updates** — Updates without a matching base game
* **Obsolete Updates** — Updates that are no longer the latest installed version
* **Reports** — Library and audit information
* **Settings** — VCC configuration
* **Git** — Repository/version information

The dashboard uses AG Grid for interactive tables, including sorting, filtering and resizing.

## Architecture

VCC is built around a Python backend with a SQLite database and a web interface.

```text
Vitesse Control Center
¦
+-- Library Scanner
¦   +-- Scans the Nintendo Switch game library
¦
+-- SQLite Database
¦   +-- Stores games, updates, versions and audit information
¦
+-- Tinfoil Synchronization
¦   +-- Synchronizes external title/update information
¦
+-- Auditor
¦   +-- Compares the local library against external data
¦
+-- Web Dashboard
    +-- Provides monitoring and library management
```

## Project Structure

```text
vitesse-control-center/
¦
+-- data/
¦   +-- Local database and application data
¦
+-- docs/
¦   +-- Project documentation
¦
+-- src/
¦   +-- VCC application source code
¦
+-- tools/
¦   +-- Supporting and maintenance tools
¦
+-- run.py
¦   +-- Main application entry point
¦
+-- web.py
¦   +-- Web interface entry point
¦
+-- requirements.txt
¦   +-- Python dependencies
¦
+-- README.md
```

## Requirements

* Python 3.8+
* SQLite
* Synology DSM (primary target platform)
* Access to the Nintendo Switch game library
* Network access for Tinfoil synchronization

## Current Status

VCC is currently in active development.

The core library scanning, database, Tinfoil synchronization, auditing and web dashboard functionality are operational and continue to be refined.

Current development is focused on:

* Improving library auditing
* Expanding update detection
* Improving dashboard usability
* Refining search and filtering
* Improving reporting
* Expanding automation and maintenance functionality

## Running VCC

The main application can be started using:

```bash
python run.py
```

The web interface can be started using:

```bash
python web.py
```

The exact configuration depends on the deployment environment and Synology setup.

## Development

VCC is primarily developed in Python and is intended to run on a Synology NAS, although development and testing can also be performed on other platforms.

The project is under active development, so configuration, database schema and individual components may change between versions.

## Disclaimer

Vitesse Control Center is a library management and auditing project. It does not distribute Nintendo Switch games, updates or other copyrighted content.

---

**Vitesse Control Center — manage, audit and understand your Nintendo Switch library.**
