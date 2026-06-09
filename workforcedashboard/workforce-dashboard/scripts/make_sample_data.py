"""Generate realistic sample job postings for the Southwest Valley so the
dashboard has something to show before an Adzuna API key is configured.

Writes workforce-dashboard/data/sample_jobs.json. Re-run any time:
    python workforce-dashboard/scripts/make_sample_data.py
"""

import json
import random
from datetime import date, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# (title, company, city, category, salary range, description with embedded skills)
TEMPLATES = [
    ("Warehouse Associate", "Amazon Fulfillment", "Goodyear", "Logistics & Warehouse Jobs", (34000, 41000),
     "Picking and packing customer orders in a fast-paced fulfillment center. Must be able to lift up to 50 lbs and stand for long periods. Teamwork and attention to detail required. Forklift experience a plus."),
    ("Warehouse Associate", "REI Distribution Center", "Goodyear", "Logistics & Warehouse Jobs", (35000, 42000),
     "Shipping and receiving, cycle counting, and order fulfillment using a WMS. Dependable team player with strong work ethic. Pallet jack experience preferred."),
    ("Forklift Operator", "Macy's Logistics", "Goodyear", "Logistics & Warehouse Jobs", (37000, 45000),
     "Operate forklift and reach truck to move inventory. OSHA safety standards, loading and unloading trailers, inventory control. Attention to detail and reliability a must."),
    ("Forklift Operator", "Ferrero USA", "Tolleson", "Logistics & Warehouse Jobs", (38000, 46000),
     "Certified forklift operator for food distribution warehouse. Shipping and receiving, cycle counts, food safety standards. Must pass background check."),
    ("CDL-A Truck Driver", "Knight-Swift Transportation", "Tolleson", "Logistics & Warehouse Jobs", (62000, 85000),
     "Local routes, home daily. Valid CDL-A commercial driver's license required with clean MVR. Delivery driving experience, customer service mindset, dependable."),
    ("Delivery Driver", "UPS", "Avondale", "Logistics & Warehouse Jobs", (45000, 60000),
     "Route delivery driver. Lifting up to 70 lbs, customer service, time management. CDL not required but a plus."),
    ("Supply Chain Analyst", "Ball Corporation", "Goodyear", "Logistics & Warehouse Jobs", (60000, 78000),
     "Analyze supply chain data using Excel and SQL. Inventory management, problem-solving, communication skills, project management exposure."),
    ("Registered Nurse - Med Surg", "Abrazo West Campus", "Goodyear", "Healthcare & Nursing Jobs", (72000, 95000),
     "RN with current Arizona license. Patient care, medication administration, EHR documentation in Cerner. BLS and ACLS required. Strong communication and critical thinking."),
    ("Registered Nurse - ER", "Banner Health", "Buckeye", "Healthcare & Nursing Jobs", (75000, 98000),
     "Emergency department RN. Registered nurse license, BLS, ACLS, patient care in fast-paced environment. Epic EHR experience preferred. Teamwork essential."),
    ("Certified Nursing Assistant", "Avondale Care Center", "Avondale", "Healthcare & Nursing Jobs", (33000, 39000),
     "CNA certification required. Direct patient care, vital signs, assisting with daily living. CPR certified, dependable, compassionate. Bilingual Spanish a plus."),
    ("Medical Assistant", "Adelante Healthcare", "Goodyear", "Healthcare & Nursing Jobs", (36000, 43000),
     "Front and back office. Vital signs, phlebotomy, scheduling appointments, EHR data entry, medical terminology, HIPAA compliance. Bilingual English and Spanish preferred."),
    ("Phlebotomist", "Sonora Quest Laboratories", "Avondale", "Healthcare & Nursing Jobs", (35000, 42000),
     "Blood draws and specimen processing. Phlebotomy certification, venipuncture skill, attention to detail, customer service, HIPAA."),
    ("Pharmacy Technician", "Walgreens", "Litchfield Park", "Healthcare & Nursing Jobs", (35000, 42000),
     "Licensed pharmacy technician. Data entry, inventory management, customer service, attention to detail. Medical terminology helpful."),
    ("Dental Assistant", "West Valley Dental", "Litchfield Park", "Healthcare & Nursing Jobs", (38000, 48000),
     "Chairside assisting, sterilization, scheduling, record keeping. X-ray certification, attention to detail, communication skills."),
    ("HVAC Technician", "Parker & Sons", "Avondale", "Trade & Construction Jobs", (52000, 78000),
     "Residential HVAC service and repair. EPA 608 certification, refrigeration, electrical troubleshooting, customer service. Company truck provided. Problem-solving and reliability."),
    ("Electrician - Journeyman", "Rosendin Electric", "Buckeye", "Trade & Construction Jobs", (58000, 82000),
     "Journeyman electrician for commercial and data center projects. Read blueprints and schematics, electrical systems installation, OSHA 30, hand and power tools."),
    ("Maintenance Technician", "Andersen Windows", "Goodyear", "Trade & Construction Jobs", (48000, 62000),
     "Preventive maintenance on production equipment. Electrical troubleshooting, welding, hydraulics, blueprints, lockout/tagout. Problem-solving and teamwork."),
    ("Solar Installer", "SunPower by PGT", "Buckeye", "Trade & Construction Jobs", (42000, 56000),
     "Install residential solar panel systems. Photovoltaic experience a plus, comfortable on roofs, hand and power tools, OSHA safety, physically demanding work."),
    ("Construction Laborer", "DR Horton", "Buckeye", "Trade & Construction Jobs", (36000, 45000),
     "New home construction. Hand and power tools, lifting up to 80 lbs, safety protocols, reliability, teamwork. Bilingual crews welcome."),
    ("Production Operator", "Ball Corporation", "Goodyear", "Manufacturing Jobs", (40000, 50000),
     "Operate high-speed can manufacturing equipment. Quality control checks, preventive maintenance support, OSHA safety, attention to detail, 12-hour shifts."),
    ("Machine Operator", "Daybreak Foods", "Tolleson", "Manufacturing Jobs", (38000, 46000),
     "Food production machine operation. Quality assurance, food safety, ServSafe a plus, standing for long periods, teamwork and dependability."),
    ("CNC Machinist", "Precision Aerospace", "Goodyear", "Manufacturing Jobs", (50000, 68000),
     "CNC machining of aerospace parts. Read blueprints, quality control with micrometers, attention to detail, problem-solving. 2+ years machining experience."),
    ("Diesel Mechanic", "Penske Truck Leasing", "Tolleson", "Manufacturing Jobs", (52000, 70000),
     "Diesel engine repair and preventive maintenance. ASE certification preferred, electrical troubleshooting, hand and power tools, dependable."),
    ("Data Center Technician", "Microsoft", "Goodyear", "IT Jobs", (55000, 75000),
     "Maintain server racks and data center infrastructure. Networking fundamentals, TCP/IP, hardware troubleshooting, CompTIA A+ or Server+ preferred. Teamwork and communication."),
    ("IT Support Specialist", "Agua Fria Union High School District", "Avondale", "IT Jobs", (45000, 58000),
     "Help desk and desktop support for staff and students. Troubleshoot hardware and software, Microsoft Office, networking basics, customer service, problem-solving."),
    ("Network Technician", "Cox Communications", "Avondale", "IT Jobs", (48000, 64000),
     "Install and troubleshoot residential networking. TCP/IP, LAN/WAN, customer service, time management, valid driver's license."),
    ("Junior Software Developer", "Isagenix", "Goodyear", "IT Jobs", (62000, 80000),
     "Develop internal tools in Java and SQL. Python scripting a plus, AWS cloud services, problem-solving, collaboration, attention to detail."),
    ("Cybersecurity Analyst", "Luke AFB Contractor", "Litchfield Park", "IT Jobs", (70000, 95000),
     "Information security monitoring. Security+ certification required, networking, SQL, problem-solving, communication skills. Clearance eligible."),
    ("Customer Service Representative", "Chewy", "Goodyear", "Customer Services Jobs", (33000, 38000),
     "Inbound customer support. Customer service skills, data entry, communication, problem-solving, dependable attendance. Bilingual Spanish a plus."),
    ("Customer Service Representative", "Desert Financial Credit Union", "Avondale", "Customer Services Jobs", (34000, 40000),
     "Member service. Cash handling, customer service, communication skills, attention to detail, Microsoft Office."),
    ("Retail Sales Associate", "Target", "Avondale", "Retail Jobs", (30000, 35000),
     "Sales floor and checkout. Customer service, cash handling, POS systems, merchandising, stocking shelves, teamwork, flexible schedule."),
    ("Retail Sales Associate", "Home Depot", "Goodyear", "Retail Jobs", (30000, 36000),
     "Help customers in hardware. Customer service, sales goals, merchandising, lifting up to 50 lbs, dependable."),
    ("Bank Teller", "Chase", "Litchfield Park", "Accounting & Finance Jobs", (34000, 39000),
     "Cash handling, customer service, attention to detail, communication skills, sales referrals. Bilingual preferred."),
    ("Administrative Assistant", "City of Avondale", "Avondale", "Admin Jobs", (38000, 47000),
     "Front office support. Microsoft Office including Excel and Outlook, scheduling meetings, record keeping, data entry, communication skills, bilingual Spanish a plus."),
    ("Office Manager", "Goodyear Family Medicine", "Goodyear", "Admin Jobs", (45000, 56000),
     "Manage front office staff. Scheduling, bookkeeping with QuickBooks, payroll, HIPAA compliance, leadership, time management."),
    ("Accounting Clerk", "City of Goodyear", "Goodyear", "Accounting & Finance Jobs", (40000, 50000),
     "Accounts payable and receivable, data entry, Excel, record keeping, attention to detail."),
    ("High School Math Teacher", "Agua Fria Union High School District", "Avondale", "Teaching Jobs", (48000, 62000),
     "Teach Algebra and Geometry. Arizona teaching certificate, IVP fingerprint clearance card, classroom management, lesson planning, curriculum development, communication with families."),
    ("Elementary Teacher", "Litchfield Elementary School District", "Litchfield Park", "Teaching Jobs", (46000, 58000),
     "Self-contained classroom. Arizona teaching certification, lesson plans, classroom management, collaboration with grade-level team."),
    ("Special Education Paraprofessional", "Avondale Elementary School District", "Avondale", "Teaching Jobs", (30000, 35000),
     "Support students with IEPs. Special education experience, patience, teamwork, classroom management support, fingerprint clearance card."),
    ("Preschool Teacher", "Bright Horizons", "Goodyear", "Teaching Jobs", (32000, 38000),
     "Early childhood classroom. Childcare experience, lesson planning, CPR certified, communication with parents, reliability."),
    ("Security Officer", "Allied Universal", "Tolleson", "Other/General Jobs", (33000, 38000),
     "Patrol distribution campus. Guard card, surveillance monitoring, report writing, customer service, dependable, standing for long periods."),
    ("Line Cook", "Texas Roadhouse", "Avondale", "Hospitality & Catering Jobs", (31000, 37000),
     "Food preparation on the line. Food handler card, ServSafe a plus, teamwork, time management, fast-paced cooking."),
    ("Server", "Olive Garden", "Goodyear", "Hospitality & Catering Jobs", (28000, 42000),
     "Guest service, POS systems, cash handling, teamwork, communication skills, food safety."),
    ("Landscaper", "BrightView", "Laveen", "Trade & Construction Jobs", (30000, 38000),
     "Commercial landscape maintenance. Hand and power tools, irrigation basics, physically demanding, reliability, valid driver's license."),
    ("Behavioral Health Technician", "Copa Health", "Laveen", "Healthcare & Nursing Jobs", (34000, 40000),
     "Direct care for adults with disabilities. Patient care, medication administration support, CPR, record keeping, compassion, dependability."),
    ("Warehouse Supervisor", "XPO Logistics", "Tolleson", "Logistics & Warehouse Jobs", (52000, 65000),
     "Supervise inbound team. Leadership, WMS, inventory management, OSHA safety, scheduling staff, problem-solving, communication."),
]

random.seed(20260609)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today()
    jobs = []
    job_num = 1
    for title, company, city, category, (lo, hi), desc in TEMPLATES:
        # Each template appears 1-5 times, spread over the last ~10 weeks,
        # so the dashboard shows believable counts and a trend line.
        for _ in range(random.randint(1, 5)):
            posted = today - timedelta(days=random.randint(0, 70))
            jobs.append(
                {
                    "id": f"sample-{job_num:04d}",
                    "title": title,
                    "company": company,
                    "city": city,
                    "location": f"{city}, AZ",
                    "category": category,
                    "description": desc,
                    "salary_min": lo + random.randint(-1, 1) * 1000,
                    "salary_max": hi + random.randint(-1, 1) * 1000,
                    "posted_date": posted.isoformat(),
                    "url": None,
                }
            )
            job_num += 1
    random.shuffle(jobs)
    out = DATA_DIR / "sample_jobs.json"
    out.write_text(json.dumps(jobs, indent=1))
    print(f"Wrote {len(jobs)} sample postings to {out}")


if __name__ == "__main__":
    main()
