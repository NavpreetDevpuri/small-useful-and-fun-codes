import sys
from selenium import webdriver

course = "b.sc"
year_of_exam = "2019"
sem = "iv"  # you can leave it blank like ""
helper_text = "medical"  # you can leave it blank like ""

driver = webdriver.Chrome()
driver.get("https://pupdepartments.ac.in/puexam/t2/results/results.php?listrslinks=10000")
results = driver.execute_script('''
course = "''' + course + '''";
year_of_exam = "''' + year_of_exam + '''";
sem = "''' + sem + '''"; // you can leave it blank like ""
helper_text = "''' + helper_text + '''"; // you can leave it blank like ""

sem = sem.toLowerCase();
course = course.toLowerCase();
helper_text = helper_text.toLowerCase();
var a = document.querySelectorAll(".aLst1");
r = [];
for (i = 0; i < a.length - 5; ++i) {
	subn = a[i].innerText.split("\\n")[0].toLowerCase();
	yearn = a[i].querySelector("sup").innerText.toLowerCase();
	if (sem == "") {
		is_year = yearn == ("- dec-" + year_of_exam) || yearn == ("- may-" + year_of_exam);
	} else {
		temp = ((sem == "i" || sem == "iii" || sem == "v") ? "- dec-" : "- may-") + year_of_exam;
		is_year = yearn == temp;
	}
	if (is_year) {
		if (subn.indexOf(course) != -1) {
			if (sem != "") {
				if (subn.indexOf("sem-" + sem) != -1 || 
				subn.indexOf("sem - " + sem) != -1 || 
				subn.indexOf("semester-" + sem) != -1 || 
				subn.indexOf("semester - " + sem) != -1)
					if (helper_text != "") {
						if (subn.indexOf(helper_text) != -1) 
						    r.push([i, subn, yearn, a[i].querySelector("a").href]);
					} else
						r.push([i, subn, yearn, a[i].querySelector("a").href]);
			} else {
				if (helper_text != "") {
					if (subn.indexOf(helper_text) != -1) 
					    r.push([i, subn, yearn, a[i].querySelector("a").href]);
				} else
					r.push([i, subn, yearn, a[i].querySelector("a").href]);
			}
		}
	}
}
return r;
''')

print(results)

driver.quit()

# For browser console
'''
course = "b.sc";
year_of_exam = "2019";
sem = "iv"; // you can leave it blank like ""
helper_text = "medical"; // you can leave it blank like ""

sem = sem.toLowerCase();
course = course.toLowerCase();
helper_text = helper_text.toLowerCase();
var a = document.querySelectorAll(".aLst1");
for (i = 0; i < a.length - 5; ++i) {
	subn = a[i].innerText.split("\n")[0].toLowerCase();
	yearn = a[i].querySelector("sup").innerText.toLowerCase();
	if (sem == "") {
		is_year = yearn == ("- dec-" + year_of_exam) || 
		yearn == ("- may-" + year_of_exam);
	} else {
		temp = ((sem == "i" || sem == "iii" || sem == "v") ? 
		"- dec-" : 
		"- may-") + year_of_exam;
		is_year = yearn == temp;
	}
	if (is_year) {
		if (subn.indexOf(course) != -1) {
			if (sem != "") {
				if (subn.indexOf("sem-" + sem) != -1 || 
				subn.indexOf("sem - " + sem) != -1 || 
				subn.indexOf("semester-" + sem) != -1 || 
				subn.indexOf("semester - " + sem) != -1)
					if (helper_text != "") {
						if (subn.indexOf(helper_text) != -1) 
							console.log(i, subn, yearn, "\n" + a[i].querySelector("a").href);
					} else
						console.log(i, subn, yearn, "\n" + a[i].querySelector("a").href);
			} else {
				if (helper_text != "") {
					if (subn.indexOf(helper_text) != -1) 
						console.log(i, subn, yearn, "\n" + a[i].querySelector("a").href);
				} else
					console.log(i, subn, yearn, "\n" + a[i].querySelector("a").href);
			}
		}
	}
}
'''
