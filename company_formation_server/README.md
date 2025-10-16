# Company Formation Server

This server accepts company formation data and generates Articles of Incorporation/Organization for Delaware, California, and New York corporations and LLCs.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

## API Usage

Send a POST request to `/form-company` with a JSON payload in the following format:

### Delaware Example:
```json
{
    "company_name": "Acme Corp, Inc.",
    "state_of_formation": "DE",
    "company_type": "corporation",
    "incorporator_name": "John Smith"
}
```

### New York Example:
```json
{
    "company_name": "Empire State Corp.",
    "state_of_formation": "NY",
    "company_type": "corporation",
    "incorporator_name": "Sarah Williams",
    "incorporator_address": "418 Broadway Ste Y, Albany, Albany County, NY 12207",
    "county": "Albany County",
    "shares": 1000,
    "par_value": 0.01
}
```

### Validation Rules:
- **Company name**: Can contain alphanumeric characters, spaces, commas, periods, apostrophes, and ampersands
- **State of formation**: Must be a valid US state or territory code (DE, CA, or NY supported)
- **Company type**: Must be either "corporation" or "LLC"
- **Incorporator name**: Required field
- **Incorporator address**: Optional (required for NY)
- **County**: Optional (required for NY)
- **Shares**: Optional (used for NY corporations, defaults to 200)
- **Par value**: Optional (used for NY corporations, defaults to 0.0 for no par value)

### Supported States:
- **Delaware (DE)**: Corporations and LLCs
- **California (CA)**: Corporations and LLCs
- **New York (NY)**: Corporations and LLCs

### Response:
Returns a PDF file containing the Certificate of Incorporation/Formation or Articles of Organization

## Example cURL Requests:

### Delaware Corporation:
```bash
curl -X POST http://localhost:8080/form-company \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp, Inc.",
    "state_of_formation": "DE",
    "company_type": "corporation",
    "incorporator_name": "John Smith"
  }' -o certificate.pdf
```

### New York Corporation:
```bash
curl -X POST http://localhost:8080/form-company \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Empire State Corp.",
    "state_of_formation": "NY",
    "company_type": "corporation",
    "incorporator_name": "Sarah Williams",
    "incorporator_address": "418 Broadway Ste Y, Albany, Albany County, NY 12207",
    "county": "Albany County",
    "shares": 1000,
    "par_value": 0.01
  }' -o ny_certificate.pdf
```

### New York LLC:
```bash
curl -X POST http://localhost:8080/form-company \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Big Apple Ventures, LLC",
    "state_of_formation": "NY",
    "company_type": "LLC",
    "incorporator_name": "David Chen",
    "incorporator_address": "123 Main Street, New York, NY 10001",
    "county": "New York County"
  }' -o ny_llc.pdf
```
