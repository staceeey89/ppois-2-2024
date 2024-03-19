from controller.search_criteria import SearchCriteria
from model.student import Student


def check_search_criteria(stud: Student, search_criteria: SearchCriteria) -> bool:
    if search_criteria.criteria is not None:
        for term in search_criteria.criteria:
            limit_min = search_criteria.criteria[term][0]
            limit_max = search_criteria.criteria[term][1]
            match term:
                case 'sick':
                    if stud.absences_sick > limit_max or stud.absences_sick < limit_min:
                        return False
                case 'other':
                    if stud.absences_other > limit_max or stud.absences_other < limit_min:
                        return False
                case 'unjust':
                    if stud.absences_unjust > limit_max or stud.absences_unjust < limit_min:
                        return False
    return True
