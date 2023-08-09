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
GRAFANA_DASHBOARDS_LOAD_PATH = os.getenv(r"GRAFANA_DASHBOARDS_LOAD_PATH")
DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS = eval(str(os.getenv(r"DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS")))

# --------------------------------------------------------------------
FOLDER_TITLE_NAME = str(os.getenv(r"FOLDER_TITLE_NAME"))

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

        logger.info("GRAFANA_DASHBOARDS_LOAD_PATH: " + str(GRAFANA_DASHBOARDS_LOAD_PATH))

        logger.info("DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS: " + str(DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS))
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

# get specific folder data
def grafana_get_specific_dashboard_folder_data_by_folder_title(folderTitle):
    logger.info("grafana_get_specific_dashboard_folder_data_by_folder_title() ...")
    try:
        foldersJsonStr = grafana_get_folder()
        foldersJsonList = json.loads(foldersJsonStr)
    
        # get specific folders data by title
        for folderJsonDic in foldersJsonList:
            if folderJsonDic["title"] == str(folderTitle):
                return folderJsonDic
        
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("grafana_get_specific_dashboard_folder_data_by_folder_title() finish")
    return 0

# delete specific folder by folderUid
def grafana_delete_specific_dashboard_folder_data_by_folderuid(folderUid):
    logger.info("grafana_delete_specific_dashboard_folder_data_by_folderuid() ...")
    try:
        payload = ''
        headers = {
            'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data=send_request("DELETE", "/api/folders/" + folderUid, payload, headers)
        #print(data.decode("utf-8"))
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("grafana_delete_specific_dashboard_folder_data_by_folderuid() finish")
    return data

# create grafana dashboard's folder
def create_grafana_dashboard_folder(folderJsonDic):
    logger.info("create_grafana_dashboard_folder(folderJsonDic) ...")
    try:
        payload = json.dumps(folderJsonDic)

        logger.debug("folderJsonStr: " + str(folderJsonDic))
        logger.debug("payload: " + payload)
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data = send_request("POST", "/api/folders", payload, headers)
        logger.info(data)
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("create_grafana_dashboard_folder(folderJsonDic) finish")
    return data

# create grafana dashboard
def create_grafana_dashboard(dashboardJsonDict):
    logger.info("create_grafana_dashboard(dashboardJsonDict) ...")
    try:
        payload = json.dumps(dashboardJsonDict)

        logger.debug("dashboardJsonDictStr: " + str(dashboardJsonDict))
        logger.debug("payload: " + payload)
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data = send_request("POST", "/api/dashboards/db", payload, headers)
        logger.info(data)
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("create_grafana_dashboard(dashboardJsonDict) finish")
    return data

# create grafana dashboard
def create_grafana_all_dashboard_in_folder(dashboardLoadPathStr, folderGrafanaJsonDic):
    logger.info("create_grafana_all_dashboard_in_folder(dashboardLoadPathStr, folderGrafanaJsonDic) ...")
    try:
        logger.info("dashboardLoadPathStr: " + dashboardLoadPathStr)
        dashboardList = [item for item in os.listdir(dashboardLoadPathStr) if os.path.isfile(os.path.join(dashboardLoadPathStr, item))]
        logger.debug("dashboardList: " + str(dashboardList))
        for dashboardName in dashboardList:
            logger.info("dashboardName: " + dashboardName)
            dashboardLoadPath = os.path.join(dashboardLoadPathStr, dashboardName)
            logger.info("dashboardLoadPath: " + dashboardLoadPath)
            
            with open(dashboardLoadPath, 'r', encoding='UTF-8') as f:
                dashboardJsonStr = str(f.read())
                #logger.debug("dashboardJsonStr: "+ dashboardJsonStr)
                dashboardJsonDict = json.loads(dashboardJsonStr)
                #logger.debug("dashboardJsonDict: " + str(dashboardJsonDict["meta"]))
            
            dashboardJsonDict["folderId"] = folderGrafanaJsonDic["id"]
            dashboardJsonDict["folderUid"] = folderGrafanaJsonDic["uid"]
            dashboardJsonDict["dashboard"]["id"] = None
            dashboardJsonDict["dashboard"]["uid"] = None
            dashboardJsonDict["meta"]["url"] = folderGrafanaJsonDic["url"]
            create_grafana_dashboard(dashboardJsonDict)
            
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("create_grafana_all_dashboard_in_folder(dashboardLoadPathStr, folderGrafanaJsonDic) finish")
    return 0

# create all grafana dashboards in specific folder
def create_specific_grafana_folder_dashboards(dashboardFolder):
    logger.info("create_specific_grafana_folder_dashboards(dashboardFolder) ...")
    try:
        logger.info("-------------------------------------")
        logger.info("dashboardFolder: " + dashboardFolder)
        
        # get grafana dashboard folder load path
        folderLoadPath = os.path.join(GRAFANA_DASHBOARDS_LOAD_PATH, dashboardFolder)
        logger.info("folderLoadPath: " + folderLoadPath)
        
        # get grafana dashboard folder json load path
        folderJsonLoadPath = os.path.join(folderLoadPath, "folder.json")
        logger.info("folderJsonLoadPath: " + folderJsonLoadPath)
        
        # read dashboard folder json and create dashboard folder and get folder return json data
        with open(folderJsonLoadPath, 'r', encoding='UTF-8') as f:
            folderJsonDic = eval(f.read())
            folderCreateReturnJsonDic = json.loads(create_grafana_dashboard_folder(folderJsonDic))
            logger.debug("folderCreateReturnJsonDic: " + str(folderCreateReturnJsonDic))
            logger.info("folder id: " + str(folderCreateReturnJsonDic["id"]))
            logger.info("folder title: " + str(folderCreateReturnJsonDic["title"]))
            logger.info("folder uid: " + str(folderCreateReturnJsonDic["uid"]))
            logger.info("folder url: " + str(folderCreateReturnJsonDic["url"]))
            
            dashboardsLoadPath = os.path.join(folderLoadPath, "dashboards")
            create_grafana_all_dashboard_in_folder(dashboardsLoadPath, folderCreateReturnJsonDic)
            
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("create_specific_grafana_folder_dashboards(dashboardFolder) finish")
    return 0

# restore all grafana dashboards from local grafana files
def restore_specific_grafana_dashboards_by_foldertitle(folderTitle):
    logger.info("restore_specific_grafana_dashboards_by_foldertitle(folderTitle) ...")
    try:
        logger.info("=====================================")
        if DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS:
            folderUid = str(grafana_get_specific_dashboard_folder_data_by_folder_title(folderTitle)["uid"])
            grafana_delete_specific_dashboard_folder_data_by_folderuid(folderUid)
        create_specific_grafana_folder_dashboards(folderTitle)
        logger.info("=====================================")
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("restore_specific_grafana_dashboards_by_foldertitle(folderTitle) finish")
    return 0

# ====================================================================


def main(argc, argv, envp):
    
    restore_specific_grafana_dashboards_by_foldertitle(FOLDER_TITLE_NAME)
    
    return 0



if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))