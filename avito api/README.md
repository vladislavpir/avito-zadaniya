# Avito Ads API Test Solution

## Description

A practical pytest-based API test project for the Avito internship ads microservice.

Verified endpoints:

- `POST /api/1/item`
- `GET /api/1/item/{item_id}`
- `GET /api/1/{seller_id}/item`
- `GET /api/1/statistic/{item_id}`

The project includes:

- API client with Allure request/response attachments
- reusable response assertions
- pydantic-based response validation
- positive, negative, edge, and E2E tests
- `TESTCASES.md` with `automated` / `manual` status
- `BUGS.md` with confirmed defects only
- Ruff / Black / isort configuration

## Project Structure

```text
avito api/
├── framework/
│   ├── api_client.py
│   ├── assertions.py
│   ├── config.py
│   ├── factories.py
│   ├── generators.py
│   └── models.py
├── tests/
│   ├── api/
│   │   ├── test_create_item.py
│   │   ├── test_edge_cases.py
│   │   ├── test_e2e_items_flow.py
│   │   ├── test_get_item.py
│   │   ├── test_get_seller_items.py
│   │   └── test_get_statistics.py
│   └── conftest.py
├── .gitignore
├── BUGS.md
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
└── TESTCASES.md
```

## Requirements

- Python 3.10+
- Internet access to `https://qa-internship.avito.com`
- Optional: Java + Allure CLI

## Environment Setup

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Optional environment variables:

- `BASE_URL` - default: `https://qa-internship.avito.com`
- `REQUEST_TIMEOUT` - default: `15`

Examples:

```powershell
$env:BASE_URL="https://qa-internship.avito.com"
$env:REQUEST_TIMEOUT="20"
```

```bash
export BASE_URL="https://qa-internship.avito.com"
export REQUEST_TIMEOUT="20"
```

## Run Tests

Run all tests:

```bash
pytest
```

Run smoke:

```bash
pytest -m smoke
```

Run regression:

```bash
pytest -m regression
```

Run edge cases:

```bash
pytest -m edge
```

Run negative scenarios:

```bash
pytest -m negative
```

Run E2E:

```bash
pytest -m e2e
```

Run one module:

```bash
pytest tests/api/test_get_item.py -v
```

## Run Allure

Generate results:

```bash
pytest --alluredir=allure-results
```

Open interactive report:

```bash
allure serve allure-results
```

Build static report:

```bash
allure generate allure-results --clean -o allure-report
```

## Run Code Quality Tools

```bash
ruff check .
black --check .
isort --check-only .
```

Auto-fix:

```bash
ruff check . --fix
black .
isort .
```

## sellerId Strategy

Tests generate seller IDs in the recommended `111111-999999` range to reduce collisions with shared public data.

For the empty seller list scenario, the suite tries multiple random seller IDs until it finds one that returns an empty list. If no such seller is found in the shared environment, the test is skipped with an explicit reason.

## Verified Contract Notes

- `GET /api/1/item/{item_id}` returns a list with one item, not a single object.
- `GET /api/1/statistic/{item_id}` returns a list with one statistics object.
- The statistics response currently contains `likes`, `contacts`, and `viewCount` only. It does **not** return `itemId`, so the suite does not invent that field in validations.
- `POST /api/1/item` requires `sellerId`, `name`, `price`, and `statistics` with `likes`, `viewCount`, and `contacts`.

## Known Defects

See [BUGS.md](BUGS.md).

Confirmed defect currently covered by an `xfail` test:

- invalid typed JSON body may return misleading status `"не передано тело объявления"` instead of a field validation error

## Reproducibility Notes

- Dependencies are pinned in `requirements.txt`.
- Generated files are excluded by `.gitignore`.
- The suite was designed to run immediately after `pip install -r requirements.txt`.
- The project depends on a shared external environment, so intermittent failures are still possible if the public API changes or becomes unavailable.
