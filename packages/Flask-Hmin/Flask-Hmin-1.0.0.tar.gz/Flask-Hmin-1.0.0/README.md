# Flask-Hmin

## 安装
使用`pip`进行安装：
```shell
pip install Flask-Hmin
```

或者使用`pipenv`：
```shell
pipenv install Flask-Hmin
```

或者使用`poetry`：
```shell
poetry add Flask-Hmin
```

您也可以下载存储库并手动安装它，执行以下操作：
```shell
git clone https://github.com/zhenzi0322/Flask-Hmin.git
cd Flask-Hmin
python setup.py install
```

## 使用方法
```python
from flask import Flask, render_template
from flask_hmin import HMin

app = Flask(__name__)
app.config["HMIN_COMPRESS_HTML"] = True

hmin = HMin(app=app)


@app.route("/")
@hmin.compress
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
```