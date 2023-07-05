import json

from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.region.region import Region
from huaweicloudsdkiotda.v5 import *
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.auth.credentials import DerivedCredentials

def getclient():
    ak = "VHFCPMB3CDEXUD6QDPFU"
    sk = "zytdTBHZJoQ0ygHupsK9xoNoRwa8IkcA0gYRaowQ"
    project_id = "1dc58e416b8f4702b3345b1343af3bb3"
    # region_id：如果是上海一，请填写"cn-east-3"；如果是北京四，请填写"cn-north-4"；如果是华南广州，请填写"cn-south-4"
    region_id = "cn-north-4"
    # endpoint：请在控制台的"总览"界面的"平台接入地址"中查看"应用侧"的https接入地址
    endpoint = "https://9bcb25f028.st1.iotda-app.cn-north-4.myhuaweicloud.com:443/v5/iot/1dc58e416b8f4702b3345b1343af3bb3/devices/64619ff7a1e0862b43d0adff_20210515/shadow"

    # 标准版/企业版：需自行创建Region对象
    REGION = Region(region_id, endpoint)

    # 创建认证
    # 创建BasicCredentials实例并初始化
    credentials = BasicCredentials(ak, sk, project_id)

    # 标准版/企业版需要使用衍生算法，基础版请删除该配置
    credentials.with_derived_predicate(
        DerivedCredentials.get_default_derived_predicate()
    )

    # 基础版：请选择IoTDAClient中的Region对象 如： .with_region(IoTDARegion.CN_NORTH_4)
    # 标准版/企业版：需要使用自行创建的Region对象
    client = (
        IoTDAClient.new_builder()
        .with_credentials(credentials)
        .with_region(REGION)
        .build()
    )
    return client

def getallDevice():
    client = getclient()
    request = ListDevicesRequest()
    response = client.list_devices(request)
    print(response)
    # 将返回值转化为JSON字符串
    JSONStr = str(response)
    # print(JSONStr)
    # 将JSON字符串转化为字典
    JSONlist = json.loads(JSONStr)  # 字典
    # print(type(JSONlist))
    shadowList = JSONlist["devices"]  # 列表
    result = []
    for item in shadowList:
        device_id = item["device_id"]
        node_id = item["node_id"]
        device_name = item["device_name"]
        product_name = item["product_name"]
        status = item["status"]
        item_dict = {
            "device_id": device_id,
            "node_id": node_id,
            "device_name":device_name,
            "product_name":product_name,
            "status": status
        }
        result.append(item_dict)
    print(result)
    return result

def listDevice():
    client = getclient()
    request = ListDevicesRequest()
    response = client.list_devices(request)
    # print(response)

    # 将返回值转化为JSON字符串
    JSONStr = str(response)
    # print(JSONStr)
    # 将JSON字符串转化为字典
    JSONlist = json.loads(JSONStr)  # 字典
    # print(type(JSONlist))
    shadowList = JSONlist["devices"]  # 列表
    result = []
    for item in shadowList:
        device_id = item["device_id"]
        status = item["status"]
        item_dict = {
            "device_id": device_id,
            "status": status
        }
        result.append(item_dict)
        # print("Device ID:", device_id)
        # print("Status:", status)

    # print(result)
    return result

if __name__ == "__main__":
    # print(listDevice())
    getallDevice()