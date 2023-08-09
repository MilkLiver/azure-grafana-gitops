# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:54:45 2023

@author: user
"""

import sys,os
import logging
import http.client
import ssl
import json

logging.basicConfig()
logger = logging.getLogger()
#logger.setLevel(logging.NOTSET)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

# --------------------------------------------------------------------
GRAFANA_IP = str(os.getenv(r"GRAFANA_IP"))
GRAFANA_PORT = int(str(os.getenv(r"GRAFANA_PORT")))
GRAFANA_BEARER = str(os.getenv(r"GRAFANA_BEARER"))
GRAFANA_ISHTTPS = eval(str(os.getenv(r"GRAFANA_ISHTTPS")))

# --------------------------------------------------------------------
IGNORE_DATASOURCE_FOLDER_IS_EXISTS = eval(str(os.getenv(r"IGNORE_DATASOURCE_FOLDER_IS_EXISTS")))
GRAFANA_DATASOURCE_SAVE_PATH = os.getenv(r"GRAFANA_DATASOURCE_SAVE_PATH")

# --------------------------------------------------------------------
# Not finished yet, not sure if this is needed.
IGNORE_GENERAL_FOLDER = True
#IGNORE_GENERAL_FOLDER = eval(str(os.getenv(r"IGNORE_GENERAL_FOLDER")))

# used to do some init jobs and show info
def init_env():
    logger.info("init_env() ...")
    try:
        logger.info("GRAFANA_IP: " + str(GRAFANA_IP))
        logger.info("GRAFANA_PORT: " + str(GRAFANA_PORT))
        logger.info("GRAFANA_BEARER: " + "**************")
        logger.info("GRAFANA_ISHTTPS: " + str(GRAFANA_ISHTTPS))

    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("init_env() finish")
    return 0

# copy this data = send_request()
# used to send request
def send_request(method,uri,payload,headers):
    logger.info("send_request() ...")
    try:
        if GRAFANA_ISHTTPS:
            conn = http.client.HTTPSConnection(GRAFANA_IP, GRAFANA_PORT, context = ssl._create_unverified_context())
        else:
            conn = http.client.HTTPConnection(GRAFANA_IP, GRAFANA_PORT)
        logger.debug("method: " + str(method))
        logger.debug("uri: " + str(uri))
        logger.debug("payload: " + str(payload))
        logger.debug("headers: " + str(headers))
        conn.request(str(method), str(uri), payload, headers)
        res = conn.getresponse()
        data = res.read()
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("send_request() finish")
    return data.decode("utf-8")

# get grafana datasource list
def grafana_get_datasource():
    logger.info("grafana_get_datasource() ...")
    try:
        payload = ''
        headers = {
            'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data=send_request("GET", "/api/datasources", payload, headers)
        
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("grafana_get_datasource() finish")
    return data

def get_and_create_grafana_datasource():
    logger.info("get_and_create_grafana_datasource() ...")
    
    datasourceJsonStr = grafana_get_datasource()
    datasourceJsonList = json.loads(datasourceJsonStr)
    
    logger.info("create save datasource folder " + GRAFANA_DATASOURCE_SAVE_PATH + " ...")
    os.makedirs(GRAFANA_DATASOURCE_SAVE_PATH, exist_ok=IGNORE_DATASOURCE_FOLDER_IS_EXISTS)
    logger.info("create save datasource folder " + GRAFANA_DATASOURCE_SAVE_PATH + " finish")
    
    # get all datasource data
    for datasourceJsonDict in datasourceJsonList:
        try:
            logger.info("-------------------------------------")
            logger.debug("datasource Json: " + str(datasourceJsonDict))
            
            logger.info("datasource title: " + str(datasourceJsonDict["name"]))
            logger.info("datasource uid: " + str(datasourceJsonDict["uid"]))
            logger.info("datasource id: " + str(datasourceJsonDict["type"]))
        
        
            datasourceJsonSavePath = os.path.join(GRAFANA_DATASOURCE_SAVE_PATH, str(datasourceJsonDict["name"]))    
            # get and create folder json
            logger.info("save datasource json " + datasourceJsonSavePath + " ...")
            with open(datasourceJsonSavePath, 'w+', encoding='UTF-8') as f:
                f.write(str(datasourceJsonDict))
            logger.info("save datasource json " + datasourceJsonSavePath + " finish")
        except FileNotFoundError:
            logger.info("The 'docs' directory does not exist")
        except Exception as e:
            logger.debug(e, stack_info=True, exc_info=True)
            logger.error(e)
    logger.info("get_and_create_grafana_datasource() finish")
    return 0

# backup grafana all datasource to local
def backup_grafana_datasource():
    logger.info("backup_grafana_datasource() ...")
    get_and_create_grafana_datasource()
    logger.info("backup_grafana_datasource() finish")
    return 0

# ====================================================================


def main(argc, argv, envp):
    
    backup_grafana_datasource()
    
    return 0



if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))