import requests
import urllib.request
import json
import ssl


class LaTeXDelegate:
    def __init__(self):
        self.png_url = 'https://latex2png.com'
        self.api_url = 'https://latex2png.com/api/convert'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        ssl._create_default_https_context = ssl._create_unverified_context

    def latex2png(self, expression='1+1=2',
                  local_file_name='../resources/images/test_latex.png',
                  resolution=600,
                  color_str='000000'):
        try:
            data = {"auth": {"user": "guest", "password": "guest"},
                    "latex": expression, "resolution": resolution, "color": color_str}

            response = requests.post(self.api_url, data=json.dumps(data), verify=False)
            js = json.loads(response.content)

            if js['result-code'] == 0:
                png_url = self.png_url + js['url']
                urllib.request.urlretrieve(png_url, filename=local_file_name)
                return True, local_file_name
            else:
                return False, str(js['result-message'])
        except Exception as e:
            return False, repr(e)
