
from testcase_script.utl import get_docx_files
import yaml

class loadConfig():

    def __init__(self, config_path=None) -> None:
        # if a custom path is provided, use it
        if config_path is not None:
            self.config_path = config_path
        else:
            # else use the default path
            self.config_path = "./testcase_script/config.yaml"

        self.configs = {}

    def load_config(self):
        # load environment variables

        # self.configs = dict(os.environ)

        # 打开配置文件
        with open(self.config_path, "r", encoding='utf-8') as file:
            # load yaml file
            yaml_data = yaml.safe_load(file)

        # add yaml data to configs dictionary
        self.configs.update(yaml_data)
        #load all docx files in the specified directory
        self.configs['NEEDS_NAME'] = get_docx_files('media/requirements/documents/')
        #print('配置文件加载成功')
        print(self.configs['NEEDS_NAME'])
        return self.configs
