import xlrd
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

indices = {
    "rollno": 3,
    "regno": 2,
    "student name": 4,
    "father name": 5,
    "mother name": 6,
    "dob": 7,
    "category": 11,
    "addresses": [12, 13, 14, 15, 16],
}
data = {
    "rollno": [],
    "regno": [],
    "student name": [],
    "father name": [],
    "mother name": [],
    "dob": [],
    "category": [],
    "addresses": []
}

loc = ("sheets/bsc1.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
addressArr = []
for i in indices:
    if (i == "addresses"):
        for j in range(indices[i].__len__()):
            addressArr.append([])
            for k in range(2, sheet.nrows):
                addressArr[j].append(sheet.cell_value(k, indices[i][j]))
        addresses = []
        for j in range(sheet.nrows - 2):
            address = ""
            for k in range(addressArr.__len__()):
                if (k == addressArr.__len__() - 1):
                    address += " - " + str(int(addressArr[k][j]))
                else:
                    if (addressArr[k][j] != ''):
                        address += addressArr[k][j].upper()
                        if (k != addressArr.__len__() - 2):
                            address += ", "
            addresses.append(address.upper())
        data[i] = addresses
    else:
        if (i == "rollno"):
            for j in range(2, sheet.nrows):
                data[i].append(str(int(sheet.cell_value(j, indices[i]))))
        elif (i == "dob"):
            for j in range(2, sheet.nrows):
                data[i].append(xlrd.xldate_as_tuple(sheet.cell_value(j, indices[i]), 0)[0:3])
        else:
            for j in range(2, sheet.nrows):
                data[i].append(sheet.cell_value(j, indices[i]))

dist = ["-Select-", "Barnala", "Bathinda", "Faridkot", "Fatehgarh sahib", "Mansa", "Mohali", "Patiala", "Rupnagar", "Sangrur", "Others"]
districts = ["-SELECT-", "BARNALA", "BATHINDA", "FARIDKOT", "FATEHGARH SAHIB", "MANSA", "MOHALI", "PATIALA", "RUPNAGAR", "SANGRUR", "OTHERS"]
states = ["-SELECT-", "ANDAMAN AND NICOBAR ISLANDS", "ANDHRA PRADESH", "ARUNACHAL PRADESH", "ASSAM", "BIHAR", "CHANDIGARH", "CHHATTISGARH", "DADRA AND NAGAR HAVELI", "DAMAN AND DIU", "DELHI", "GOA", "GUJARAT", "HARYANA", "HIMACHAL PRADESH", "JAMMU AND KASHMIR", "JHARKHAND", "MEGHALAYA", "KARNATAKA", "KERALA", "LAKSHADWEEP", "MADHYA PRADESH", "MAHARASHTRA", "MANIPUR", "MEGHALAYA", "MIZORAM", "NAGALAND", "ODISHA", "PONDICHERRY", "PUNJAB", "RAJASTHAN", "SIKKIM", "TAMIL NADU", "TRIPURA", "UTTARAKHAND", "WEST BENGAL", "UTTAR PRADESH"]
categories = ["-SELECT-", "GENERAL", "SC", "ST", "BC", "OBC"]

browser = webdriver.Chrome("chromedriver")
browser.get("https://gs.pupexamination.ac.in/Default.aspx")
browser.execute_script("""
document.getElementById("ContentPlaceHolder1_txtUserName").value = "612";
document.getElementById("ContentPlaceHolder1_txtPWD").value = "*******";
document.getElementById("ContentPlaceHolder1_btnSubmit").click();
""")

WebDriverWait(browser, 21).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddCourse")))

browser.execute_script("""
document.getElementById("ContentPlaceHolder1_ddCourse").value = 3118;
document.getElementById("ContentPlaceHolder1_Submit").click();
""")

for i in range(1):  # btnlist.__len__()):
    btnlist = browser.find_elements_by_css_selector(".btn-warning ")
    btnlist[i].click()
    browser.switch_to.window(browser.window_handles[1])
    WebDriverWait(browser, 21).until(EC.presence_of_element_located((By.ID, "TxtRollNo")))
    names = browser.execute_script("""
    return [document.getElementById("TxtApp_NameEng").value,document.getElementById("TxtApp_FatherNameEng").value,document.getElementById("TxtApp_MotherNameEng").value];
    """)
    sindices = [j for j, x in enumerate(data["student name"]) if x == names[0]]
    findices = []
    mindices = []
    for j in sindices:
        if data["father name"][j] == names[1]:
            findices.append(j)
    for j in findices:
        if data["mother name"][j] == names[2]:
            mindices.append(j)

    district = districts.index(addressArr[addressArr.__len__() - 3][mindices[0]].upper()) if \
        addressArr[addressArr.__len__() - 3][mindices[0]].upper() in districts else districts.__len__() - 1
    print(district)
    category = str(categories.index(data["category"][mindices[0]].upper()))
    isScolar = "Yes" if category == "2" or category == "5" else "No"

    if mindices.__len__() == 1:
        browser.execute_script("""
        document.getElementById("TxtRollNo").value ='""" + str(data["rollno"][mindices[0]]) + """';
        document.getElementById("TxtRegistration_No").value ='""" + str(data["regno"][mindices[0]]) + """';
        document.getElementById("DDLApp_DobDay").value ='""" + str(data["dob"][mindices[0]][2]) + """';
        document.getElementById("DDLApp_DobMonth").value ='""" + str(data["dob"][mindices[0]][1]) + """';
        document.getElementById("DDLApp_DobYear").value ='""" + str(data["dob"][mindices[0]][0]) + """';
        document.getElementById("DDLCat").value ='""" + category + """';
        document.getElementById("TxtCA_House").value ='""" + data["addresses"][mindices[0]] + """';
        document.getElementById("DDLCA_State").value ='""" + str(states.index(addressArr[addressArr.__len__() - 2][mindices[0]].upper()) - 1) + """';
        document.getElementById("TxtPA_PinCode").value ='""" + str(int(addressArr[addressArr.__len__() - 1][mindices[0]])) + """';
        document.getElementById("DDLCA_District").value ='""" + dist[district] + """';
        document.getElementById("DDLAppearing_TwoExam").value = 'No';
        document.getElementById("DDLExam_Medium").value = 'English';
        document.getElementById("DDLPostmatricScholarship").value ='""" + str(isScolar) + """';
        document.getElementById("ChkBoxSamePA").click();
        document.getElementById("CBDeclaration").click();
        document.getElementById("TxtPA_District").value ='""" + dist[district] + """';
        """)
        fatherNE = browser.find_element_by_name("TxtApp_FatherNamePbi")
        motherNE = browser.find_element_by_name("TxtApp_MotherNamePbi")
        browser.execute_script("""
        document.getElementsByName("TxtApp_FatherNamePbi")[0].value = "";
        document.getElementsByName("TxtApp_MotherNamePbi")[0].value = "";
        """)

        fl = names[1].split(" ")
        for j in fl:
            fatherNE.send_keys(j)
            fatherNE.send_keys(Keys.SPACE)
        ml = names[2].split(" ")
        for j in ml:
            motherNE.send_keys(j)
            motherNE.send_keys(Keys.SPACE)

    browser.switch_to.window(browser.window_handles[0])

browser.quit()
