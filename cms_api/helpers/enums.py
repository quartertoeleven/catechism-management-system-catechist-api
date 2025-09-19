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
