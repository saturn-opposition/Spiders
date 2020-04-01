# Spiders
1. 汽车之家爬虫：使用scrapy框架，爬取宝马五系各个部位所有图片。

2. B站爬虫：
+ 用户基本信息爬虫：使用selenium控制Chrome浏览器，用BeautifulSoup解析网页，获取用户昵称、等级、会员、投稿数、频道数、收藏数、订阅番剧名、关注数、粉丝数、生日，并存入mysql数据库。
+ B站弹幕：主要是通过检查网页加载时下载的文件，来获得传输弹幕的网址，从而爬取视频的弹幕。

3. 腾讯视频弹幕爬虫：同理，找到下载弹幕的网址、弹幕更新的规律是关键。

4. 微博爬虫：
<br>①用户全部微博爬虫：2种写法
+ zyx_weibo.py：通过weibo.cn获取数据，selenium自动登录、requests库进行访问，Beautifulsoup解析网页内容，最后将用户的微博内容、点赞数、转发数、评论数保存至csv文件。
+ w.py：可通过传入uid list爬取多个用户微博
<br>&nbsp;&nbsp;&nbsp;通过m.weibo.cn获取数据。
<br>&nbsp;&nbsp;&nbsp;通过def __init__()设置爬取原创/转发微博，起始时，是否写入mongodb、mysql，是否下载图片、视频，设置需要爬取的用户id。
<br>&nbsp;&nbsp;&nbsp;通过def get_user_info()获取用户信息，如用户uid、用户名、性别、粉丝数、个人简介、头像、等级等。
<br>&nbsp;&nbsp;&nbsp;def parse_weibo()对返回的微博网页内容进行解析。

<br>②微博话题爬虫：通过关键词检索微博并爬取。
+ 使用fake_useragent切换UserAgent
+ 使用的微博接口为weibo.cn
+ 爬取到约130页会抓不到数据
+ 可设置是否爬取原创，起始时间，将数据存入csv或mysql数据库

<br>③微博评论爬虫：使用scrapy框架，可以对微博话题爬虫爬取的每一条微博，逐一爬取微博的评论，但由于微博限制问题，获取的评论数量有限。

