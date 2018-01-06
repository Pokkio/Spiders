from scrapy import cmdline
# cmdline.execute(['scrapy', 'crawl', 'gz.lianjia'])
cmdline.execute("scrapy crawl gz.lianjia -o info.csv -t csv".split())  # 生成 csv 文件
