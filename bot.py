#!/usr/bin/env/python3

import aiohttp
import asyncio
import pyppeteer
from pyppeteer import *
from bs4 import BeautifulSoup as bs
import os
import re

pyppeteer.DEBUG = True
names = ['Noah H']
emails = ['test@gmail.com']
phone_numbers = ['631-222-3234']
addresses = ['345 Test rd']
ccard_numbers = ['TEST']
ccard_sec_numbers = ['456']
ccard_months = ['03']
ccard_years = ['2023']
zip_num = '11943'
city = 'Bowery'
state = 'New York'


async def find_new_ids(link, client):
	ids = []
	async with client.get(link) as res:
		soup = bs(await res.text())
		for div in soup.find('div', {'class':'turbolink_scroller'}):
			for tag in div.find_all('a'):
				ids.append(re.split('^.*supremenewyork.com\/shop',tag.get('href'))[0])
	return ids

async def manage_ids(link, client):
	ids = await find_new_ids(link, client)
	new_ids = []
	buff = []

	if os.path.isfile('./supremenyc.txt'):
		with open('','r') as fp:
			buff = fp.readlines()

	for elem in ids:
		if elem not in buff:
			new_ids.append(elem)

	with open('supremenyc_ids.txt','w+') as fp:
		for elem in new_ids:
			fp.write(elem)
			fp.write('\n')

	return ids


async def add_product_to_cart(id_num):
	browser = await launch(headless=False)
	context = await browser.createIncognitoBrowserContext()
	page = await context.newPage()
	await page.goto('https://www.supremenewyork.com/shop/' + id_num)
	await page.click('input.button')
#	await page.waitForSelector('a.button:nth-child(3)')
	await asyncio.wait([page.click('a.button:nth-child(3)'),page.waitForNavigation()])
	return page

async def purchase_product(id_num,name,email,phone,address,zip_num,city, state, ccard_number, ccard_sec, ccard_month, ccard_year):
	page = await add_product_to_cart(id_num)

	form_data = {'#order_billing_name' : name, '#order_email' : email, '#order_tel' : phone, '#bo' : address, '#order_billing_zip' : zip_num, '#order_billing_city' : city, '#nnaerb': ccard_number, '#orcer': ccard_sec}
	selector_wheel_data = {'#order_billing_state': state, '#credit_card_month': ccard_month, '#credit_card_year': ccard_year}

	for k,v in form_data.items():
		await page.evaluate('()=>$("{0}").val("{1}")'.format(k,v))

#	for k,v in selector_wheel_data.items():
#		await page.select(k,v)

#	page.click('#cart-cc > fieldset > p:nth-child(4) > label > div > ins')
#	page.click('#pay > input')
#	await page.screenshot({'/home/noah/':'4.png'})
	await page.close()

async def prog_loop(ids):
	tasks = []
	ids = ['tops-sweaters/oh4txezw5/pw6q40ltk']

#	async with aiohttp.ClientSession() as session:
#		ids = await manage_ids('https://supremenewyork.com/shop/new',session)

	for id_num in ids:
		for name, email, phone, address, ccard_num, ccard_sec, ccard_mon, ccard_year in zip(names,emails,phone_numbers,addresses,ccard_numbers,ccard_sec_numbers,ccard_months,ccard_years):
			tasks.append(asyncio.ensure_future(purchase_product(id_num,name,email,phone,address,zip_num,city,state,ccard_num,ccard_sec,ccard_mon,ccard_year)))

	await asyncio.gather(*tasks)

def main():
	ids = []
	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(prog_loop(ids))
	finally:
		loop.close()

main()
