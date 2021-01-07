# --------------- web.py Python Webserver ---------
#  Listens on Port 8081
#  Takes JSONs and branches

# -----------------   This is the backend for the access bastion configuration GUI
#                     26.05.2020 CB
#   It runs as a service on Linux:
#         systemctl status bastion
#   To see logs: journalctl  --full -u bastion -f
#
#   Service looks like this:
#[Unit]
#Description=bastion
#After=syslog.target network.target
#
#[Service]
#Type=simple
##StandardOutput=journal+console
#WorkingDirectory=/var/www/stock/bastion
#Environment="VIRTUAL_ENV=/var/www/stock/bastion/venv"
#Environment="PATH=$VIRTUAL_ENV/bin:$PATH"
#ExecStart=/var/www/stock/bastion/venv/bin/python -u backend.py 8081
#
#[Install]
#WantedBy=multi-user.target

#For windows we do:
#cd C:\programmieren\HTML\200515_MARC
#call venv\Scripts\activate.bat
#python backend.py 8081


#Library web.py for Webserver
import web
import json

#divers libraries
import time
import datetime
import os
import pprint
import requests
import sys
import traceback
import csv
import urllib3
import socket
#disable some warnings of post and get concerning ssl
requests.packages.urllib3.disable_warnings()



#for UTF8 UTF16
import io

# ---- Die html Homepage bekommt einen Ast zugewiesen. Dort wiederum eine Klasse zugewiesen, hier:
urls = (
	'/test/index.html', 'test',
	'/', 'test',
	'/categories','categories',
	'/createsingleressource','createsingleressource',
	'/csv','csv',		
	'/execute_prod','execute_prod',
	'/login','login',
	'/values_after_login','values_after_login'
	
 )

# --- display on stdout e.g. Current Time: 26.05.2020 17:05:20  
def display_current_time():
	t  = datetime.datetime.now()
	t2 = t.timetuple()		
	print "Current Time: "+time.strftime("%d.%m.%Y %H:%M:%S", t2)
		
		

# -- own  global variables here. Because webpy tree classes seem to be recreated every time
class cInput:
	#login handler
	data= {}	

c = cInput()



#classname given by tree entry
class test:
	# class simply returns a json
	# --------------------- GET -------------------------------------
	def GET(self):
		#server side allow Cross Origin queries
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')	

        #return json text MIME
		web.header('Content-Type', 'application/json')

		return '{"Command":"GET","Say":"Test OK!"}'
		#json_return = "{\"Command\":\""+user_data.command.upper()+"\","+mitte+"}"
	
	# --------------------- POST ------------------------------------
	def POST(self):
		#server side allow Cross Origin queries		
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')

		print web.input()
		
		#return json text MIME
		web.header('Content-Type', 'application/json')
		
		return '{"Command":"POST","Say":"Test OK!"}'


class categories:
	# class executes a webservice login and get-query to retrieve a list of categories. It will return a json
	# --------------------- GET -------------------------------------
	def GET(self):
		#server side allow Cross Origin queries
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')	

        #return json text MIME
		web.header('Content-Type', 'application/json')

		#		
		display_current_time()

		#login
		r = requests.post('https://safe.strg.arte/publicapi/api-auth', verify=False, json={'login':'XXXXXXXXXX', 'password':'YYYYYYYYYYY','org':'arte'})
		data = r.json()
		
		#recupere les categories et les affiche dans une liste deroulante--------------------------
		data_oin={}
		try:
			id = data['id']
			print("Authentication succeded")
			print(id)
			adata   = "json={}"
			header={'Authorization':str(id)}
			time.sleep(2)
			rcat = requests.get('https://safe.strg.arte/publicapi/arte/categories/',verify=False,json={},headers=header)
			#print rcat
			data_oin = rcat.json()
			
			for x in range(len(data_oin)):
				print(data_oin[x])        
		except:			
			traceback.print_exc(file=sys.stdout)
			print("Authentication failure")
			#sys.exit(1)
    
    
		#a={}
		#a["Command"]="GET-categories-json"
		#a["Say"]="Test OK"
		#a[1]={"name":"Poc-Philips"}
		#a[2]={"name":"INEWS"}
		#convert dictionary to string
		json_return=""
		json_return=json.dumps(data_oin)
		#return '{"Command":"GET-categories","Say":"Test OK!"}'
		#json_return = "{\"Command\":\""+user_data.command.upper()+"\","+mitte+"}"
		return json_return


class categories_old:
	# test class returns a json
	# --------------------- GET -------------------------------------
	def GET(self):
		#server side allow Cross Origin queries
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')	

        #return json text MIME
		web.header('Content-Type', 'application/json')

		a={}
		a["Command"]="GET-categories-json"
		a["Say"]="Test OK"
		a[1]={"name":"Poc-Philips"}
		a[2]={"name":"INEWS"}
		#convert dictionary to string
		json_return=""
		json_return=json.dumps(a)
		#return '{"Command":"GET-categories","Say":"Test OK!"}'
		#json_return = "{\"Command\":\""+user_data.command.upper()+"\","+mitte+"}"
		return json_return



class createsingleressource:
	# class executes a webservice post with json inputdata
	# --------------------- POST ------------------------------------
	def POST(self):
		#server side allow Cross Origin queries		
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')

        #return json text MIME
		web.header('Content-Type', 'application/json')
		display_current_time()
		
		#get Storage Object
		storage =  web.input()
		#<Storage {'{"RES_Description":"srv-ced-001","RES_IP":"127.0.0.1"}': u''}>
		print storage		
		
		#Convert storage to string
		storage_string = json.dumps(storage)
		#{"{\"RES_Description\":\"srv-ced-001\",\"RES_IP\":\"127.0.0.1\"}": ""}
		print storage_string
		
		#Convert string to dictionary
		storage_dictionary = json.loads(storage_string)
		#{u'{"RES_Description":"srv-ced-001","RES_IP":"127.0.0.1"}': u''}
		#print storage_dictionary
		#print "aa"+storage_dictionary.keys()[0]
		
		#Get the jsonstring which is a key of the dictionary array		
		storage_keyslist = storage_dictionary.keys()
		#[u'{"RES_Description":"srv-ced-001","RES_IP":"127.0.0.1"}']
		print storage_keyslist
		
		#Get the first key of the dictionary which is a json string
		storage_jsonstring = storage_keyslist[0]
		#{"RES_Description":"srv-ced-001","RES_IP":"127.0.0.1"}
		print storage_jsonstring
		
		#Construct data dictionary
		data = json.loads(storage_jsonstring)
		#{u'RES_IP': u'127.0.0.1', u'RES_Description': u'srv-ced-001'}
		print ""
		print data
		
		# ------------  ALL VALUES NEEDED FOR THE WEBSERVICE LISTED HERE:
		#get hostname and IP
		RES_Description = data["RES_Description"]
		RES_IP          = data["RES_IP"]
		RES_Comm        = data["RES_Comm"]
		RES_User        = data["RES_User"] 
		SERVICE_Type    = data["SERVICE_Type"]
		CATEGORIE       = "https://safe.strg.arte/publicapi/arte/categories/"+data["CATEGORIE"]+"/"
			
		
		#RES_Description = app.getEntry("ServerName")
		#RES_IP = app.getEntry("IP")
		#RES_Comm = "COMMENTAIRE"
		#RES_User = "user-automation-regie"
		#SERVICE_Type = app.getOptionBox("Connection Type")
		#CATEGORIE = "https://safe.strg.arte/publicapi/arte/categories/"+str(CAT_NUM)+"/"

    	
		# --- test mode
		#if data["CATEGORIE"]  == "24":
		#	print "------TESTMODE ON--------  (category is TEST)"
		#else:
		#	return '{"Command":"POST","Say":"NO TESTMODE. Stopping"}'
			
		
		# --- execute call
		
		#login		
		r = requests.post('https://safe.strg.arte/publicapi/api-auth', verify=False, json={'login':'XXXXXXXX', 'password':'YYYYYYYYYYY','org':'arte'})
		data = r.json()
		c.data = data						
		try:
			id = c.data['id']
			print("Authentication succeded")
			print(id)
			fine = True
			header={'Authorization':str(id)}
			time.sleep(2)			
		except:			
			traceback.print_exc(file=sys.stdout)
			print("Authentication failure")
			fine = False
		
		def handleResult(self,rres):
			print "handleResult"
			try:	
				status = rres.status_code
				if status == 500:
					return '{"Command":"POST","Say":"500 - probably ressource exist."}'
				elif  status == 201:
					return '{"Command":"POST","Say":"201 - Ressource created!"}'	
			except:
				return ""
				
		return_json=""		
		try:
			#socket.inet_aton(RES_IP)			
			if SERVICE_Type == 'RDP':
				rres = requests.post('https://safe.strg.arte/publicapi/arte/rdpservices/',verify=False,json={"alias": RES_User,"ask_id": False,"auth_domain": "","colors": 24,"connect_local_com_port": False,"console_mode": False,"description": "","dynamic": False,"enable_AUP": False,"enable_CSSP": True,"enable_SSO": "sso-fixe","enable_wallpaper": True,"launch_directory": "","mask": "","motd": "","mount_local_disk": False,"mount_local_printer": False,"noagent": True,"plug_and_play": "","redirect_audio_input": False,"redirect_clipboard": True,"remote_application": "","resolution": "fullscreen","resource": {  "category": CATEGORIE,  "name": RES_Description,  "resource_description": RES_Comm,  "resource_id": 666},"server": RES_IP,"service_id": 84,"type": "","use_all_screen": False},headers=header)
				print(rres)
				return_json = handleResult(self,rres)
			elif SERVICE_Type == 'HTML5RDP':
				rres = requests.post('https://safe.strg.arte/publicapi/arte/html5rdpservices/',verify=False,json={"alias": RES_User,"auth_domain": "","colors": 32,"console_mode": False,"description": "","dynamic": False,"enable_SSO": "sso-fixe","enablewallpaper": True,"keyboard": "1036","launch_directory": "","mask": "","motd": "","noagent": False,"port": 3389,"remote_application": "","resolution": "fullscreen","resource": {"category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm,"resource_id": 161},"security_mode": "rdp","server": RES_IP,"service_id": 33,"type": ""},headers=header)
				print(rres)
				return_json = handleResult(self,rres)
			elif SERVICE_Type == 'SSH':
				rres = requests.post('https://safe.strg.arte/publicapi/arte/sshservices/',verify=False,json={"alias": RES_User,"remote_ip": RES_IP,"local_port": 0,"locale_ip": "127.0.0.1","dynamic": False,"remote_port": 22,"motd":"","enable_SSO": "sso-fixe","description": "","resource": { "category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm }},headers=header)
				print(rres)
				return_json = handleResult(self,rres)
			elif SERVICE_Type == 'HTML5SSH':
				rres = requests.post('https://safe.strg.arte/publicapi/arte/html5sshservices/',verify=False,json={"alias": RES_User,"server": RES_IP,"dynamic": False,"port": 22,"motd":"","enable_SSO": "sso-fixe","description": "","resource": { "category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm }},headers=header)
				print(rres)
				return_json = handleResult(self,rres)
			elif SERVICE_Type == 'VNC':
				rres = requests.post('https://safe.strg.arte/publicapi/arte/vncservices/',verify=False,json={"alias": RES_User,"server": RES_IP,"dynamic": False,"port": 5900,"motd":"","enable_SSO": "sso-fixe","description": "","resource": { "category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm }},headers=header)
				print(rres)
				return_json = handleResult(self,rres)
			elif SERVICE_Type == 'HTML5VNC':
				rres = requests.post('https://safe.strg.arte/publicapi/arte/html5vncservices/',verify=False,json={"alias": RES_User,"description": "","dynamic": False,"enable_SSO": "sso-fixe","server": RES_IP,"port": 5900,"motd":"","resource": { "category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm }},headers=header)
				print(rres)
				return_json = handleResult(self,rres)
			else:
				print ("unknown service")
			print rres.status_code 
		except:
			traceback.print_exc(file=sys.stdout)			
			return '{"Command":"POST","Say":"ERROR - Ask Admin for logs"}'
		
		
		#return '{"Command":"POST","Say":"'+RES_Description+" and "+RES_IP+' and more.."}'
		if return_json == "":
			return '{"Command":"POST","Say":"'+RES_Description+" and "+RES_IP+' and more.."}'
		else:
			return return_json
		
		#return '{"Command":"POST","Say":"createsingleressource OK!"}'
		

       
# -- save returncodes here
statuscodes=[]
class csv:
	# class takes a json list to send to webservice
	# --------------------- POST ------------------------------------
	def POST(self):
		#server side allow Cross Origin queries		
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		# -- reset to zero
		global statuscodes
		statuscodes=[]

        #return json text MIME
		web.header('Content-Type', 'application/json')
		
		
		#get Storage Object
		storage =  web.input()
		#<Storage {'{"RES_Description":"srv-ced-001","RES_IP":"127.0.0.1"}': u''}>
		#<Storage {'[["testcb","10.1.1.1","DESC1","user-automation-regie","RDP"],["testcb1","10.1.1.2","DESC2","user-automation-regie","HTML5RDP"],
		#       ["testcb4","10.1.1.4","DESC4","user-automation-regie","SSH"]]': u''}>
		#<Storage {'{"RES_ARRAY":"[[\\"testcb\\",\\"10.1.1.1\\",\\"DESC1\\",\\"user-automation-regie\\",\....
		print storage

		#Convert storage to string
		storage_string = json.dumps(storage)
		print storage_string
		
		#Convert string to dictionary
		storage_dictionary = json.loads(storage_string)
		storage_keyslist = storage_dictionary.keys()
		#[u'{"RES_ARRAY":[["testcb","10.1.1.1","DESC1","user-automation-regie"
		print storage_keyslist
		
		#Get the first key of the dictionary which is a json string
		storage_jsonstring = storage_keyslist[0]
		#{"RES_ARRAY":[["testcb","10.1.1.1","DESC1","user-autom
		print storage_jsonstring
		
		#Construct data dictionary
		data = json.loads(storage_jsonstring)
		print ""
		print data
		#{u'RES_ARRAY': [[u'testcb', u'10.1.1.1', u'DESC1', u'user-automation-regie'
		data2 = data["RES_ARRAY"]
		
		#get the array
		#print data["RES_ARRAY"][0]
		#[u'testcb', u'10.1.1.1', u'DESC1', u'user-automation-regie', u'RDP']
		
		
		
		#now construct data arrays
		RES_Descriptions = []     #servername
		RES_IPs          = []
		RES_Comms        = []    # a comment
		RES_Users        = []
		SERVICE_Typs     = []
		CATEGORIE        = "https://safe.strg.arte/publicapi/arte/categories/"
		
		#rint data
		#print data["RES_Description"]
		#print data[2]
		#data2 = eval(data)
		#print data2[0]
		for c in data2:
			print c
			if c[0] == "cat_id":
				print "Cat_id:"+c[1]
				CATEGORIE = CATEGORIE + c[1] + "/"
			else:
				RES_Description = c[0]
				RES_Descriptions.append(RES_Description)
				RES_IP = c[1]
				RES_IPs.append(RES_IP)
				RES_Comm = c[2]
				RES_Comms.append(RES_Comm)
				RES_User = c[3]
				RES_Users.append(RES_User)
				SERVICE_Typ = c[4]
				SERVICE_Typs.append(SERVICE_Typ)
					
				
				
		print "Array Descriptions:"
		print RES_Descriptions
		print "Array IPs:"
		print RES_IPs
		print "Array Comments:"
		print RES_Comms
		print "Array Servicetypes:"
		print SERVICE_Typs
		print "Categorie via ID:"
		print CATEGORIE
		
		# -- arrived here we can construct our call
		
	
		#---function invoked after each csv line. It will build statuscode array
		def handleResults(self,rres,RES_Description):
			global statuscodes
			print "handleResults"
			 
			#try:	
			status = rres.status_code
			print "Got:"+str(status)
			print statuscodes 
			if status == 500:
				statuscodes.append(RES_Description+" exists")
			elif status == 201:
				statuscodes.append(RES_Description+" ok")
			else:
				statuscodes.append(RES_Description+str(status))
			#except:
			return ""
				
		
		prodmode=True
		
		if prodmode == True:
			#login		
			r = requests.post('https://safe.strg.arte/publicapi/api-auth', verify=False, json={'login':'XXXXXXXXXX', 'password':'YYYYYYYYYYYYY','org':'arte'})
			data = r.json()						
			try:
				id = data['id']
				print("Authentication succeded")
				print(id)
				fine = True
				header={'Authorization':str(id)}
				time.sleep(2)			
			except:			
				traceback.print_exc(file=sys.stdout)
				print("Authentication failure")
				fine = False
				return '{"Command":"POST","Say":"ERROR - Ask Admin for logs"}'
		else:
			print " _____ DEBUGMODE - no login request send"
		
		
			
			
		#print len(RES_Descriptions)
		for i in range(len(RES_Descriptions)):
			RES_Description = RES_Descriptions[i]
			RES_IP          = RES_IPs[i]
			RES_Comm        = RES_Comms[i]			
			RES_User        = RES_Users[i] 
			SERVICE_Type    = SERVICE_Typs[i]			
			print "HANDLE "+str(i)+"-----------"
			print " RES_Description: "+RES_Description
			print " RES_IP         : "+RES_IP
			print " RES_Comm       : "+RES_Comm
			print " RES_User       : "+RES_User
			print " SERVICE_Type   : "+SERVICE_Type
			print " CATEGORIE      : "+CATEGORIE

			try:
				#socket.inet_aton(RES_IP)			
				if SERVICE_Type == 'RDP':
					rres = requests.post('https://safe.strg.arte/publicapi/arte/rdpservices/',verify=False,json={"alias": RES_User,"ask_id": False,"auth_domain": "","colors": 24,"connect_local_com_port": False,"console_mode": False,"description": "","dynamic": False,"enable_AUP": False,"enable_CSSP": True,"enable_SSO": "sso-fixe","enable_wallpaper": True,"launch_directory": "","mask": "","motd": "","mount_local_disk": False,"mount_local_printer": False,"noagent": True,"plug_and_play": "","redirect_audio_input": False,"redirect_clipboard": True,"remote_application": "","resolution": "fullscreen","resource": {  "category": CATEGORIE,  "name": RES_Description,  "resource_description": RES_Comm,  "resource_id": 666},"server": RES_IP,"service_id": 84,"type": "","use_all_screen": False},headers=header)
					print(rres)
					handleResults(self,rres,RES_Description)
				elif SERVICE_Type == 'HTML5RDP':
					rres = requests.post('https://safe.strg.arte/publicapi/arte/html5rdpservices/',verify=False,json={"alias": RES_User,"auth_domain": "","colors": 32,"console_mode": False,"description": "","dynamic": False,"enable_SSO": "sso-fixe","enablewallpaper": True,"keyboard": "1036","launch_directory": "","mask": "","motd": "","noagent": False,"port": 3389,"remote_application": "","resolution": "fullscreen","resource": {"category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm,"resource_id": 161},"security_mode": "rdp","server": RES_IP,"service_id": 33,"type": ""},headers=header)
					print(rres)
					handleResults(self,rres,RES_Description)
				elif SERVICE_Type == 'SSH':
					rres = requests.post('https://safe.strg.arte/publicapi/arte/sshservices/',verify=False,json={"alias": RES_User,"remote_ip": RES_IP,"local_port": 0,"locale_ip": "127.0.0.1","dynamic": False,"remote_port": 22,"motd":"","enable_SSO": "sso-fixe","description": "","resource": { "category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm }},headers=header)
					print(rres)
					handleResults(self,rres,RES_Description)
				elif SERVICE_Type == 'HTML5SSH':
					rres = requests.post('https://safe.strg.arte/publicapi/arte/html5sshservices/',verify=False,json={"alias": RES_User,"server": RES_IP,"dynamic": False,"port": 22,"motd":"","enable_SSO": "sso-fixe","description": "","resource": { "category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm }},headers=header)
					print(rres)
					handleResults(self,rres,RES_Description)
				elif SERVICE_Type == 'VNC':
					rres = requests.post('https://safe.strg.arte/publicapi/arte/vncservices/',verify=False,json={"alias": RES_User,"server": RES_IP,"dynamic": False,"port": 5900,"motd":"","enable_SSO": "sso-fixe","description": "","resource": { "category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm }},headers=header)
					print(rres)
					handleResults(self,rres,RES_Description)
				elif SERVICE_Type == 'HTML5VNC':
					rres = requests.post('https://safe.strg.arte/publicapi/arte/html5vncservices/',verify=False,json={"alias": RES_User,"description": "","dynamic": False,"enable_SSO": "sso-fixe","server": RES_IP,"port": 5900,"motd":"","resource": { "category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm }},headers=header)
					print(rres)
					handleResults(self,rres,RES_Description)
				else:
					print ("unknown service")
				print rres.status_code 
			except:
				traceback.print_exc(file=sys.stdout)			
				#return '{"Command":"POST","Say":"ERROR - Ask Admin for logs"}'
				
			#wait a litte before sending next remote command
			time.sleep(1)
				
		#return json
		return '{"Command":"POST","Say":"'+" ".join(statuscodes)+'"}'
			
		
			
		
	

class csv_old:
	# class test simply returns a json
	# --------------------- POST ------------------------------------
	def POST(self):
		#server side allow Cross Origin queries		
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')

        #return json text MIME
		web.header('Content-Type', 'application/json')
		
		#get Storage Object
		storage =  web.input()
		#<Storage {'{"RES_Description":"srv-ced-001","RES_IP":"127.0.0.1"}': u''}>
		print storage	
		
					

						
class execute_prod:
	# test class does a simple test by calling webservice post to bastion
	# --------------------- GET -------------------------------------
	def GET(self):
		#server side allow Cross Origin queries
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')	

        #return json text MIME
		web.header('Content-Type', 'application/json')
		
		#login
		r = requests.post('https://safe.strg.arte/publicapi/api-auth', verify=False, json={'login':'XXXXXXXXXXX', 'password':'YYYYYYYYYYYY','org':'arte'})
		data = r.json()
		
		#recupere les categories et les affiche dans une liste deroulante--------------------------
		#data_oin={}
		try:
			id = data['id']
			print("Authentication succeded")
			print(id)
			adata   = "json={}"
			header={'Authorization':str(id)}
			time.sleep(2)
			#rcat = requests.get('https://safe.strg.arte/publicapi/arte/categories/',verify=False,json={},headers=header)
			RES_User =  "user-automation-regie"
			RES_IP = "172.24.122.116"
			#CATEGORIE = "https://safe.strg.arte/publicapi/arte/categories/"+str(CAT_NUM)+"/"
			CATEGORIE = "https://safe.strg.arte/publicapi/arte/categories/24/"
			SERVICE_Type  = "VNC"
			RES_Description = "srv-test-cb2"
			RES_Comm = "COMMENTAIRE"
	
			rres = requests.post('https://safe.strg.arte/publicapi/arte/vncservices/',verify=False,json={"alias": RES_User,"server": RES_IP,"dynamic": False,"port": 5900,"motd":"","enable_SSO": "sso-fixe","description": "","resource": { "category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm }},headers=header)
			#rres = requests.post('https://safe.strg.arte/publicapi/arte/vncservices/',verify=False,json={"alias": RES_User,"server": RES_IP,"dynamic": False,"port": 5900,"motd":"","enable_SSO": "sso-fixe","description": "","resource": { "category": CATEGORIE,"name": RES_Description,"resource_description": RES_Comm }},headers=header)
			print rres
			#data_oin = rres.json()
			#print data_oin
			#print rcat
			#data_oin = rcat.json()
			
			#for x in range(len(data_oin)):
			#		print(data_oin[x])        
		except:			
			traceback.print_exc(file=sys.stdout)
			print("Authentication failure")
			#sys.exit(1)
			
		 
         
         

		return '{"Command":"GET","Say":"Test OK!"}'
		#json_return = "{\"Command\":\""+user_data.command.upper()+"\","+mitte+"}"
	
	# --------------------- POST ------------------------------------			

#Klassennamen gegeben durch Baum in urls

#  ---- executes a simple login post call and saves login handle to c.data
class login:
	# class does a login post call and returns a json saying fine or not
	# --------------------- GET -------------------------------------
	def GET(self):
		#server side allow Cross Origin queries
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')	

        #return json text MIME
		web.header('Content-Type', 'application/json')
	
		#we write the handler inside this class c	
		global c
		#login
		r = requests.post('https://safe.strg.arte/publicapi/api-auth', verify=False, json={'login':'XXXXXXXXXX', 'password':'YYYYYYYYYYYY','org':'arte'})
		data = r.json()
		c.data = data
		
		fine = True
		
		try:
			id = c.data['id']
			print("Authentication succeded")
			print(id)
			fine = True			
		except:			
			traceback.print_exc(file=sys.stdout)
			print("Authentication failure")
			fine = False
			
		if fine == True:			
			return '{"Command":"Login","Says":"Fine"}'
		else:
			return '{"Command":"Login","Says":"Error"}'				
		
class values_after_login:
	# a  test class to execute a get query to get list of categories
	# --------------------- GET -------------------------------------
	def GET(self):
		#server side allow Cross Origin queries
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')	

        #return json text MIME
		web.header('Content-Type', 'application/json')

		#login previously
		global c
		data = c.data
			
		
		#recupere les categories et les affiche dans une liste deroulante--------------------------
		data_oin={}
		try:
			id = data['id']
			print("Authentication succeded")
			print(id)
			adata   = "json={}"
			header={'Authorization':str(id)}
			time.sleep(2)
			rcat = requests.get('https://safe.strg.arte/publicapi/arte/categories/',verify=False,json={},headers=header)
			#print rcat
			data_oin = rcat.json()
			
			for x in range(len(data_oin)):
				print(data_oin[x])        
		except:			
			traceback.print_exc(file=sys.stdout)
			print("Authentication failure")
			#sys.exit(1)
    
    
		#a={}
		#a["Command"]="GET-categories-json"
		#a["Say"]="Test OK"
		#a[1]={"name":"Poc-Philips"}
		#a[2]={"name":"INEWS"}
		#convert dictionary to string
		json_return=""
		json_return=json.dumps(data_oin)
		#return '{"Command":"GET-categories","Say":"Test OK!"}'
		#json_return = "{\"Command\":\""+user_data.command.upper()+"\","+mitte+"}"
		return json_return
		
		

	
if __name__ == "__main__":
	simulate = False
	if simulate:
		#Test class
		#a = index()		
		#print c.file_lines
		#print a.convert_array_to_big_jsonstring(c.file_lines)
		print "simulate standalone mode"	
				
	else:
		#Start Webservice
		app = web.application(urls, globals())
		#change port via: python app.py 8081
		app.run()	
