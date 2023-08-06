from loguru import logger
import json
from common.common.api_driver import APIDriver
from common.common.constant import Constant
from common.data.handle_common import get_system_key


class ATFPlatForm(object):

    @classmethod
    def db_ops(self, _key, _sql, env: str = Constant.ENV):
        """
        执行SQL操作
        :param _key:
        :param _sql:
        :param env:
        :return:
        """
        _sqltemp=_sql.encode("utf-8").decode("latin1")
        if get_system_key(env) is not None:
            env = get_system_key(env)
        sql_type = _sql.strip().split(" ")[0].lower()
        if "select" == sql_type:
            _tempdata = APIDriver.http_request(url=f"{Constant.ATF_URL_API}/querySetResult/{_key}/{env}",
                                               method='post', parametric_key='data', data=_sqltemp,
                                               _log=False)
            logger.info(f"执行sql成功:{_sql}")
            return list(_tempdata.json())
        if "insert" == sql_type or "delete":
            _tempdata = APIDriver.http_request(url=f"{Constant.ATF_URL_API}/doExecute/{_key}/{env}",
                                               method='post', parametric_key='data', data=_sqltemp)
            logger.info(f"执行sql成功:{_sql}")
            return _tempdata.text
        else:
            logger.error("不支持其他语句类型执行，请检查sql")


    @classmethod
    def runDeploy(self,jobName, _pramater):
        """
        推送测试结果
        :param jobName:
        :param _pramater:
        :return:
        """
        _tempdata = APIDriver.http_request(url=f"{Constant.ATF_URL}/jenkins/runDeploy/{jobName}",
                                               method='get', parametric_key='params', data=_pramater)
        return _tempdata


    @classmethod
    def getProjectData(self, projectName, projectKey):
        """
        获取项目数据
        :param projectName: 项目别名
        :param projectKey: 关键词
        :return:
        """

        try:
            content = APIDriver.http_request(url=f"{Constant.ATF_URL}/api/getProjectData/{projectName}/{projectKey}",
            method='get')
            return (json.loads(content.content)["data"]["projectValue"])
        except Exception as e:
            logger.info(f"{Constant.ATF_URL}/api/getProjectData/{projectName}/{projectKey}" + "获取不到value")
            return None

    @classmethod
    def setProjectData(self, projectKey, value, type = 1):
        """
        设置项目数据
        :param projectName: 项目别名
        :param projectKey: 关键词
        :param value: 值
        :param type: 数据类型[0可以重复使用，1不可以重复使用]
        :return:
        """
        if get_system_key('ProjectAlice') is not None and get_system_key('ProjectAlice').strip() != '':
            projectName = get_system_key('ProjectAlice')
            return APIDriver.http_request(
                url=f"{Constant.ATF_URL}/api/setProjectData/{projectName}/{projectKey}/{value}/{type}",
                method='get'
                )

if __name__ == '__main__':
    ATFPlatForm.setProjectData("id_test2", "7892", 0)
    result = ATFPlatForm.getProjectData("ams", "id_test2")
    print (result)