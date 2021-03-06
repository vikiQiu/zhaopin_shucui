# coding=utf-8
'''
viki - 2016.11.08
scrapy: 1.0.3
python: 2.7.12
system: mac10,windows8
output coding: utf-8
'''  

import scrapy
from qiancheng.items import QianchengItem
import time
import datetime

class QianchengSpider(scrapy.Spider):
    name = "qiancheng"

    DOWNLOAD_DELAY = 1
    COOKIES_ENABLED=False

    page_num=1
    date=''
    keyword='数据挖掘'

    def get_yesterday(self):
        yesterday = str(datetime.date.today() - datetime.timedelta(days=2))
        print('##### yesterday is %s #######' % yesterday)
        yesterdays = yesterday.split('-')
        return(yesterdays[1] + '-' + yesterdays[2])

    def start_requests(self):
        # today = time.strftime('%m-%d',time.localtime(time.time()))
        self.date = self.get_yesterday()
        #keywords=['数据挖掘','数据分析','大数据','机器学习']
        # keywords=['数据挖掘']

        url='http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=000000%2C00&district=000000&funtype=0000&keyword='+self.keyword+'&keywordtype=2&curr_page='+str(self.page_num)+'&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9'
        print ('######################  第%d页(%s): %s ###################' % (self.page_num, self.keyword, url))
        yield scrapy.Request(url=url, callback=self.parse_page)
#
    def parse_page(self, response):
        print('####### begin #######')
        dates=response.xpath('//span[@class="t5"]/text()').extract()
        print (dates[1])
        if dates[1] < self.date: 
            print('over')
            return
        # if dates[len(dates)-1] > self.date: 
        #     print('continue page is', self.page_num)
        #     self.get_nextPage()
        #     print('after nextpage, page is', self.page_num)
        #     return
        bodys=response.css('div.el')
        for index,body in enumerate(bodys):
            url=body.xpath('./p[@class="t1 "]/span/a/@href').extract_first()
            if url is None:
               continue
            print(url)
            if index>30: break
            #print '＃＃＃＃第%d个岗位########## new new new' % index
            item=QianchengItem()
            item['date']=body.css('span.t5::text').extract_first()
            if item['date'] != self.date: continue
            item['job_name']=body.css('p.t1 span a::attr(title)').extract_first()
            item['job_url']=url
            item['job_enterprise']=body.css('span.t2 a::attr(title)').extract_first()
            item['job_place']=body.css('span.t3::text').extract_first()
            if body.css('span.t4::text'):
               item['salary']=body.css('span.t4::text').extract_first()
            else:
               item['salary']='Null'
            yield scrapy.Request(url=url,callback=self.parse_content,meta=item)
            item['edu']=response.css('em.i2::text').extract_first()
            item['keyword']=self.keyword; print('####### %s ######' % self.keyword)
        self.page_num = self.page_num+1
        print('page_num is ',self.page_num)
        url='http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=000000%2C00&district=000000&funtype=0000&keyword='+self.keyword+'&keywordtype=2&curr_page='+str(self.page_num)+'&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9'
        print ('######################  第%d页(%s):%s  ###################' % (self.page_num, self.keyword, url))
        yield scrapy.Request(url=url, callback=self.parse_page)
            
    def parse_content(self,response):
        item=response.meta
        temp=response.css('span.sp4')
        # @ education
        # edu=temp.re(r'<em class="i2"></em>\s*(.*)</span>')
        # item['edu']=edu if len(edu)==1 else 'Null'
        # 下面不用判断null
        item['edu']=response.xpath('//em[@class="i2"]/parent::span/text()').extract_first()
        # @ 招聘人数
        # num=temp.re(r'<em class="i3"></em>\s*(.*)</span>')
        # item['job_num']=num if len(num)==1 else 'Null'
        item['job_num']=response.xpath('//em[@class="i3"]/parent::span/text()').extract_first()
        # @ 工作经验
        # exp=temp.re(r'<em class="i1"></em>\s*(.*)</span>')
        # item['job_exp']=exp if len(exp)==1 else 'Null'
        item['job_exp']=response.xpath('//em[@class="i1"]/parent::span/text()').extract_first()
        # @ 具体信息
        temp=response.xpath('//div[@class="bmsg job_msg inbox"]/text()').extract()
        info=''
        for i in temp:
            info=info+i.strip()
        item['job_info']=info
        # @ 公司信息
        temp=response.xpath('//p[@class="msg ltype"]/text()').extract_first().split()
        item['enterprise_attr']=temp[0]
        item['enterprise_scale']=temp[2]
        item['enterprise_industry']=temp[4]

        yield item





