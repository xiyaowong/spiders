import importlib
import os
import re

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/')
async def index():
    content = '''
<!DOCTYPE html>
<html lang="zh-cn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Spiders</title>
    <style>
      a {
        display: block;
      }
    </style>
  </head>
  <body>
    <a href="https://github.com/xiyaowong/spiders">Github仓库地址</a>
    <a href="/docs">使用文档一</a>
    <a href="/redoc">使用文档二</a>
  </body>
</html>
'''
    return HTMLResponse(content)

def register_api(app: FastAPI):
    module_names = []
    for file in os.listdir('api'):
        if file in ('__pycache__', 'base.py', '__init__.py'):
            continue
        # .py
        if module_name := re.findall(r'(\w+)\.py', file):
            module_names.append(module_name[0])
        else:
            # package
            module_names.append(file)

    for module_name in module_names:
        module = importlib.import_module(f'api.{module_name}')
        if hasattr(module, 'ResponseModel') and hasattr(module, 'process'):
            app.post(
                f'/{module_name}',
                response_model=module.ResponseModel,
                description=module.__doc__ or '',
            )(module.process)


register_api(app)
