# MyRoute

这是一个学习经验分享网站，使用`python2.7`，`flask`框架搭建，数据库使用`mongodb`。

-------------------------------

互联网上学习资料非常多，但是对其分类汇总的比较少。

知乎，达到汇总的作用，质量也很高，但是不是专门的汇总网站，分类也不是专为此设计，想找到需要的学习资料汇总也要花费很多时间。

如果只是单纯的资料汇总，会比较杂乱，容易找不到学习方向。所以我们想到使用`学习路线`这种形式组织资料。

不只是用来查询，更多的用来进行交流和问答。

## 愿景 

成为一个分类完善的学习交流社区，大牛可以在此分享学习经验和资料，同学们可以在此讨论学习中的问题。

## 现状
着重实现了学习经验以及学习资料的分享。
* 实现了完善的分类系统
  - 大类页面
  - 面包屑导航
  - 子分类中热门路线的展示
* 实现了学习路线的创建，学习资料的添加，资料的完成，路线的评价
* 实现了同学学习情况的记录

交流部分暂时使用disqus的评论系统达到比较完善的评论功能。

## 前台
* 使用了自定义修改的bootstrap，在实现响应式布局的情况下让界面更美观

## 安全性
* 帐户密码加盐哈希保存，即使拖库用户密码不会泄露。
* 对用户上传的标签及其属性进行过滤，预防xss
