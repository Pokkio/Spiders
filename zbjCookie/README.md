##api接口地址（cookie随机返回）   
:spider: https://0.0.0.0:8080/cookie/random  

##入口文件
:spider: api.py

##定时任务文件
:spider: --scheduler.py

##获取cookie文件
:spider: autoCookies.py

##操作redis及相关获取cookie逻辑文件
:spider: operatingRedis.py

##日志器配置文件
:spider: log.py

##存放图片文件夹
:spider: ​images

##日志文件夹
:spider: log/api.log -- 请求接口日志
:spider: ​log/cookie.log -- 获取cookie日志
:spider: log/scheduler.log -- 调度器日志