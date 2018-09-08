# ShareRoom
一个交换分享书籍，电影以及各类资源的平台



## 使用方法

- 安装环境

  ```shell
  pip install pipenv
  cd ShareRoom
  pipenv install
  pipenv shell
  ```

- 配置 `secure.py`

  ```shell
  cd ./app
  nano secure.py
  ```

  配置项如下

  ```python
  DEBUG = True
  
  # 数据库配置
  SQLALCHEMY_DATABASE_URI = "mysql+cymysql://root:password@127.0.0.1:3306/database?charset=utf8"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = ""
  
  # Email 配置
  MAIL_SERVER = 'smtp.qq.com'
  MAIL_PORT = 465
  MAIL_USE_SSL = True
  MAIL_USE_TSL = False
  MAIL_USERNAME = 'username@test.com'
  MAIL_PASSWORD = 'password'
  MAIL_SUBJECT_PREFIX = '[Codes-Room]'
  MAIL_SENDER = 'name <support@codes-room.com>'
  ```

- 运行 `share.py`

  (此时应该在pipenv shell中)

  ```shell
  cd ../
  pyhon3 share.py
  ```


## 运行截图

