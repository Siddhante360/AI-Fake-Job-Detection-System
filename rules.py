# rules.py

HIGH_RISK_KEYWORDS = [
    "bank account",
    "passport copy",
    "aadhaar",
    "aadhar",
    "pan card",
    "identity document",
    "processing fee",
    "registration fee",
    "security deposit",
    "wire transfer",
    "western union",
    "crypto payment",
    "bitcoin",
    "pay upfront",
    "advance payment"
]

SUSPICIOUS_EMAILS = [
    "@gmail.com",
    "@yahoo.com",
    "@hotmail.com",
    "@outlook.com"
]

UNREALISTIC_SALARY_TERMS = [
    "$5000/week",
    "$10000/week",
    "$12000/week",
    "earn huge money",
    "earn instantly",
    "quick money",
    "guaranteed income"
]

SUSPICIOUS_PATTERNS = [
    "immediate hiring",
    "urgent hiring",
    "work from anywhere",
    "work from home",
    "limited vacancies",
    "no experience needed",
    "no experience required",
    "instant approval",
    "instant joining",
    "easy money",
    "guaranteed selection",
    "hiring immediately"
]


def calculate_risk(text):

    text = text.lower()

    risk_score = 0
    reasons = []
    breakdown = {}

    # ============================
    # HIGH RISK KEYWORDS
    # ============================

    for keyword in HIGH_RISK_KEYWORDS:

        if keyword in text:

            risk_score += 25

            reasons.append(
                f"High Risk Keyword: {keyword}"
            )

            breakdown[keyword] = 25

    # ============================
    # SUSPICIOUS EMAILS
    # ============================

    for email in SUSPICIOUS_EMAILS:

        if email in text:

            risk_score += 15

            reasons.append(
                f"Suspicious Email: {email}"
            )

            breakdown[email] = 15

    # ============================
    # UNREALISTIC SALARY
    # ============================

    for salary in UNREALISTIC_SALARY_TERMS:

        if salary in text:

            risk_score += 20

            reasons.append(
                f"Unrealistic Salary Claim: {salary}"
            )

            breakdown[salary] = 20

    # ============================
    # SUSPICIOUS PATTERNS
    # ============================

    for pattern in SUSPICIOUS_PATTERNS:

        if pattern in text:

            risk_score += 8

            reasons.append(
                f"Suspicious Pattern: {pattern}"
            )

            breakdown[pattern] = 8

    # ============================
    # RISK SCORE LIMIT
    # ============================

    risk_score = min(risk_score, 100)

    # ============================
    # CATEGORY
    # ============================

    if risk_score <= 25:

        category = "SAFE"

    elif risk_score <= 50:

        category = "LOW SUSPICION"

    elif risk_score <= 75:

        category = "SUSPICIOUS"

    else:

        category = "HIGH RISK FRAUD"

    return risk_score, reasons, category, breakdown