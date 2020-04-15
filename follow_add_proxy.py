import random,time,config
import requests
from bs4 import BeautifulSoup
import csv
import re
import random
import datetime
import os

def del_list():
	f = open('list.txt', 'w')
	f.close()

def phn():
    phone=list('00000')
    first = [917,987,952,999,950,953,960,905,968,966]
    phone[0] = str(8)
    phone[1] = str(random.choice(first))
    phone[2] = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
    phone[3] = str(random.randint(0,9)) + str(random.randint(0,9))
    phone[4] = str(random.randint(0,9)) + str(random.randint(0,9))
    result = phone[0] + ' ' + phone[1] + ' ' + phone[2] + '-' + phone[3] + '-' + phone[4]
    return result

def write_csv(data):
    with open('property.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['url'], data['phone_number'],data['datetime'],data['price']))

def get_page(url):
	headers = {'User-Agent': config.list_user_agent[0]}
	proxies = {'https': 'https://{}'.format(config.list_proxies[0])}
	try:
		r = requests.get(url,headers=headers,proxies=proxies, timeout=10)
		print(proxies)
		print(headers)
		if r.status_code == 200:
			try:
				response = r.text
				soup = BeautifulSoup(response, 'lxml')
				check_info = soup.find('a',class_='header-services-menu-link-TRWKh header-services-menu-link-not-authenticated-3kAga').text
				print(check_info)
				return response
			except:
				print('Доступ заблокирован')
				config.change_proxy_header()
				get_page(url)
		else:
			print('Получил статус код {},пробует заново'.format(r.status_code))
			config.change_proxy_header()
			get_page(url)
	except:
		print('Не соеденился пошел через except,пробуем заново')
		config.change_proxy_header()
		get_page(url)  # решение:config.url

def get_page_data(html):
	global msg_answer
	msg_answer = None
	soup2 = BeautifulSoup(html, 'lxml')
	flat_items = soup2.find_all('div', class_='item__line')
	
	if os.stat("list.txt").st_size == 0:
		with open ("list.txt", 'w') as w:
			for flat in flat_items:
				flat_id = flat.find('a', class_ = 'snippet-link').get('href').split('_')[-1]
				w.write(str(flat_id) + ' ')	
		
	with open ("list.txt") as w:
		s1 = w.readline().strip() 
		l=s1.split(' ')
	
	for flat in flat_items:
		flat_id = flat.find('a', class_ = 'snippet-link').get('href').split('_')[-1]
		
		if flat_id not in l:
			l.insert(0,flat_id)
			if len(l)>60:
				l.pop()
			with open ("list.txt", 'w') as w:
				for i in l:
					w.write(str(i) + ' ')
			try:
				url = flat.find('a', class_ = 'snippet-link').get('href')
				full_url = 'https://www.avito.ru' + url
			except:			
				full_url=''
			try:
				#price = flat.find('span', class_ = 'snippet-price snippet-price-vas').text
				price = flat.find('span', class_='snippet-price').text.strip()
				clean_price = price[0:6] + ' ' + 'P'
				print(clean_price)
			except:
				price = ''
			phone_number = phn()
			datetime_object = datetime.datetime.now()
			data={ 'url' : full_url,
			       'phone_number' : phone_number,
			       'datetime' : str(datetime_object),
				   'price' : clean_price }
			write_csv(data)
			msg_answer = data['url'] + '\n' + config.emoji_phone() + ' ' + data['phone_number'] + '\n' + data['price']

def main():
	url = 'https://www.avito.ru/kazan/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1'

	get_page_data(get_page(url))
	time.sleep(random.randint(28, 34))
	if msg_answer is not None:
		print(msg_answer)
		return msg_answer
	else:
		print('Всё хорошо,сообщение собрано и отправлено,либо не найдено.')

if __name__ == '__main__':
	main()	
