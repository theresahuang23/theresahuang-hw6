from flask import Flask, request, jsonify, send_file
from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
import re
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import os

app = Flask(__name__)

class CompanyFormation(BaseModel):
    company_name: str = Field(..., description="Company name")
    state_of_formation: str = Field(..., description="US state or territory")
    company_type: Literal["corporation", "LLC"] = Field(..., description="Type of company")
    incorporator_name: str = Field(..., description="Name of incorporator")
    incorporator_address: Optional[str] = Field(None, description="Address of incorporator (required for NY)")
    county: Optional[str] = Field(None, description="County for office location (required for NY)")
    shares: Optional[int] = Field(None, description="Number of shares (required for NY corporations)")
    par_value: Optional[float] = Field(None, description="Par value per share (required for NY corporations)")

    @validator('company_name')
    def validate_company_name(cls, v):
        if not re.match(r'^[a-zA-Z0-9\s,\.\'&]+$', v):
            raise ValueError('Company name can only contain alphanumeric characters, spaces, commas, periods, apostrophes, and ampersands')
        return v

    @validator('state_of_formation')
    def validate_state(cls, v):
        states = {
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
            'DC', 'PR', 'GU', 'VI', 'AS', 'MP'
        }
        if v.upper() not in states:
            raise ValueError('Invalid US state or territory')
        return v.upper()

def generate_delaware_articles(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "CERTIFICATE OF INCORPORATION")
    c.setFont("Helvetica", 12)
    
    # Article First - Company Name
    c.drawString(50, 700, "FIRST: The name of this corporation is:")
    c.drawString(70, 680, company_data.company_name)
    
    # Article Second - Registered Office
    c.drawString(50, 630, "SECOND: Its registered office in the State of Delaware is located at:")
    c.drawString(70, 610, "251 Little Falls Drive, Wilmington, New Castle County, Delaware 19808")
    
    # Article Third - Purpose
    c.drawString(50, 560, "THIRD: The purpose of the corporation is to engage in any lawful act or activity for")
    c.drawString(50, 540, "which corporations may be organized under the General Corporation Law of Delaware.")
    
    # Article Fourth - Authorized Shares
    c.drawString(50, 490, "FOURTH: The total number of shares of stock which this corporation is authorized")
    c.drawString(50, 470, "to issue is 1,000 shares of Common Stock with $0.01 par value per share.")
    
    # Incorporator
    c.drawString(50, 200, f"IN WITNESS WHEREOF, the undersigned, being the incorporator hereinbefore named,")
    c.drawString(50, 180, f"has executed this Certificate of Incorporation this {datetime.now().strftime('%d')} day of")
    c.drawString(50, 160, f"{datetime.now().strftime('%B, %Y')}.")
    
    c.drawString(50, 100, "Incorporator:")
    c.drawString(70, 80, company_data.incorporator_name)
    
    c.save()
    buffer.seek(0)
    return buffer

def generate_delaware_llc_certificate(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "CERTIFICATE OF FORMATION")
    c.setFont("Helvetica", 12)
    
    # Article First - Company Name
    c.drawString(50, 700, "FIRST: The name of the limited liability company is:")
    c.drawString(70, 680, company_data.company_name)
    
    # Article Second - Registered Office
    c.drawString(50, 630, "SECOND: The address of its registered office in the State of Delaware is:")
    c.drawString(70, 610, "251 Little Falls Drive, Wilmington, New Castle County, Delaware 19808")
    
    # Article Third - Registered Agent
    c.drawString(50, 560, "THIRD: The name and address of its registered agent in the State of Delaware is:")
    c.drawString(70, 540, "Corporation Service Company")
    c.drawString(70, 520, "251 Little Falls Drive")
    c.drawString(70, 500, "Wilmington, DE 19808")
    
    # Article Fourth - Management
    c.drawString(50, 450, "FOURTH: The limited liability company shall be managed by its members.")
    
    # Execution
    c.drawString(50, 200, f"IN WITNESS WHEREOF, the undersigned has executed this Certificate of Formation this {datetime.now().strftime('%d')} day of")
    c.drawString(50, 180, f"{datetime.now().strftime('%B, %Y')}.")
    
    c.drawString(50, 100, "Authorized Person:")
    c.drawString(70, 80, company_data.incorporator_name)
    
    c.save()
    buffer.seek(0)
    return buffer

def generate_california_articles(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "ARTICLES OF INCORPORATION")
    c.setFont("Helvetica", 12)
    
    # Article I - Company Name
    c.drawString(50, 700, "ARTICLE I: The name of this corporation is:")
    c.drawString(70, 680, company_data.company_name)
    
    # Article II - Purpose
    c.drawString(50, 630, "ARTICLE II: The purpose of the corporation is to engage in any lawful act or activity")
    c.drawString(50, 610, "for which a corporation may be organized under the General Corporation Law of California.")
    
    # Article III - Agent for Service
    c.drawString(50, 560, "ARTICLE III: The name and address in California of the corporation's initial agent for service of process is:")
    c.drawString(70, 540, "California Registered Agent, Inc.")
    c.drawString(70, 520, "123 Main Street")
    c.drawString(70, 500, "Los Angeles, CA 90001")
    
    # Incorporator
    c.drawString(50, 200, f"IN WITNESS WHEREOF, the undersigned, being the incorporator hereinbefore named,")
    c.drawString(50, 180, f"has executed these Articles of Incorporation this {datetime.now().strftime('%d')} day of")
    c.drawString(50, 160, f"{datetime.now().strftime('%B, %Y')}.")
    
    c.drawString(50, 100, "Incorporator:")
    c.drawString(70, 80, company_data.incorporator_name)
    
    c.save()
    buffer.seek(0)
    return buffer

def generate_california_llc_certificate(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "ARTICLES OF ORGANIZATION")
    c.setFont("Helvetica", 12)
    
    # Article I - Company Name
    c.drawString(50, 700, "ARTICLE I: The name of the limited liability company is:")
    c.drawString(70, 680, company_data.company_name)
    
    # Article II - Purpose
    c.drawString(50, 630, "ARTICLE II: The purpose of the limited liability company is to engage in any lawful business.")
    
    # Article III - Agent for Service
    c.drawString(50, 560, "ARTICLE III: The name and address in California of the LLC's initial agent for service of process is:")
    c.drawString(70, 540, "California Registered Agent, Inc.")
    c.drawString(70, 520, "123 Main Street")
    c.drawString(70, 500, "Los Angeles, CA 90001")
    
    # Execution
    c.drawString(50, 200, f"IN WITNESS WHEREOF, the undersigned has executed these Articles of Organization this {datetime.now().strftime('%d')} day of")
    c.drawString(50, 180, f"{datetime.now().strftime('%B, %Y')}.")
    
    c.drawString(50, 100, "Authorized Person:")
    c.drawString(70, 80, company_data.incorporator_name)
    
    c.save()
    buffer.seek(0)
    return buffer

def generate_new_york_articles(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(300, 750, "CERTIFICATE OF INCORPORATION")
    c.drawCentredString(300, 730, "OF")
    c.drawCentredString(300, 710, company_data.company_name)
    c.setFont("Helvetica", 11)
    c.drawCentredString(300, 690, "Under Section 402 of the Business Corporation Law")
    
    # FIRST - Company Name
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 650, "FIRST:")
    c.setFont("Helvetica", 11)
    c.drawString(100, 650, "The name of this corporation is:")
    c.drawString(70, 630, company_data.company_name)
    
    # SECOND - Purpose
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 590, "SECOND:")
    c.setFont("Helvetica", 11)
    c.drawString(100, 590, "The purpose of the corporation is to engage in any lawful act or activity for which")
    c.drawString(50, 570, "a corporation may be organized under the Business Corporation Law. The corporation is not")
    c.drawString(50, 550, "formed to engage in any act or activity requiring the consent or approval of any state official,")
    c.drawString(50, 530, "department, board, agency or other body without such consent or approval first being obtained.")
    
    # THIRD - County
    county = company_data.county if company_data.county else "NEW YORK COUNTY"
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 490, "THIRD:")
    c.setFont("Helvetica", 11)
    c.drawString(100, 490, "The county, within this state, in which the office of the corporation is to be located")
    c.drawString(50, 470, f"is: {county.upper()}.")
    
    # FOURTH - Shares
    shares = company_data.shares if company_data.shares else 200
    par_value = company_data.par_value if company_data.par_value is not None else 0.0
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 430, "FOURTH:")
    c.setFont("Helvetica", 11)
    c.drawString(100, 430, "The corporation shall have authority to issue one class of shares consisting of")
    if par_value > 0:
        c.drawString(50, 410, f"{shares} common shares with ${par_value:.2f} par value per share.")
    else:
        c.drawString(50, 410, f"{shares} common shares without par value.")
    
    # FIFTH - Secretary of State as agent
    incorporator_address = company_data.incorporator_address if company_data.incorporator_address else "123 Main Street, Albany, NY 12207"
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 370, "FIFTH:")
    c.setFont("Helvetica", 11)
    c.drawString(100, 370, "The Secretary of State is designated as agent of the corporation upon whom process")
    c.drawString(50, 350, "against the corporation may be served.")
    c.drawString(50, 330, "The post office address to which the Secretary of State shall mail a copy of any process")
    c.drawString(50, 310, "against the corporation served upon the Secretary of State by personal delivery is:")
    c.drawString(70, 290, incorporator_address)
    
    # Incorporator
    c.drawString(50, 180, "Incorporator:")
    c.drawString(70, 160, f"/s/ {company_data.incorporator_name}")
    c.drawString(70, 140, incorporator_address)
    
    c.drawString(50, 100, "Filer's Name and Address:")
    c.drawString(70, 80, f"/s/ {company_data.incorporator_name}")
    c.drawString(70, 60, incorporator_address)
    
    c.save()
    buffer.seek(0)
    return buffer

def generate_new_york_llc_certificate(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(300, 750, "ARTICLES OF ORGANIZATION")
    c.drawCentredString(300, 730, "OF")
    c.drawCentredString(300, 710, company_data.company_name)
    c.setFont("Helvetica", 11)
    c.drawCentredString(300, 690, "Under Section 203 of the Limited Liability Company Law")
    
    # FIRST - Company Name
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 650, "FIRST:")
    c.setFont("Helvetica", 11)
    c.drawString(100, 650, "The name of the limited liability company is:")
    c.drawString(70, 630, company_data.company_name)
    
    # SECOND - Purpose
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 590, "SECOND:")
    c.setFont("Helvetica", 11)
    c.drawString(100, 590, "The purpose of the limited liability company is to engage in any lawful act or activity")
    c.drawString(50, 570, "for which limited liability companies may be organized under the Limited Liability Company Law.")
    
    # THIRD - County
    county = company_data.county if company_data.county else "NEW YORK COUNTY"
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 530, "THIRD:")
    c.setFont("Helvetica", 11)
    c.drawString(100, 530, "The county, within this state, in which the office of the limited liability company is")
    c.drawString(50, 510, f"to be located is: {county.upper()}.")
    
    # FOURTH - Secretary of State as agent
    incorporator_address = company_data.incorporator_address if company_data.incorporator_address else "123 Main Street, Albany, NY 12207"
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 470, "FOURTH:")
    c.setFont("Helvetica", 11)
    c.drawString(100, 470, "The Secretary of State is designated as agent of the limited liability company upon")
    c.drawString(50, 450, "whom process against it may be served.")
    c.drawString(50, 430, "The post office address to which the Secretary of State shall mail a copy of any process")
    c.drawString(50, 410, "against the limited liability company served upon the Secretary of State is:")
    c.drawString(70, 390, incorporator_address)
    
    # Organizer
    c.drawString(50, 180, "Organizer:")
    c.drawString(70, 160, f"/s/ {company_data.incorporator_name}")
    c.drawString(70, 140, incorporator_address)
    
    c.drawString(50, 100, "Filer's Name and Address:")
    c.drawString(70, 80, f"/s/ {company_data.incorporator_name}")
    c.drawString(70, 60, incorporator_address)
    
    c.save()
    buffer.seek(0)
    return buffer

@app.route('/form-company', methods=['POST'])
def form_company():
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                "company_name": request.form.get("company_name"),
                "state_of_formation": request.form.get("state_of_formation"),
                "company_type": request.form.get("company_type"),
                "incorporator_name": request.form.get("incorporator_name")
            }
        
        company_data = CompanyFormation(**data)
        
        if company_data.state_of_formation == 'DE':
            if company_data.company_type == 'corporation':
                pdf_buffer = generate_delaware_articles(company_data)
            elif company_data.company_type == 'LLC':
                pdf_buffer = generate_delaware_llc_certificate(company_data)
            else:
                return jsonify({"error": "Unsupported company type"}), 400
        elif company_data.state_of_formation == 'CA':
            if company_data.company_type == 'corporation':
                pdf_buffer = generate_california_articles(company_data)
            elif company_data.company_type == 'LLC':
                pdf_buffer = generate_california_llc_certificate(company_data)
            else:
                return jsonify({"error": "Unsupported company type"}), 400
        elif company_data.state_of_formation == 'NY':
            if company_data.company_type == 'corporation':
                pdf_buffer = generate_new_york_articles(company_data)
            elif company_data.company_type == 'LLC':
                pdf_buffer = generate_new_york_llc_certificate(company_data)
            else:
                return jsonify({"error": "Unsupported company type"}), 400
        else:
            return jsonify({
                "error": "Only Delaware, California, and New York entities are supported at this time"
            }), 400
    
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{company_data.company_name}_certificate.pdf"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/form-company-schema', methods=['GET'])
def form_company_schema():
    examples = [
        {
            "company_name": "Acme Corp, Inc.",
            "state_of_formation": "DE",
            "company_type": "corporation",
            "incorporator_name": "John Smith"
        },
        {
            "company_name": "Smith & Sons, LLC",
            "state_of_formation": "DE",
            "company_type": "LLC",
            "incorporator_name": "Jane Doe"
        },
        {
            "company_name": "Tech Innovators Co.",
            "state_of_formation": "CA",
            "company_type": "corporation",
            "incorporator_name": "Michael Johnson"
        },
        {
            "company_name": "California Dreaming, LLC",
            "state_of_formation": "CA",
            "company_type": "LLC",
            "incorporator_name": "Emily Chen"
        },
        {
            "company_name": "Empire State Corp.",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Sarah Williams",
            "incorporator_address": "418 Broadway Ste Y, Albany, Albany County, NY 12207",
            "county": "Albany County",
            "shares": 1000,
            "par_value": 0.01
        },
        {
            "company_name": "Big Apple Ventures, LLC",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "David Chen",
            "incorporator_address": "123 Main Street, New York, NY 10001",
            "county": "New York County"
        }
    ]
    return jsonify(examples)

@app.route('/', methods=['GET'])
def company_form():
    states = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
        'DC', 'PR', 'GU', 'VI', 'AS', 'MP'
    ]
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Company Formation</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }}
            form {{ display: grid; gap: 15px; }}
            label {{ font-weight: bold; }}
            input, select {{ padding: 8px; font-size: 16px; }}
            button {{ background: #007bff; color: white; border: none; padding: 10px 20px; cursor: pointer; }}
            button:hover {{ background: #0056b3; }}
        </style>
    </head>
    <body>
        <h1>Company Formation</h1>
        <form action="/form-company" method="POST">
            <label for="company_name">Company Name:</label>
            <input type="text" id="company_name" name="company_name" required>
            
            <label for="state_of_formation">State of Formation:</label>
            <select id="state_of_formation" name="state_of_formation" required>
                <option value="">Select a state</option>
                {"".join(f'<option value="{state}">{state}</option>' for state in states)}
            </select>
            
            <label for="company_type">Company Type:</label>
            <select id="company_type" name="company_type" required>
                <option value="">Select a type</option>
                <option value="corporation">Corporation</option>
                <option value="LLC">LLC</option>
            </select>
            
            <label for="incorporator_name">Incorporator Name:</label>
            <input type="text" id="incorporator_name" name="incorporator_name" required>
            
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, port=port)
