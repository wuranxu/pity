[English](https://github.com/wuranxu/pity/blob/main/README_EN.md)

![png](https://img.shields.io/badge/Python-3.8+-green)
![png](https://img.shields.io/badge/React-17+-blue)
![png](https://img.shields.io/badge/FastApi-green)
![png](https://img.shields.io/badge/contributors-3-green)

> ~~pity正在微服务化中，近期功能迭代暂缓。~~
> 
> 由于微服务个人来做能力实在有限，不走弯路了，继续开发功能...

### 🎉 技术栈

- [x] 🎨 FastApi(前期Flask，所以教程初期也是Flask)
- [x] 🎶 SQLAlchemy(你可以看到很多sqlalchemy的用法) 
- [x] 🎉 Apscheduler(定时任务框架) 
- [x] 🎃 mitmproxy(mock，用例录制生成) 
- [x] 🔒 Redis
- [x] 🏐 Gunicorn(内含uvicorn，部署服务)
- [x] 🎲 Nginx(反向代理，https配置等)
- [x] 💎 七牛云oss(用于文件上传时接口测试文件存储)
- [x] 👟 asyncio(几乎全异步写法，值得参考)
- [ ] ⛏ Grpc(支持Grpc请求，即将支持) 

### ⚽ 前端地址

  [🎁 快点我](https://github.com/wuranxu/pityWeb)

![](https://static.pity.fun/picture/20220807220041.png)


## ☕ 说明

这是一个具备完整`开发手册`(开发手册，手把手教那种)，严格按照`写一块内容`，`补一篇文章`的形式创作而成，其中也经历了从`Flask`到`FastApi`
的快速过渡。也许代码质量没有很高，但是对于新人来说，跟着一步一步，不但可以完成从`接口自动化框架`到`接口自动化平台`的转变，还能从中看到作者不断优化的过程。

如果你也想从0到1开始打造一个测试平台，那`pity`将是你不二的选择。话不多说，赶快开始体验吧！靓仔靓女们~

<details open="open">
<summary>火热开发中</summary>

| 功能点      | 敬请期待             |
|:---------|:-----------------|
| 数据工厂     | 🍔🍔🍔🍔         |
| Locust结合 | 🍔🍔🍔🍔🍔 |
| Mock     | 🍔             |

</details>


[在线体验 🍍](https://pity.fun/)

<details open="open">
<summary>🌙 已有功能</summary>

| 功能点            | 状态  |
|:---------------|:----|
| 精美的邮件/钉钉通知模板   | ✅  |
| 用例录制生成 🔥      | ✅   |
| har导入 🔥       | ✅   |
| http测试         | ✅   |
| 测试集合           | ✅   |
| 定时任务           | ✅   |
| 全局变量           | ✅   |
| 自定义脚本          | ✅   |
| 场景测试           | ✅   |
| 后台管理           | ✅   |
| 文件上传测试         | ✅   |
| 在线SQL          | ✅   |
| 在线Redis        | ✅   |
| 测试报告           | ✅   |
| 项目管理           | ✅   |
| 权限系统           | ✅   |
| 串行/并行执行用例      | ✅   |
| 参数提取           | ✅   |

</details>

### 🚚 即将到来

| 功能点          | 敬请期待 |
|:-------------|:-----|
| CI/CD        | 🎉🎉🎉   |
| HttpRunner支持 | 🎉🎉🎉   |
| 数据工厂         | 🎉🎉🎉   |
| 精准测试         | 🎉🎉🎉   |
| 组织架构         | 🎉🎉🎉   |
| 用例评分         | 🎉🎉🎉   |

<details>
<summary>平台预览(点击可展开)</summary>

#### 🍦 工作台

![](https://static.pity.fun/picture/2022-2-28/1646063228180-image.png)

#### 测试计划

![](https://static.pity.fun/picture/2022-2-25/1645803999678-image.png)

#### 测试报告

![](https://static.pity.fun/picture/2022-2-25/1645804075353-image.png)

#### 测试用例

![](https://static.pity.fun/picture/2022-2-25/1645804276470-image.png)

#### 钉钉通知

![](https://static.pity.fun/picture/20220813173821.png)


#### SQL客户端

![](https://static.pity.fun/picture/2022-2-25/1645804151559-image.png)

#### 项目管理

![项目管理](https://static.pity.fun/picture/2022-2-26/1645854332681-image.png)

</details>

## ✉ 使用文档

[使用文档(github)](https://wuranxu.github.io/pityDoc/)

[备用地址(gitee)](https://woodywrx.gitee.io/pityDoc/)

## 😊 开发参考文章

[开发文档-公众号](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyMjUwOTk5Mw==&action=getalbum&album_id=1983195471686762500&scene=173&from_msgid=2247484522&from_itemidx=8&count=3&nolastread=1#wechat_redirect)

[开发文档-掘金](https://juejin.cn/column/6977933898952998926)

### 😢 关于Pity平台

pity是一款专注于api自动化的工具，采用`Python`+`FastApi`+`React`开发，目前还不能作为生产级别的工具，作者正在努力之中。

这个项目叫pity，一个从0开始写的自动化测试平台(基于FastApi)，旨在总结自己最近几年的工作经验，也顺便帮助大家进步。目前还在火热更新中，基本上每周都会更新几篇吧，前期以教学+编码为主，后期以实现功能为主。希望大家能够喜欢！~

项目起源是本人很期待的某家公司🐧拒绝了我，觉得特别遗憾吧😅。加上这一年`浑浑噩噩`的，也没有什么产出，做的东西不如18，19年多。所以打算把自己18-19的项目重写出来，给大家一些参考。

### Docker部署

1. 安装Docker Desktop
2. 打开终端并进入pity目录
3. 执行以下命令，安静等待pity启动即可（不需要额外安装mysql redis等，一键启动直接起飞）

  **docker镜像由卫衣哥（QYZHG倾情制作👏👏👏）**

```bash
docker-compose -f .\ops\docker-compose.yaml up
```

### 🎉 二次开发

1. 拉取代码

```bash
$ git clone https://github.com/wuranxu/pity
$ cd pity
```

2. 安装依赖

```bash
# 可换豆瓣源或者清华源安装依赖
$ pip install -r requirements.txt
```

3. 安装并启动redis

4. 安装并启动mysql

5. 修改conf/dev.env

修改其中mysql和redis连接信息，redis虽然可以不开启，但是会导致`定时任务重复执行`（基于redis实现了分布式锁）。

6. 启动服务

```bash
$ python pity.py
```

7. 注册用户

打开浏览器输入: `http://localhost:7777`进入登录页。

点击注册按钮，第一个注册的用户会成为`超级管理员`，拥有一切权限。

![](https://static.pity.fun/picture%2F%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20220504235808.png)

登录后就可以开启pity之旅啦！

### 📞 作者介绍

    大家好，我是米洛，一个乐于分享，喜欢钻研技术的测试开发工程师，目前就职于上海某互联网公司。

    一个打游戏不拿首胜不睡觉的韭0后。

    个人技术公众号: `米洛的测开日记`，欢迎大家关注我，掌握最新测试开发知识。

![](https://static.pity.fun/picture/2022-1-1/1641020334827-qrcode_for_gh_f52fb2135f68_430.jpg)

### ❤️ 平台初心

虽说各大公司都有自己的接口测试平台，并且做的肯定比我的强。但是还是有`很多公司`，并没有这样的条件去投入人力专职开发接口测试平台。

博主我在18年的时候接触到了Yapi这款接口文档管理工具，那是去哪儿团队开发的，但现在已经连官网都找不到了，仅仅只留下一个github.io的地址，让人叹息。

扯远了，我看到他们大前端团队开源了如此一款精美的工具，内心也是激动万分。

人活一辈子，并不长久，总得做些有意义的事情。虽然开源这件事情基本上没有什么收益可言，但总得有人做，世界才会`更美好`是不？

所以我打算制作这样一款工具，面向的就是中小型公司，他们没有那么多时间/人力成本，甚至是测试资源较为匮乏，那么如果你来到了这儿，我想这款工具可以给你们带来帮助！如果是有一定的经验的Python测试开发，这款工具也可以给你带来一定的借鉴作用。

### 💪 落地效果

可能有人会怀疑项目是否能真正运用到生产系统里，这款工具其实是我在某大型共享单车公司实践2年多的一款工具。之前是golang开发，如今我离开那家公司，打算保留原本功能的基础之上进一步优化，并新增更多丰富的特性。所以大家可以放心，它绝对是一款能方便解决你api自动化测试的利器。

### 😊 已有功能

+ [x] 🔥 完善的用户登录/注册机制，提供第三方(github)登录
- [x] 🀄 完善的项目管理机制
* [x] 🚴 结合FastApi，利用asyncio让Python代码也可以起飞
- [x] 💎 完整的接口测试流程
- [x] 📝 强大的数据构造器, 解决接口数据依赖问题
- [x] 🎨 在线调试http请求，堪比网页版本postman
- [x] 🍷 完善的全局变量机制，拒绝case中的死数据
- [x] 🚀 速度还挺快的
- [x] 🐍 在线redis请求
- [x] 🐎 测试计划/集合
- [x] 🙈 在线数据库ide，数据库管理功能
- [x] 📰 漂亮的邮件通知
- [x] 😹 定时构建测试用例
- [x] 🐧 精美的测试报告展示页面

## 🙋 待开发的功能

- [ ] 💀 app管理功能，支持app的导入和导出

* [ ] 😼 ~~代码覆盖率增量/全量统计功能~~

- [ ] 🐘 微服务化
- [ ] 🐄 数据工厂，强大的造数功能
- [ ] 🐸 用例支持har，jmx等格式导入
- [ ] 👍 CI/CD，类pipeline功能
- [ ] 🌼 推送功能，支持钉钉/企信推送
- [ ] 🌛 支持dubbo/grpc
- [ ] 🐛 打通yapi
- [ ] 🌽 等等等等

### 赞助

如果您觉得这个项目对你`有所帮助`，可以请我吃根辣条哦~或者帮忙点个star，让我创作更有动力！！！谢谢大家啦！

![](http://oss.pity.fun/picture/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20220513224046.jpg
)

![](http://oss.pity.fun/picture/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20220513224054.jpg)

### 🏅️ 金牌赞助商（排名不分先后）

- All Fiction
- Vic
- 老虎哥
- 晴天
- 春熙路
- 方总
- 榜一大哥
- 汤总
- 我去热饭
- Bluesqiang
- 全国知名气人代练
- 鸡哥

## 🎨 微信交流群

二维码会经常过期，可以加我个人微信: `wuranxu`，我拉你到群聊。

![](https://static.pity.fun/picture/2022-1-2/1641097484952-ddff5bf23bdccaaf23fa227aa2e9957.jpg)