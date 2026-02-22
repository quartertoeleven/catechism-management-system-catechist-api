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
    LEAVE = "leave"


class AttendanceTypeEnum(enum.Enum):
    LESSON = "lesson"
    MASS = "mass"


class ContactInfoTypeEnum(enum.Enum):
    EMAIL = "email"
    PHONE = "phone"
    ZALO = "zalo"
    FACEBOOK = "facebook"
    OTHER = "other"


class ContactRelationTypeEnum(enum.Enum):
    FATHER = "father"
    MOTHER = "mother"
    GRANDFATHER = "grandfather"
    GRANDMOTHER = "grandmother"
    BROTHER = "brother"
    SISTER = "sister"
    AUNT = "aunt"
    UNCLE = "uncle"
    OTHER = "other"
