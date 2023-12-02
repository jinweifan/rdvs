##

~~~json
{
  "current_page": 3,
  "current_page_item": 2,
  "target_page": 5
}
~~~

## 爬取行业数据

使用技术：请求库request、解析库xpath、存储mongodb

~~~json
{
  "first_industry": "技术",
  "second_industry": "后端开发",
  "third_industry": "java",
  "url": ""
}
~~~

## 爬取招聘数据

使用技术：请求selenium、解析：xpath、存储mongo

### 目标

1. 不重复爬取，已爬过的数据
2. 爬虫代码的健壮性、记忆性（爬虫中断后，记录中断位置。下一次在终端位置开始爬取）

### 已完成功能

1. 招聘信息的爬取
2. 招聘信息的存储
3. 防止IP封禁

### 待完成功能
1. 将带爬取数据URL等信息放到redis
2. 使用多任务异步协程进行并发爬取数据
3. 

### 解决问题
1. 如何记住爬取数据的位置


## 多任务爬取速度比较
### 多线程

### 多进程



### 协程
有代码调度的线程
