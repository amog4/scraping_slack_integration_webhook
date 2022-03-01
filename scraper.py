# import necessary packages 
import os, sys
from urllib import response
import requests
import logging
from bs4 import BeautifulSoup
import json
import datetime

slack_hook = os.environ.get("SLACK_HOOK_DEMO")

logging.basicConfig(filename='hotshop.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logging.info('start of the script')
word_list = list()
d_now = datetime.datetime.now()
datetime_now = str(datetime.datetime.strftime(d_now , "%Y_%m_%d_%H_%M_%S"))


try:
    response = requests.get(url = 'https://www.tradezero.co/hotshorts')


    if response.status_code == 200:
        logging.info(response.headers)
        get_html = response.text
        soup = BeautifulSoup(get_html, 'html.parser')
        anchor_list = soup.findAll("a",{"class":"anchor"})
        for index in range(0,len(anchor_list)):
            anchor = anchor_list[index]
            word_list.append(anchor.text)
        wl = ''.join(word_list)
        word_dict = {index:str(a)for index,a in enumerate(word_list)}

        with open(f'hotshot_{datetime_now }.json', 'w', encoding ='utf8') as json_file:
            json.dump(word_dict, json_file, ensure_ascii = False)

        wl = ''.join(word_list)
        # slack access bot token
        slack_url = "https://hooks.slack.com/services/" + str(slack_hook)   
        headers = {"Content-type": "application/json"}
        slack_response = requests.post(url = slack_url,
                                     data=   json.dumps(word_dict )
                                     headers=headers
                                    
                                )

        if slack_response.status_code != 200:
            raise Exception(slack_response.status_code)
    else:
        logging.info(response.status_code)
        raise Exception (response.status_code)

    

except Exception as error:
    logging.exception(str(error))

finally:
    logging.info('end of the script')