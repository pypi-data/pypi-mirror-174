import os


def get_device_list():
    """获取当前连接的手机列表"""
    cmd = 'adb devices'
    output = os.popen(cmd).read()
    device_list = [item.split('\t')[0] for item in output.split('\n') if item.endswith('device')]
    return device_list


