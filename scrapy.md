Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架。 其可以应用在数据挖掘，信息处理或存储历史数据等一系列的程序中。
其最初是为了页面抓取 (更确切来说, 网络抓取 )所设计的， 也可以应用在获取API所返回的数据(例如 Amazon Associates Web Services ) 或者通用的网络爬虫。Scrapy用途广泛，可以用于数据挖掘、监测和自动化测试。

Scrapy主要包括了以下组件：
* 引擎(Scrapy):用来处理整个系统的数据流处理, 触发事务(框架核心)
* 调度器(Scheduler):用来接受引擎发过来的请求, 压入队列中, 并在引擎再次请求的时候返回. 可以想像成一个URL（抓取网页的网址或者说是链接）的优先队列, 由它来决定下一个要抓取的网址是什么, 同时去除重复的网址
* 下载器(Downloader):用于下载网页内容, 并将网页内容返回给蜘蛛(Scrapy下载器是建立在twisted这个高效的异步模型上的)
* 爬虫(Spiders):爬虫是主要干活的, 用于从特定的网页中提取自己需要的信息, 即所谓的实体(Item)。用户也可以从中提取出链接,让Scrapy继续抓取下一个页面
* 项目管道(Pipeline):负责处理爬虫从网页中抽取的实体，主要的功能是持久化实体、验证实体的有效性、清除不需要的信息。当页面被爬虫解析后，将被发送到项目管道，并经过几个特定的次序处理数据。
* 下载器中间件(Downloader Middlewares):位于Scrapy引擎和下载器之间的框架，主要是处理Scrapy引擎与下载器之间的请求及响应。
* 爬虫中间件(Spider Middlewares):介于Scrapy引擎和爬虫之间的框架，主要工作是处理蜘蛛的响应输入和请求输出。
* 调度中间件(Scheduler Middewares):介于Scrapy引擎和调度之间的中间件，从Scrapy引擎发送到调度的请求和响应。

## 创建项目
命令行输入：  
` scrapy startproject your_project_name`  
项目文件说明：

* scrapy.cfg ：项目的配置信息，主要为Scrapy命令行工具提供一个基础的配置信息。（真正爬虫相关的配置信息在settings.py文件中）  
* items.py：设置数据存储模板，用于结构化数据，如：Django的Model
* pipelines：数据处理行为，如：一般结构化的数据持久化
* settings.py：配置文件，如：递归的层数、并发数，延迟下载等
* spiders：爬虫目录，如：创建文件，编写爬虫规则

## 创建爬虫文件
在项目目录下输入：  
`scrapy genspider 文件名 域名`  

更改如下设置：
```
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_LEVEL = 'ERROR'
```

scrapy默认遵守robotstxt，改为False，并把USER_AGENT改为浏览器，增加 LOG_LEVEL = 'ERROR'，设置为出错时才打印日志文件。

## 运行

进入project_name目录，运行命令
`scrapy crawl spider_name [--nolog]`  
--nolog 不显示日志 

## scrapy的持久化(示例)
爬取数据并进行持久化处理

items.py：
```Python
# 规范持久化的格式
import scrapy

class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field()
```

爬虫应用：
```Python
import scrapy
from  myspider.items import MyspiderItem


class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.com']
    start_urls = ['https://dig.chouti.com/']

    def parse(self, response):
        # print(response.text)
        a_list = response.xpath('//div[@id="content-list"]//div[@class="part1"]/a[@class="show-content color-chag"]/@href').extract() # extract()将标签中数据取出
        for url in a_list:
            yield MyspiderItem(url=url)
```

yield每执行一次，process_item就调用yield Item对象。

此处代码的关键在于：  
* 将获取的数据封装在了Item对象中
* yield Item对象 （一旦parse中执行yield Item对象，则自动将该对象交个pipelines的类来处理）

使用scrapy解析文本内容时，可以使用每个应用中的response.xpath(xxx) 进行数据的解析。

print(response.xpath(...))  得到的是一个Selector对象。selector对象可以继续xpath进行数据的解析。

xpath使用方法：
1.//+标签  表示从全局的子子孙孙中查找标签    
2./+标签   表示从子代中查找标签
3.查找带有xxx属性的标签：   标签+[@标签属性="值"]   
4.查找标签的某个属性：  /标签/@属性  
5.从当前标签中查找时：.//+标签     
```Python
response = HtmlResponse(url='http://example.com', body=html,encoding='utf-8')
hxs = HtmlXPathSelector(response)
print(hxs)   # selector对象
hxs = Selector(response=response).xpath('//a')
print(hxs)    #查找所有的a标签
hxs = Selector(response=response).xpath('//a[2]')
print(hxs)    #查找某一个具体的a标签    取第三个a标签
hxs = Selector(response=response).xpath('//a[@id]')
print(hxs)    #查找所有含有id属性的a标签
hxs = Selector(response=response).xpath('//a[@id="i1"]')
print(hxs)    # 查找含有id=“i1”的a标签
# hxs = Selector(response=response).xpath('//a[@href="link.html"][@id="i1"]')
# print(hxs)   # 查找含有href=‘xxx’并且id=‘xxx’的a标签
# hxs = Selector(response=response).xpath('//a[contains(@href, "link")]')
# print(hxs)   # 查找 href属性值中包含有‘link’的a标签
# hxs = Selector(response=response).xpath('//a[starts-with(@href, "link")]')
# print(hxs)   # 查找 href属性值以‘link’开始的a标签
# hxs = Selector(response=response).xpath('//a[re:test(@id, "i\d+")]')
# print(hxs)   # 正则匹配的用法   匹配id属性的值为数字的a标签
# hxs = Selector(response=response).xpath('//a[re:test(@id, "i\d+")]/text()').extract()
# print(hxs)    # 匹配id属性的值为数字的a标签的文本内容
# hxs = Selector(response=response).xpath('//a[re:test(@id, "i\d+")]/@href').extract()
# print(hxs)    #匹配id属性的值为数字的a标签的href属性值
# hxs = Selector(response=response).xpath('/html/body/ul/li/a/@href').extract()
# print(hxs)
# hxs = Selector(response=response).xpath('//body/ul/li/a/@href').extract_first()
# print(hxs)
 
# ul_list = Selector(response=response).xpath('//body/ul/li')
# for item in ul_list:
#     v = item.xpath('./a/span')
#     # 或
#     # v = item.xpath('a/span')
#     # 或
#     # v = item.xpath('*/a/span')
#     print(v)
```
备注：xpath中支持正则的使用：

1.标签+[re:test（@属性值，"正则表达式"）]

2.获取标签的文本内容：   /text()     

3.获取第一个值需要  selector_obj.extract_first()    获取所有的值  selector_obj.extract()  值在一个list中
 
pipelines.py：
```Python
class MyspiderPipeline(object):

    def __init__(self,file_path):
        self.f = None
        self.file_path = file_path

    @classmethod
    def from_crawler(cls,crawler):
        '''
        执行pipeline类时，会先去类中找from_crawler的方法，
        如果有，则先执行此方法，并且返回一个当前类的对象，
        如果没有，则直接执行初始化方法
        :param crawler:
        :return:
        '''
        # 可以进行一些初始化之前的处理，比如：文件的路径配置到settings文件中，方便后期的更改。
        file_path = crawler.settings.get('PACHONG_FILE_PATH')
        return cls(file_path)

    def open_spider(self,spider):
        '''
        爬虫开始时被调用
        :param spider:
        :return:
        '''
        self.f = open(self.file_path,'w',encoding='utf8')

    def process_item(self, item, spider):
        '''
        执行持久化的逻辑操作
        :param item: 爬虫yield过来的item对象  (一个字典)
        :param spider:  爬虫对象
        :return:
        '''
        self.f.write(item['url']+'\n')
        self.f.flush()   #将写入到内存的文件强刷到文件中，防止夯住，不使用此方法会夯住
        return item

    def close_spider(self,spider):
        '''
        爬虫结束时调用
        :param spider: 
        :return: 
        '''
        self.f.close()
```

上述中的pipelines中可以有多个类，定义各个类的优先级，要在settings.py中做如下配置：
```Python
ITEM_PIPELINES = {
    'xxx': 300,
    'xxx': 100,
}
# 每行后面的整型值，确定了他们运行的顺序，item按数字从低到高的顺序，通过pipeline，通常将这些数字定义在0-1000范围内。
```

获取所有页面：
```Python
import scrapy
from  myspider.items import MyspiderItem
from scrapy.http import Request

class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['chouti.com']
    start_urls = ['https://dig.chouti.com/']

    def parse(self, response):
        a_list = response.xpath('//div[@id="content-list"]//div[@class="part1"]/a[@class="show-content color-chag"]/@href').extract()
        for url in a_list:
            yield MyspiderItem(url=url)

        # 获取分页的url
        url_list = response.xpath('//div[@id="dig_lcpage"]//a/@href').extract()
        for url in url_list:
            url = 'https://dig.chouti.com%s'%url
            yield Request(url=url,callback=self.parse)
```
以上代码之所以可以进行“递归”的访问相关URL，关键在于parse方法使用了 yield Request对象。

注：可以修改settings.py 中的配置文件，以此来指定“递归”的层数，如： DEPTH_LIMIT = 1 

 

在生成的每一个爬虫应用中，会有一个起始url，start_urls = ['https://dig.chouti.com/']，这个起始url执行完后会被parse回调函数接收响应结果。那我们如何修改这个回调函数呢？
其实，在每一个爬虫应用继承的父类中，会执行一个方法  start_requests ，这个方法，会将起始的url生成一个request对象，传给调度器。
```Python
class Spider(object_ref):

        def start_requests(self):
        cls = self.__class__
        if method_is_overridden(cls, Spider, 'make_requests_from_url'):
            warnings.warn(
                "Spider.make_requests_from_url method is deprecated; it "
                "won't be called in future Scrapy releases. Please "
                "override Spider.start_requests method instead (see %s.%s)." % (
                    cls.__module__, cls.__name__
                ),
            )
            for url in self.start_urls:
                yield self.make_requests_from_url(url)
        else:
            for url in self.start_urls:
                yield Request(url, dont_filter=True)
```

备注：在执行爬虫应用时，会先执行start_requests方法，所以我们可以重写此方法自定制。

## 请求传参
使用请求传参原因：需要爬取的数据不在同一页面
```Python
class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['www.id97.com']
    start_urls = ['http://www.id97.com/']

    def parse(self, response):
        div_list = response.xpath('//div[@class="col-xs-1-5 movie-item"]')

        for div in div_list:
            item = MovieproItem()
            item['name'] = div.xpath('.//h1/a/text()').extract_first()
            item['score'] = div.xpath('.//h1/em/text()').extract_first()
            #xpath(string(.))表示提取当前节点下所有子节点中的数据值（.）表示当前节点
            item['kind'] = div.xpath('.//div[@class="otherinfo"]').xpath('string(.)').extract_first()
            item['detail_url'] = div.xpath('./div/a/@href').extract_first()
            #请求二级详情页面，解析二级页面中的相应内容,通过meta参数进行Request的数据传递
            yield scrapy.Request(url=item['detail_url'],callback=self.parse_detail,meta={'item':item})

    def parse_detail(self,response):
        #通过response获取item
        item = response.meta['item']
        item['actor'] = response.xpath('//div[@class="row"]//table/tr[1]/a/text()').extract_first()
        item['time'] = response.xpath('//div[@class="row"]//table/tr[7]/td[2]/text()').extract_first()
        item['long'] = response.xpath('//div[@class="row"]//table/tr[8]/td[2]/text()').extract_first()
        #提交item到管道
        yield item
```
scrapy.Request函数通过meta参数把item传递给回调函数parse_detail，parse_detail可以通过reponse.meta调用item，在该函数内完成对二级页面的爬取，最后将item提交给管道。

 
 ## 中间件
 下载中间件
下载器中间件是介于Scrapy的request/response处理的钩子框架，是用于全局修改Scrapy request和response的一个轻量、底层的系统。

主要作用:

* 在Scrapy将请求发送到网站之前修改,处理请求,如：更换代理ip，header等
* 在将响应传递给引擎之前处理收到的响应，如：响应失败重新请求，或将失败的做一定处理再返回给引擎
* 忽略一些响应或者请求  

scrapy内置了一些默认配置，这些是不允许被修改的，通常是_BASE结尾的设置，比如DOWNLOADER_MIDDLEWARES_BASE下载中间件的默认设置，如下
 ```Python
 {
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
    'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}
 ```
 scrapy就是按照上面数字从小到大依次执行的，比如执行完RobotsTxtMiddleware的process_request()方法后会继续执行下面HttpAuthMiddleware等process_request()，可以看作串联的形式依次过流水线。

如果我们要添加自定义的下载中间件，需要在settings.py中激活DOWNLOADER_MIDDLEWARES。同时想取消默认的一些中间件，也可以设置为None。注意的是激活DOWNLOADER_MIDDLEWARES并不会覆盖DOWNLOADER_MIDDLEWARES_BASE，而是继续串联起来

```Python
DOWNLOADER_MIDDLEWARES = {
    'myproject.middlewares.CustomDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}
```

自定义下载中间件
在创建项目后，再项目文件夹中有一middlewares.py文件，里面自动生成了两个中间件示例或者说模板。我们如果要自定义中间件的话，可以在给的示例上修改，或者新建类实现方法，或者继承已有的中间件重写方法

以下是下载中间件可以实现的方法，在自定义中间件时，可以根据需求实现

1.process_request(self, request, spider)

当每个request通过下载中间件时，该方法被调用。process_request() 必须返回其中之一: 返回 None 、返回一个 Response 对象、返回一个 Request 对象或raise IgnoreRequest 。最常使用的是返回None
* 如果其返回 None ，会将处理过后的request丢给中间件链中的下一个中间件的process_request()方法处理，直到丢到下载器，由下载器下载
* 如果其返回 Response 对象，Scrapy将不会调用任何其他的 process_request() 或 process_exception() 方法，也不会丢到下载器下载；直接将其返回的response丢到中间件链的process_response()处理。可以通过scrapy.http.Response构建Response 
* 如果其返回 Request 对象，Scrapy则停止调用process_request方法并重新调度返回的request。当新返回的request被执行后， 相应地中间件链将会根据下载的response被调用。
* 如果其raise一个 IgnoreRequest 异常，则安装的下载中间件的 process_exception() 方法会被调用。如果没有任何一个方法处理该异常， 则request的errback(Request.errback)方法会被调用。如果没有代码处理抛出的异常， 则该异常被忽略且不记录(不同于其他异常那样)。

参数:  
request(Request 对象)–处理的request  
spider(Spider 对象)–该request对应的spider

2.process_response(self, request, response, spider)   
当下载的response返回时，process_response()被调用，且 必须返回以下之一: 返回一个 Response 对象、 返回一个 Request 对象或raise一个 IgnoreRequest 异常。
* 如果其返回一个 Response (可以与传入的response相同，也可以是全新的对象)， 该response会被在链中的其他中间件的 process_response() 方法处理。
* 如果其返回一个 Request 对象，则中间件链停止， 返回的request会被重新调度下载。处理类似于 process_request() 返回request所做的那样。
* 如果其抛出一个 IgnoreRequest 异常，则调用request的errback(Request.errback)。 如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)。

参数:  
request (Request 对象) – response所对应的request  
response (Response 对象) – 被处理的response  
spider (Spider 对象) – response所对应的spider

3.process_exception(self, request, exception, spider)  
当下载处理器(download handler)或 process_request() (下载中间件)抛出异常(包括IgnoreRequest异常)时，Scrapy调用 process_exception() 。process_exception() 应该返回以下之一: 返回 None 、 一个 Response 对象、或者一个 Request 对象。  
* 如果其返回 None ，Scrapy将会继续处理该异常，接着调用已安装的其他中间件的 process_exception() 方法，直到所有中间件都被调用完毕，则调用默认的异常处理。
* 如果其返回一个 Response 对象，则已安装的中间件链的 process_response() 方法被调用。Scrapy将不会调用任何其他中间件的 process_exception() 方法。
* 如果其返回一个 Request 对象， 则返回的request将会被重新调用下载。这将停止中间件的 process_exception() 方法执行，就如返回一个response的那样。

参数:  
request (是 Request 对象) – 产生异常的request  
exception (Exception 对象) – 抛出的异常    
spider (Spider 对象) – request对应的spider  

4.from_crawler(cls, crawler)

如果存在，则调用此类方法创建中间件实例Crawler。它必须返回一个新的中间件实例。Crawler对象提供对所有Scrapy核心组件的访问，如设置和信号; 它是中间件访问它们并将其功能挂钩到Scrapy的一种方式。  
参数:  
    crawler（Crawlerobject）- 使用此中间件的爬网程序

设置随机User-Agent的中间件：
```Python
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5"
]

class UserAgent_Middleware():

    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        request.headers['User-Agent'] = ua
```

设置代理中间件
```Python
proxy_list=[
    "http://180.76.154.5:8888",
    "http://14.109.107.1:8998",
    "http://106.46.136.159:808",
    "http://175.155.24.107:808",
    "http://124.88.67.10:80",
    "http://124.88.67.14:80",
    "http://58.23.122.79:8118",
    "http://123.157.146.116:8123",
    "http://124.88.67.21:843",
    "http://106.46.136.226:808",
    "http://101.81.120.58:8118",
    "http://180.175.145.148:808"]
class proxy_Middleware(object):

    def process_request(self,request,spider):
        proxy = random.choice(proxy_list)
        request.meta['proxy'] = proxy
```
集成selenium的scrapy(selenium用于爬取动态加载的数据)
```Python
from selenium import webdriver
from scrapy.http import HtmlResponse
import time

class SeleniumMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def process_request(self, request, spider):
        self.driver.get(request.url)
        time.sleep(2)
        body = self.driver.page_source
        return HtmlResponse(self.driver.current_url,
                           body=body,
                           encoding='utf-8',
                           request=request)
```
最好是在爬虫文件中创建浏览器对象，然后在中间件middlewares.py中通过spider.xxx调用浏览器对象，避免多次创建。

### spider中间件

spider中间件用于处理引擎传回的response及spider生成的item和Request

主要作用：
* 处理spider的异常
* 对item在进入管道之前操作
* 根据引擎传入的响应，再进入回调函数前先处理

默认spider中间件  
SPIDER_MIDDLEWARES_BASE
```Python
{
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
}
```
同理，激活中间件
```Python
SPIDER_MIDDLEWARES = {
    'myproject.middlewares.CustomSpiderMiddleware': 543,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
}
```

自定义spider中间件  
1.process_spider_input(self, response, spider)

对于通过spider中间件并进入spider的每个响应，都会调用此方法进行处理。

process_spider_input()应该返回None或提出异常。

* 如果它返回None，Scrapy将继续处理此响应，执行所有其他中间件，直到最后，响应被交给spider进行处理。
* 如果它引发异常，Scrapy将不会调用任何其他spider中间件的process_spider_input()，将调用请求errback(如果有的话)，否则它将进入process_spider_exception()链
参数：  
　　response（Responseobject） - 正在处理的响应  
　　spider（Spiderobject） - 此响应所针对的spider

2.process_spider_output(self, response, result, spider)

在处理完响应之后，使用Spider返回的结果调用此方法。

process_spider_output()必须返回一个可迭代的 Request，dict或Item 对象。

参数：  
　　response（Responseobject） - 从spider生成此输出的响应  
　　result（可迭代的Request，dict或Item对象） - spider返回的结果  
　　spider（Spiderobject） - 正在处理其结果的spider  

3.process_spider_exception(self, response, exception, spider)

当spider或process_spider_output() 方法（来自先前的spider中间件）引发异常时，将调用此方法。

process_spider_exception()应该返回一个None或一个可迭代的Request，dict或 Item对象。

* 如果它返回None，Scrapy将继续处理此异常，执行process_spider_exception()以下中间件组件中的任何其他组件，直到没有剩余中间件组件并且异常到达引擎（它被记录并丢弃）。
* 如果它返回一个iterable，那么process_spider_output()管道将从下一个spider中间件开始启动，并且不会process_spider_exception()调用其他任何一个 。

参数：
　　response（Responseobject） - 引发异常时正在处理的响应
　　exception（异常对象） - 引发异常
　　spider（Spiderobject） - 引发异常的spider

4.process_start_requests(self, start_requests, spider)

当spider运行到start_requests()的时候，爬虫中间件的process_start_requests()方法被调用

它接收一个iterable（在start_requests参数中）并且必须返回另一个可迭代的Request对象。

参数：  
start_requests（可迭代Request） - 开始请求  
spider（Spiderobject） - 启动请求所属的spider

5.from_crawler(cls, crawler)  

这个类方法通常是访问settings和signals的入口函数

spider中间件总结
1.spider开始start_requests()的时候，spider中间件的process_start_requests()方法被调用

2.下载response成功后，返回到spider 回调函数parse前，调用process_spider_input()

3.当spider yield scrapy.Request()或者yield item的时候，spider中间件的process_spider_output()方法被调用。

4.当spider出现了Exception的时候，spider中间件的process_spider_exception()方法被调用。

## crawlspider
作用:全站数据爬取，处理不在同一页面的数据

创建命令：
```
scrapy startproject xx
cd xx
scrapy genspider -t crawl xxx xxxx.com
```
属性：
```Python
class ChoutiSpider(CrawlSpider):
    name = 'chouti'
    # allowed_domains = ['dig.chouti.com']
    start_urls = ['https://dig.chouti.com']
    # 链接提取器:从起始url对应的页面中提取符合规则的链接，参数allow=正则表达式，提取符合该正则的链接
    link = LinkExtractor(allow=r'Items/')
    rules = (
        # 规则解析器:将链接提取器提取到的链接对应的页面源码进行指定规则(callback)的解析
        # follow=True 将链接提取器继续作用到链接提取器提取到的链接对应的页面源码中(即可以提取到所有分页)
        Rule(link, callback='parse_item', follow=True),
    )
```

## 总结

- scrapy使用流程
    - 创建一个工程:scrapy startproject xxx
    - cd xxx
    - 创建爬虫文件:scrapy genspider xxx www.xxx.com
    - 执行:scrapy crawl xxx
- 持久化存储:
    - 基于终端指令:scrapy crawl xxx -o file_path.csv
        - 好处:便捷
        - 弊端:局限性强(只可以写入本地文件，文件类型有限制)
    - 基于管道：
        - 数据解析
        - 在item类中声明相关的属性用于存储解析到的数据
        - 将解析到的数据存储封装到item类型的对象中
        - 将item对象提交给管道
        - item会被管道类中的process_item方法中的item参数进行接收
        - 在process_item方法中编写基于item持久化存储的操作
        - 在配置文件中开启管道
    - 管道细节处理
        - 管道文件中的一个类表示的是将解析到的数据存储到某一个具体的平台中
        - process_item的返回值(return item)就是将item传递给下一个即将被执行的管道类
        - open_spider, close_spider的使用

- 请求传参
    - 应用场景: 爬取得数据不在同一页面
    - 实现:scrapy.Request(url,callback,meta={'':''})
           callback回调函数内通过response.meta['']调用传递的参数
　　　　
- 中间件
    - 批量拦截请求和响应
    - 拦截请求:UA伪装(process_request), 代理IP(process_exception: return request)
    - 拦截响应:process_response
    - scrapy+selenium

- crawlspider
    作用:全站数据爬取
    - spider的一个子类
    - LinkExtractor:链接提取器:从起始url对应的页面中提取符合规则的链接，参数allow=正则表达式，提取符合该正则的链接
    - Rule:规则解析器:将链接提取器提取到的链接对应的页面源码进行指定规则(callback)的解析
    - 一个链接提取器对用一个规则解析器
