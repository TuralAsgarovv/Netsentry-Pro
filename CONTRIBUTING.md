# Contributing to NetSentry-Pro

We welcome contributions! Please follow these guidelines to ensure code quality and safety.

1. **Fork & Branch**: Create a feature branch (`feature/ipv6-support`) rather than pushing to main.
2. **Type Hinting**: All new functions must include Python type hints.
3. **Tests**: Add unit tests in `tests/` for any new utility logic.
4. **Safety**: Do not include any exploit payloads or aggressive flooding logic. This is an audit tool, not a weapon.
5. **Linting**: Run `flake8` before submitting.

## TODO Roadmap
- [ ] Implement OS Fingerprinting.
- [ ] Add JSON output format.
- [ ] Add UDP scanning support.
