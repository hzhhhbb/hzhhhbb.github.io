---
layout: default
title: 使用SSH连接GitHub
nav_order: 2
parent: git
description: 使用SSH连接GitHub的配置说明
---

# 使用SSH连接GitHub

## 关于SSH
使用SSH协议，可以连接到远程服务器和服务并进行身份验证。 使用SSH密钥，可以连接到GitHub，而无需在每次访问时都提供用户名或密码。

## 生成新的 SSh Key 

1. 打开 Git Bash 并输入以下命令(用你的GitHub电子邮件地址替换命令中的电子邮件地址)
    ```
    $ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```

2. 当看到以下命令提示时，按回车，就会把文件存在默认的路径下（可以改路径，改路径后，在后边的操作需要额外的操作，这里我不改路径）
    ```
    > Enter a file in which to save the key (/c/Users/you/.ssh/id_rsa):
    ```

3. 当看到以下命令提示时，输入自定义密码（不是GitHub密码），这个密码在连接GitHub时会用到，比如pull、push的时候
    ```
    > Enter passphrase (empty for no passphrase): [Type a passphrase]
    > Enter same passphrase again: [Type passphrase again]
    ```
4. 确保生成成功
    - 当在目录c/Users/you/.ssh/下看到刚才生成的文件时（id_rsa、id_rsa.pub），表示生成成功


## 把 SSh Key 添加到 ssh-agent
1. 确保 ssh-agent 在运行
    - 一般情况下，都是自动启动的
    - 也可以用以下命令手动启动(输出：Agent pid 59566)
        ```
        eval $(ssh-agent -s)
        ```
2. 把SSH 私钥添加到ssh-agent。如果你使用其他名称创建密钥，或者要添加具有其他名称的现有密钥，使用私有密钥文件的名称替换命令中的id_rsa。
    ```
    $ ssh-add ~/.ssh/id_rsa
    ```

## 把SSH Key添加到Github账号中
将新的SSH密钥添加到GitHub帐户后，就可以重新配置任何本地仓库以使用SSH。

1. 复制SSH Key
    - 执行命令复制
        ```
        $ clip < ~/.ssh/id_rsa.pub
        ```
    - 打开c/Users/you/.ssh/id_rsa.pub文件手动复制

2. 在GitHub网站页面，点击右上角的个人头像，点击Settings

    [![GitHub Settings](/assets/images/docs/git/connecting-to-github-with-ssh/githubSettings.png "GitHub Settings")](https://github.com/settings/profile)

3. 点击左侧栏目中的“SSH and GPG keys”

    [![SSH and GPG keys](/assets/images/docs/git/connecting-to-github-with-ssh/sshAndGPGKeys.png "SSH and GPG keys")](https://github.com/settings/keys)

4. 点击右上角的“New SSH key”

    [![New SSH key](/assets/images/docs/git/connecting-to-github-with-ssh/newSSHKey.png "New SSH key")](https://github.com/settings/ssh/new)

5. 在打开的页面中的Title中填入这个key的描述，如Company Computer；在Key中粘贴复制的SSH Key；然后点击Add SSH Key按钮

    [![Add SSH key](/assets/images/docs/git/connecting-to-github-with-ssh/addSSHKey.png "Add SSH key")](https://github.com/settings/ssh/new)

6. 在弹出的页面中输入Github密码
7. 完成添加

## 把本地仓库的远程URL从HTTPS切换到SSH
1. 打开Git Bash
2. 切换到本地仓库根目录
3. 查看当前仓库使用的仓库地址
    ```
    $ git remote -v
    > origin  https://github.com/USERNAME/REPOSITORY.git (fetch)
    > origin  https://github.com/USERNAME/REPOSITORY.git (push)
    ```
4. 切换
    ```
    $ git remote set-url origin git@github.com:USERNAME/REPOSITORY.git
    ```
5. 验证
    ```
    $ git remote -v
    # Verify new remote URL
    > origin  git@github.com:USERNAME/REPOSITORY.git (fetch)
    > origin  git@github.com:USERNAME/REPOSITORY.git (push)
    ```
6. 其他方法
    打开本地仓库目录中的.git文件夹，找到config文件，修改其中的url值

## Done
到此，切换完成。后续的pull、push等操作就会使用SSH了


