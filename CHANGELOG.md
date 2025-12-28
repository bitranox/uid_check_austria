# Changelog

All notable changes to this project will be documented in this file following
the [Keep a Changelog](https://keepachangelog.com/) format.



## [2.3.0] - 2025-12-28

### Fixed

- **Security: HTML injection in email notifications**: Added `html.escape()` to all external data (company names, addresses, error messages) inserted into HTML email bodies. Prevents potential XSS in email clients from malicious company names in BMF responses.

- **Security: Credentials exposed in debug logs**: Masked TID and BENID in debug log output using the same masking function already applied to PIN and session ID.

- **SOAP timeout not applied**: Fixed Zeep client initialization to actually use the configured timeout. Previously, the timeout parameter was stored but never passed to the Transport, allowing SOAP requests to hang indefinitely.

- **Austrian UID validation incomplete**: Strengthened `uid_tn` validation from simple prefix check to full regex pattern `^ATU\d{8}$`. Previously accepted malformed values like "ATU" (just prefix), "ATUXYZ" (letters after prefix), or "ATU1" (wrong length).

- **Cache timestamp semantics**: Cached results now return the original query timestamp instead of the retrieval time. This ensures consistent behavior where `timestamp` always reflects when the UID was verified, not when the cache was read.

- **Duplicate CliExitCode enum value**: Removed `UID_VALID = 0` alias which was identical to `SUCCESS = 0`. Python IntEnum treats same-value members as aliases, causing iteration issues.

- **Email notification failures not visible**: Added `click.echo()` output for email notification failures so CLI users see the warning even without log configuration.

- **from_cache/cached_at invariant not enforced**: Added `__post_init__` validation to `UidCheckResult` ensuring `cached_at` is set when `from_cache=True`.

- **Type hint style**: Removed unnecessary string quotes from type annotations where `from __future__ import annotations` makes them redundant.

### Added

- Translations for email notification warning messages (de, es, fr, ru)

## [2.2.0] - 2025-12-28

### Added

- **UID input sanitization**: UID numbers are now automatically cleaned from copy-paste artifacts in both interactive and script modes:
  - Removes all whitespace (spaces, tabs, newlines, non-breaking spaces, Unicode spaces)
  - Removes zero-width and invisible characters (BOM, zero-width space, joiner, etc.)
  - Removes control characters
  - Normalizes to uppercase
  - Example: `"  de 123 456 789  "` becomes `"DE123456789"`

- **Retry mode with countdown** (`--retryminutes`): New option for interactive mode that retries the check at specified intervals until success or cancellation:
  - Requires `--interactive` mode
  - Shows animated countdown display with time until next attempt and total attempts
  - Only retries on transient errors (network, session, rate limit)
  - Stops immediately on permanent errors (invalid UID, auth, config)
  - Email notification sent only on final result (success or final error), not during retries
  - Handles Ctrl+C gracefully via `lib_cli_exit_tools` signal handling
  - Example: `finanzonline-uid check --interactive --retryminutes 5`

### Changed

- **Code simplifications** (internal, no API changes):
  - Consolidated duplicate parsing functions (`parse_float`, `parse_int`, `parse_string_list`) from `mail.py` into `config.py`
  - Simplified `sanitize_uid()` to use single-pass filtering with combined character set
  - Inlined tiny helper functions in `behaviors.py` into `emit_greeting()`
  - Modernized type hints: replaced `Tuple` with `tuple`, `Optional[X]` with `X | None`

### Fixed

- **Retry mode not retrying on retryable return codes**: The `--retryminutes` option now correctly retries when the FinanzOnline service returns transient errors (return codes -2, -3, 12, 1511, 1512, 1513, 1514). Previously, retryable return codes like 1511 (Service Unavailable) would exit immediately instead of waiting and retrying.
- **Countdown display now shows UID**: The retry countdown animation now displays which UID is being checked, improving visibility during long retry sessions.
- **Retry mode countdown fully localized**: All text in the countdown display is now properly translated (de, es, fr, ru). Removed emoji icon from display for cleaner output.

## [2.1.0] - 2025-12-23

### Fixed

- **Email notification status for service errors**: Return code 1511 (service unavailable) and similar codes no longer incorrectly show status as "INVALID". Email notifications now properly distinguish between:
  - `VALID` / `Valid` - UID is valid (return code 0)
  - `INVALID` / `Invalid` - UID is invalid (return code 1)
  - `UNAVAILABLE` / `Service Unavailable` - Service temporarily unavailable (return codes 1511, 1512, -2)
  - `RATE LIMITED` / `Rate Limited` - Rate limit exceeded (return codes 1513, 1514)
  - `ERROR` / (return code meaning) - Other error codes

### Added

- **Translations for new status labels**: Added translations for UNAVAILABLE, RATE LIMITED, Valid, Invalid, Service Unavailable, and Rate Limited in German, Spanish, French, and Russian locales

## [2.0.1] - 2025-12-23

### Fixed

- **Address not showing in output**: BMF returns address fields as `adrz1`-`adrz6`, not `adr_1`-`adr_6` as documented. Fixed SOAP response extraction to use correct attribute names.
- **Address hidden when name empty**: JSON and console formatters now show company address even when company name is empty (uses `has_company_info` property instead of gating on `name`).

## [2.0.0] - 2025-12-20

### Changed (BREAKING)

- **Package renamed** from `uid_check_austria` to `finanzonline_uid`
- **CLI commands renamed** from `uid-check-austria` / `uid_check_austria` to `finanzonline-uid` / `finanzonline_uid`
- **Environment variable prefix** changed from `UID_CHECK_AUSTRIA___` to `FINANZONLINE_UID___`
- **Configuration paths** changed from `uid-check-austria` to `finanzonline-uid`:
  - Linux: `~/.config/finanzonline-uid/`
  - macOS: `~/Library/Application Support/bitranox/FinanzOnline UID/`
- **Import statements** changed: `from uid_check_austria import ...` → `from finanzonline_uid import ...`

### Migration

To migrate from 1.x:
1. Update imports: replace `uid_check_austria` with `finanzonline_uid`
2. Update CLI calls: replace `uid-check-austria` with `finanzonline-uid`
3. Rename config directories if customized
4. Update environment variables: replace `UID_CHECK_AUSTRIA___` prefix with `FINANZONLINE_UID___`

## [1.0.0] - 2025-12-18

- initial release
