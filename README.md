# CertbotHooks（Certbot通配符证书续期工具）（当前仅支持阿里云）

## 需求

 * 安装了Certbot
 * 证书已经申请好并完成了配置
 * Python 3

## 配置

### 安装Python依赖

```
pip install -r requirements.txt
```

### 修改配置

```
vim configs.py
```

将阿里云的ACCESS_KEY_ID和SECRET填上

### 修改hook脚本auth.sh和cleanup.sh

cmd变量要改成自己服务器环境所对应的

如果启动有问题，也可以指定一下PYTHONPATH

### 为auth.sh和cleanup.sh添加执行权限

```
chmod 744 auth.sh
chmod 744 cleanup.sh
chmod 744 deploy.sh
```

## 执行

将脚本目录和通配符证书域名名称改成你自己的

```
certbot-auto certonly --no-self-upgrade --agree-tos --manual-public-ip-logging-ok --manual --manual-auth-hook "/脚本目录/auth.sh" --manual-cleanup-hook "/脚本目录/cleanup.sh" -d "*.celerysoft.com暨通配符证书域名名称" --server https://acme-v02.api.letsencrypt.org/directory
```

## 定时执行

```
crontab -e
```

因为只有在证书有效期 < 30天时，才会执行renew操作，所以定时任务的执行间隔可以增大一些

```
# 更新单个证书
0 6 */7 * * root certbot-auto certonly --no-self-upgrade --agree-tos --manual-public-ip-logging-ok --manual --deploy-hook "/脚本目录/deploy.sh" --manual-auth-hook "/脚本目录/auth.sh" --manual-cleanup-hook "/脚本目录/cleanup.sh" -d "*.celerysoft.com暨通配符证书域名名称" --server https://acme-v02.api.letsencrypt.org/directory
# 更新所有证书
0 6 */7 * * root certbot-auto renew --no-self-upgrade --agree-tos --manual-public-ip-logging-ok --manual --deploy-hook "/脚本目录/deploy.sh" --manual-auth-hook "/脚本目录/auth.sh" --manual-cleanup-hook "/脚本目录/cleanup.sh" --server https://acme-v02.api.letsencrypt.org/directory
```

如果想在更新完证书之后重启一下Nginx，需要编辑一下`deploy.sh`文件，将重启Nginx的命令添加进deploy.sh
当然，你可以执行任何后续操作，只需将命令写进`deploy.sh`文件即可

如果你同时想更新一下七牛的证书，可以看看这个项目：

[https://github.com/celerysoft/QiniuCloudSDK](https://github.com/celerysoft/QiniuCloudSDK)

## 附录

### Certbot 控制台选项简介

[官方文档](https://certbot.eff.org/docs/using.html#certbot-command-line-options)

 * certonly 申请或更新证书，但是不安装（自动更新nginx配置文件）
 * renew 更新所有之前申请的、即将过期的证书
 * --no-self-upgrade 阻止Certbot自动更新
 * --agree-tos 同意用户协议
 * --manual-public-ip-logging-ok 同意记录当前ip地址
 * --keep-until-expiring 如果证书存在，则只在证书快过期时才执行更新操作
 * --force-renewal 如果证书存在，无论它离过期时间还有多久，都立即更新它
 * --manual 
 * --manual-auth-hook
 * --manual-cleanup-hook
 * --deploy-hook
 * -d 需要申请证书的域名，可以使用逗号分隔来一次性指定多个域名
 * --server ACME Directory Resource URI

## License

[Apache License 2.0](./LICENSE)