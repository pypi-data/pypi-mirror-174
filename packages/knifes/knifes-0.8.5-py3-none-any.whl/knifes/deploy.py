from .shell import *
from .file import read_file
import time
import sys
from datetime import datetime, timedelta


def print_help(project_dir):
    print('reload   --reload gunicorn\n'
          'modules  --install modules\n'
          'log n    --read gunicorn last log\n'
          'start    --start gunicorn\n'
          'knifes   --force install latest knifes\n\n'
          'activate virtual environment cmd:\n\n'
          'source {}venv/bin/activate'.format(project_dir))


def main_script(chdir, logdir, app_name):
    args = sys.argv[1:]
    if not args:
        print_help(chdir)
    elif args[0] == 'reload':
        reload_gunicorn(chdir, logdir)
    elif args[0] == 'modules':
        install_modules(chdir)
    elif args[0] == 'log':
        line_count = 10 if len(args) == 1 else args[1]
        read_last_log(logdir, line_count)
    elif args[0] == 'start':
        start_gunicorn(chdir, logdir, app_name)
    elif args[0] == 'knifes':
        install_latest_knifes(chdir)
    else:
        print_help(chdir)


def install_latest_knifes(project_dir):
    cmd = 'source {}venv/bin/activate && pip install knifes --index-url https://pypi.python.org/simple -U'.format(project_dir)
    succ, err = exec_shell(cmd)
    print_succ(succ)
    print_err(err)


def install_modules(project_dir):
    cmd = 'source {}venv/bin/activate && pip install -r {}requirements.txt'.format(project_dir, project_dir)
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ret.returncode != 0:
        print_err(ret.stderr.decode())
        raise SystemExit
    print_succ(ret.stdout.decode())
    print_succ(ret.stderr.decode())  # warning message


def read_last_log(log_dir, line_count):
    succ, err = exec_shell('tail -{} {}error.log'.format(line_count, log_dir))
    print_succ(succ)
    print_err(err)
    return succ, err


def start_gunicorn(project_dir, log_dir, app_name):
    """
    调用前先在project目录下创建venv环境,如:
    /root/.pyenv/versions/3.7.2/bin/python -m venv venv
    
    gunicorn >= 20.1.0
    在conf文件中配置wsgi_app
    根据app_name加载相应的配置文件
    """
    install_modules(project_dir)

    cmd = '{}venv/bin/gunicorn -c {}gunicorn_{}_conf.py'.format(project_dir, project_dir, app_name)
    # 判断是否已启动
    succ, err = exec_shell("pgrep -f '{}'".format(cmd))
    if succ:
        print_err('当前已启动！请通过reload命令重启')
        return

    succ, err = exec_shell(cmd)
    print_succ(succ)
    print_err(err)
    time.sleep(1)
    read_last_log(log_dir, 6)


def reload_gunicorn(project_dir, log_dir):
    install_modules(project_dir)

    pid_filename = '{}pid.pid'.format(log_dir)
    pid = read_file(pid_filename).strip()
    if not pid:
        print_err('重启gunicorn失败,pid不存在:{}'.format(pid_filename))
    exec_shell('kill -HUP {}'.format(pid))
    time.sleep(1)
    succ, err = read_last_log(log_dir, 30)
    if not succ:
        print_err('重启失败！重启失败！重启失败！')
        return

    # 判断时间是不是3s内
    lines = filter(lambda x: 'Hang up: Master' in x, succ.split('\n'))
    if not lines:
        print_err('重启失败！重启失败！重启失败！')
        return

    for line in lines:
        if datetime.strptime(line[0:19], '%Y-%m-%d %H:%M:%S') > (datetime.now() - timedelta(seconds=3)):
            print_succ('重启成功:{}'.format(line[0:19]))
            return

    print_err('重启失败！重启失败！重启失败！')

