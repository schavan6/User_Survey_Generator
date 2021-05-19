import sys
import json

primary_key_column = ""

def generateDisplayHTML(db):
  fileName = db["name"]+"_display.html"
  f = open(fileName, "w")
  html='<html>\n<head>\n<title>Data Display</title>\n<script src="'+db["name"]+'.js"></script>\n'
  html = html+'<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>\n'
  html = html+'<link rel="stylesheet" href="'+db["name"]+'.css">\n</head>\n<body>\n<button id="display-data" type="button" onClick="displayData(this)">Display All Data</button>\n<br>\n<br>\n'
  html = html+'<div id="results"></div>\n</body>\n</html>\n'
  f.write(html)
def generateFormHTML(db):
  elements= db["elements"]
  fileName = db["name"]+".html"
  f = open(fileName, "w")
  html = '<html>\n<head>\n'+'<title>'+db["caption"]+'</title>\n<link rel="stylesheet" href="'+db["name"]+'.css">\n\n<script src="'+db["name"]+'.js"></script>\n<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>\n</head>\n';
  html = html+'<body>\n<form  action="javascript:;" onsubmit="submitData(this)">\n'

  for element in elements:
    inputType = element['etype']
    
    if inputType == 'textbox':
      html = html+"<label for ='"+element['ename']+"'>"+ element['caption'] + '</label>\n<br>\n'
      if element['datatype'] == 'integer':
        html = html+ "<input type='number' name='"+element['ename']+"' id='"+element['ename']+"' size='"+element['size']+"' maxlength='"+element['maxlength']

      else:
        html = html+ "<input type='text' name='"+element['ename']+"' id='"+element['ename']+"' size='"+element['size']+"' maxlength='"+element['maxlength']
      if 'key' in element:	
        html = html+"' required/>\n<br>\n"
      else:
        if element['required'] == 'true':
          html = html+"' required/>\n<br>\n"
        else:
          html = html+"' />\n<br>\n"
      html = html+"<br>"

    if inputType == 'checkbox':
      html = html+"<label>"+ element['caption'] + '</label>\n<br>\n'
      for check in element['group']:
        html = html + "<input type='checkbox' name='"+element['ename']+ "' value='"+check['caption']+"'"
        if "checked" in check:
          html = html +" checked='checked'/>"
        else:
          html = html + "/>"
        html = html + "<label>"+check['caption']+"</label>\n<br>\n"
      html = html+"<br>"
    if inputType == 'selectlist':
      html = html+"<label>"+ element['caption'] + '</label>\n<br>\n'
      html = html+"<select name='"+element['ename']+"' id='"+element['ename']+"'>\n<br>\n"
      for option in element['group']:
        html = html+"<option value='"+option['caption']+"'>"+option['caption']+"</option>\n<br>\n"
      html = html+"</select>\n<br>\n"	
      html = html+"<br>"
    if inputType == 'radiobutton':	
      name = 	element['ename']
      html = html + "<label>"+element['caption']+"</label>\n<br>\n"
      for option in element['group']:
        html = html + "<input type='radio' name='"+name +"' value='"+option['caption']+"' id='"+option['value']+"'/>"
        html = html + "<label for='"+option['value']+"'>"+option['caption']+"</label>\n<br>\n"
      html = html+"<br>"
    if inputType == 'submit':
      html = html+"<button type='submit'>"+element['caption']+"</button>"
    if inputType == 'reset':
      html = html+"<button type='reset'>"+element['caption']+"</button>"
    if inputType == 'multiselectlist':
      html = html+"<label>"+ element['caption'] + '</label>\n<br>\n'
      html = html+"<select name='"+element['ename']+"' id='"+element['ename']+"' multiple>\n<br>\n"
      for option in element['group']:
        html = html+"<option value='"+option['caption']+"'>"+option['caption']+"</option>\n<br>\n"
      html = html+"</select>\n<br>\n"	
      html = html+"<br>"

  html = html + '\n</form>\n'
  html = html + '<div id="success" hidden>\n<h1>Your data has been successfully submitted.</h1>\n<a href="'+db["name"]+'.html">Make Another Enrty</a>\n</div>'
  html = html + '</body>\n</html>'
  f.write(html)
def generateJavaScript(db):
  elements= db["elements"]
  fileName = db["name"]+".js"
  f = open(fileName, "w")
  js = "function submitData(data){\n"
  js = js+ "var formData = _getFormData();\n"
  js = js+ "var url = 'http://localhost:5000/webforms/insert/';\n"
  js = js+ "$.ajax({\nurl: url,\ntype: 'POST',\ndata: JSON.stringify(formData),\ncontentType: 'application/json; charset=utf-8',\ndataType: 'json',\n"
  js = js+ "success: function(response) {\n$('form').hide();\n$('#success').show();\n},\n"
  js = js+ "error: function(error) {\nalert('ERROR');\nconsole.log(error);\n}\n});\n"
  js=js + "}\n"

  js=js + "function _getFormData(){\n"
  js=js + "var formData = {};\n"
  js=js + "$('input').each(function(){\nif(this.type === 'checkbox'){\n"
  js=js + "if(this.checked){\n"
  js=js + "if(!(this.name in formData)){\nformData[this.name] = [];\n}\n"
  js=js + "formData[this.name].push(this.value);\n}\n}\n"
  js=js + "else if(this.type === 'radio'){\nif(this.checked){\nformData[this.name] = this.value;\n"
  js=js + "}\n}\nelse{\nformData[this.name] = this.value;\n}\n});\n"
  js=js + "$('select').each(function(){\nif(this.multiple){\nfor(option of this.selectedOptions){\nvar val = option.value;\n"
  js=js + "if(!(this.name in formData)){\n"
  js=js + "formData[this.name] = [];\n}\nformData[this.name].push(val);\n}\n}\nelse{\nformData[this.name] = this.options[this.selectedIndex].value;\n}\n});\n"
  js=js + "return formData;\n}\n"

  js=js + "function displayData(item){\n"
  js=js + "$('#display-data').hide();\n"
  js=js + "var url = 'http://localhost:5000/webforms/display/';\n"
  js=js + "$.ajax({\nurl: url,\ntype: 'GET',\nsuccess: function(resultColumns) {\nvar htmlString = '';\n"
  js=js + "for (var x in resultColumns){\n htmlString += '<p>The data of table <b>'+x+ '</b>:</p>';\n htmlString += '<table><thead><tr>';\n "
  js=js + "for(i=0; i<resultColumns[x]['header'].length; i++){\nhtmlString += '<th>'+resultColumns[x]['header'][i][0]+ '</th>'\nconsole.log(resultColumns[x]['header'][i][0])\n}\n"
  js=js + "htmlString += '</thead><tbody>';\nfor(i=0;i<resultColumns[x]['data'].length;i++){\n"
  js=js + "htmlString += '<tr>';\nfor(j=0;j<resultColumns[x]['data'][i].length;j++){\nhtmlString += '<td>' + resultColumns[x]['data'][i][j] + '</td>';\n}\nhtmlString += '</tr>';\n}\n"
  js=js + "htmlString += '</tbody></table>';\nhtmlString += '<br><br>';\n}\n$('#results').html(htmlString);\n},\n"
  js=js + "error: function(error) {\nalert('ERROR');\nconsole.log(error);\n}\n});\n}\n"


  f.write(js)

def max_length(x):
    size = "(MAX)"
    z =[]
    if 'maxlength' in x:
        size = "(" +x['maxlength']+")"
    else:
        if 'group' in x:
            for y in x['group']:
                z.append(y['caption'])
            size = "(" + str(len(max(z, key= len))) + ")"
    return size

def sql_producer(js):
    # uid = js['mysqlUserID']
    # pwd = js['mysqlPWD']
    name = js['name']
    db = js['mysqlDB']
    checkdb = "CREATE DATABASE IF NOT EXISTS "+ db+ ";\nUSE "+db+";"
    # host = js['backendHost']
    # conn = connect(host,uid,pwd,db)
    sqlstring = "SET FOREIGN_KEY_CHECKS = 0;\n\n drop table if exists "+name+";\n\n SET FOREIGN_KEY_CHECKS = 1; \n\n create table "+ name +"( \n"
    followupstring =""
    tablelist=[]
    tablelist.append(name)

    if 'elements' in js:
        pk = ""
        firstcol =""
        firstcolname=""
        for x in js['elements']:
            if 'key' in x:
                pk =   "primary key ("+ x['ename'] + ")"
                firstcolname=x['ename']
                global primary_key_column
                primary_key_column = firstcolname
                firstcol = x['ename']+" VARCHAR"+ max_length(x)+","           
            if x['etype'] == "textbox" or x['etype'] == "selectlist" or x['etype'] == "radiobutton" :
                colname = x['ename']
                datatype = x['datatype']
                size = max_length(x)
                sqlstring = sqlstring + colname + " VARCHAR"+ size + ",\n" 
            else:
                if x['etype'] == "checkbox" or x['etype'] == "multiselectlist":
                    tname= x['ename']
                    tablelist.append(tname)
                    innercolname = tname+"_col"
                    innerdatatype = 'VARCHAR'
                    innerdatatypesize = max_length(x)
                    followupstring = followupstring+"\n\ndrop table if exists "+tname+";\n create table "+tname+"(\n"+firstcol+"\n"+innercolname+" "+innerdatatype+innerdatatypesize+",\n primary key ("+firstcolname+","+innercolname+"),\nforeign key ("+firstcolname+") references "+ name+"("+firstcolname+"));\n"
        sqlstring = checkdb +"\n"+ sqlstring + pk +");\n\n"+followupstring
        sqlstring = sqlstring.replace("string", "VARCHAR")
    filename = name+".sql"
    with open(filename, 'w+') as output:
        output.write(sqlstring)
    return(tablelist)

def generateCSS(db):
  fileName = db["name"]+".css"
  f = open(fileName, "w")
  css="table, th, td {\nborder: 1px solid black;\n}"
  f.write(css)

def generatePython(db,tablelist):
  tablelist=tablelist
  db_name = db["mysqlDB"]
  table_name = db['name']
  fileName = table_name+".py"
  f = open(fileName, "w")

  urlComps = db["backendURL"].split("/")
  url = urlComps[len(urlComps)-2]

  if "localhost" in url:
    url = urlComps[len(urlComps)-1]



  py = "from flask import Flask, jsonify\nfrom flask import abort\nfrom flask import make_response\nfrom flask import request\nimport mysql.connector as mysql\nfrom flask_cors import CORS\n"
  py = py + "app = Flask(__name__)\nCORS(app)\n"
  py = py + "@app.route('/"+url+"/insert/', methods=['POST'])\ndef insert_record():\n"
  py = py + "   for key in request.json:\n      print(key, '->', request.json[key])\n   queries = ['INSERT INTO "+table_name+"']\n   query = queries[0]\n"
  py = py + '   keys = " ("\n   values = " ("\n   i=0\n'
  py = py + '   for key in request.json:\n      if isinstance(request.json[key],str):\n         if i==0:\n            i = i+1\n'
  py = py + '         else:\n            keys =  keys + ","\n            values = values + ","\n'
  py = py + '         keys =  keys + key\n         values = values + "'
  py = py + "'" + '" + request.json[key] + "'+"'"+'"\n'
  py = py + '      else:\n         for val in request.json[key]:\n'
  py = py + '            query2 = "INSERT INTO " + key + " (" + key + "_col , '+primary_key_column+') VALUES ('+"'"+'"'
  py = py + "+val"+'+"'+"'"+ ', '+"'"+ '"+request.json['+"'"+primary_key_column+"'"+']+"'+"'"+')"\n'
  py = py + '            queries.append(query2)\n'
  py = py + '   keys =  keys + ")"\n   values = values + ")"\n   query = query + keys + " VALUES " + values\n   queries[0] = query\n   ok = True\n'
  py = py + '   db = mysql.connect(\n'
  py = py + '      host="localhost",\n      database="'+db_name+'",\n      user="'+db["mysqlUserID"]+'",\n      passwd="'+db["mysqlPWD"]+'",\n      auth_plugin="mysql_native_password"\n      )\n'
  py = py + '   for q in queries:\n      cursor = db.cursor()\n      try:\n'
  py = py + '         cursor.execute(q)\n         db.commit()\n         cursor.close()\n      except Exception as e:\n'
  py = py + '         db.rollback()\n         cursor.close()\n         ok=False\n'
  py = py + '   db.close()\n   result = {"ok": ok}\n   return jsonify(result)\n'

  # get function
  py = py + "@app.route('/"+url+"/display/', methods=['GET'])\ndef display_data():\n"
  py = py + '   tables=[]\n'
  for i in tablelist:
    py = py + '   tables.append(\''+i+'\')\n'
  py = py + '   print(tables)\n'
  py = py + '   tablequery= "show tables from '+db_name+';"\n'
  py = py + '   db = mysql.connect(\n'
  py = py + '       host="localhost",\n      database="'+db_name+'",\n      user="'+db["mysqlUserID"]+'",\n      passwd="'+db["mysqlPWD"]+'",\n      auth_plugin="mysql_native_password"\n      )\n'
  py = py + '   cursor = db.cursor()\n'
  py = py + '   cursor.execute(tablequery)\n'
  py = py + '   t=cursor.fetchall()\n'
  py = py + '   tablelist=[]\n'
  py = py + '   for i in t:\n'
  py = py + '      tablelist.append(i[0])\n'
  py = py + '   result={}\n'
  py = py + '   for i in tables:\n'
  py = py + '     columnquery= "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='+"'"+db_name+"'"+' and TABLE_NAME = '+"'"+'"+i+"'+"'"+' order by ordinal_position;"\n'
  py = py + '     dataquery= "select * from "'+'+i+'+'";"\n'
  py = py + '     db = mysql.connect(\n'
  py = py + '       host="localhost",\n      database="'+db_name+'",\n      user="'+db["mysqlUserID"]+'",\n      passwd="'+db["mysqlPWD"]+'",\n      auth_plugin="mysql_native_password"\n      )\n'
  py = py + '     cursor = db.cursor()\n'
  py = py + '     cursor.execute(columnquery)\n'
  py = py + '     columns=cursor.fetchall()\n'
  py = py + '     cursor.execute(dataquery)\n'
  py = py + '     data=cursor.fetchall()\n'
  py = py + '     cursor.close()\n'
  py = py + '     db.close()\n'
  py = py + '     tbldata={}\n'
  py = py + "     tbldata['header']=columns\n"
  py = py + "     tbldata['data']=data\n"
  py = py + "     result[i]=tbldata\n"
  py = py + '   return jsonify(result)\n'
  py = py + "if __name__ == '__main__':\n   app.run(host='localhost',debug=True)\n\n"
 

  f.write(py)

def errorcheck(js):
    if 'elements' in js:
        multivalel=0
        reqkey=0
        check1=0
        check2=0
        count=0
        k={}
        for x in js['elements']:
            if x['etype'] == "checkbox" or x['etype'] == "multiselectlist":
                multivalel= 1            
            if 'key' in x:
                if x['key']=="key" and x['required'] =="true":
                    reqkey = 1
            k[x['ename']]=count
            count+=1
        if(multivalel==reqkey==1):
            check1=1
        if(len(k)==count):
            check2=1
        if(check1==check2==1):
            print("file doesn't have any errors.")
            tablelist=sql_producer(js)
            generateFormHTML(js)
            generateDisplayHTML(js)
            generateCSS(js)
            generateJavaScript(js)
            generatePython(js,tablelist)
            print("Files are Generated.")
        else:
            print("file has errors:\n")
            if check1 != 1:
                print("The json form doesn't contains primary key element if there are mutivalued elements in it\n")
            if check2 != 1:
                print("The json form have duplicate element names\n")
            print("Please input a file without erros.")



def main():
  
   
  # Arguments passed
  print("\nName of Python script:", sys.argv[1])

  with open(sys.argv[1],'r') as fp:
    db = json.load(fp)
  errorcheck(db)

main()
 