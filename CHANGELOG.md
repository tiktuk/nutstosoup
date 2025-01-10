# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2024-01-24

### Added
- Complete dataclass representation of broadcast and mixtape JSON structures
- Raw JSON field to dataclasses for access to original API response
- Helper methods for simplified API responses

### Changed
- Improved package organization and documentation
- Moved data models to dedicated file for better code organization
- Renamed Media to BroadcastMedia for better naming consistency
- Enhanced API design for improved usability

### Fixed
- Various test improvements and fixes

## [0.3.0] - 2024-01-07

### Added
- HTML entity unescaping for broadcast titles (e.g. "&amp;" becomes "&")

## [0.2.0] - Initial Release

Initial version with basic NTS Radio API functionality.
