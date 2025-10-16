# Test Summary for NY Corporation and LLC Support

## Overview
Comprehensive test suite verifying that the server correctly generates New York corporation and LLC certificates matching official NY Department of State formats.

## Test File
`test_ny_support.py` - 542 lines, 18 tests

## Test Results
✅ **All 18 tests passing**

## Test Coverage

### 1. TestNYCorporationCertificate (7 tests)
Tests for NY Corporation Certificate of Incorporation (Section 402 of the Business Corporation Law)

#### Tests:
- ✅ `test_ny_corporation_basic_fields` - Validates all required fields are accepted
- ✅ `test_ny_corporation_optional_fields_defaults` - Tests minimal fields with defaults
- ✅ `test_ny_corporation_pdf_generation` - Verifies valid PDF generation
- ✅ `test_ny_corporation_certificate_structure` - Validates FIRST through FIFTH articles format
- ✅ `test_ny_corporation_incorporator_section` - Checks incorporator and filer sections
- ✅ `test_ny_corporation_shares_without_par_value` - Tests shares without par value
- ✅ `test_ny_corporation_default_values` - Validates default values when fields omitted

#### Key Validations:
- Certificate title: "CERTIFICATE OF INCORPORATION"
- Legal reference: "Section 402 of the Business Corporation Law"
- **FIRST**: Company name
- **SECOND**: Purpose clause with consent/approval language
- **THIRD**: County location
- **FOURTH**: Share authorization (number and par value)
- **FIFTH**: Secretary of State as agent for service of process
- Incorporator signature and address
- Filer information

### 2. TestNYLLCCertificate (5 tests)
Tests for NY LLC Articles of Organization (Section 203 of the Limited Liability Company Law)

#### Tests:
- ✅ `test_ny_llc_basic_fields` - Validates all required fields are accepted
- ✅ `test_ny_llc_pdf_generation` - Verifies valid PDF generation
- ✅ `test_ny_llc_certificate_structure` - Validates FIRST through FOURTH articles format
- ✅ `test_ny_llc_organizer_section` - Checks organizer (not incorporator) section
- ✅ `test_ny_llc_different_counties` - Tests multiple NY counties

#### Key Validations:
- Certificate title: "ARTICLES OF ORGANIZATION"
- Legal reference: "Section 203 of the Limited Liability Company Law"
- **FIRST**: Company name
- **SECOND**: Purpose clause (simpler than corporation)
- **THIRD**: County location
- **FOURTH**: Secretary of State as agent (note: FOURTH not FIFTH for LLCs)
- Organizer signature and address (uses "Organizer" not "Incorporator")
- Filer information

### 3. TestNYAPIEndpoints (3 tests)
Tests for API endpoint functionality

#### Tests:
- ✅ `test_ny_corporation_endpoint` - POST /form-company for NY corporation
- ✅ `test_ny_llc_endpoint` - POST /form-company for NY LLC
- ✅ `test_ny_examples_in_schema` - GET /form-company-schema includes NY examples

#### Key Validations:
- Endpoints return 200 status
- Response is valid PDF (application/pdf mimetype)
- Schema endpoint includes at least 2 NY examples (corp + LLC)
- NY examples include all required fields (county, shares, par_value, incorporator_address)

### 4. TestNYCertificateComparison (3 tests)
Tests comparing generated certificates to official NY example formats

#### Tests:
- ✅ `test_corporation_matches_example_format` - Matches example corporation certificate
- ✅ `test_llc_matches_example_format` - Matches example LLC certificate
- ✅ `test_corporation_vs_llc_differences` - Validates appropriate differences

#### Example Certificate References:
**Corporation Example:**
- Company: "Test Company"
- County: "ALBANY COUNTY"
- Address: "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207"
- Shares: 1,000 common shares with $0.01 par value

**LLC Example:**
- Company: "Test Company"
- County: "ALBANY COUNTY"
- Address: "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207"

#### Key Validations:
- All required elements present in generated certificates
- Corporation uses "Incorporator", LLC uses "Organizer"
- Corporation has share information, LLC does not
- Corporation has FIFTH article, LLC has FOURTH article
- Both designate Secretary of State as agent

## Test Data Examples

### NY Corporation Test Data:
```json
{
    "company_name": "Test Company",
    "state_of_formation": "NY",
    "company_type": "corporation",
    "incorporator_name": "Testy McTestface",
    "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
    "county": "ALBANY COUNTY",
    "shares": 1000,
    "par_value": 0.01
}
```

### NY LLC Test Data:
```json
{
    "company_name": "Test Company",
    "state_of_formation": "NY",
    "company_type": "LLC",
    "incorporator_name": "Testy McTestface",
    "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
    "county": "ALBANY COUNTY"
}
```

## Default Values Tested
- **County**: Defaults to "NEW YORK COUNTY" if not provided
- **Shares**: Defaults to 200 if not provided
- **Par Value**: Defaults to 0.0 (no par value) if not provided
- **Address**: Defaults to "123 Main Street, Albany, NY 12207" if not provided

## Running the Tests

### Run NY tests only:
```bash
pytest test_ny_support.py -v
```

### Run all tests:
```bash
pytest -v
```

### Run with coverage:
```bash
pytest test_ny_support.py --cov=app --cov-report=term-missing
```

## Test Statistics
- **Total Tests**: 18
- **Passing**: 18 (100%)
- **Failing**: 0
- **Test Classes**: 4
- **Lines of Test Code**: 542
- **Execution Time**: ~0.34 seconds

## Compliance
These tests verify compliance with:
- **NY Business Corporation Law Section 402** (Corporations)
- **NY Limited Liability Company Law Section 203** (LLCs)
- Official NY Department of State certificate formats
- NY Division of Corporations, State Records and Uniform Commercial Code requirements
