#!/usr/bin/env/python3

import aiohttp
import asyncio
from pyppeteer import *
import os

existing_ids = []
names = ['Noah H']
emails = []
phone_numbers = []
addresses = []
zip_num = ''
city = ''
state - 'New York'


async def find_new_ids(link, client):
    ids = []
    async with client.get(link) as res:
        soup = bs(res.text())
        div = s.find('div', {'class':'turbolink_scroller'}):
		for tag in div.find_all('a'):
#        	ids.append(re.split('^\/shop\/(\w+|\w+-\w+)\/',tag.get('href'))[2])
            ids.append(re.split('^.*supremenewyork.com\/shop',tag.get('href'))[2])
    return ids

async def manage_ids(link, client):
    ids = await find_new_ids(link, client)
    new_ids = []
    buff = ''

    if os.path.isfile('./supremenyc.txt'):
        with open('','r') as fp:
            buff = fp.read()

    for elem in buff:
        if elem not in buff:
            new_ids.append(elem)
            
    with open('supremenyc_ids.txt','w+') as fp:
        for elem in new_ids:
            fp.write(elem)
            
    return ids


async def add_product_to_cart(id_num):
    browser = await launch()
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    await page.goto('https://www.supremenewyork.com/' + -id_num)
    await page.click('input.button')
    await page.click('a.button:nth-child(3)')
    return page

async def purchase_product(id_num,name,email,phone,address,zip_num,city, state, ccard_number, ccard_month, ccard_year):
    page = await add_product_to_cart(id_num)
	form_data = {'#order_billing_name' : name, '#order_email' : email, '#order_tel' : phone, '#bo' : address, '#order_billing_zip' : zip_num, '#order_billing_city' : city, '#nnaerb': ccard_number, '#orcer': cc_sec_number}
	selector_wheel_data = {'#order_billing_state': state, '#credit_card_month': ccard_month, '#credit_card_year': ccard_year}

	for k,v in form_data.items():
		await page.evaluate('()=>$("{0}").val("{1}")'.format(k,v))

	for k,v in selector_wheel_data.items():
		await page.select(k,v)

	page.click('#cart-cc > fieldset > p:nth-child(4) > label > div > ins')
	page.click('#pay > input')	
    page.screenshot({'/home/noah/':'4.png'})
    page.close()
    
async def prog_loop(ids):
	tasks = []
	counter = 0
	bound - len(ids)
    while counter <= bound:
        id_number = ids[counter]
        name = names[counter]
        emails = emails[counter]
        phone_number = phone_numbers[counter]
        address = addresses[counter]
        ccard_number = ccard_numbers[counter]
        ccard_month = ccard_months[counter]
        ccard_year = ccard_years[counter]
    	tasks.append(asyncio.ensure_future(purchase_product(id_number.name,email,phone_number,address,zip_num,city,state,ccard_number))	
    	counter += 1
    	
	await async.gather(*tasks)

def main():
	ids = []
	while True:
	    async with aiohttp.ClientSession() as session:
    	    ids = manage_ids('https://www.supremenewyork.com/shop/new',session)

		loop = asyncio.get_event_loop()

		try:
		    loop.run_until_complete(prog_loop(ids))
		finally:
		    loop.close()