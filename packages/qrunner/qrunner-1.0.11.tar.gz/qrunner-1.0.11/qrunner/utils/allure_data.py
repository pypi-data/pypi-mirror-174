import json
import os.path


# 从allure数据中获取用例执行情况
def get_allure_data(allure_path):
    # 从json文件中获取执行结果列表
    case_list = []
    no_repeat_tags = []
    file_list = []
    for filename in os.listdir(allure_path):
        # 读取以result.json结尾的文件
        if filename.endswith('result.json'):
            file_list.append(filename)
            with open(os.path.join(allure_path, filename), 'r', encoding='UTF-8') as f:
                content = json.load(f)
        else:
            continue

        # 获取需要的字段
        name = content.get('name')
        status = content.get('status')
        full_name = content.get('fullName')
        decription = content.get('description')
        parameters = content.get('parameters', None)
        log_name = [item.get('source') for item in content.get('attachments') if item.get('name') == 'log'][0]
        start = content.get('start')
        end = content.get('stop')
        case_data = {
            "name": name,
            "full_name": full_name,
            "description": decription,
            "log": log_name,
            "status": status,
            "start_time": start,
            "end_time": end,
            "parameters": parameters
        }

        # 去除重试导致的重复用例
        if (full_name, parameters) not in no_repeat_tags:
            no_repeat_tags.append((full_name, parameters))
            case_list.append(case_data)
        else:
            # if status != 'passed':
            #     for case in case_list:
            #         if case.get('full_name') == full_name and case.get('parameters') == parameters:
            #             if case.get('status') != 'passed':
            #                 case_list.remove(case)
            #                 case_list.append(case_data)
            # else:
            #     for case in case_list:
            #         if case.get('full_name') == full_name and case.get('parameters') == parameters:
            #             case_list.remove(case)
            #             case_list.append(case_data)
            for case in case_list:
                if case.get('full_name') == full_name and case.get('parameters') == parameters:
                    if case.get('status') != 'passed':
                        case_list.remove(case)
                        case_list.append(case_data)

    # 获取用例统计数据
    passed_list = []
    fail_list = []
    for case in case_list:
        status = case.get('status')
        if status == 'passed':
            passed_list.append(case)
        else:
            fail_list.append(case)
    total = len(case_list)
    passed = len(passed_list)
    failed = len(fail_list)
    rate = round((passed / total) * 100, 2)

    # 获取整个任务的开始和结束时间
    start_time, end_time = case_list[0].get('start_time'), case_list[0].get('end_time')
    for case in case_list:
        inner_start = case.get('start_time')
        inner_end = case.get('end_time')
        if inner_start < start_time:
            start_time = inner_start
        if inner_end > end_time:
            end_time = inner_end

    # 获取接口统计数据
    interface_list = []
    for case in case_list:
        log = os.path.join(allure_path, case.get('log'))
        with open(log, 'r') as f:
            for line in f.readlines():
                if 'url]: ' in line:
                    interface = line.strip().split('url]: ')[1]
                    interface_list.append(interface)
    interface_list = list(set(interface_list))
    app_names = []
    for interface in interface_list:
        app_name = interface.split('/')[3]
        if app_name not in app_names:
            app_names.append(app_name)
    interface_count = len(interface_list)
    # print(len(interface_list))

    return {
        'total': total,
        'passed': passed,
        'failed': failed,
        'rate': rate,
        'api_num': interface_count,
        'apps': app_names,
        'start': start_time,
        'end': end_time
    }


if __name__ == '__main__':
    print(get_allure_data('/Users/UI/PycharmProjects/qrunner_new_gitee/allure-results'))



