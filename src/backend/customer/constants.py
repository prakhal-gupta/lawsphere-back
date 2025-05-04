STATUS_CHOICES = [
        ("filed", "Case Filed"),
        ("under_investigation", "Under Investigation"),
        ("charges_framed", "Charges Framed"),
        ("trial", "Trial in Progress"),
        ("awaiting_verdict", "Awaiting Verdict"),
        ("judgment_pronounced", "Judgment Pronounced"),
        ("convicted", "Convicted"),
        ("acquitted", "Acquitted"),
        ("closed", "Case Closed"),
        ("appealed", "Appealed to Higher Court"),
        ("withdrawn", "Withdrawn"),
        ("settled", "Settled Out of Court"),
        ("reopened", "Reopened"),
    ]

PRIORITY_CHOICES = [
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
    ("urgent", "Urgent"),
]

CASE_TYPE_CHOICES = [
    ("criminal", "Criminal"),
    ("civil", "Civil"),
    ("family", "Family"),
    ("labour", "Labour"),
    ("consumer", "Consumer"),
    ("land_dispute", "Land Dispute"),
    ("corporate", "Corporate"),
    ("tax", "Tax"),
    ("environment", "Environment"),
    ("constitutional", "Constitutional"),
    ("cyber", "Cyber Crime"),
    ("intellectual_property", "Intellectual Property"),
]
