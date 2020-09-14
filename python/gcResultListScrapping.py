from selenium import webdriver 
import xlsxwriter
import time

rollRange = [9151, 9227]
resultId = "11077482"
fileName = "BScSem5_lp.xlsx"

workbook = xlsxwriter.Workbook(fileName)
worksheet = workbook.add_worksheet()
b = webdriver.Chrome("chromedriver")
subjets=[]
#subjets.append('Punjabi(Compulsory)')
#subjets.append('Punjabi (Mudla Gyan)')
worksheet.write(0,0,'Rollno')
worksheet.write(0,1,'Name')
worksheet.write(0,2,'Result')
worksheet.write(0,3,'persentage')
worksheet.write(0,4,'Total')
#worksheet.write(0,5,'Punjabi(Compulsory)')
#worksheet.write(0,6,'Punjabi (Mudla Gyan)')
csub=7
x=0
getResultScript='''var table = document.getElementById("resultTbl"); 
if(table==null) return 0;
var result=document.getElementsByClassName("c5")[1].children[0].firstElementChild.innerHTML.split("<br>")[0]; 
var fail=true;
var aw = true;
if(result.indexOf("FAIL")==-1) fail=false;
if(result.indexOf("AW")==-1) aw=false;
else result+="(";
var maxmarks={ "Mathematics":150, "Physics":150, "Chemistry":150, "Drug Abuse Problem, Management and Prevention":0};
var subjects=[]; 
var marks=[]; 
var rows=table.firstElementChild.children; 
var total=0; 
for(var i=1;i<rows.length-1;++i) { 
 marks.push(0); 
 var columns=rows[i].children; 
 subjects.push(columns[0].innerText); 
 var subtotal=parseInt(columns[columns.length-1].innerText); 
 if(!isNaN(subtotal)) { 
  marks[i-1]=subtotal; total+=subtotal; continue; 
 } 
 var subn=subjects[i-1].slice(0,4);
 if(subn == "Comp") if(parseInt(columns[1].innerText < 16)) result+=subn+",";
 else if(subn == "ENV") if(parseInt(columns[1].innerText < 16)) result+=subn+",";
 else if(fail || aw) result+=subn+",";
 subtotal=0; 
 for(var j=1;j<columns.length-1;++j) { 
  var no=parseInt(columns[j].innerText); 
  if(!isNaN(no)) subtotal+=no;
 }
 
 marks[i-1]=subtotal; total+=subtotal; 
} 
if(fail || aw) result+=")";
var maxtotal=0; 
for(var i=0;i<subjects.length;++i) { 
 var temp=maxmarks[subjects[i]]; 
 maxtotal+=((temp!=undefined)?temp:100); 
} 
marks.push(total);
marks.push(maxtotal); 
marks.push(parseFloat((total/maxtotal*100).toFixed(2))); 
var rtrn=[]; 
rtrn.push(document.getElementsByClassName("c3")[0].innerText); 
rtrn.push(subjects); 
rtrn.push(marks);
rtrn.push(result);
return rtrn;
'''
for i in range(rollRange[0],rollRange[1]+1):
    b.get("http://pupdepartments.ac.in/puexam/t2/results/results.php?rslstid="+resultId+"&ROLL="+str(i)+"&submit=Submit")
    r=b.execute_script(getResultScript)
    if(r==0): continue
    print(r)
    x=x+1
    print(x,i)
    worksheet.write(x, 0, i)
    worksheet.write(x, 1, r[0])
    worksheet.write(x, 2, r[3])
    worksheet.write(x, 3, r[2][r[2].__len__()-1])
    worksheet.write(x, 4, str(r[2][r[2].__len__()-3])+'/'+str(r[2][r[2].__len__()-2]))
    for j in range (r[1].__len__()):
        if(r[1][j] in subjets):
            index = subjets.index(r[1][j])
            worksheet.write(x, index+5, r[2][j])
        else:
            subjets.append(r[1][j])
            worksheet.write(0, csub , r[1][j])
            worksheet.write(x, csub, r[2][j])
            csub=csub+1
    
workbook.close()
b.quit()
