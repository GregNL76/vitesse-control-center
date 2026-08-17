# Changelog

All notable changes to Vitesse Control Center (VCC) are documented in this file.

The project is currently under active development. Entries are grouped by release or development state as the project evolves.

---

## [Unreleased]

### Added
- Expanded web dashboard navigation and management sections.
- Search popup links for external game search services:
  - NSWGF
  - RomsLab
  - EggNS Emulator
  - Ziperto
- Viewport-aware positioning for Search popups.
- Automatic popup repositioning when insufficient space is available on the right, left or bottom of the browser window.

### Improved
- Search popup hover behavior across the dashboard.
- Search popups remain open while moving the cursor from the Search button to the popup.
- Search popups remain open while hovering over individual search links.
- Search popups automatically close after the cursor leaves both the button and popup.
- Added a short hide delay to prevent accidental popup closing while moving the cursor.
- Improved Search popup usability on the Games and Missing Updates pages.
- Standardized search/filter behavior between dashboard pages.
- Improved Games page search filtering by using AG Grid's filter model on the Game/name column.
- Improved Games Search popup positioning for the rightmost table column.
- Improved usability on smaller browser windows and constrained screen sizes.

### Fixed
- Search popups remaining visible after the mouse had left the Search button.
- Search popups being partially clipped outside the browser viewport.
- Games page Search field not filtering the game list correctly.
- Inconsistent Search behavior between Games and Missing Updates.

### Documentation
- Reworked the main README to reflect the current state of VCC instead of the original Foundation milestone.
- Updated project documentation to describe the current library management, Tinfoil synchronization, auditing and web dashboard functionality.

---

## Project Status

VCC is actively developed. Core functionality including library scanning, SQLite storage, Tinfoil synchronization, auditing and the web dashboard is operational and continues to be refined.

Future changes may be reorganized into numbered releases once a formal versioning scheme is established.
