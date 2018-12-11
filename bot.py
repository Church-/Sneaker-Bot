#!/usr/bin/env/python3

import aiohttp
import asyncio
from pyppeteer import *
import os

existing_ids = []
names = []
emails = []
phone_numbers = []
addresses = []
zip = ''
city = ''



async def find_new_ids(link, client):
    ids = []
    async with client.get(link) as res:
        soup = bs(res.text())
        div = s.find('div', {'class':'turbolink_scroller'}):
		for tag in div.find_all('a'):
        	ids.append(re.split('^\/shop\/(\w+|\w+-\w+)\/',tag.get('href'))[2])
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


async def add_product_to_cart(id):
    browser = await launch()
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    await page.goto('https://www.supremenewyork.com/' + link)
    await page.click('input.button')
    await page.click('a.button:nth-child(3)')
    return page

async def purchase_product(id,name,email,phone,address,zip,city):
    page = await add_product_to_cart(id)
	form_data = {'#order_billing_name' : name, '' : email, '' : phone, '' : address, '' : zip, '' : city }
	selector_wheel_data = {}
	
	for k,v in form_data.items():
		await page.evaluate('()=>$("{0}").val("{1}")'.format(k,v))

	for k,v in selector_wheel_data.items():
		page.select()

	page.click('#cart-cc > fieldset > p:nth-child(4) > label > div > ins')
	page.click('#pay > input')	
    page.close()
    
async def prog_loop(ids):
	tasks = []
	
	for i in ids:
		tasks.append(asyncio.ensure_future(i))	

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