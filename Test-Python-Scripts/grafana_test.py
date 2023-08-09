# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:54:45 2023

@author: user
"""

import sys,os
import logging

logging.basicConfig()
logger = logging.getLogger()
#logger.setLevel(logging.NOTSET)
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

import json

# --------------------------------------------------------------------
GRAFANA_IP = str(os.getenv(r"GRAFANA_IP"))
GRAFANA_PORT = int(str(os.getenv(r"GRAFANA_PORT")))
GRAFANA_BEARER = str(os.getenv(r"GRAFANA_BEARER"))
GRAFANA_ISHTTPS = eval(str(os.getenv(r"GRAFANA_ISHTTPS")))

# --------------------------------------------------------------------
GRAFANA_DASHBOARDS_SAVE_PATH = os.getenv(r"GRAFANA_DASHBOARDS_SAVE_PATH")
GRAFANA_DASHBOARDS_LOAD_PATH = os.getenv(r"GRAFANA_DASHBOARDS_LOAD_PATH")
IGNORE_DASHBOARD_FOLDER_IS_EXISTS = eval(str(os.getenv(r"IGNORE_DASHBOARD_FOLDER_IS_EXISTS")))
DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS = eval(str(os.getenv(r"DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS")))

# --------------------------------------------------------------------
IGNORE_DATASOURCE_FOLDER_IS_EXISTS = eval(str(os.getenv(r"IGNORE_DATASOURCE_FOLDER_IS_EXISTS")))
GRAFANA_DATASOURCE_SAVE_PATH = os.getenv(r"GRAFANA_DATASOURCE_SAVE_PATH")
GRAFANA_DATASOURCE_LOAD_PATH = os.getenv(r"GRAFANA_DATASOURCE_LOAD_PATH")

DELETE_CURRENT_ALL_GRAFANA_DATASOURCE = eval(str(os.getenv(r"DELETE_CURRENT_ALL_GRAFANA_DATASOURCE")))

# --------------------------------------------------------------------
# Not finished yet, not sure if this is needed.
IGNORE_GENERAL_FOLDER = True
#IGNORE_GENERAL_FOLDER = eval(str(os.getenv(r"IGNORE_GENERAL_FOLDER")))

# used to do some init jobs and show info
def init_env():
    import http.client
    logger.info("init_env() ...")
    try:
        logger.info("GRAFANA_IP: " + str(GRAFANA_IP))
        logger.info("GRAFANA_PORT: " + str(GRAFANA_PORT))
        logger.info("GRAFANA_BEARER: " + "**************")
        logger.info("GRAFANA_ISHTTPS: " + str(GRAFANA_ISHTTPS))

        logger.info("GRAFANA_DASHBOARDS_SAVE_PATH: " + str(GRAFANA_DASHBOARDS_SAVE_PATH))
        logger.info("GRAFANA_DASHBOARDS_LOAD_PATH: " + str(GRAFANA_DASHBOARDS_LOAD_PATH))

        logger.info("IGNORE_DASHBOARD_FOLDER_IS_EXISTS: " + str(IGNORE_DASHBOARD_FOLDER_IS_EXISTS))

        logger.info("DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS: " + str(DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS))
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("init_env() finish")
    return 0

# copy this data = send_request()
# used to send request
def send_request(method,uri,payload,headers):
    import http.client
    import ssl
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
    import http.client
    import ssl
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

# get all grafana dashboards list
def grafana_get_all_dashboard_data():
    import http.client
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

# get all folder data
def grafana_get_all_dashboard_folder_data():
    import http.client
    logger.info("grafana_get_all_dashboard_folder_data() ...")
    try:
        payload = ''
        headers = {
            'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data=send_request("GET", "/api/search?type=dash-folder", payload, headers)
        #print(data.decode("utf-8"))
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("grafana_get_all_dashboard_folder_data() finish")
    return data

# delete specific folder by folderUid
def grafana_delete_specific_dashboard_folder_data_by_folderuid(folderUid):
    import http.client
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

# get specific folder data
def grafana_get_specific_dashboard_folder_data_by_folder_title(folderTitle):
    import http.client
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

# get specific dashboard json with dashboard uid
def grafana_get_dashboard_json(dashboard_uid):
    import http.client
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

# Get all grafana dashboard json
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

# create grafana dashboard
def create_grafana_dashboard(dashboardJsonDict):
    import http.client
    import json
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

# create grafana dashboard's folder
def create_grafana_dashboard_folder(folderJsonDic):
    import http.client
    import json
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

# delete grafana dashboard's folder
def delete_grafana_dashboard_folder(folderUid):
    import http.client
    import json
    logger.info("delete_grafana_dashboard_folder(folderUid) ...")
    try:
        logger.info("delete_grafana_dashboard_folder delete folder folderUid " + folderUid + " ...")
        payload = ''

        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + GRAFANA_BEARER
        }
        data = send_request("DELETE", "/api/folders/" + folderUid, payload, headers)
        logger.info(data)
        logger.info("delete_grafana_dashboard_folder delete folder folderUid " + folderUid + " finish")
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("delete_grafana_dashboard_folder(folderUid) finish")
    return data

# create all grafana dashboards
def create_grafana_dashboards():
    logger.info("create_grafana_dashboards() ...")
    try:
        dashboardFoldersList = [item for item in os.listdir(GRAFANA_DASHBOARDS_LOAD_PATH) if os.path.isdir(os.path.join(GRAFANA_DASHBOARDS_LOAD_PATH, item))]
        for dashboardFolder in dashboardFoldersList:
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
                logger.debug("folderJsonDic: " + str(folderJsonDic))
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
    logger.info("create_grafana_dashboards() finish")
    return 0

# delete all grafana dashboards and folders
def delete_all_grafana_dashboards():
    logger.info("delete_all_grafana_dashboards() ...")
    dashboardFoldersInfoJsonStr = grafana_get_all_dashboard_folder_data()
    dashboardFoldersInfoJsonList = json.loads(dashboardFoldersInfoJsonStr)
    for dashboardFoldersInfoJson in dashboardFoldersInfoJsonList:
        logger.info("dashboardFoldersInfoJson: " + str(dashboardFoldersInfoJson))
        delete_grafana_dashboard_folder(str(dashboardFoldersInfoJson["uid"]))
    logger.info("delete_all_grafana_dashboards() finish")
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
def restore_grafana_dashboards():
    logger.info("restore_grafana_dashboards() ...")
    try:
        logger.info("=====================================")
        if DELETE_CURRENT_ALL_GRAFANA_DASHBOARDS:
            delete_all_grafana_dashboards()
        create_grafana_dashboards()
        logger.info("=====================================")
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("restore_grafana_dashboards() finish")
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

# get all grafana dashboards list by folderId
def grafana_get_all_dashboard_data_by_folderId(folderId):
    import http.client
    logger.info("grafana_get_all_dashboard_data_by_folderId(folderId) ...")
    try:
        payload = ''
        headers = {
            'Authorization': 'Bearer ' + GRAFANA_BEARER
        }

        data = send_request("GET", "/api/search?type=dash-db&folderIds=" + str(folderId), payload, headers)
    except Exception as e:
        logger.debug(e, stack_info=True, exc_info=True)
        logger.error(e)
    logger.info("grafana_get_all_dashboard_data_by_folderId(folderId) finish")
    return data

# backup grafana all dashboards to local
def backup_specific_grafana_dashboards_by_foldertitle(folderTitle):
    logger.info("backup_specific_grafana_dashboards_by_foldertitle(folderTitle) ...")
    get_and_create_grafana_dashboards_folder_by_foldertitle(folderTitle)

    folderId = str(grafana_get_specific_dashboard_folder_data_by_folder_title(folderTitle)["id"])
    #download_grafana_dashboards()
    download_grafana_dashboards_by_folderId(folderId)
    logger.info("backup_specific_grafana_dashboards_by_foldertitle(folderTitle) finish")
    return 0


# get and create specific grafana dash-folder by folderTitle
def get_and_create_grafana_dashboards_folder_by_foldertitle(folderTitle):
    logger.info("get_and_create_grafana_dashboards_folder_by_foldertitle(folderTitle) ...")
    
    foldersJsonStr = grafana_get_folder()
    
    logger.info("restore_grafana_dashboards() ...")
    try:
        folderJsonDict = grafana_get_specific_dashboard_folder_data_by_folder_title(folderTitle)
        folderCreatePath = os.path.join(GRAFANA_DASHBOARDS_SAVE_PATH, str(folderTitle))
        logger.info("-------------------------------------")
        logger.debug("folder Json: " + str(folderJsonDict))
        logger.info("folder title: " + str(folderTitle))
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
    logger.info("get_and_create_grafana_dashboards_folder_by_foldertitle(folderTitle) finish")
    return 0

# Get all grafana dashboard json in specific folder (Progressing)
def download_grafana_dashboards_by_folderId(folderId):
    logger.info("download_grafana_dashboards_by_folderId(folderId) ...")
    dashboardsInfoJsonStr = grafana_get_all_dashboard_data_by_folderId(folderId)
    dashboardsInfoJsonList = json.loads(dashboardsInfoJsonStr)
    for dashboardInfoJson in dashboardsInfoJsonList:
        try:
            logger.info("-------------------------------------")
            logger.debug("dashboard Json: " + str(dashboardInfoJson))
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
    logger.info("download_grafana_dashboards_by_folderId(folderId) finish")
    return 0


# ====================================================================

# get grafana datasource list
def grafana_get_datasource():
    import http.client
    import ssl
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

# create grafana dashboard
def create_grafana_datasource(datasourceJsonDic):
    import http.client
    import json
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

# delete grafana datasource
def delete_grafana_datasource(datasourceUid):
    import http.client
    import json
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
    
    #backup_grafana_dashboards()
    restore_grafana_dashboards()
    
    #backup_specific_grafana_dashboards_by_foldertitle("DEV")
    #restore_specific_grafana_dashboards_by_foldertitle("DEV")
    
    #restore_specific_grafana_dashboards_by_foldertitle("PROD")
    
    
    #backup_grafana_datasource()
    restore_grafana_datasource()
    
    return 0



if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))