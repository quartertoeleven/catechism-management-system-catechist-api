import enum

class GenderEnum(enum.Enum):
    MALE = "male"
    FEMALE = "female"

class TitleEnum(enum.Enum):
    MALE_CATECHIST = "male_catechist"
    FEMALE_CATECHIST = "female_catechist"
    NUN = "nun"
    MONK = "monk"
    FATHER = "father"

class SemesterEnum(enum.Enum):
    FIRST = "first"
    SECOND = "second"

class AttendanceStatusEnum(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"

class AttendanceTypeEnum(enum.Enum):
    LESSON = "lesson"
    MASS = "mass"
