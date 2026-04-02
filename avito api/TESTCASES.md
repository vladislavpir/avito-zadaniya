# TESTCASES

## Scope

Verified endpoints:

- `POST /api/1/item`
- `GET /api/1/item/{item_id}`
- `GET /api/1/{seller_id}/item`
- `GET /api/1/statistic/{item_id}`

## Notes

- `item_id` is validated as UUID by the API.
- The statistics endpoint returns `likes`, `contacts`, and `viewCount` only; `itemId` is not present in the factual response.
- Every case below has explicit status: `automated` or `manual`.

## Cases

| ID | Endpoint | Scenario | Type | Priority | Status |
| --- | --- | --- | --- | --- | --- |
| TC-CRT-001 | `POST /api/1/item` | Create item with valid payload | positive | P0 | automated |
| TC-CRT-002 | `POST /api/1/item` | Create item with `sellerId=111111` | edge | P1 | automated |
| TC-CRT-003 | `POST /api/1/item` | Create item with `sellerId=999999` | edge | P1 | automated |
| TC-CRT-004 | `POST /api/1/item` | Repeated create with same payload returns different IDs | functional | P1 | automated |
| TC-CRT-101 | `POST /api/1/item` | Missing `name` | negative | P0 | automated |
| TC-CRT-102 | `POST /api/1/item` | Missing `price` | negative | P0 | automated |
| TC-CRT-103 | `POST /api/1/item` | Missing `sellerId` | negative | P0 | automated |
| TC-CRT-104 | `POST /api/1/item` | Missing `statistics` | negative | P0 | automated |
| TC-CRT-105 | `POST /api/1/item` | Missing `statistics.likes` | negative | P0 | automated |
| TC-CRT-106 | `POST /api/1/item` | Missing `statistics.viewCount` | negative | P0 | automated |
| TC-CRT-107 | `POST /api/1/item` | Missing `statistics.contacts` | negative | P0 | automated |
| TC-CRT-108 | `POST /api/1/item` | Malformed JSON body | negative | P1 | automated |
| TC-CRT-109 | `POST /api/1/item` | Invalid field types in JSON body | negative | P0 | automated-xfail |
| TC-GET-001 | `GET /api/1/item/{item_id}` | Read created item by ID | positive | P0 | automated |
| TC-GET-002 | `GET /api/1/item/{item_id}` | Validate item response structure and types | functional | P0 | automated |
| TC-GET-101 | `GET /api/1/item/{item_id}` | Invalid UUID format | negative | P0 | automated |
| TC-GET-102 | `GET /api/1/item/{item_id}` | Nonexistent UUID | negative | P0 | automated |
| TC-SLR-001 | `GET /api/1/{seller_id}/item` | Seller response contains created item | positive | P0 | automated |
| TC-SLR-002 | `GET /api/1/{seller_id}/item` | Seller response contains two created items | functional | P0 | automated |
| TC-SLR-003 | `GET /api/1/{seller_id}/item` | All returned items belong to requested seller | functional | P1 | automated |
| TC-SLR-101 | `GET /api/1/{seller_id}/item` | Invalid seller ID format | negative | P0 | automated |
| TC-SLR-201 | `GET /api/1/{seller_id}/item` | Empty seller list | edge | P1 | automated |
| TC-STA-001 | `GET /api/1/statistic/{item_id}` | Read created item statistics | positive | P0 | automated |
| TC-STA-002 | `GET /api/1/statistic/{item_id}` | Validate statistics response structure and types | functional | P0 | automated |
| TC-STA-101 | `GET /api/1/statistic/{item_id}` | Invalid UUID format | negative | P0 | automated |
| TC-STA-102 | `GET /api/1/statistic/{item_id}` | Nonexistent UUID | negative | P0 | automated |
| TC-FNC-001 | cross-endpoint | Create -> get item -> get statistics consistency | functional | P0 | automated |
| TC-FNC-002 | cross-endpoint | Create two items -> get by seller consistency | functional | P0 | automated |
| TC-EDG-001 | `POST /api/1/item` | Zero `price` | edge | P1 | automated |
| TC-EDG-002 | `POST /api/1/item` | Zero `likes` | edge | P1 | automated |
| TC-EDG-003 | `POST /api/1/item` | Negative `price` is persisted by current API | edge | P2 | automated |
| TC-EDG-004 | `POST /api/1/item` | Negative statistics are persisted by current API | edge | P2 | automated |
| TC-EDG-005 | `POST /api/1/item` | Very long `name` | edge | P2 | automated |
| TC-EDG-006 | `POST /api/1/item` | Special characters in `name` | edge | P2 | automated |
| TC-EDG-007 | `POST /api/1/item` | Non-ASCII `name` | edge | P2 | automated |
| TC-NFR-001 | all endpoints | Basic response time observation | non-functional | P2 | manual |
| TC-NFR-002 | all endpoints | Sequential stability checks | non-functional | P2 | manual |
| TC-CON-001 | `POST /api/1/item` | Parallel creates for one seller | concurrency | P2 | manual |
| TC-CON-002 | read endpoints | Parallel reads of one item | concurrency | P3 | manual |

## Why Some Cases Remain Manual

The project keeps non-functional and concurrency checks as manual because no SLA, rate-limit contract, or environment-isolation guarantees were provided. Automating such checks against a public shared host would create noisy results and false confidence.
