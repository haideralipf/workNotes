import re
import datetime

def num_to_word(self, number):
	try:
		di = {'4': 'A', '8': 'B', '6': 'b', '9': 'g', '1': 'I', '0': 'O', '5': 'S', '7': 'T', '2': 'Z'}
		return "".join([di[str(i)] if i in di else i for i in number])
	except:
		return ""


def word_to_num(self, letters):
	try:
		letters = letters.upper()
		di = {'A':'4', 'B':'8', 'b':'6', 'G':'9', 'I':'1', 'O':'0', 'Q':'0', 'D': '0', 'S':'5', 'T':'7', 'Z':'2'}
		return "".join([di[str(i)] if i in di else i for i in letters])
	except:
		return ""


def fetch_capital_name(self, string):
	try:
		return " ".join([word for word in string.split() if word.isalpha() and word.isupper()])
	except:
		return ""


def fetch_capital_name_regex(self, string):
    try:
        string = string.replace('/', '')
        string = string.replace(".", ",")
        match = re.search("[A-Z][A-Z ,\-]+(?= |$|[^A-Z])", string)
        if match:
            final_str = match.group(0).strip("-,.")
            return final_str
        else:
            return ""
    except:
        return ""


def parse_full_name(self, full_name):
	try:
		temp_name = full_name.replace("\n", " ")
		temp_name = temp_name.replace('.', ',')
		match = re.search("[A-Z][A-Z ,\-]+(?= |$)", temp_name)
		if match:
			return match.group(0)
		else:
			return ""
	except:
		return ""

def fetch_last_name_from_two_lines_name(self, name):
	try:
		name = name.split('\n')[0]
		name = name.replace(".", ",")
		match = re.search("[A-Z][A-Z ,\-]+(?= |$)", name)
		if match:
			return match.group(0)
		else:
			return ""
	except:
		return ""

def fetch_first_name_from_two_lines_name(self, name):
	try:
		name = name.split('\n')[-1]
		name = name.replace(".", ",")
		match = re.search("[A-Z][A-Z ,\-]+(?= |$)", name)
		if match:
			return match.group(0)
		else:
			return ""
	except:
		return ""

def fetch_date_from_garbage(self, string_date):
	string_date = string_date.replace(" ", "")
	match = re.search("\w{2}[.\\- ]\w{2}[.\\- ]\w{4}", string_date)
	if match:
		parsed_date = self.word_to_num(match.group(0))
		return parsed_date
	else:
		return ""



def fetch_capital_pob_regex(string):
	try:
		match = re.findall("[A-Z][A-Z ,.\-()]+", string)
		if match:
			match = sorted(match, key=lambda k: len(k), reverse=True)
			return match[0]
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

# "mmddYYYY" --> "YYYY-mm-dd"
def validate_date(self, date_text):
    try:
    	date_text = date_text.replace("/", " ").replace("-", " ").replace(".", " ").replace(" ", "")
    	date_text = self.word_to_num(date_text)
        if len(date_text) != 8:
            return ""
        return datetime.strptime(date_text, "%m%d%Y").strftime("%Y-%m-%d")
    except Exception as e:
        return ""


# "ddmmYYYY" --> "YYYY-mm-dd"
def validate_date(self, date_text):
    try:
    	date_text = date_text.replace("/", " ").replace("-", " ").replace(".", " ").replace(" ", "")
    	date_text = self.word_to_num(date_text)
        if len(date_text) != 8:
            return ""
        return datetime.strptime(date_text, "%d%m%Y").strftime("%Y-%m-%d")
    except Exception as e:
        return ""

def parse_date(self,date):
    try:
        match = re.search("\w{2}[./\- ]\w{2}[./\- ]\w{4}", date)
        if match:
            date = self.word_to_num(match.group(0))

        ls = re.split('[ /\-.]', date)
        comp_list = []
        for i in ls:
            if i[0] == '4':
                comp_list.append('1' + i[1:])
            elif i[0] == '6' or i[0] == '9':
                comp_list.append('0' + i[1:]) 
            elif i[0] == '8':
                comp_list.append('3' + i[1:]) 
            else:
                comp_list.append(i)

        date = "-".join(comp_list)

        ans = ''.join(i for i in date if i.isnumeric())
        if len(ans) == 8:
            date = datetime.datetime.strptime(ans, "%m%d%Y").strftime("%Y-%m-%d")
        else:
            date = ""
        return date
    except Exception as ex:
        return ""

def parse_document_type(self, doc_type):
    try:
        ls_of_chars = ["DRIVER", "LICENSE", "IDENTIFICATION", "CARD"]
        fuzzed_type = []
        for item in doc_type.split():
            highest = process.extractOne(item,ls_of_chars)
            if highest[1] > 70:
                 fuzzed_type.append(highest[0])
            else:
                fuzzed_type.append(item)
        return " ".join(fuzzed_type)
    except:
        return ""

#parse address
def parse_address(self, address, upper_field = ''):
    try:
        index = 0
        for i in range(len(address)):
            if address[i].isdigit():
                index = i
                break
        address = address[index:].strip()
        address = address.replace('\n', ' ').replace(".",",")

        if upper_field:
            try:
                temp = " "+upper_field.split()[-1]+" "
                raw_field = r"{}".format(temp)
                match = re.search(temp, address)
                if match:
                    address = address[match.end():].strip()
            except:
                pass

        str1 = re.sub('[^A-Z0-9 ,-]', '', address)
        str1 = re.sub('(?<= )-(?= )', '', str1).strip()
        str1 = " ".join(str1.split())
        str1 = str1.lstrip('8')

        match = re.search('\d+[A-Z0-9 ,-]+[A-Z]{2} ?\d+([ -]+\d+)?', str1)

        if match:
            address = match.group(0)
            temp_add = address.split()
            if len(temp_add) > 2:
                if len(temp_add[0]) == 1 and temp_add[0].isnumeric() and temp_add[1].isnumeric():
                    temp_add = temp_add[1:]

            if len(temp_add[-1]) == 1:
                return " ".join(temp_add[:-1])
            else:
                return " ".join(temp_add)
        else:
            return ""
    except Exception as ex:
        return ""
        

#parse document_number
def parse_document_number(self, number):
	try:
		number = number.replace(' ', '')
		number = number.split(":")[-1]
		number = self.word_to_num(number)
	except:
		return ""

#document number with dd
def parse_document_number(self,doc_number):
    try:
        doc_number = doc_number.upper()
        doc_number = re.sub('^\d{2} ', '', doc_number)
        doc_number = re.split('^\d?[., \-]*\w*[DOP] ', doc_number)[-1]
        new_personal_number=''.join([i for i in doc_number if i.isalnum()])
        return new_personal_number
    except:
        return ""

#parse_gender
def parse_gender(self, text):
    try:
        text = text.upper()
        if 'F' in text or 'T' in text or '7' in text: 
            return 'F'
        elif 'M' in text or 'N' in text or 'A' in text or 'W' in text or 'w' in text:
            return 'M'
        else:
            return ""
    except:
        return ""

def parse_personal_number(self,doc_number):
    try:
        if not "/" in doc_number:
            new_personal_number=''.join([i for i in doc_number if i.isdigit()])
            if len(new_personal_number) == 10:
                new_personal_number = new_personal_number[1:]
            return new_personal_number
        return ""
    except:
        return ""


#gender roi
diff1 = int(abs(roi[1] - roi[3]))
diff = int(abs(roi[0] - roi[2]))

label == "eng-gender":
roi[0] -= diff * 0.20
roi[2] += diff * 0.10
roi[1] -= diff1 * 0.10
roi[3] += diff1 * 0.05


#get passport data using mrz
def get_passport_mrz_data(selfmrz):
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


