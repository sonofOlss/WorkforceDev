"""Skill lexicon for the Southwest Valley workforce dashboard.

Each entry maps a display name to a category and a list of regex patterns
(matched case-insensitively, on word boundaries) that count as a mention of
that skill in a job title or description.

To track a new skill, add an entry here -- the next scheduled run will apply
it to every posting in the database, including old ones.
"""

SKILLS = {
    # --- Logistics & Warehouse ---
    "Forklift Operation": {"category": "Logistics & Warehouse", "patterns": [r"forklift", r"reach truck", r"order picker", r"pallet jack"]},
    "Inventory Management": {"category": "Logistics & Warehouse", "patterns": [r"inventory (management|control|count)", r"cycle count(s|ing)?"]},
    "Shipping & Receiving": {"category": "Logistics & Warehouse", "patterns": [r"shipping and receiving", r"shipping/receiving", r"\bload(ing)? and unload(ing)?"]},
    "Warehouse Management Systems": {"category": "Logistics & Warehouse", "patterns": [r"\bWMS\b", r"warehouse management system"]},
    "Picking & Packing": {"category": "Logistics & Warehouse", "patterns": [r"pick(ing)? and pack(ing)?", r"order fulfillment"]},
    "CDL License": {"category": "Logistics & Warehouse", "patterns": [r"\bCDL(-| )?(A|B)?\b", r"commercial driver'?s? license"]},
    "Supply Chain": {"category": "Logistics & Warehouse", "patterns": [r"supply chain"]},
    "Delivery Driving": {"category": "Logistics & Warehouse", "patterns": [r"delivery driv(er|ing)", r"route delivery", r"local routes?"]},

    # --- Healthcare ---
    "Patient Care": {"category": "Healthcare", "patterns": [r"patient care", r"direct care", r"bedside"]},
    "RN License": {"category": "Healthcare", "patterns": [r"\bRN\b", r"registered nurse"]},
    "CNA Certification": {"category": "Healthcare", "patterns": [r"\bCNA\b", r"certified nursing assistant", r"nurse aide"]},
    "BLS/CPR Certification": {"category": "Healthcare", "patterns": [r"\bBLS\b", r"\bCPR\b", r"\bACLS\b", r"basic life support"]},
    "Electronic Health Records": {"category": "Healthcare", "patterns": [r"\bEHR\b", r"\bEMR\b", r"\bEpic\b", r"\bCerner\b", r"electronic (health|medical) record"]},
    "Phlebotomy": {"category": "Healthcare", "patterns": [r"phlebotom(y|ist)", r"blood draw", r"venipuncture"]},
    "Medication Administration": {"category": "Healthcare", "patterns": [r"medication (administration|pass)", r"administer(ing)? medication"]},
    "Medical Terminology": {"category": "Healthcare", "patterns": [r"medical terminology"]},
    "Vital Signs": {"category": "Healthcare", "patterns": [r"vital signs"]},
    "HIPAA Compliance": {"category": "Healthcare", "patterns": [r"\bHIPAA\b"]},

    # --- Skilled Trades & Manufacturing ---
    "HVAC": {"category": "Skilled Trades & Manufacturing", "patterns": [r"\bHVAC\b", r"refrigeration", r"\bEPA 608\b"]},
    "Electrical Work": {"category": "Skilled Trades & Manufacturing", "patterns": [r"electrical (systems?|work|wiring|troubleshooting)", r"electrician", r"journeyman"]},
    "Plumbing": {"category": "Skilled Trades & Manufacturing", "patterns": [r"plumbing", r"plumber"]},
    "Welding": {"category": "Skilled Trades & Manufacturing", "patterns": [r"weld(ing|er)?\b", r"\bMIG\b", r"\bTIG\b"]},
    "Blueprint Reading": {"category": "Skilled Trades & Manufacturing", "patterns": [r"blueprints?", r"schematics?", r"technical drawings?"]},
    "CNC Machining": {"category": "Skilled Trades & Manufacturing", "patterns": [r"\bCNC\b", r"machinist", r"machining"]},
    "Preventive Maintenance": {"category": "Skilled Trades & Manufacturing", "patterns": [r"preventiv?e maintenance", r"\bPM\b program", r"equipment maintenance"]},
    "Hand & Power Tools": {"category": "Skilled Trades & Manufacturing", "patterns": [r"(hand|power) tools"]},
    "OSHA Safety": {"category": "Skilled Trades & Manufacturing", "patterns": [r"\bOSHA\b", r"safety (standards|protocols|procedures|regulations)", r"lockout[/ ]tagout", r"\bLOTO\b"]},
    "Quality Control": {"category": "Skilled Trades & Manufacturing", "patterns": [r"quality (control|assurance|inspection)", r"\bQC\b", r"\bQA\b"]},
    "Solar Installation": {"category": "Skilled Trades & Manufacturing", "patterns": [r"solar (panel|installation|install)", r"photovoltaic", r"\bPV\b system"]},
    "Automotive Repair": {"category": "Skilled Trades & Manufacturing", "patterns": [r"(automotive|diesel|engine) repair", r"\bASE certif", r"mechanic"]},

    # --- Information Technology ---
    "IT Support": {"category": "Information Technology", "patterns": [r"help ?desk", r"technical support", r"desktop support", r"troubleshoot(ing)? (hardware|software|computers)"]},
    "Networking": {"category": "Information Technology", "patterns": [r"network(ing)? (administration|infrastructure|troubleshooting)", r"\bTCP/IP\b", r"\bLAN\b", r"\bWAN\b", r"\bCisco\b"]},
    "Data Center Operations": {"category": "Information Technology", "patterns": [r"data cente(r|rs)", r"server (racks?|hardware|maintenance)"]},
    "Cybersecurity": {"category": "Information Technology", "patterns": [r"cyber ?security", r"information security", r"\bSecurity\+\b"]},
    "SQL & Databases": {"category": "Information Technology", "patterns": [r"\bSQL\b", r"databases?\b"]},
    "Python": {"category": "Information Technology", "patterns": [r"\bPython\b"]},
    "Java": {"category": "Information Technology", "patterns": [r"\bJava\b(?!Script)"]},
    "Cloud Computing": {"category": "Information Technology", "patterns": [r"\bAWS\b", r"\bAzure\b", r"cloud (computing|infrastructure|services)"]},
    "CompTIA Certification": {"category": "Information Technology", "patterns": [r"\bCompTIA\b", r"\bA\+ certif"]},

    # --- Business & Office ---
    "Microsoft Office": {"category": "Business & Office", "patterns": [r"microsoft office", r"\bMS Office\b", r"\bExcel\b", r"\bWord\b and \bExcel\b", r"\bPowerPoint\b", r"\bOutlook\b"]},
    "Data Entry": {"category": "Business & Office", "patterns": [r"data entry"]},
    "Scheduling": {"category": "Business & Office", "patterns": [r"schedul(e|ing) (appointments|meetings|staff|shifts)", r"calendar management"]},
    "Bookkeeping & Accounting": {"category": "Business & Office", "patterns": [r"bookkeeping", r"accounts (payable|receivable)", r"\bQuickBooks\b", r"payroll"]},
    "Record Keeping": {"category": "Business & Office", "patterns": [r"record keeping", r"recordkeeping", r"maintain(ing)? records"]},
    "Project Management": {"category": "Business & Office", "patterns": [r"project management"]},
    "Bilingual (Spanish)": {"category": "Business & Office", "patterns": [r"bilingual", r"spanish[- ]speaking", r"english and spanish"]},

    # --- Sales & Customer Service ---
    "Customer Service": {"category": "Sales & Customer Service", "patterns": [r"customer service", r"customer (support|satisfaction|experience)", r"guest service"]},
    "Cash Handling": {"category": "Sales & Customer Service", "patterns": [r"cash handling", r"\bPOS\b", r"point[- ]of[- ]sale", r"cash register"]},
    "Sales": {"category": "Sales & Customer Service", "patterns": [r"sales (goals|targets|experience|skills)", r"upsell(ing)?", r"close[sd]? sales"]},
    "Merchandising": {"category": "Sales & Customer Service", "patterns": [r"merchandis(e|ing)", r"stock(ing)? shelves", r"planograms?"]},
    "Food Safety": {"category": "Sales & Customer Service", "patterns": [r"food (safety|handler)", r"\bServSafe\b"]},
    "Food Preparation": {"category": "Sales & Customer Service", "patterns": [r"food prep(aration)?", r"line cook", r"cooking"]},

    # --- Education & Public Service ---
    "Classroom Management": {"category": "Education & Public Service", "patterns": [r"classroom management"]},
    "Lesson Planning": {"category": "Education & Public Service", "patterns": [r"lesson plan(s|ning)?", r"curriculum"]},
    "Teaching Certification": {"category": "Education & Public Service", "patterns": [r"teaching certificat(e|ion)", r"(arizona|AZ) (teacher|teaching) certif", r"fingerprint clearance card", r"\bIVP\b"]},
    "Special Education": {"category": "Education & Public Service", "patterns": [r"special education", r"\bSPED\b", r"\bIEP\b"]},
    "Childcare": {"category": "Education & Public Service", "patterns": [r"childcare", r"child care", r"early childhood"]},
    "Security & Surveillance": {"category": "Education & Public Service", "patterns": [r"security (guard|officer|patrol)", r"surveillance", r"guard card"]},

    # --- Soft Skills ---
    "Communication": {"category": "Soft Skills", "patterns": [r"communication skills", r"(verbal|written) communication", r"communicate (clearly|effectively)"]},
    "Teamwork": {"category": "Soft Skills", "patterns": [r"team ?work", r"team player", r"work(ing)? (in|as part of) a team", r"collaborat(e|ion|ive)"]},
    "Problem Solving": {"category": "Soft Skills", "patterns": [r"problem[- ]solv(ing|er)", r"critical thinking"]},
    "Time Management": {"category": "Soft Skills", "patterns": [r"time management", r"meet(ing)? deadlines", r"prioritiz(e|ing|ation)"]},
    "Attention to Detail": {"category": "Soft Skills", "patterns": [r"attention to detail", r"detail[- ]oriented"]},
    "Leadership": {"category": "Soft Skills", "patterns": [r"leadership", r"supervis(e|ing|ory)", r"mentor(ing)?"]},
    "Physical Stamina": {"category": "Soft Skills", "patterns": [r"lift(ing)? (up to )?\d+ (lbs|pounds)", r"stand(ing)? for long periods", r"physically demanding"]},
    "Reliability": {"category": "Soft Skills", "patterns": [r"depend(able|ability)", r"reliab(le|ility)", r"punctual(ity)?", r"strong work ethic"]},
}
