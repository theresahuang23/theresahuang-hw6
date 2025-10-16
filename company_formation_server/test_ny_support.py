"""
Thorough tests for New York corporation and LLC support.

These tests verify that the server correctly generates NY certificates
matching the format of official NY Department of State documents:
- Certificate of Incorporation (Section 402 of the Business Corporation Law)
- Articles of Organization (Section 203 of the Limited Liability Company Law)
"""

import pytest
from app import (
    CompanyFormation, 
    generate_new_york_articles, 
    generate_new_york_llc_certificate,
    app
)
from pydantic import ValidationError
from PyPDF2 import PdfReader
import json


class TestNYCorporationCertificate:
    """Tests for NY Corporation Certificate of Incorporation"""
    
    def test_ny_corporation_basic_fields(self):
        """Test that NY corporation accepts all required fields"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Testy McTestface",
            "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
            "county": "ALBANY COUNTY",
            "shares": 1000,
            "par_value": 0.01
        }
        company = CompanyFormation(**data)
        assert company.state_of_formation == "NY"
        assert company.company_type == "corporation"
        assert company.county == "ALBANY COUNTY"
        assert company.shares == 1000
        assert company.par_value == 0.01
    
    def test_ny_corporation_optional_fields_defaults(self):
        """Test that NY corporation works with minimal fields and uses defaults"""
        data = {
            "company_name": "Minimal Corp",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "John Doe"
        }
        company = CompanyFormation(**data)
        assert company.county is None  # Will use default in generation
        assert company.shares is None  # Will use default in generation
        assert company.par_value is None  # Will use default in generation
    
    def test_ny_corporation_pdf_generation(self):
        """Test that NY corporation generates a valid PDF"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Testy McTestface",
            "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
            "county": "ALBANY COUNTY",
            "shares": 1000,
            "par_value": 0.01
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        # Verify it's a valid PDF
        reader = PdfReader(pdf_buffer)
        assert len(reader.pages) > 0
        
        # Extract text from all pages
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Verify document title and header
        assert "CERTIFICATE OF INCORPORATION" in text
        assert "Test Company" in text
        assert "Section 402 of the Business Corporation Law" in text
    
    def test_ny_corporation_certificate_structure(self):
        """Test that NY corporation certificate follows official format with FIRST through FIFTH articles"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Testy McTestface",
            "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
            "county": "ALBANY COUNTY",
            "shares": 1000,
            "par_value": 0.01
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # FIRST: Company name
        assert "FIRST:" in text
        assert "The name of this corporation is:" in text
        assert "Test Company" in text
        
        # SECOND: Purpose clause
        assert "SECOND:" in text
        assert "The purpose of the corporation is to engage in any lawful act or activity" in text
        assert "Business Corporation Law" in text
        assert "consent or approval" in text
        
        # THIRD: County
        assert "THIRD:" in text
        assert "county, within this state" in text
        assert "ALBANY COUNTY" in text
        
        # FOURTH: Shares
        assert "FOURTH:" in text
        assert "authority to issue one class of shares" in text
        assert "1000" in text or "1,000" in text
        assert "0.01" in text
        
        # FIFTH: Secretary of State as agent
        assert "FIFTH:" in text
        assert "Secretary of State is designated as agent" in text
        assert "against the corporation may be served" in text
        assert "418 BROADWAY STE Y" in text
    
    def test_ny_corporation_incorporator_section(self):
        """Test that incorporator and filer information is included"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Testy McTestface",
            "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
            "county": "ALBANY COUNTY",
            "shares": 1000,
            "par_value": 0.01
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Incorporator section
        assert "Incorporator:" in text
        assert "/s/ Testy McTestface" in text or "Testy McTestface" in text
        
        # Filer section
        assert "Filer's Name and Address:" in text
    
    def test_ny_corporation_shares_without_par_value(self):
        """Test NY corporation with shares without par value"""
        data = {
            "company_name": "No Par Value Corp",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "John Smith",
            "incorporator_address": "123 Main St, New York, NY 10001",
            "county": "NEW YORK COUNTY",
            "shares": 200,
            "par_value": 0.0  # No par value
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        assert "200" in text
        assert "without par value" in text or "0.00" in text
    
    def test_ny_corporation_default_values(self):
        """Test that default values are used when optional fields are omitted"""
        data = {
            "company_name": "Default Values Corp",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Jane Doe"
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Should use default county
        assert "NEW YORK COUNTY" in text or "county" in text.lower()
        
        # Should use default shares (200)
        assert "200" in text
        
        # Should have default address
        assert "Albany" in text or "NY" in text


class TestNYLLCCertificate:
    """Tests for NY LLC Articles of Organization"""
    
    def test_ny_llc_basic_fields(self):
        """Test that NY LLC accepts all required fields"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "Testy McTestface",
            "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
            "county": "ALBANY COUNTY"
        }
        company = CompanyFormation(**data)
        assert company.state_of_formation == "NY"
        assert company.company_type == "LLC"
        assert company.county == "ALBANY COUNTY"
    
    def test_ny_llc_pdf_generation(self):
        """Test that NY LLC generates a valid PDF"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "Testy McTestface",
            "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
            "county": "ALBANY COUNTY"
        }
        
        pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        # Verify it's a valid PDF
        reader = PdfReader(pdf_buffer)
        assert len(reader.pages) > 0
        
        # Extract text
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Verify document title
        assert "ARTICLES OF ORGANIZATION" in text
        assert "Test Company" in text
        assert "Section 203 of the Limited Liability Company Law" in text
    
    def test_ny_llc_certificate_structure(self):
        """Test that NY LLC certificate follows official format with FIRST through FOURTH articles"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "Testy McTestface",
            "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
            "county": "ALBANY COUNTY"
        }
        
        pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # FIRST: Company name
        assert "FIRST:" in text
        assert "The name of the limited liability company is:" in text
        assert "Test Company" in text
        
        # SECOND: Purpose (Note: NY LLC has simpler purpose than corporation)
        assert "SECOND:" in text
        assert "purpose of the limited liability company" in text
        assert "lawful act or activity" in text
        
        # THIRD: County
        assert "THIRD:" in text
        assert "county, within this state" in text
        assert "ALBANY COUNTY" in text
        
        # FOURTH: Secretary of State as agent (Note: LLC uses "FOURTH" not "FIFTH")
        assert "FOURTH:" in text
        assert "Secretary of State is designated as agent" in text
        assert "limited liability company" in text
        assert "418 BROADWAY STE Y" in text
    
    def test_ny_llc_organizer_section(self):
        """Test that organizer and filer information is included (LLC uses 'Organizer' not 'Incorporator')"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "Testy McTestface",
            "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
            "county": "ALBANY COUNTY"
        }
        
        pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Organizer section (not Incorporator for LLCs)
        assert "Organizer:" in text
        assert "Testy McTestface" in text
        
        # Filer section
        assert "Filer's Name and Address:" in text
    
    def test_ny_llc_different_counties(self):
        """Test NY LLC with different county locations"""
        counties = ["NEW YORK COUNTY", "KINGS COUNTY", "QUEENS COUNTY", "ALBANY COUNTY"]
        
        for county in counties:
            data = {
                "company_name": f"{county} LLC",
                "state_of_formation": "NY",
                "company_type": "LLC",
                "incorporator_name": "Test Person",
                "incorporator_address": "123 Main St, New York, NY 10001",
                "county": county
            }
            
            pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**data))
            pdf_buffer.seek(0)
            
            reader = PdfReader(pdf_buffer)
            text = "\n".join(page.extract_text() for page in reader.pages)
            
            assert county in text


class TestNYAPIEndpoints:
    """Test API endpoints for NY corporations and LLCs"""
    
    @pytest.fixture
    def client(self):
        """Create a test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_ny_corporation_endpoint(self, client):
        """Test POST to /form-company for NY corporation"""
        data = {
            "company_name": "Empire State Corp.",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Sarah Williams",
            "incorporator_address": "418 Broadway Ste Y, Albany, Albany County, NY 12207",
            "county": "Albany County",
            "shares": 1000,
            "par_value": 0.01
        }
        
        response = client.post('/form-company',
                              data=json.dumps(data),
                              content_type='application/json')
        
        assert response.status_code == 200
        assert response.mimetype == 'application/pdf'
        assert len(response.data) > 0
    
    def test_ny_llc_endpoint(self, client):
        """Test POST to /form-company for NY LLC"""
        data = {
            "company_name": "Big Apple Ventures, LLC",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "David Chen",
            "incorporator_address": "123 Main Street, New York, NY 10001",
            "county": "New York County"
        }
        
        response = client.post('/form-company',
                              data=json.dumps(data),
                              content_type='application/json')
        
        assert response.status_code == 200
        assert response.mimetype == 'application/pdf'
        assert len(response.data) > 0
    
    def test_ny_examples_in_schema(self, client):
        """Test that /form-company-schema includes NY examples"""
        response = client.get('/form-company-schema')
        
        assert response.status_code == 200
        examples = json.loads(response.data)
        
        # Find NY examples
        ny_examples = [ex for ex in examples if ex.get('state_of_formation') == 'NY']
        
        assert len(ny_examples) >= 2  # Should have at least corp and LLC
        
        # Check for corporation example
        ny_corp = next((ex for ex in ny_examples if ex.get('company_type') == 'corporation'), None)
        assert ny_corp is not None
        assert 'county' in ny_corp
        assert 'shares' in ny_corp
        assert 'par_value' in ny_corp
        assert 'incorporator_address' in ny_corp
        
        # Check for LLC example
        ny_llc = next((ex for ex in ny_examples if ex.get('company_type') == 'LLC'), None)
        assert ny_llc is not None
        assert 'county' in ny_llc
        assert 'incorporator_address' in ny_llc


class TestNYCertificateComparison:
    """
    Tests comparing generated certificates to official NY examples.
    
    Based on the provided example certificates:
    - Corporation: Test Company under Section 402
    - LLC: Test Company under Section 203
    """
    
    def test_corporation_matches_example_format(self):
        """Test that generated corporation certificate matches the example format"""
        # Data matching the example certificate
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Testy McTestface",
            "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
            "county": "ALBANY COUNTY",
            "shares": 1000,
            "par_value": 0.01
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Verify all key elements from the example certificate
        required_elements = [
            "CERTIFICATE OF INCORPORATION",
            "Test Company",
            "Section 402 of the Business Corporation Law",
            "FIRST:",
            "The name of this corporation is:",
            "SECOND:",
            "purpose of the corporation",
            "THIRD:",
            "ALBANY COUNTY",
            "FOURTH:",
            "authority to issue one class of shares",
            "FIFTH:",
            "Secretary of State is designated as agent",
            "418 BROADWAY STE Y",
            "Incorporator:",
            "Filer's Name and Address:"
        ]
        
        for element in required_elements:
            assert element in text, f"Missing required element: {element}"
    
    def test_llc_matches_example_format(self):
        """Test that generated LLC certificate matches the example format"""
        # Data matching the example LLC certificate
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "Testy McTestface",
            "incorporator_address": "418 BROADWAY STE Y, ALBANY, ALBANY COUNTY, NY 12207",
            "county": "ALBANY COUNTY"
        }
        
        pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Verify all key elements from the example LLC certificate
        required_elements = [
            "ARTICLES OF ORGANIZATION",
            "Test Company",
            "Section 203 of the Limited Liability Company Law",
            "FIRST:",
            "The name of the limited liability company is:",
            "SECOND:",
            "ALBANY COUNTY",
            "THIRD:",
            "Secretary of State is designated as agent",
            "limited liability company",
            "418 BROADWAY STE Y",
            "Organizer:",
            "Filer's Name and Address:"
        ]
        
        for element in required_elements:
            assert element in text, f"Missing required element: {element}"
    
    def test_corporation_vs_llc_differences(self):
        """Test that corporation and LLC certificates have appropriate differences"""
        corp_data = {
            "company_name": "Test Corp",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Test Person",
            "county": "NEW YORK COUNTY",
            "shares": 200
        }
        
        llc_data = {
            "company_name": "Test LLC",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "Test Person",
            "county": "NEW YORK COUNTY"
        }
        
        corp_pdf = generate_new_york_articles(CompanyFormation(**corp_data))
        llc_pdf = generate_new_york_llc_certificate(CompanyFormation(**llc_data))
        
        corp_text = "\n".join(page.extract_text() for page in PdfReader(corp_pdf).pages)
        llc_text = "\n".join(page.extract_text() for page in PdfReader(llc_pdf).pages)
        
        # Corporation-specific elements
        assert "CERTIFICATE OF INCORPORATION" in corp_text
        assert "Section 402" in corp_text
        assert "Business Corporation Law" in corp_text
        assert "Incorporator:" in corp_text
        assert "shares" in corp_text.lower()
        
        # LLC-specific elements
        assert "ARTICLES OF ORGANIZATION" in llc_text
        assert "Section 203" in llc_text
        assert "Limited Liability Company Law" in llc_text
        assert "Organizer:" in llc_text
        assert "limited liability company" in llc_text.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
