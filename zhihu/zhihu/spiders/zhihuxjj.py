# -*- coding: utf-8 -*-
import json
from zhihu.items import ZhihuItem,ZhihuActivityItem
from scrapy import Spider,Request
import re
"""
采用scrapy框架爬取知乎的信息，根据某个用户以及设定的深度，爬取其关注的用户列表信息以及更广的用户信息
"""
class ZhihuSpider(Spider):
    # 爬虫的名称
    name='zhihu'
    # 访问网站的域名
    allowed_domains = ["www.zhihu.com"]
    # 开始爬虫的页面链接
    start_urls = ["https://www.zhihu.com/"]
    # 开始的用户ID
    start_user = "jixin"
    # 关注的用户列表链接
    followees_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset={offset}&limit=20'
    # 用户主页链接
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    # 用户活动页
    activities_url = 'https://www.zhihu.com/api/v4/members/{user}/activities?limit=10&desktop=True'
    # 需要爬取的用户信息;locations表示用户的所在城市
    user_include = 'locations'
    #可选内容：locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics
    # 重写爬虫的启动请求
    def start_requests(self):
        # 请求关注者列表的信息
        yield Request(self.followees_url.format(user=self.start_user,offset=0),callback=self.parse_fo)
        # 请求开始的用户的个人信息
        yield Request(self.user_url.format(user=self.start_user,include = self.user_include),callback=self.parse_user)
        # 请求开始的用户的活动信息
        yield Request(self.activities_url.format(user=self.start_user),callback=self.parse_activities)

    # 解析用户主页信息
    def parse_user(self, response):
        # 通过json的方式解析用户数据
        result = json.loads(response.text)
        print(result)
        # 创建一个实体数据类
        item = ZhihuItem()
        # 用户名
        item['user_name'] = result['name']
        # 用户性别
        item['sex'] = result['gender']  # gender为1是男，0是女，-1是未设置
        # 用户签名
        item['user_sign'] = result['headline']
        # 用户头像
        item['user_avatar'] = result['avatar_url_template'].format(size='xl')
        # 用户主页链接
        item['user_url'] = 'https://www.zhihu.com/people/' + result['url_token']
        # 需要爬取的附加信息，比如所在城市
        if len(result['locations']):
            item['user_add'] = result['locations'][0]['name']
        else:
            item['user_add'] = ''
        yield item
    # 解析关注者列表
    def parse_fo(self, response):
        # json方式解析数据
        results = json.loads(response.text)
        # 遍历数据
        for result in results['data']:
            # 请求详细的个人主页信息
            yield Request(self.user_url.format(user=result['url_token'], include=self.user_include),callback=self.parse_user)
            # 请求详细的个人活动页的信息
            yield Request(self.activities_url.format(user=result['url_token']),callback=self.parse_activities)
            if result['url_token'] !=self.start_user:
                # 对关注者的关注者进行遍历，爬取深度depth+=1
                yield Request(self.followees_url.format(user=result['url_token'], offset=0),callback=self.parse_fo)  
            else:
                pass
        #关注列表页是否为尾页
        if results['paging']['is_end'] is False: 
            # 链接地址进行处理
            next_url = results['paging']['next'].replace('http','https')
            yield Request(next_url,callback=self.parse_fo)
        else:
            pass

    # 解析用户活动页数据
    def parse_activities(self,response):
        # 通过json的方式解析用户数据
        result = json.loads(response.text)
        # 用户名
        user_name = result['data'][0]['actor']['name']
        # gender = result['data'][0]['actor']['gender']
        for d in result['data']:
            item = ZhihuActivityItem()
            item['user_name'] = user_name
            print(d['verb'])
            # 回答列表
            if d['verb'] == 'ANSWER_CREATE':
                content = re.sub('<.*?>','',d['target']['content'])
                item['title'] = d['target']['question']['title']
                item['activity_type'] = '回答列表'
                yield item
            # 发表文章列表
            elif d['verb'] == 'MEMBER_CREATE_ARTICLE':
                content = re.sub('<.*?>','',d['target']['content'])
                # print(content)
                item['title'] = d['target']['title']
                item['activity_type'] = '发表文章列表'
                yield item
                # article_list.append([d['target']['title'],content])
            #创建问题列表
            elif d['verb'] == 'QUESTION_CREATE':
                print(d['target']['title'])
                item['title'] = d['target']['title']
                item['activity_type'] = '创建问题列表'
                yield item
            #赞同回答+赞同文章列表
            elif d['verb'] == 'ANSWER_VOTE_UP':
                content = re.sub('<.*?>','',d['target']['content'])
                print(d['target']['question']['title'])
                item['title'] = d['target']['question']['title']
                item['activity_type'] = '赞同回答+赞同文章列表'
                yield item
                # print(content)
                # vote_list.append([d['target']['question']['title'],content])
            # 关注问题列表
            elif d['verb'] == 'QUESTION_FOLLOW':
                print(d['target']['title'])
                item['title'] = d['target']['title']
                item['activity_type'] = '关注问题列表'
                yield item
                # question_follow.append(d['target']['title'])
                # question_follow_number+=1
            #关注话题列表
            elif d['verb'] == 'TOPIC_FOLLOW':
                print(d['target']['name'])
                # topic_follow.append(d['target']['name'])
                # topic_follow_number+=1
                item['title'] = d['target']['name']
                item['activity_type'] = '关注话题列表'
                yield item
            #赞同回答+赞同文章列表
            elif d['verb'] == 'MEMBER_VOTEUP_ARTICLE':
                content = re.sub('<.*?>','',d['target']['content'])
                print(d['target']['title'])
                # print(content)
                # vote_list.append([d['target']['title'],content])
                item['title'] = d['target']['title']
                item['activity_type'] = '赞同回答+赞同文章列表'
                yield item
            #关注专栏列表
            elif d['verb'] == 'MEMBER_FOLLOW_COLUMN':
                print(d['target']['title'])
                # column_follow.append(d['target']['title'])
                item['title'] = d['target']['title']
                item['activity_type'] = '关注专栏列表'
                yield item
            #关注收藏夹列表
            elif d['verb'] == 'MEMBER_FOLLOW_COLLECTION':
                print(d['target']['title'])
                item['title'] = d['target']['title']
                item['activity_type'] = '关注收藏夹列表'
                yield item
            #参加的live列表
            elif d['verb'] == 'LIVE_JOIN':
                print(d['target']['subject'])
                item['title'] = d['target']['subject']
                item['activity_type'] = '参加的live列表'
                yield item
        if result['paging']['is_end'] is False:
            next_url = result['paging']['next']
            yield Request(next_url,callback=self.parse_activities)
        else:
            pass

