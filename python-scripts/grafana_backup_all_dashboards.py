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
GRAFANA_DASHBOARDS_SAVE_PATH = os.getenv(r"GRAFANA_DASHBOARDS_SAVE_PATH")
IGNORE_DASHBOARD_FOLDER_IS_EXISTS = eval(str(os.getenv(r"IGNORE_DASHBOARD_FOLDER_IS_EXISTS")))

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

        logger.info("GRAFANA_DASHBOARDS_SAVE_PATH: " + str(GRAFANA_DASHBOARDS_SAVE_PATH))

        logger.info("IGNORE_DASHBOARD_FOLDER_IS_EXISTS: " + str(IGNORE_DASHBOARD_FOLDER_IS_EXISTS))

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

# get grafana dashboard's folders list
def grafana_get_folder():
    logger.info("grafana_get_folder() ...")
    try:
        payload = ''
        headers = {
            'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data=send_request("GET", "/api/folders", payload, headers)
        #print(data.decode("utf-8"))
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("grafana_get_folder() finish")
    return data

# create local folder which is used to save grafana dashboard json
def get_and_create_grafana_dashboards_folder():
    logger.info("get_and_create_grafana_dashboards_folder() ...")
    
    foldersJsonStr = grafana_get_folder()
    foldersJsonList = json.loads(foldersJsonStr)
    
    # get all folders data
    for folderJsonDict in foldersJsonList:
        try:
            folderCreatePath = os.path.join(GRAFANA_DASHBOARDS_SAVE_PATH, str(folderJsonDict["title"]))
            logger.info("-------------------------------------")
            logger.debug("folder Json: " + str(folderJsonDict))
            logger.info("folder title: " + str(folderJsonDict["title"]))
            logger.info("folder uid: " + str(folderJsonDict["uid"]))
            logger.info("folder id: " + str(folderJsonDict["id"]))
            
            # create folder
            logger.info("create folder " + folderCreatePath + " ...")
            os.makedirs(folderCreatePath, exist_ok=IGNORE_DASHBOARD_FOLDER_IS_EXISTS)
            logger.info("create folder " + folderCreatePath + " finish")
        
        
            folderJsonSavePath = os.path.join(folderCreatePath, "folder.json")
            # get and create folder json
            logger.info("save folder json " + folderJsonSavePath + " ...")
            with open(folderJsonSavePath, 'w+', encoding='UTF-8') as f:
                f.write(str(folderJsonDict))
            logger.info("save folder json " + folderJsonSavePath + " finish")
        except FileNotFoundError:
            logger.info("The 'docs' directory does not exist")
        except Exception as e:
            logger.debug(e, stack_info=True, exc_info=True)
            logger.error(e)
    logger.info("get_and_create_grafana_dashboards_folder() finish")
    return 0

# get all grafana dashboards list
def grafana_get_all_dashboard_data():
    logger.info("grafana_get_all_dashboard_data() ...")
    try:
        payload = ''
        headers = {
            'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data = send_request("GET", "/api/search?type=dash-db", payload, headers)
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("grafana_get_all_dashboard_data() finish")
    return data

# get specific dashboard json with dashboard uid
def grafana_get_dashboard_json(dashboard_uid):
    logger.info("grafana_get_dashboard_json(dashboard_uid) ...")
    try:
        payload = ''
        headers = {
          'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data=send_request("GET", "/api/dashboards/uid/" + dashboard_uid, payload, headers)
        #print(data.decode("utf-8"))
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("grafana_get_dashboard_json(dashboard_uid) finish")
    return data

def download_grafana_dashboards():
    logger.info("download_grafana_dashboards() ...")
    dashboardsInfoJsonStr = grafana_get_all_dashboard_data()
    dashboardsInfoJsonList = json.loads(dashboardsInfoJsonStr)
    logger.info("dashboardsInfoJsonStr: " + dashboardsInfoJsonStr)
    for dashboardInfoJson in dashboardsInfoJsonList:
        try:
            logger.info("-------------------------------------")
            logger.debug("dashboard Json: " + str(dashboardInfoJson))

            # is default dash-folder
            if dashboardInfoJson.get("folderId") is None:
                if IGNORE_GENERAL_FOLDER:
                    continue
                else:
                    logger.info("dashboard title: " + str(dashboardInfoJson["title"]))
                    logger.info("dashboard uid: " + str(dashboardInfoJson["uid"]))
                    logger.info("dashboard id: " + str(dashboardInfoJson["id"]))
                    
                    folderCreatePath = os.path.join(GRAFANA_DASHBOARDS_SAVE_PATH, "General")
                    dashboardSaveDirPath = os.path.join(folderCreatePath, "dashboards")
                
            # not default dash-folder
            else:
                logger.info("dashboard folderTitle: " + str(dashboardInfoJson["folderTitle"]))
                logger.info("dashboard folderId: " + str(dashboardInfoJson["folderId"]))
                logger.info("dashboard folderUid: " + str(dashboardInfoJson["folderUid"]))
                logger.info("dashboard title: " + str(dashboardInfoJson["title"]))
                logger.info("dashboard uid: " + str(dashboardInfoJson["uid"]))
                logger.info("dashboard id: " + str(dashboardInfoJson["id"]))
                
                folderCreatePath = os.path.join(GRAFANA_DASHBOARDS_SAVE_PATH, str(dashboardInfoJson["folderTitle"]))
                dashboardSaveDirPath = os.path.join(folderCreatePath, "dashboards")
    
            # create dashboard folder
            if not os.path.exists(dashboardSaveDirPath):
                logger.info("create dashboard folder " + folderCreatePath + " ...")
                os.makedirs(dashboardSaveDirPath, exist_ok=IGNORE_DASHBOARD_FOLDER_IS_EXISTS)
                logger.info("create dashboard folder " + folderCreatePath + " finish")
            dashboardJsonSavePath = os.path.join(dashboardSaveDirPath, str(dashboardInfoJson["title"]))
            
            dashboardJsonStr = grafana_get_dashboard_json(str(dashboardInfoJson["uid"]))
            
            logger.info("save dashboard json " + dashboardJsonSavePath + " ...")
            with open(dashboardJsonSavePath, 'w+', encoding='UTF-8') as f:
                f.write(str(dashboardJsonStr))
            logger.info("save folder json " + dashboardJsonSavePath + " finish")

        except FileNotFoundError:
            logger.info("The 'docs' directory does not exist")
        except Exception as e:
            logger.debug(e, stack_info=True, exc_info=True)
            logger.error(e)
    logger.info("download_grafana_dashboards() finish")
    return 0

# backup grafana all dashboards to local
def backup_grafana_dashboards():
    logger.info("backup_grafana_dashboards() ...")
    get_and_create_grafana_dashboards_folder()
    download_grafana_dashboards()
    logger.info("backup_grafana_dashboards() finish")
    return 0

# ====================================================================

def main(argc, argv, envp):
    
    backup_grafana_dashboards()
    
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))