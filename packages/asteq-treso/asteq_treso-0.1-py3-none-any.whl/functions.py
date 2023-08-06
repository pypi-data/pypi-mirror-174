import excel
import operations
import json

# ---------------------------------------------------------------- FUNCTIONS ----------------------------------------------------------------
def equals(json1,json2,keys_to_compare):
    for key in keys_to_compare:
        if not(key in json1 and key in json2):
            return False
        if (json1[key] != json2[key]):
            return False
    return True

def removeFromFirstPresenceArray(element,array_json_target,keys_to_compare:list[str],inOrder=True):
    for i,json_obj in enumerate(array_json_target) :
        if equals(json_obj,element,keys_to_compare):
            return array_json_target[i+1:]
    return array_json_target

def createDefaultFiles(filename_excel, sheet_name):
    excel.createExcelIfNotExisting(filename_excel)
    excel.createSheetIfNotExisting(filename_excel,sheet_name)
# ---------------------------------------------------------------- MAIN ----------------------------------------------------------------

def main_function(filename_excel, sheet_name):
    # Ordre
    # 1 : Fetch excel vers JSON
    # 2 : Fetch web vers JSON
    # 3 : Ajuster web en fonction de plus récent excel
    # 4 : Ajouter à excel web ajusté
    
    # 1
    excel_json_str = excel.excelToJson(filename_excel, sheet_name)
    excel_json = json.loads(excel_json_str)
    print("JSON generated from xlsx file")

    # 2
    web_json_str = operations.fetchOperationsToJson()
    web_json = json.loads(web_json_str)
    print("JSON generated from web Société Générale")

    # 3
    if len(excel_json) > 0 : web_json_new = removeFromFirstPresenceArray(excel_json[-1],web_json,['date','debit','credit','nature'])
    else : web_json_new = web_json

    #4
    if len(web_json_new) > 0 : excel.appendJsonToExcel(web_json_new,filename_excel,sheet_name)

    print(f"{len(web_json_new)} lines added to excel")

def isUserIDRightFormat(user_id):
    try :
        if len(str(int(user_id))) != 8 :
            return False
    except :
        return False