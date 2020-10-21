// Go to https://pupdepartments.ac.in/puexam/t2/results/results.php?listrslinks=10000
// run following code in browser console

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


/* B.SC 2017-2020

SEM-1 dec 2017 
https://pupdepartments.ac.in/puexam/t2/results/results.php?rslstid=11074878

SEM-2 may 2018
https://pupdepartments.ac.in/puexam/t2/results/results.php?rslstid=11075530

SEM-3 dec 2018
https://pupdepartments.ac.in/puexam/t2/results/results.php?rslstid=11076262

SEM-4 may 2019
https://pupdepartments.ac.in/puexam/t2/results/results.php?rslstid=11076803

SEM-5 dec 2019
https://pupdepartments.ac.in/puexam/t2/results/results.php?rslstid=11077482


REAPPEARS
SEM-1 dec 2018
https://pupdepartments.ac.in/puexam/t2/results/results.php?rslstid=11076224

SEM-1 dec 2019
https://pupdepartments.ac.in/puexam/t2/results/results.php?rslstid=11077553

SEM-2 may 2019
https://pupdepartments.ac.in/puexam/t2/results/results.php?rslstid=11076857

SEM-3 dec 2019
Awaiting
*/
