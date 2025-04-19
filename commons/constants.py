#  permission code format

#  A|C|R|N:CODE:R:O

# A = ADMIN , C = CREATOR , R = REVIEWER , N = NORMAL USER

# code = unique number

# R = REQUIRED, O = OPTIONAL

CAN_MANAGE_ROLES = "A1R"

CAN_MANAGE_SKILLS = "A2R"

CAN_MANAGE_TOPICS = "A3R"

CAN_MANAGE_ALL_BOOTCAMPS = "A4R"

CAN_MANAGE_QUESTIONS = "A5O"

CAN_MANAGE_RUBRICS = "A4R"

CAN_MANAGE_ASSESSMENT = "A6R"

CAN_REVIEW_VIDEOS = "R7R"

CAN_MANAGE_USERS = "A8R"

CAN_REVIEW_CREATORS_ANALYTICS = "A9R"

CAN_REVIEW_REVIEWERS_ANALYTICS = "A10R"

CAN_MANAGE_ASSIGNED_SKILLS = "C11R"

CAN_MANAGE_RUBRICS_ON_ASSIGNED_SKILL = "C12R"

CAN_MANAGE_QUESTIONS_ON_ASSIGNED_SKILL = "C13R"

CAN_MANAGE_ASSESSMENT_ON_ASSIGNED_SKILL = "C14R"

CAN_MANAGE_TOPICS_ON_ASSIGNED_SKILLS = "C15R"

CAN_ASSIGN_CREATORS_TO_SKILL = "A16R"

CAN_CREATE_PROFILES_OF_ROLES = "N17R"

CAN_TAKE_ASSESSMENTS = "N18R"

CAN_TAKE_CONTENT_ASSESSMENTS = "N23R"

CAN_MANAGE_CONTENTS = "A19O"

CAN_MANAGE_CONTENTS_ON_ASSIGNED_SKILL = "C20R"

CAN_MANAGE_SUB_TOPICS = "A21R"

CAN_MANAGE_SUB_TOPICS_ON_ASSIGNED_SKILL = "C22R"

CAN_VIEW_CONTENTS_OF_ASSIGNED_ROLES = "N24R"

CAN_CREATE_CONTENT_QUESTIONS = "C25R"

CAN_RETRIEVE_CONTENT_OF_ASSIGNED_ROLES = "N26R"

CAN_RETRIEVE_PRESIGNED_URL = "N27R"

CAN_GET_CATEGORIES_CONTENTS = "N28R"

CAN_ADD_STUDENT_RELATED_PROFILE_INFO = "N29R"

ADMIN_WANTS = [
    CAN_MANAGE_ROLES,
    CAN_MANAGE_SKILLS,
    CAN_MANAGE_TOPICS,
    CAN_MANAGE_USERS,
    CAN_REVIEW_CREATORS_ANALYTICS,
    CAN_REVIEW_REVIEWERS_ANALYTICS,
    CAN_ASSIGN_CREATORS_TO_SKILL,
    CAN_MANAGE_SUB_TOPICS,
    CAN_MANAGE_CONTENTS,
    CAN_MANAGE_ALL_BOOTCAMPS,
    CAN_MANAGE_ASSESSMENT,
    CAN_MANAGE_RUBRICS,
]

CONTENT_ADMIN_WANTS = [
    CAN_MANAGE_ASSIGNED_SKILLS,
    CAN_MANAGE_RUBRICS_ON_ASSIGNED_SKILL,
    CAN_MANAGE_QUESTIONS_ON_ASSIGNED_SKILL,
    CAN_MANAGE_ASSESSMENT_ON_ASSIGNED_SKILL,
    CAN_MANAGE_TOPICS_ON_ASSIGNED_SKILLS,
    CAN_MANAGE_CONTENTS_ON_ASSIGNED_SKILL,
    CAN_MANAGE_SUB_TOPICS_ON_ASSIGNED_SKILL,
    CAN_CREATE_CONTENT_QUESTIONS,
]

REVIEWER_WANTS = [CAN_REVIEW_VIDEOS]

NORMAL_USER_WANTS = [
    CAN_CREATE_PROFILES_OF_ROLES,
    CAN_TAKE_ASSESSMENTS,
    CAN_TAKE_CONTENT_ASSESSMENTS,
    CAN_VIEW_CONTENTS_OF_ASSIGNED_ROLES,
    CAN_RETRIEVE_CONTENT_OF_ASSIGNED_ROLES,
    CAN_RETRIEVE_PRESIGNED_URL,
    CAN_GET_CATEGORIES_CONTENTS,
    CAN_ADD_STUDENT_RELATED_PROFILE_INFO,
]

PERMISSIONS = [
    {
        "name": "Can Manage Roles",
        "code": CAN_MANAGE_ROLES,
        "humanized_var": "CAN_MANAGE_ROLES",
        "description": "",
    },
    {
        "name": "Can Manage Skills",
        "code": CAN_MANAGE_SKILLS,
        "humanized_var": "CAN_MANAGE_SKILLS",
        "description": "",
    },
    {
        "name": "Can Manage Topics",
        "code": CAN_MANAGE_TOPICS,
        "humanized_var": "CAN_MANAGE_TOPICS",
        "description": "",
    },
    {
        "name": "Can Manage Rubrics",
        "code": CAN_MANAGE_RUBRICS,
        "humanized_var": "CAN_MANAGE_RUBRICS",
        "description": "",
    },
    {
        "name": "Can Manage Questions",
        "code": CAN_MANAGE_QUESTIONS,
        "humanized_var": "CAN_MANAGE_QUESTIONS",
        "description": "",
    },
    {
        "name": "Can Manage Assessment",
        "code": CAN_MANAGE_ASSESSMENT,
        "humanized_var": "CAN_MANAGE_ASSESSMENT",
        "description": "",
    },
    {
        "name": "Can Review Videos",
        "code": CAN_REVIEW_VIDEOS,
        "humanized_var": "CAN_REVIEW_VIDEOS",
        "description": "",
    },
    {
        "name": "Can Manage Users",
        "code": CAN_MANAGE_USERS,
        "humanized_var": "CAN_MANAGE_USERS",
        "description": "",
    },
    {
        "name": "Can Review Creators Analytics",
        "code": CAN_REVIEW_CREATORS_ANALYTICS,
        "humanized_var": "CAN_REVIEW_CREATORS_ANALYTICS",
        "description": "",
    },
    {
        "name": "Can Review Reviewers Analytics",
        "code": CAN_REVIEW_REVIEWERS_ANALYTICS,
        "humanized_var": "CAN_REVIEW_REVIEWERS_ANALYTICS",
        "description": "",
    },
    {
        "name": "Can Manage Assigned Skills",
        "code": CAN_MANAGE_ASSIGNED_SKILLS,
        "humanized_var": "CAN_MANAGE_ASSIGNED_SKILLS",
        "description": "",
    },
    {
        "name": "Can Manage Rubrics on Assigned Skill",
        "code": CAN_MANAGE_RUBRICS_ON_ASSIGNED_SKILL,
        "humanized_var": "CAN_MANAGE_RUBRICS_ON_ASSIGNED_SKILL",
        "description": "",
    },
    {
        "name": "Can Manage Questions on Assigned Skill",
        "code": CAN_MANAGE_QUESTIONS_ON_ASSIGNED_SKILL,
        "humanized_var": "CAN_MANAGE_QUESTIONS_ON_ASSIGNED_SKILL",
        "description": "",
    },
    {
        "name": "Can Manage Assessment on Assigned Skill",
        "code": CAN_MANAGE_ASSESSMENT_ON_ASSIGNED_SKILL,
        "humanized_var": "CAN_MANAGE_ASSESSMENT_ON_ASSIGNED_SKILL",
        "description": "",
    },
    {
        "name": "Can Manage Topics on Assigned Skills",
        "code": CAN_MANAGE_TOPICS_ON_ASSIGNED_SKILLS,
        "humanized_var": "CAN_MANAGE_TOPICS_ON_ASSIGNED_SKILLS",
        "description": "",
    },
    {
        "name": "Can Assign Creators to Skills",
        "code": CAN_ASSIGN_CREATORS_TO_SKILL,
        "humanized_var": "CAN_ASSIGN_CREATORS_TO_SKILL",
        "description": "",
    },
    {
        "name": "Can Create Profile Of Roles",
        "code": CAN_CREATE_PROFILES_OF_ROLES,
        "humanized_var": "CAN_CREATE_PROFILES_OF_ROLES",
        "description": "",
    },
    {
        "name": "Can Add Student related profile info",
        "code": CAN_ADD_STUDENT_RELATED_PROFILE_INFO,
        "humanized_var": "CAN_ADD_STUDENT_RELATED_PROFILE_INFO",
        "description": "",
    },
    {
        "name": "Can Take Assessments",
        "code": CAN_TAKE_ASSESSMENTS,
        "humanized_var": "CAN_TAKE_ASSESSMENTS",
        "description": "",
    },
    {
        "name": "Can Take Content Assessments",
        "code": CAN_TAKE_CONTENT_ASSESSMENTS,
        "humanized_var": "CAN_TAKE_CONTENT_ASSESSMENTS",
        "description": "",
    },
    {
        "name": "Can Manage Contents",
        "code": CAN_MANAGE_CONTENTS,
        "humanized_var": "CAN_MANAGE_CONTENTS",
        "description": "",
    },
    {
        "name": "Can Manage Contents on Assigned Skills",
        "code": CAN_MANAGE_CONTENTS_ON_ASSIGNED_SKILL,
        "humanized_var": "CAN_MANAGE_CONTENTS_ON_ASSIGNED_SKILL",
        "description": "",
    },
    {
        "name": "Can View Contents of Assigned Roles",
        "code": CAN_VIEW_CONTENTS_OF_ASSIGNED_ROLES,
        "humanized_var": "CAN_VIEW_CONTENTS_OF_ASSIGNED_ROLES",
        "description": "",
    },
    {
        "name": "Can Manage Sub Topics",
        "code": CAN_MANAGE_SUB_TOPICS,
        "humanized_var": "CAN_MANAGE_SUB_TOPICS",
        "description": "",
    },
    {
        "name": "Can Manage Sub Topics on Assigned Skill",
        "code": CAN_MANAGE_SUB_TOPICS_ON_ASSIGNED_SKILL,
        "humanized_var": "CAN_MANAGE_SUB_TOPICS_ON_ASSIGNED_SKILL",
        "description": "",
    },
    {
        "name": "Can Create Content Questions",
        "code": CAN_CREATE_CONTENT_QUESTIONS,
        "humanized_var": "CAN_CREATE_CONTENT_QUESTIONS",
        "description": "",
    },
    {
        "name": "Can Retrieve Content Of Assigned Roles ",
        "code": CAN_RETRIEVE_CONTENT_OF_ASSIGNED_ROLES,
        "humanized_var": "CAN_RETRIEVE_CONTENT_OF_ASSIGNED_ROLES",
        "description": "",
    },
    {
        "name": "Can Retrieve Presigned Url",
        "code": CAN_RETRIEVE_PRESIGNED_URL,
        "humanized_var": "CAN_RETRIEVE_PRESIGNED_URL",
        "description": "",
    },
    {
        "name": "Can Get Categories Contents",
        "code": CAN_GET_CATEGORIES_CONTENTS,
        "humanized_var": "CAN_GET_CATEGORIES_CONTENTS",
        "description": "",
    },
    {
        "name": "Can Manage all Bootcamps",
        "code": CAN_MANAGE_ALL_BOOTCAMPS,
        "humanized_var": "CAN_MANAGE_ALL_BOOTCAMPS",
        "description": "Permission for levelup admin to manage all bootcamps",
    },
]
