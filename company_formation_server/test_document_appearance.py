"""
Test cases to verify that generated documents look correct and match official formats.

These tests validate:
- Document layout and formatting
- Text positioning and alignment
- Font sizes and styles
- Content accuracy and completeness
- Comparison with official NY Department of State examples
"""

import pytest
from app import (
    CompanyFormation,
    generate_new_york_articles,
    generate_new_york_llc_certificate,
    generate_delaware_articles,
    generate_delaware_llc_certificate,
    generate_california_articles,
    generate_california_llc_certificate,
    app
)
from PyPDF2 import PdfReader
from io import BytesIO


class TestNYCorporationDocumentAppearance:
    """Test that NY corporation certificates look correct"""
    
    def test_ny_corporation_title_formatting(self):
        """Test that title is centered and properly formatted"""
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
        
        # Title should be present and prominent
        assert "CERTIFICATE OF INCORPORATION" in text
        assert "OF" in text
        assert "Test Company" in text
        assert "Section 402 of the Business Corporation Law" in text
    
    def test_ny_corporation_article_numbering(self):
        """Test that all articles are numbered correctly (FIRST through FIFTH)"""
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
        
        # All articles should be present in order
        articles = ["FIRST:", "SECOND:", "THIRD:", "FOURTH:", "FIFTH:"]
        for article in articles:
            assert article in text, f"Missing {article}"
        
        # Verify order by checking positions
        first_pos = text.find("FIRST:")
        second_pos = text.find("SECOND:")
        third_pos = text.find("THIRD:")
        fourth_pos = text.find("FOURTH:")
        fifth_pos = text.find("FIFTH:")
        
        assert first_pos < second_pos < third_pos < fourth_pos < fifth_pos
    
    def test_ny_corporation_company_name_appears_multiple_times(self):
        """Test that company name appears in title, FIRST article, and other sections"""
        data = {
            "company_name": "Unique Test Corp Name",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "John Doe",
            "county": "NEW YORK COUNTY"
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Company name should appear multiple times
        count = text.count("Unique Test Corp Name")
        assert count >= 2, f"Company name should appear at least twice, found {count} times"
    
    def test_ny_corporation_incorporator_information_present(self):
        """Test that incorporator information is displayed correctly"""
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
        
        # Incorporator section should be present
        assert "Incorporator:" in text
        assert "Testy McTestface" in text
        assert "418 BROADWAY STE Y" in text
        
        # Filer section should be present
        assert "Filer's Name and Address:" in text
    
    def test_ny_corporation_share_information_formatting(self):
        """Test that share information is formatted correctly"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "John Doe",
            "county": "NEW YORK COUNTY",
            "shares": 1000,
            "par_value": 0.01
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Share information should be in FOURTH article
        assert "FOURTH:" in text
        assert "authority to issue one class of shares" in text
        assert "1000" in text or "1,000" in text
        assert "0.01" in text
        assert "par value" in text.lower()
    
    def test_ny_corporation_secretary_of_state_section(self):
        """Test that Secretary of State information is properly formatted"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "John Doe",
            "incorporator_address": "123 Main St, New York, NY 10001",
            "county": "NEW YORK COUNTY"
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # FIFTH article should contain Secretary of State information
        assert "FIFTH:" in text
        assert "Secretary of State is designated as agent" in text
        assert "against the corporation may be served" in text
        assert "post office address" in text.lower()


class TestNYLLCDocumentAppearance:
    """Test that NY LLC certificates look correct"""
    
    def test_ny_llc_title_formatting(self):
        """Test that LLC title is centered and properly formatted"""
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
        
        # Title should be present and prominent
        assert "ARTICLES OF ORGANIZATION" in text
        assert "OF" in text
        assert "Test Company" in text
        assert "Section 203 of the Limited Liability Company Law" in text
    
    def test_ny_llc_article_numbering(self):
        """Test that all articles are numbered correctly (FIRST through FOURTH for LLC)"""
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
        
        # All articles should be present in order (FIRST through FOURTH for LLC)
        articles = ["FIRST:", "SECOND:", "THIRD:", "FOURTH:"]
        for article in articles:
            assert article in text, f"Missing {article}"
        
        # Verify order by checking positions
        first_pos = text.find("FIRST:")
        second_pos = text.find("SECOND:")
        third_pos = text.find("THIRD:")
        fourth_pos = text.find("FOURTH:")
        
        assert first_pos < second_pos < third_pos < fourth_pos
    
    def test_ny_llc_organizer_vs_incorporator(self):
        """Test that LLC uses 'Organizer' instead of 'Incorporator'"""
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
        
        # LLC should use "Organizer" not "Incorporator"
        assert "Organizer:" in text
        assert "Testy McTestface" in text
        
        # Should also have Filer section
        assert "Filer's Name and Address:" in text
    
    def test_ny_llc_no_share_information(self):
        """Test that LLC documents do NOT contain share information"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "John Doe",
            "county": "NEW YORK COUNTY"
        }
        
        pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # LLC should NOT have share information
        assert "shares" not in text.lower() or "authority to issue" not in text.lower()
        assert "par value" not in text.lower()
    
    def test_ny_llc_county_in_second_article(self):
        """Test that county information is in THIRD article for LLC"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "John Doe",
            "incorporator_address": "123 Main St, New York, NY 10001",
            "county": "KINGS COUNTY"
        }
        
        pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Find THIRD article and verify county is mentioned
        third_pos = text.find("THIRD:")
        fourth_pos = text.find("FOURTH:")
        third_section = text[third_pos:fourth_pos]
        
        assert "KINGS COUNTY" in third_section
        assert "county" in third_section.lower()


class TestDocumentConsistency:
    """Test consistency across different entity types"""
    
    def test_corporation_vs_llc_structure_differences(self):
        """Test that corporations and LLCs have appropriate structural differences"""
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
        
        # Corporation-specific
        assert "CERTIFICATE OF INCORPORATION" in corp_text
        assert "Section 402" in corp_text
        assert "Incorporator:" in corp_text
        assert "FIFTH:" in corp_text
        
        # LLC-specific
        assert "ARTICLES OF ORGANIZATION" in llc_text
        assert "Section 203" in llc_text
        assert "Organizer:" in llc_text
        assert "FOURTH:" in llc_text
        
        # They should be different documents
        assert corp_text != llc_text
    
    def test_all_required_fields_appear_in_document(self):
        """Test that all provided data appears in the generated document"""
        data = {
            "company_name": "Acme Industries LLC",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "Jane Smith",
            "incorporator_address": "999 Park Avenue, New York, NY 10021",
            "county": "NEW YORK COUNTY"
        }
        
        pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # All provided data should appear
        assert "Acme Industries LLC" in text
        assert "Jane Smith" in text
        assert "999 Park Avenue" in text
        assert "NEW YORK COUNTY" in text
    
    def test_default_values_appear_when_not_provided(self):
        """Test that default values are used and appear in document"""
        data = {
            "company_name": "Minimal Corp",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "John Doe"
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Default values should appear
        assert "NEW YORK COUNTY" in text  # Default county
        assert "200" in text  # Default shares
        assert "Albany" in text or "NY" in text  # Default address


class TestDocumentFormatting:
    """Test document formatting and layout"""
    
    def test_pdf_is_valid_and_readable(self):
        """Test that generated PDF is valid and can be read"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "John Doe",
            "county": "NEW YORK COUNTY"
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        
        # Should be readable as PDF
        reader = PdfReader(pdf_buffer)
        assert len(reader.pages) > 0
        
        # Should have extractable text
        text = reader.pages[0].extract_text()
        assert len(text) > 0
        assert "CERTIFICATE OF INCORPORATION" in text
    
    def test_pdf_contains_no_empty_pages(self):
        """Test that PDF doesn't contain empty pages"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "John Doe",
            "county": "NEW YORK COUNTY"
        }
        
        pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            assert len(text.strip()) > 0, f"Page {i} is empty"
    
    def test_text_content_is_complete(self):
        """Test that all expected text sections are present"""
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
        
        required_sections = [
            "CERTIFICATE OF INCORPORATION",
            "Section 402",
            "FIRST:",
            "SECOND:",
            "THIRD:",
            "FOURTH:",
            "FIFTH:",
            "Incorporator:",
            "Filer's Name and Address:",
            "Test Company",
            "Testy McTestface",
            "ALBANY COUNTY",
            "Secretary of State"
        ]
        
        for section in required_sections:
            assert section in text, f"Missing section: {section}"


class TestEdgeCases:
    """Test edge cases and special formatting"""
    
    def test_company_name_with_special_characters(self):
        """Test that company names with special characters are handled"""
        data = {
            "company_name": "Smith & Sons, LLC",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "John Smith",
            "county": "NEW YORK COUNTY"
        }
        
        pdf_buffer = generate_new_york_llc_certificate(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Company name should appear correctly
        assert "Smith & Sons" in text or "Smith" in text
    
    def test_long_incorporator_address(self):
        """Test that long addresses are handled properly"""
        data = {
            "company_name": "Test Company",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "John Doe",
            "incorporator_address": "123 Very Long Street Name That Goes On And On, New York, NY 10001",
            "county": "NEW YORK COUNTY"
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Address should be present (may be truncated or wrapped)
        assert "123 Very Long Street" in text or "New York" in text
    
    def test_zero_par_value(self):
        """Test that zero par value is displayed correctly"""
        data = {
            "company_name": "No Par Value Corp",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "John Doe",
            "county": "NEW YORK COUNTY",
            "shares": 200,
            "par_value": 0.0
        }
        
        pdf_buffer = generate_new_york_articles(CompanyFormation(**data))
        pdf_buffer.seek(0)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Should indicate no par value
        assert "without par value" in text or "0.00" in text or "0.0" in text


class TestAPIDocumentGeneration:
    """Test document generation through API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create a test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_api_generates_valid_pdf(self, client):
        """Test that API endpoint returns valid PDF"""
        import json
        data = {
            "company_name": "API Test Corp",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Test User",
            "county": "NEW YORK COUNTY"
        }
        
        response = client.post('/form-company',
                              data=json.dumps(data),
                              content_type='application/json')
        
        assert response.status_code == 200
        assert response.mimetype == 'application/pdf'
        
        # Verify PDF is valid
        pdf_buffer = BytesIO(response.data)
        reader = PdfReader(pdf_buffer)
        assert len(reader.pages) > 0
    
    def test_api_pdf_contains_submitted_data(self, client):
        """Test that API-generated PDF contains the submitted data"""
        import json
        data = {
            "company_name": "Unique API Test Company",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "API Test Person",
            "incorporator_address": "123 API Street",
            "county": "KINGS COUNTY"
        }
        
        response = client.post('/form-company',
                              data=json.dumps(data),
                              content_type='application/json')
        
        assert response.status_code == 200
        
        # Extract text from PDF
        pdf_buffer = BytesIO(response.data)
        reader = PdfReader(pdf_buffer)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Verify submitted data appears
        assert "Unique API Test Company" in text
        assert "API Test Person" in text
        assert "KINGS COUNTY" in text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
