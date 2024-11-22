import json
import re
import sys
from routerconfig import RouterConfig

if __name__ == '__main__':

    data = json.loads(re.sub('\'', '\"', sys.argv[1]))

    RouterConfig.configRouter(data)





