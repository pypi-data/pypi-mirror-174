# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [7.2.1 - 2022-11-01]

### Changed

- Fixed on Python 3.7 and 3.8.

## [7.2.0 - 2022-11-01]

### Changed

- Use new format for new tokens.

## [7.1.2 - 2022-11-01]

### Changed

- Fixed launch output with recent API changes.

## [7.1.1 - 2022-09-29]

### Changed

- Fixed hostname related bug when launching a server.

## [7.1.0 - 2022-09-27]

### Added

- `sporestack server autorenew-enable/disable`

### Changed

- Show autorenew status and associated token in `sporestack server list` (not in all cases, however)

## [7.0.0 - 2022-09-07]

### Added

- `sporestack server list` now accepts `--local` or `--no-local`.
- `sporestack server operating-systems`

### Changed

- `sporestack server` subcommands take `--hostname` or `--machine-id`.
- `sporestack server flavors` output is slightly more readable.

### Removed

- `sporestack server delete` (in favor of: `sporestack server destroy`)
- `sporestack server get-attribute`

## [6.2.0 - 2022-09-07]

### Added

- Allow for new *beta* `--autorenew` feature with `sporestack server launch`.

### Changed

- No longer save server JSON to disk for new servers.

## [6.1.0 - 2022-06-14]

### Changed

- Use servers launched by token endpoint in `sporestack server list`.
- Send server hostname to SporeStack API at launch time.

## [6.0.3 - 2022-04-22]

### Changed

- Bug fixes.

## [6.0.2 - 2022-04-22]

### Changed

- Replace setuptools with flit.

## [6.0.1 - 2022-04-22]

### Changed

- Use `requests` session for improved performance, in particular for `sporestack server list`.

## [6.0.0 - 2022-04-14]

### Fixed

- Use specified API endpoint for `sporestack server list` command.

## [6.0.0a3 - 2022-04-05]

### Removed

- Get rid of deprecated TokenEnable usage.

## [6.0.0a2 - 2022-04-01]

### Added

- `--quote` / `--no-quote` to launch/topup. Prompt by default if price to draw from token is acceptable.

### Removed

- affiliate_amount

### Fixed

- Protect files in ~/.sporestack with aggressive `umask`.

## [6.0.0a1 - 2022-03-31]

Remember to backup your ~/.sporestack folder as any tokens you generate will be stored there!

### Changed

- Now token-centric. You can only use `sporestack` to launch or topup servers from a token.
- `sporestack launch/info/topup`, etc, moved to `sporestack server launch/info/topup`, etc.
- `--token` argument takes the name of the token, and not the key. Defaults to `primary`.
- `--ssh-key-file` now defaults to `~/.ssh/id_rsa.pub`.
- Import generated tokens from the key with: `sporestack token import (token reference name, default is primary) --key (the token key in hex format)`

### Added

- New token commands: `sporestack token create/list`

## [5.2.3 - 2022-03-30]

### Added

- Use `~/.sporestack/servers` instead of `~/.sporestack`. Will migrate existing servers automatically.

## [5.2.2 - 2022-02-24]

### Added

- Better `sporestack list` expired server handling.

## [5.2.1 - 2022-02-10]

### Added

- New, 32 character machine ID format. (Old, 64 hex character format still supported.)
- CHANGELOG.md in Keep a Changelog format.

## [5.2.0 - 2022-01-31]

### Added

- `sporestack rebuild` command.

## [5.1.2 - 2021-10-18]

### Added

- Send `sporestack-python/version` in Use-Agent header.
