# coding: utf-8

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.auth.credentials import DerivedCredentials
from huaweicloudsdkcore.region.region import Region
from huaweicloudsdkiotda.v5.region.iotda_region import IoTDARegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkiotda.v5 import *

def CreateCommand():
    ak = "VHFCPMB3CDEXUD6QDPFU"
    sk = "zytdTBHZJoQ0ygHupsK9xoNoRwa8IkcA0gYRaowQ"
    project_id = "1dc58e416b8f4CreateCommand702b3345b1343af3bb3"
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


    request = CreateCommandRequest()
    request.device_id = "648c57b7ec46a256bca6829f_yushi"
    request.body = DeviceCommandRequest(
        paras="{\"name\":\"报警\"}"
    )
    response = client.create_command(request)
    print(response)
    return response

if __name__ == "__main__":
    print(CreateCommand())