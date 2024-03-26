class PersonalInformation:
    def __init__(self, seria, nr, cnp, sex, last_name, first_name, nationality, place_of_birth, address, issued_by, validity, mrz, id):
        self._seria = seria
        self._nr = nr
        self._cnp = cnp
        self._sex = sex
        self._last_name = last_name
        self._first_name = first_name
        self._nationality = nationality
        self._place_of_birth = place_of_birth
        self._address = address
        self._issued_by = issued_by
        self._validity = validity
        self._mrz = mrz
        self._id = id

    def __str__(self):
        return f"Seria: {self._seria}\nNr: {self._nr}\nCNP: {self._cnp}\nSex: {self._sex}\n" \
               f"Last Name: {self._last_name}\nFirst Name: {self._first_name}\nNationality: {self._nationality}\n" \
               f"Place of birth: {self._place_of_birth}\nAddress: {self._address}\nIssued by: {self._issued_by}\n" \
               f"Validity: {self._validity}\nMRZ: {self._mrz}\nId: {self._id}"

    def get_seria(self):
        return self._seria

    def get_nr(self):
        return self._nr

    def get_cnp(self):
        return self._cnp

    def get_sex(self):
        return self._sex

    def get_last_name(self):
        return self._last_name

    def get_first_name(self):
        return self._first_name

    def get_nationality(self):
        return self._nationality

    def get_place_of_birth(self):
        return self._place_of_birth

    def get_address(self):
        return self._address

    def get_issued_by(self):
        return self._issued_by

    def get_validity(self):
        return self._validity

    def get_mrz(self):
        return self._mrz

    def get_id(self):
        return self._id

    def set_seria(self, value):
        self._seria = value

    def set_nr(self, value):
        self._nr = value

    def set_cnp(self, value):
        self._cnp = value

    def set_sex(self, value):
        self._sex = value

    def set_last_name(self, value):
        self._last_name = value

    def set_first_name(self, value):
        self._first_name = value

    def set_nationality(self, value):
        self._nationality = value

    def set_place_of_birth(self, value):
        self._place_of_birth = value

    def set_address(self, value):
        self._address = value

    def set_issued_by(self, value):
        self._issued_by = value

    def set_validity(self, value):
        self._validity = value

    def set_mrz(self, value):
        self._mrz = value


    def set_id(self, value):
        self._id = value
