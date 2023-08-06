import json
import os
import pytest
from loguru import logger
from common.common.constant import Constant
from common.plat.jira_platform import JiraPlatForm
from common.autotest.handle_allure import convert_severity
from common.config.config import LOG_PATH_FILE, TEST_PATH, TEST_TARGET_RESULTS_PATH, TEST_TARGET_REPORT_PATH,TEST_UI_PATH
from common.data.handle_common import get_system_key, set_system_key
from common.file.handle_system import del_file
from common.data.data_process import DataProcess


class PytestPlugin(object):

    @classmethod
    def getMethodCase(cls):
        """
        运行测试周期内的自动化用例（目前只支持场景用例）
        :return:
        """
        if (get_system_key('RuntType') == 'jenkins'):
            cycle_id = get_system_key('SRTCYCLE')
            if not cycle_id:
                return
        else:
            cycle_id = 20173
        TEST_CASE_PATH = os.path.join(TEST_PATH, 'test_scene')
        case_package = "test_scene/"

        jirakey = get_system_key(Constant.ISSUE_KEY)
        if get_system_key('CaseName'):
            case_name_list = get_system_key('CaseName').split(",")
        else:
            if get_system_key('Result'):
                case_name_list = JiraPlatForm.getCaseNameListFromCircleId(jirakey, cycle_id, get_system_key('Result'))
            else:
                case_name_list = JiraPlatForm.getCaseNameListFromCircleId(jirakey, cycle_id)
        logger.info("需要执行的用例列表： \n %s" % str(case_name_list))
        set_system_key(Constant.TEST_CASE_NAME_LIST, str(case_name_list), True)
        case_path_name_list = []
        for path, dir_list, file_list in os.walk(TEST_CASE_PATH):
            for file_name in file_list:
                if file_name.find("test") >= 0 and file_name[-3:] == ".py":
                    case_path = os.path.join(path, file_name)
                    try:
                        with open(case_path, 'r+', encoding='utf8') as f:
                            file_info = f.readlines()
                    except UnicodeDecodeError as e:
                        with open(case_path, 'r+', encoding='gbk') as f:
                            file_info = f.readlines()
                    for i in range(len(file_info)):
                        if file_info[i].find("allure.title") >= 0 and file_info[i].find("#") < 0 and \
                                file_info[i].split("'")[-2] in case_name_list:
                            k = 1
                            while k < 4:
                                if file_info[i + k].find("allure") < 0 and file_info[i + k].find("test") >= 0 and \
                                        file_info[i + k].find("def") >= 0 :
                                    case_path_name_list.append(
                                        case_package + file_name + "::Testcase::" + (file_info[i + k].split(" ")[-1].split("(")[0]))
                                    break
                                k += 1
        case_list_result = str(",".join(case_path_name_list))
        set_system_key(Constant.TEST_CASE_PATH, case_list_result, True)

    @classmethod
    def pytest_run_case(cls, _deleteResult:bool= True):
        """
        运行自动化用例
        :return:
        """
        logger.add(LOG_PATH_FILE, enqueue=True, encoding='utf-8')
        TEST_CASE_PATH = cls._convert_case_path(get_system_key(Constant.TEST_CASE_PATH))
        if _deleteResult:
            del_file(TEST_TARGET_RESULTS_PATH)
        if get_system_key(Constant.TEST_CASE_MARK) is None or get_system_key(Constant.TEST_CASE_MARK).strip() == '':
            TEST_CASE_PATH_ARR = TEST_CASE_PATH.split(',')
            for case_path in TEST_CASE_PATH_ARR:
                logger.info("开始执行脚本的路径:" + case_path)
                pytest.main(
                    args=[case_path, f'--alluredir={TEST_TARGET_RESULTS_PATH}'])
                logger.info("执行脚本成功:" + case_path)
        else:
            TEST_CASE_MARK = convert_severity(get_system_key(Constant.TEST_CASE_MARK))
            logger.info("执行用例的优先级:" + TEST_CASE_MARK)
            pytest.main(
                args=[TEST_CASE_PATH, '--alluredir', f'{TEST_TARGET_RESULTS_PATH}', '--allure-severities', f'{TEST_CASE_MARK}'])

    @classmethod
    def allure_report(cls):
        """
        生成测试报告
        :return:
        """

        if get_system_key(Constant.ALLURE_PATH) is not None:
            ALLURE_PATH = get_system_key(Constant.ALLURE_PATH)
        else:
            ALLURE_PATH = ''
        if get_system_key(Constant.RUN_TYPE) is None or get_system_key(Constant.RUN_TYPE) != 'jenkins' or get_system_key(Constant.RUN_TYPE) == '':
            os.system(f'{ALLURE_PATH}allure generate {TEST_TARGET_RESULTS_PATH} -o {TEST_TARGET_REPORT_PATH} --clean')
            logger.success('Allure测试报告已生成')


    @classmethod
    def change_allure_title(cls,report_html_path: str = TEST_TARGET_REPORT_PATH):
        """
        修改Allure标题
        :param name: 
        :param report_html_path: 
        :return: 
        """
        dict = {}
        # 定义为只读模型，并定义名称为f
        with open(f'{report_html_path}/widgets/summary.json', 'rb') as f:
            # 加载json文件中的内容给params
            params = json.load(f)
            # 修改内容
            params['reportName'] = get_system_key("JOB_NAME")
            # 将修改后的内容保存在dict中
            dict = params
            logger.info("修改测试报告名称：" + get_system_key(Constant.PROJECT_NAME))
            with open(f'{report_html_path}/widgets/summary.json', 'w', encoding="utf-8") as r:
                # 将dict写入名称为r的文件中
                json.dump(dict, r, ensure_ascii=False, indent=4)

            # 关闭json读模式
            f.close()
            logger.info("修改测试报告完成")


    @classmethod
    def _convert_case_path(cls,_str):
        _path = ''
        if _str is None or _str.strip() == '':
            _path = os.path.join(TEST_PATH, 'test_single')+','+os.path.join(TEST_PATH, 'test_scene')
        else:
            _arr = _str.split(',')
            for _temp in _arr:
                _path =_path+os.path.join(TEST_PATH, _temp)+","
            _path = os.path.join(TEST_PATH, 'test_single')+','+ _path[0:len(_path)-1]
        logger.info("获取需要执行的测试脚本路径： %s " % str(_path))
        return _path

    @classmethod
    def generated_code(self, _url: str = '', _path: str = TEST_UI_PATH):
        if not DataProcess.isNotNull(_url):
            _url = get_system_key('url')
        test_case_dir = '{}{}'.format(os.getcwd(), _path)
        file_list = [os.path.join(test_case_dir, file) for file in os.listdir(test_case_dir) if "test_" in file]
        test_case_num = len(file_list) - 2
        print("{}目录下存在{}测试用例".format(test_case_dir, test_case_num))
        cmd = r"python -m playwright codegen --target pytest -o {}/test_{}.py -b chromium {}". \
            format(_path, str(test_case_num + 1).zfill(3), url)
        print("执行录制测试用例命令：{}".format(cmd))
        os.system(cmd)




if __name__ == '__main__':
    # TEST_CASE_PATH = "/Users/liqizhu/Documents/work/auto_test/ams_test_api/test/test_scene"
    # TEST_TARGET_RESULTS_PATH = TEST_CASE_PATH
    # TEST_CASE_MARK = ["normal", "critical", "trivial", "minor", "blocker"]
    # pytest.main(
    #     args=[TEST_CASE_PATH, '--alluredir', f'{TEST_TARGET_RESULTS_PATH}', '--allure-title', f'critical,blocker'])
    # print(PytestPlugin._convert_case_path`('test_scene/test_upgrade/test_WebRT_upgrade_Direct_Cny_integral_Vip_one.py,test_scene/test_upgrade/test_WebRT_upgrade_Direct_Cny_integral_Vip_one2.py'))

    PytestPlugin.generated_code()

    # pytest.main(
    #     args=['/Users/liqizhu/Documents/work/auto_test/ams_test_api/test/test_single/test_api_S27.py::Testcase::test_00_main', f'--alluredir={TEST_TARGET_RESULTS_PATH}'])



