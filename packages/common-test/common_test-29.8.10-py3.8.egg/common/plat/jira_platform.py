import json
import re
from jsonpath import jsonpath

from common.common.api_driver import APIDriver
from common.data.handle_common import extractor, get_system_key, set_system_key
from common.common.constant import Constant
from requests.auth import HTTPBasicAuth
from loguru import logger

class JiraPlatForm(object):

    @classmethod
    def getJiraIssueInfo(self, jira_no):
        """
        通过Jira号获取jira信息
        :param jira_no:
        :return:
        """
        return APIDriver.http_request(url=f"{Constant.JIRA_URL}/rest/api/2/issue/{jira_no}",method='get',
                                        _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),get_system_key(Constant.JIRA_PASSWORD)),
                                        _log=False)

    @classmethod
    def getReclyTestCase(self, testPlanIssueKey, cycleName):
        content = APIDriver.http_request(url=f"{Constant.JIRA_URL}/rest/synapse/latest/public/testPlan/{testPlanIssueKey}/cycle/{cycleName}/testRuns", method='get',
                                      _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),
                                                          get_system_key(Constant.JIRA_PASSWORD)),
                                      _log=False)
        try:
            content = json.loads(re.sub("&ldquo;|&rdquo;","", content.content.decode('gbk')))
        except UnicodeDecodeError as e:
            content = json.loads(re.sub("&ldquo;|&rdquo;","", content.content.decode('utf-8')))
        return content
        # return json.dumps(content, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))


    @classmethod
    def updatecaseByrunId(self, caseList, caseName, result_temp, comment):
        result = 4
        runid = 0
        if result_temp == 'passed':
            result=1
        if result_temp == 'failed':
            result=2
        xpath = "$..[?(@.summary =='name')].id".replace('name', re.sub("“|”|\n", "", caseName))
        logger.info(f'用例名称: {caseName} \n')
        try:
            runid=jsonpath(caseList, xpath)[0]
            logger.info(f'对应的runid: {runid} \n')
            APIDriver.http_request(
                url=f"{Constant.JIRA_URL}/rest/synapse/1.0/testRun/updateTestRunStatus?runId={runid}&status={result}",
                method='put',
                parametric_key='json',
                _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),
                                    get_system_key(Constant.JIRA_PASSWORD))
            )
            APIDriver.http_request(
                url=f"{Constant.JIRA_URL}/rest/synapse/1.0/testRun/updateTestRunComment",
                method='put',
                parametric_key='json',
                data=json.loads('{"testRunId":_runId,"testRunComment":"_comment"}'.replace('_runId', str(runid)).replace('_comment',comment)),
                _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),
                                    get_system_key(Constant.JIRA_PASSWORD))
            )
            logger.info(f'用例名称: {caseName}  用例运行ID：{runid}  结果:{result_temp}  结果描述:{comment}  推送结果：成功')
        except Exception as e:
            logger.info(f'用例名称: {caseName}  用例运行ID：{runid}  结果:{result_temp}  结果描述:{comment}  推送异常：{e}')




    @classmethod
    def setJiraFlowStatus(self, jira_key,flow_id):
        """
                触发工作流程
                :param jira_key: Jira_key
                :param flow_id: 流程ID
                :return:
                """
        return APIDriver.http_request(url=f"{Constant.JIRA_URL}/rest/api/2/issue/{jira_key}/transitions?expand=transitions.fields",
                                      method='post',
                                      parametric_key='json',
                                      data=json.loads('{"transition":{"id":"flow_id"}}'.replace('flow_id',flow_id)),
                                      _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),
                                                          get_system_key(Constant.JIRA_PASSWORD))
                                      )

    @classmethod
    def setJiraComment(self, jira_key,comment):
        """
        添加Jira的备注
        :param jira_key:
        :param comment:
        :return:
        """
        return APIDriver.http_request(url=f"{Constant.JIRA_URL}/rest/api/2/issue/{jira_key}/comment",
                                      method='post',
                                      parametric_key='json',
                                      data=json.loads('{"body":"comment"}'.replace('comment',comment)),
                                      _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME),
                                                        get_system_key(Constant.JIRA_PASSWORD))
                                     )

    @classmethod
    def getJiraIssueSummer(self, jira_no):
        try:
            if jira_no.find("http://") != -1:
                jira_no = jira_no.split("/")[-1]
            _summary = extractor(self.getJiraIssueInfo(jira_no).json(), "$.fields.summary")
            if str(_summary).find("$") != -1:
                _summary = None
                _link = f'{Constant.JIRA_URL}/browse/{jira_no}'
            else:
                _link = f'{Constant.JIRA_URL}/browse/{jira_no}'
        except Exception as e:
            _summary = None
            _link = f'{Constant.JIRA_URL}/browse/{jira_no}'
        return  _summary, _link, jira_no


    @classmethod
    def getJiraTestCaseKey(self, case_name):
        """
        通过项目id和测试用例名，获取测试用例的链接：http://jira.ceair.com:8080/browse/+key
        例如：http://jira.ceair.com:8080/browse/DS21059-2952
        """
        case_link = ""
        try:
            project_id = get_system_key(Constant.PROJECT_NAME).split("（")[-1].split("）")[0]
            content = APIDriver.http_request(
                url=f"{Constant.JIRA_URL}/rest/api/2/search",
                method='post',
                parametric_key='json',
                data={
                    "jql": "summary ~  %s AND project = %s" % (str(case_name), str(project_id)),
                    "startAt": 0,
                    "maxResults": 1000,
                    "fields": ["id", "key", "summary", "customfield_14903"]
                },
                _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME), get_system_key(Constant.JIRA_PASSWORD))
            )
            content = json.loads(content.content)
            if len(content["issues"]) == 1:
                case_link = f'{Constant.JIRA_URL}/browse/{content["issues"][0]["key"]}'
            elif len(content["issues"]) > 1:
                for item in content["issues"]:
                    if item["fields"]["summary"] == str(case_name):
                        case_link = f'{Constant.JIRA_URL}/browse/{item["key"]}'
                        break
            logger.info(f'获取用例链接成功: %s \n' % case_link)
        except Exception as e:
            logger.info(f'获取用例key失败: \n用例名：%s' % str(case_name))
        return case_link


    @classmethod
    def getCaseNameListFromCircleId(self, jira_no, cycle_id, result=""):
        """
        通过Jira的测试计划number，测试周期名字，来获取测试用例列表
        :param jira_no: 测试计划number
        :param cycle_id: 测试周期id
        :param result: 测试用例执行结果进行筛选（通过，失败，未执行等）
        :return:
        """
        content = APIDriver.http_request(
            url=f"{Constant.JIRA_URL}/rest/synapse/latest/public/testPlan/{jira_no}/cycle/{cycle_id}/testRunsByCycleId",
            method='get',
            _auth=HTTPBasicAuth(get_system_key(Constant.JIRA_USERNAME), get_system_key(Constant.JIRA_PASSWORD)),
            _log=False)

        if result != "":
            case_name_list = []
            logger.info('result结果：%s' % str(result.split(",")))
            for result_item in result.split(","):
                logger.info('result_item：%s' % str(result_item))
                case_list = jsonpath(json.loads(content.content),
                                           "$..[?(@.status == '%s')].summary" % result_item)
                if case_list:
                    case_name_list += case_list
        else:
            case_name_list = jsonpath(json.loads(content.content), "$..summary")
        return case_name_list

if __name__ == '__main__':
    # lucky_number = [0, 1, 2, 3, 0, 1, 2,3,0,1,2,3]
    # dic = {'a': 'z掌声', 'b': '2', 'c': 3}
    # js = json.dumps(dic,  ensure_ascii=False,sort_keys=True, indent=4, separators=(',', ':'))
    # print(js)
    link = JiraPlatForm.getCaseNameListFromCircleId("DO21090-1229", 18325, "失败")
    # link = JiraPlatForm.getCaseNameListFromCircleName("DEMOM-977", 20173)
    print ("result")
    print (link)