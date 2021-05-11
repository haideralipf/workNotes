import re
import datetime


def fetch_capital_name(string):
	try:
		return " ".join([word for word in string.split() if word.isalpha() and word.isupper()])
	except:
		return ""

def fetch_capital_name_regex(string):
	try:
		match = re.match("[A-Z][A-Z ,.-/]+", string)
		if match:
			return match.group(0)
		else:
			return ""
	except:
		return ""

def change_six_digit_to_date(self, dob):
    try:
        dob = str(dob)[0:6]
        changed_date = datetime.datetime.strptime(dob, "%y%m%d").strftime("%Y-%m-%d")
        current_date = datetime.datetime.now()
        changed_date_year = changed_date[0:4]
        if current_date.year < int(changed_date_year):
            changed_date = changed_date.replace(changed_date_year, str(int(changed_date_year) - 100))

        return changed_date
    except:
        return ""

def get_passport_mrz_data(mrz):
	try:

		document_number = ""
        gender = ""
        dob = ""
        expiry_date = ""

		document_match = re.search("([0-9]{10})[A-Z]{3}", mrz)
		if document_match:
			document_number = document_match.group(1)
            document_number = document_number[:-1]

		gender_match = re.search("[0-9]+ *([FM]) *[0-9]+", mrz)
		if gender_match:
			gender = gender_match.group(1)

		dob_match = re.search("[A-Z]{3}([0-9]{7}) *[FM]", mrz)
		if dob_match:
			dob = dob_match.group(1)
            dob = dob[:-1]

		expiry_match = re.search("[0-9] *[FM] *([0-9]{7})", mrz)
		if expiry_match:
            expiry_date = expiry_match.group(1)
            expiry_date = expiry_date[:-1]

        return {'document_number': document_number,
            'gender': gender,
            'dob': dob,
            'expiry_date': expiry_date} 
	except:
		return {'document_number': document_number,
            'gender': gender,
            'dob': dob,
            'expiry_date': expiry_date} 
