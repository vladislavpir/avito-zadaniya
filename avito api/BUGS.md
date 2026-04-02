# BUGS

## Status

This file contains only confirmed defects observed during factual API probing on `2026-04-01` and `2026-04-02` against the public host.

## BUG-001

**Short description**  
`POST /api/1/item` returns a misleading status value when a JSON body is present but contains invalid field types.

**Request**  
`POST https://qa-internship.avito.com/api/1/item`

**Request headers**

```http
Content-Type: application/json
Accept: */*
User-Agent: python-requests/2.32.5
```

**Steps to reproduce**  
1. Send a request with string `sellerId`:
   ```json
   {
     "sellerId": "abc",
     "name": "x",
     "price": 1,
     "statistics": {
       "likes": 1,
       "viewCount": 1,
       "contacts": 1
     }
   }
   ```
2. Repeat with string `price`:
   ```json
   {
     "sellerId": 111111,
     "name": "x",
     "price": "1",
     "statistics": {
       "likes": 1,
       "viewCount": 1,
       "contacts": 1
     }
   }
   ```

**Actual result**  
HTTP `400` with response body:

```json
{
  "result": {
    "message": "",
    "messages": {}
  },
  "status": "не передано тело объявления"
}
```

The API reports that the body was not sent, although a valid JSON body was sent with `Content-Type: application/json`.

**Expected result**  
HTTP `400` with a field validation error that points to the invalid field type, for example `sellerId` or `price`.

**Severity**  
Medium

**Environment**

- Host: `https://qa-internship.avito.com`
- Endpoint: `POST /api/1/item`
- Dates observed: `2026-04-01`, `2026-04-02`
- Client: `python-requests 2.32.5`
- OS: Windows
- Python: 3.10

---

## Bug Report Template

### BUG-XXX

**Short description**  
One-sentence summary.

**Request**  
Method and URL.

**Request headers**

```http
Content-Type: application/json
```

**Steps to reproduce**  
1. Step one.
2. Step two.
3. Step three.

**Actual result**  
What the service actually does.

**Expected result**  
What the service should do.

**Severity**  
Blocker / High / Medium / Low

**Environment**

- Host:
- Endpoint:
- Date observed:
- Client:
- OS:
- Python:
