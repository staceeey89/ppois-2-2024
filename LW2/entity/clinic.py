
class PetRecord:
    def __init__(self, pet_name, birth_date, last_visit_date, vet_full_name, diagnosis):
        self.pet_name = pet_name
        self.birth_date = birth_date
        self.last_visit_date = last_visit_date
        self.vet_full_name = vet_full_name
        self.diagnosis = diagnosis

    def __str__(self):
        return f"Pet Name: {self.pet_name}, Birth Date: {self.birth_date}, Last Visit Date: {self.last_visit_date}, Vet Full Name: {self.vet_full_name}, Diagnosis: {self.diagnosis}"

