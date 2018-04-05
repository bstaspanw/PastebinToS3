import requests
import time
import os
import csv
import sys

import os 
import boto
import boto.s3.connection
from boto.s3.key import Key

# Assume it is running on a platform with an IAM Role with appropriate permissions. Set region here. 
conn = boto.s3.connect_to_region('ap-southeast-2', calling_format = boto.s3.connection.OrdinaryCallingFormat())
pasteList = []

with open(os.getcwd() + '/log.csv', 'w') as csvfile:
	fieldnames = ['key', 'date', 'size', 'expire', 'title', 'syntax', 'user']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	while True:
		r = requests.get('https://pastebin.com/api_scraping.php')
		for paste in r.json():
			if paste['key'] in pasteList:
				pass
			else:
				pasteDirectory = os.getcwd() + '/pastes/'
				p = requests.get(paste['scrape_url'])
				pasteFile = open(pasteDirectory + '/' + paste['key'] +'.txt', "w")
				pasteFile.write(p.content)
				pasteFile.close()
				writer.writerow({'key':paste['key'],'date':paste['date'],'size':paste['size'],'expire':paste['expire'],'title':paste['title'].encode('utf-8').strip(),'syntax':paste['syntax'],'user':paste['user']})				
				bucket = conn.get_bucket('BUCKETNAME')
				key_name = paste['key'] +'.txt'
				k = bucket.new_key(key_name)
				k.set_contents_from_filename(pasteDirectory + '/' + paste['key'] +'.txt')
				pasteList.append(paste['key'])
		time.sleep(10)
