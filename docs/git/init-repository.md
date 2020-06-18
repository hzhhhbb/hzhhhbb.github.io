---
layout: default
title: 初始化仓库
nav_order: 1
parent: git
description: 介绍初始化仓库的一般步骤
---

# 初始化仓库步骤
1. 在远程仓库（如github）创建空仓库
2. 打开命令行
3. 切换到本地项目目录
4. 初始化本地仓库
```
git init
```

5. 添加全部文件到本地仓库
```
git add .
```

6. 提交文件到本地仓库
```
git commit -m "init"
```

7. 复制远程仓库地址，HTTPS、SSH都可
8. 添加远程仓库地址到本地仓库
```
git remote add origin {远程仓库地址}
```
可以用以下命令验证
```
git remote -v
```
9. push本地仓库文件到远程仓库
```
git push -u origin master
```
10. Done