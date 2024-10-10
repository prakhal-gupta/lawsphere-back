ROLES_PERMISSIONS = []
GLOBAL_PERMISSIONS = []
CONFIG = []
START_EMPLOYEE_CODE_TITLE = 'Starting Employee Code'
NON_CORE_SERVICES = "Non Core Services"
CORE_SERVICES = "Core Services"
PROFESSION = "Profession"
SETTINGS_CONSTANT = [
    {'title': 'Gender', 'can_disabled': False, 'children': []},
    {'title': PROFESSION, 'can_disabled': False, 'children': []},
    {'title': CORE_SERVICES, 'can_disabled': True, 'children': []},
    {'title': NON_CORE_SERVICES, 'can_disabled': True, 'children': []},
    {'title': 'Policies', 'can_disabled': False, 'children': []},
    {'title': 'Employee Policies', 'can_disabled': False, 'children': []},
    {'title': 'Personal Document Category',
     'children': [{'title': 'Sub Category', 'children': []}]
     },
]

ACTION_TYPE_CREATE = "created"
ACTION_TYPE_ADDED = "added"
ACTION_TYPE_BULK_ADDED = "added (in bulk)"
ACTION_TYPE_BULK_DELETED = "deleted (in bulk)"
ACTION_TYPE_REMOVED = "removed"
ACTION_TYPE_UPDATE = "updated"
ACTION_TYPE_APPROVED = "approved"
ACTION_TYPE_DELETE = "deleted"
ACTION_TYPE_REJECTED = "rejected"
ACTION_TYPE_CANCELLED = "cancelled"
ACTION_TYPE_CREDIT = "credited"
ACTION_TYPE_DEBIT = "debited"
ACTION_TYPE_ASSIGN = "assigned"
ACTION_TYPE_RESET_PASSWORD = "reset"
ACTION_TYPE_LOCK = "locked"
ACTION_TYPE_APPLY = "applied"
ACTION_TYPE_SEPARATE = "separated"
ACTION_TYPE_RETRIEVE = "retrieved"
ACTION_TYPE_CLEARED = "cleared"

# Log Actions

ACTION_OBJECT = {
    'Location': 'location',
    'DynamicSettings': 'dynamic setting'
}

# Log Category and sub category
# Categories
SETTINGS = "Settings"
PASSWORD = "password"

# Sub categories
HR_SETTINGS = "Admin settings"
RESET_PASSWORD = "Reset Password"

LOG_STRATA = {}
CREDIT = 'CREDIT'
DEBIT = 'DEBIT'

TRANSACTION_TYPES = (
    (CREDIT, CREDIT),
    (DEBIT, DEBIT),
)

TRANSACTION_SUCCESS = "Success"
TRANSACTION_PROCESSING = "Processing"
TRANSACTION_FAILED = "Failed"

GST_LICENCE = "GST Licence"
GST_FILING = "GST Filling"
FOOD_LICENCE = "Food Licence"
LABOUR_LICENCE = "Labour Licence"
IMPORT_EXPORT_CODE = "IMPORT & EXPORT CODE – IEC"
TDS_FILLING = "TDS Filling"
SERVICE_ITR = "ITR"
BOOK_KEEPING = "Book Keeping"
AUDIT = "Audit"
ESI_PF = "ESI | PF REGISTRATION & FILLING"
INCORPORATION = "Incorporation"
TM_FORM = "TM"
ROC_MCA = "ROC/MCA"
UDYOG_AADHAAR = "Udyog Aadhaar"

CA = "CA"
ADVOCATE = "Advocate"
CS = "CS"
CMA = "CMA"
ACCOUNTANT = "Accountant"
OTHER = "Other"

PROFESSIONS = ((CA, CA), (ADVOCATE, ADVOCATE), (CS, CS), (CMA, CMA),
               (ACCOUNTANT, ACCOUNTANT), (OTHER, OTHER))

LEAD = "Lead"

ACTIVE = "Active"
DEACTIVE = "Deactive"
ABSCOND = "Abscond"
RETIRED = "Retired"
LEAVED = "Leaved"

employee_STATUS = ((ACTIVE, ACTIVE), (DEACTIVE, DEACTIVE),
                  (ABSCOND, ABSCOND), (RETIRED, RETIRED),
                  (LEAVED, ACTIVE))

BLOOD_GROUPS = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)
