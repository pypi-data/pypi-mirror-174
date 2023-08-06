
# print(r'''
# .__                             __                .__ ___.
# |  |   ____________           _/  |_  ____   ____ |  |\_ |__   _______  ___
# |  |  /  ___/\____ \   ______ \   __\/  _ \ /  _ \|  | | __ \ /  _ \  \/  /
# |  |__\___ \ |  |_> > /_____/  |  | (  <_> |  <_> )  |_| \_\ (  <_> >    <
# |____/____  >|   __/           |__|  \____/ \____/|____/___  /\____/__/\_ \
#           \/ |__|                                          \/            \/
# ''')

import sys
from lsptoolbox.database_class_define import DatabaseClearThread, DatabaseManagerBean

print('thanks for using LSP tool box ,my phone is 15608447849 , sys.argv = ', sys.argv)

_db_mng_map = {}

def MYSQL_SET__GROUP_CONCAT_MAX_LEN(mysql_db, maxLen):
    '''设置mysql group_concat 函数 最大字符数量'''
    try:
        lines = mysql_db.query("show variables like 'group_concat_max_len';")
        if len(lines) == 1:
            curLen = int(lines[0][0])
            if curLen>=maxLen: return
        mysql_db.execute("SET GLOBAL group_concat_max_len = %d;" % maxLen)
        mysql_db.execute("SET SESSION group_concat_max_len = %d;" % maxLen)
        print('mysql concat_group max len: %d ' % maxLen)
    except: pass

def setting_database(database_obj):
    if database_obj.databaseType == 'mysql':
        MYSQL_SET__GROUP_CONCAT_MAX_LEN(database_obj, 4294967295)


def load_database_config(config):
    db_clear_thread = DatabaseClearThread()
    print('初始化数据库连接池空闲检测线程 ',db_clear_thread)
    for session in  config.sections():
        if session.startswith('dbload::'):
            mngName = session.replace('dbload::','',1)
            try:
                charset = config.get(session, 'charset')
            except:
                charset = 'utf8'

            databaseConnectBean = DatabaseManagerBean( db_clear_thread,
                                                       config.get(session, 'dbtype'),
                                                       config.get(session, 'host'),
                                                       config.get(session, 'port'),
                                                       config.get(session, 'username'),
                                                       config.get(session, 'password'),
                                                       config.get(session, 'database'),
                                                       charset
                                                       )
            setting_database(databaseConnectBean)
            _db_mng_map[mngName] = databaseConnectBean
            print("加载数据库 [ %s ],  %s" % (mngName, str(_db_mng_map[mngName])))

def getDatabaseOperation(databaseName):
    '''获取数据库'''
    mng = _db_mng_map.get(databaseName,None)
    if mng == None: raise ValueError("找不到指定数据库对象:%s" % databaseName)
    return mng

class CustomStdout:
    def __init__(self,appRootDir,cmd,recode=0):

        self.console = sys.stdout
        self.error = sys.stderr
        sys.stdout = self
        sys.stderr = self
        #sys.stderr = self
        self.appRootDir = appRootDir+'logs'
        # import datetime,os
        # self.procFlag = "%s_%s_%d" % (cmd,datetime.datetime.strftime(datetime.datetime.now(), '%H%M%S'),os.getpid())
        self.procFlag = cmd
        self.recode = recode
        self.msgText = []

    def write(self,outStr):
        try:
            if len(self.msgText) == 0:
                import datetime
                nowTimeStr = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                import os
                prevStr = "【%s】（%d）" % (nowTimeStr, os.getpid())
                self.msgText.append(prevStr)
                # self.console.write(prevStr)

            self.msgText.append(outStr)
            # self.console.write(outStr)
        except:
            import traceback
            traceback.print_exc()
        finally:
            try:
                if outStr.endswith('\n') and len(self.msgText)>0:
                    lineMsg = ''.join(self.msgText)
                    self.msgText.clear()
                    if 'NO CONSOLE' not in lineMsg:
                        self.console.write(lineMsg)
                    else:
                        lineMsg = lineMsg.replace('NO CONSOLE','*')
                    self.writeFile(lineMsg)
            except:
                import traceback
                traceback.print_exc()

    def flush(self): pass

    def writeFile(self, outStr):
        if self.recode == 0: return
        try:
            import datetime, os
            dir_path = self.appRootDir + '/' + datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d') +'/'
            if not os.path.exists(dir_path): os.makedirs(dir_path)
            file_path = dir_path +  self.procFlag + '.log'
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(outStr)
        except:
            import traceback
            traceback.print_exc()

# 加载配置
def load_config(project_name,cmd):
    import os
    import sys
    import configparser

    appRootDir = None
    if getattr(sys, 'frozen', False):
        appRootDir = os.path.dirname(sys.executable)
    elif __file__:
        appRootDir = os.path.dirname(os.path.realpath(sys.argv[0]))
    if appRootDir is None:
        print('程序运行路径异常,退出程序')
        os._exit(-1)

    if project_name in appRootDir:
        index = appRootDir.find(project_name)
        appRootDir = appRootDir[0:index + len(project_name)]
    if appRootDir.endswith('/') is False:
        appRootDir = appRootDir + '/'
    appRootDir = appRootDir.replace('\\', '/')
    printer = CustomStdout(appRootDir, cmd)
    print("应用(%s)(%d) 根目录路径: %s" % (project_name,os.getpid(), appRootDir))
    sys.path.append(appRootDir)

    configList = []
    for file in os.listdir(appRootDir):
        file_path = appRootDir + file
        if os.path.isfile(file_path) and os.path.splitext(file_path)[1] == '.ini':
            configList.append(file_path)


    config = configparser.RawConfigParser()
    config.read(filenames=configList, encoding='utf8')

    sections = config.sections()
    for section in sections:
        options = config.options(section)
        for option in options:
            var = config.get(section,option)
            if var.startswith('./'):
                var = appRootDir + var[2:]
                config.set(section,option,var)
            # print(section, option, var)

    printer.recode = config.getint('log','recode')

    load_database_config(config)

    return appRootDir, config
