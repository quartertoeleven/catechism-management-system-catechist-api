from cms_api.models import GeneralSchedule, StudyYear
from cms_api.models.base import OperationResult


def get_all_general_schedules(study_year_code=None):
    study_year: StudyYear

    if study_year_code is None:
        study_year = StudyYear.get_current()
    else:
        study_year = StudyYear.get_by_code(study_year_code)
        if study_year is None:
            return OperationResult(False, "Study year not found")

    general_schedules_as_dicts = [
        schedule.to_dict() for schedule in study_year.general_schedules
    ]

    return OperationResult(True, "", general_schedules_as_dicts)
