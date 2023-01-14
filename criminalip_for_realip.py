# Coding by YES

import requests
import json
import sqlite3
import csv
import ipaddress


# TODO: Cloudflare Check, Colummn 만들기

def get_ip_list(path: str):
	with sqlite3.connect(path) as conn:
		cur = conn.cursor()
		query = r"SELECT main_url, ip_address FROM illegal_sites"
		result = cur.execute(query)

		ip_list = list()
		web_list = list()

		for i in result:
			ip_list.append(i[1])
			web_list.append(i)

	return ip_list, web_list

def cloudflare_dint(ip_list):
	default_ip = ['103.21.244.0/22',
				  '103.22.200.0/22',
				  '103.31.4.0/22',
				  '104.16.0.0/12',
				  '104.24.0.0/14',
				  '108.162.192.0/18',
				  '131.0.72.0/22',
				  '141.101.64.0/18',
				  '162.158.0.0/15',
				  '172.64.0.0/13',
				  '173.245.48.0/20',
				  '188.114.96.0/20',
				  '190.93.240.0/20',
				  '197.234.240.0/22',
				  '198.41.128.0/17',
				  '199.27.128.0/21']

	result = []

	for url, ip in ip_list:
		is_cloudflare = False
		for cloudflare_ip in default_ip:
			a = ipaddress.ip_network(cloudflare_ip, strict=False)

			if ip == None:
				continue

			b = ipaddress.ip_network(ip, strict=False)
			if b.subnet_of(a) is True:
				is_cloudflare = True
				continue

		result.append((url, ip, is_cloudflare))
	return result

def criminal_site_info(ip_list: list):

	dns_list = list()
	whois_list = list()
	vulner_list = list()
	category_list = list()

	for r in ip_list:
		print(r[0], r[1])
		params = {}
		headers = {'x-api-key': 'CbZsUSM88EzE6I61m5fEKVO2FeLZExwzN14aoakZ'}
		params['ip'] = r[1]
		params['full'] = 'full'
		params['mode'] = 'out'

		res = requests.get('https://api.criminalip.com/getipdata?ip={}&full={}&mode={}'
						   .format(params['ip'], params['full'],params['mode']), headers=headers)

		if res.status_code == 200:
			result = res.json()
			try:
				dns_info = result['list_dns_info']
				whois_info = result['list_whois_info']
				vulner_info = result['list_vulnerability_info']
				category_info = result['list_ut1_info']
			except:
				print(r[0] + ': Parsing Error')
				pass

			try:
				dns_column = ['domain', 'registrar', 'confirmed_time', 'dns_register_date', 'email']
				whois_column = ['asn_name', 'org_name', 'email', 'local_address', 'org_country', 'phone_no', 'reg_date']
				vulner_column = ['app_name', 'app_version', 'cve_description', 'cve_id', 'list_cwe', 'list_edb', 'open_port_no']
				category_column = ['domain_name', 'ip_type', 'modify_dtime']

				for dns in dns_info:
					tmp = list()
					for column in dns_column:
						tmp.append(dns[column])
					dns_list.append(tuple(tmp))

				for whois in whois_info:
					tmp = list()
					tmp.append(r[0])
					tmp.append(r[1])
					tmp.append(r[2])
					for column in whois_column:
						tmp.append(whois[column])
					whois_list.append(tuple(tmp))

				for ut1 in category_info:
					tmp = list()
					for column in category_column:
						tmp.append(ut1[column])
					category_list.append(tuple(tmp))

				for vul in vulner_info:
					tmp = list()
					for v in vul:
						for column in vulner_column:
							if column == 'open_port_no':
								tmp.append(v[column]['TCP'])
							else:
								tmp.append(v[column])
							# tmp.append(vul[column])
						vulner_list.append(tuple(tmp))

				if len(vulner_info) == 1:
					vulner_list.append(('None', 'None','None','None','None'))
			except:
				pass
		# print(dns_info)
		# print(whois_info)
		# print(vulner_list)
		# print(category_info)
		else:
			print(res.status_code, res.text)
	return dns_list, whois_list, category_list, tmp

def get_realip(ip_list: str):
	for r in ip_list:
		print(r[0], r[1])
		params = {}
		params['domain'] = r[0]
		params['full'] = 'full'
		headers = {'x-api-key': 'CbZsUSM88EzE6I61m5fEKVO2FeLZExwzN14aoakZ'}
		res = requests.get('https://api.criminalip.com/getdomaindata?domain={}'.format(params['domain']), headers=headers)
		res2 = requests.get('https://api.criminalip.com/getdomaindata?domain={}&full={}'.format(params['domain'], params['full']), headers=headers)
		if res.status_code == 200:
			result = json.dumps(res.json())
			print(result)
		else:
			print(res.status_code, res.text)

		if res2.status_code == 200:
			result = json.dumps(res2.json())
			print(result)
		else:
			print(res2.status_code, res2.text)

def export_csv(info: list, category: str):
	dns_column = ['domain', 'registrar', 'confirmed_time', 'dns_register_date', 'email']
	whois_column = ['domain', 'ip', 'is_cloudflare', 'asn_name', 'org_name', 'email', 'local_address', 'org_country', 'phone_no', 'reg_date']
	vulner_column = ['app_name', 'app_version', 'cve_description', 'cve_id', 'list_cwe', 'list_edb', 'open_port_no']
	category_column = ['domain_name', 'ip_type', 'modify_dtime']

	with open('./Illegal' + category + '.csv', 'w', newline='', encoding='utf-8-sig') as f:
		w_csv = csv.writer(f)

		if category == 'dns':
			w_csv.writerow(dns_column)
			for val in info:
				w_csv.writerow(val)

		elif category == 'whois':
			w_csv.writerow(whois_column)
			for val in info:
				w_csv.writerow(val)

		elif category == 'vulner':
			w_csv.writerow(vulner_column)
			for val in info:
				w_csv.writerow(val)

		elif category == 'category':
			w_csv.writerow(category_column)
			for val in info:
				w_csv.writerow(val)
		else:
			print("Error: Confirm Your Input Category")

def main():
	result = []
	db_path = r'C:\\Users\\YES\\Desktop\\illegals.db'
	illegal_ip_list, illegal_web_list = get_ip_list(db_path)
	result_ip_list = cloudflare_dint(illegal_web_list)

	# Get Illegal Site General info
	# dns, whois, category, vul = criminal_site_info(result_ip_list)

	# Get Illegal Site RealIP info
	get_realip(result_ip_list)

	dns, whois, category, vul = criminal_site_info(result)
	# whois = criminal_site_info(result)

	# export_csv(dns, 'dns')
	export_csv(whois, 'whois')
	# export_csv(category, 'category')
	# export_csv(vul, 'vulner')

if __name__ == '__main__':
	main()