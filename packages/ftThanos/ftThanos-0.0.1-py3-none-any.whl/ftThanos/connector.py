import requests, os, json, time

class connector:
	ESC = "\x1b"
	BLACK = ESC + "[30m"
	BLUE = ESC + "[34m"
	RED = ESC + "[31m"
	GREEN = ESC + "[32m"
	DEFAULT = ESC + "[39m"
	verbose = False

	def __init__(self, **kwargs):
		env = self.dot_env_parser()
		url = 'https://api.intra.42.fr/oauth/token'
		UID = env['UID']
		SECRET = env['SECRET']
		grant_type ='client_credentials'
		scope = "public projects profile elearning tig forum"
		try:
			reply = requests.post(url,auth=(UID, SECRET),data={'scopes': scope, 'grant_type':grant_type,'client_id':UID,'client_secret':SECRET})
			reply.raise_for_status()
		except requests.exceptions.HTTPError as err:
				exit(print(self.RED + err))
		token = json.loads(reply.text)
		self.head = {'Authorization' : "Bearer {}".format(token['access_token'])}
		self.url = 'https://api.intra.42.fr/v2'
		if 'v' in kwargs:
			self.verbose = True
			print(self.BLUE + "Verbose activate." + self.DEFAULT)
		print(self.GREEN + "Connector ready to use!" + self.DEFAULT)

	def dot_env_parser(self):
		ret = {}
		try :
			with open ('.env', 'r') as file:
				for line in file:
					lst = line.split('=')
					if len(lst) != 2:
						continue
					ret[lst[0]] = lst[1][:-1]
		except IOError:
			exit(print(self.RED + 'No .env detected.' + self.DEFAULT))
		if not 'UID' in ret or not 'SECRET' in ret:
			exit(print(self.RED + 'Wrong parameters in .env, you should put in your file:\nSECRET=[Your secret token]\nUID=[Your UID token]' + self.DEFAULT))
		return (ret)

	def put_in_file(self, data, **kwargs):
		to_write = json.dumps(data, indent=4, sort_keys=True)
		if 'name' in kwargs:
			name = kwargs['name']
		else:
			name = 'output.json'
		if os.path.exists(name):
			os.remove(name)
		output = open(name, 'w')
		for line in to_write:
			output.write(line)
		print(self.GREEN + f"Data was put in {name}." + self.DEFAULT)

	def launcher(self, ftc, url, **kwargs):
		function = self.build_function_dispatch()
		lst = url.split(' ')
		self.put_in_file(function[ftc](self.build_endpoint(lst)))

	def build_function_dispatch(self):
		launch = {}
		launch['GET'] = self.get
		launch['DEL'] = self.delete
		launch['POST'] = self.post
		launch['PATCH'] = self.patch
		return (launch)

	def	build_endpoint(self, param):
		endpoint = param[0]
		for p in param[1:]:
			if '?' in endpoint:
				endpoint += "&" + p
			else:
				endpoint += "?" + p
		return (endpoint)

	def build_page(self, endpoint):
		if "?" in endpoint:
			endpoint += "&"
		else:
			endpoint += "?"
		endpoint += "page[size]=100&page[number]="
		return(endpoint)

	def get(self, url):
		i = 0
		sum_dict = []
		endpoint = self.build_page(url)
		while True:
			url = self.url + endpoint + str(i)
			try :
				reply = requests.get(url, headers=self.head)
				if reply.status_code == 429:
					continue
				reply.raise_for_status()
			except requests.exceptions.HTTPError as err:
				print(self.RED + str(err) + " on GET " + endpoint + self.DEFAULT)
				self.put_in_file(json.loads(reply.text), name='error.json')
				return (json.loads(reply.text))
			if 'X-Page' in reply.headers :
				sum_dict += json.loads(reply.text)
				if int(reply.headers['X-Page']) * int(reply.headers['X-Per-Page']) >= int(reply.headers['X-Total']):
					break
			else:
				if self.verbose == True:
					print(self.GREEN + "Success GET on " + url + self.DEFAULT)
				return (json.loads(reply.text))
			i+=1
		return (sum_dict)

	def post(self, endpoint, **kwargs):
		url = self.url + endpoint
		try:
			reply = requests.post(url, json=kwargs['body'], headers=self.head)
			reply.raise_for_status()
			if self.verbose == True:
				print(self.GREEN + "Success GET on " + url + self.DEFAULT)
		except requests.exceptions.HTTPError as err:
			self.put_in_file(json.loads(reply.text), name='error.json')
			print(self.RED + err + 'on POST ' + url + self.DEFAULT)
		return (json.loads(reply.text))

	def patch(self, endpoint, **kwargs):
		url = self.url + endpoint
		try:
			reply = requests.patch(url, json=kwargs['body'], headers=self.head, )
			reply.raise_for_status()
			if self.verbose == True:
				print(self.GREEN + "Success POST on " + url + self.DEFAULT)
		except requests.exceptions.HTTPError as err:
			self.put_in_file(json.loads(reply.text), name='error.json')
			print(self.RED + str(err) + 'on PATCH ' + url + self.DEFAULT)
		return (json.loads(reply.text))

	def delete(self, endpoint, **kwargs):
		url = self.url + endpoint
		try:
			reply = requests.delete(url, headers=self.head )
			reply.raise_for_status()
			if self.verbose == True:
				print(self.GREEN + "Success POST on " + url + self.DEFAULT)
		except requests.exceptions.HTTPError as err:
			self.put_in_file(json.loads(reply.text), name='error.json')
			print(self.RED + err + 'on DELETE ' + url + self.DEFAULT)
		return (json.loads(reply.text))
