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
GRAFANA_DATASOURCE_LOAD_PATH = os.getenv(r"GRAFANA_DATASOURCE_LOAD_PATH")

DELETE_CURRENT_ALL_GRAFANA_DATASOURCE = eval(str(os.getenv(r"DELETE_CURRENT_ALL_GRAFANA_DATASOURCE")))

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

# delete grafana datasource
def delete_grafana_datasource(datasourceUid):
    logger.info("delete_grafana_dashboard_folder(datasourceUid) ...")
    try:
        logger.info("delete_grafana_dashboard_folder delete folder datasourceUid " + datasourceUid + " ...")
        payload = ''

        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data = send_request("DELETE", "/api/datasources/uid/" + datasourceUid, payload, headers)
        logger.info(data)
        logger.info("delete_grafana_dashboard_folder delete folder datasourceUid " + datasourceUid + " finish")
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("delete_grafana_dashboard_folder(datasourceUid) finish")
    return data

# delete all grafana datasource
def delete_all_grafana_datasource():
    logger.info("delete_all_grafana_datasource() ...")
    datasourceInfoJsonStr = grafana_get_datasource()
    datasourceInfoJsonList = json.loads(datasourceInfoJsonStr)
    for datasourceInfoJsonDict in datasourceInfoJsonList:
        logger.info("datasourceInfoJson: " + str(datasourceInfoJsonDict))
        delete_grafana_datasource(str(datasourceInfoJsonDict["uid"]))
    logger.info("delete_all_grafana_datasource() finish")
    return 0

# create grafana dashboard
def create_grafana_datasource(datasourceJsonDic):
    logger.info("create_grafana_datasource_folder(datasourceJsonDic) ...")
    try:
        payload = json.dumps(datasourceJsonDic)

        logger.debug("datasourceJsonStr: " + str(datasourceJsonDic))
        logger.debug("payload: " + payload)
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data = send_request("POST", "/api/datasources", payload, headers)
        logger.info(data)
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("create_grafana_datasource_folder(datasourceJsonDic) finish")
    return data

# create all grafana datasources
def create_all_grafana_datasources():
    logger.info("create_all_grafana_datasources() ...")
    try:
        datasourcesList = [item for item in os.listdir(GRAFANA_DATASOURCE_LOAD_PATH) if os.path.isfile(os.path.join(GRAFANA_DATASOURCE_LOAD_PATH, item))]
        logger.info("datasourcesList: " + str(datasourcesList))
        for datasourceName in datasourcesList:
            logger.info("-------------------------------------")
            logger.info("datasourceName: " + datasourceName)
            
            # get grafana dashboard folder load path
            datasourceJsonLoadPath = os.path.join(GRAFANA_DATASOURCE_LOAD_PATH, datasourceName)
            logger.info("datasourceJsonLoadPath: " + datasourceJsonLoadPath)

            
            # read dashboard folder json and create dashboard folder and get folder return json data
            with open(datasourceJsonLoadPath, 'r', encoding='UTF-8') as f:
                datasourceJsonDic = eval(f.read())
                logger.debug("datasourceJsonDic: " + str(datasourceJsonDic))
                logger.info("create datasource: " + datasourceName + " ...")
                create_grafana_datasource(datasourceJsonDic)
                logger.info("create datasource: " + datasourceName + " finish")
            
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("create_all_grafana_datasources() finish")
    return 0

# restore grafana all datasource from local
def restore_grafana_datasource():
    logger.info("restore_grafana_datasource() ...")
    try:
        logger.info("=====================================")
        if DELETE_CURRENT_ALL_GRAFANA_DATASOURCE:
            delete_all_grafana_datasource()
        create_all_grafana_datasources()
        logger.info("=====================================")
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("restore_grafana_datasource() finish")
    return 0

# ====================================================================


def main(argc, argv, envp):
    
    restore_grafana_datasource()
    
    return 0



if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))