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

### 修改hook脚本authenticator.sh和cleanup.sh

cmd变量要改成自己服务器环境所对应的

如果启动有问题，也可以指定一下PYTHONPATH

## 执行

将脚本目录和通配符证书域名名称改成你自己的

```
certbot-auto certonly --no-self-upgrade --agree-tos --manual --manual-auth-hook "/脚本目录/authenticator.sh" --manual-cleanup-hook "/脚本目录/cleanup.sh" -d "*.celerysoft.com暨通配符证书域名名称" --server https://acme-v02.api.letsencrypt.org/directory
```

## 定时执行

```
crontab -e
```

因为只有在证书有效期 < 30天时，才会执行renew操作，所以定时任务的执行间隔可以增大一些

```
# 更新单个证书
0 6 */7 * * root certbot-auto certonly --no-self-upgrade --agree-tos --manual --manual-auth-hook "/脚本目录/authenticator.sh" --manual-cleanup-hook "/脚本目录/cleanup.sh" -d "*.celerysoft.com暨通配符证书域名名称" --server https://acme-v02.api.letsencrypt.org/directory
# 更新所有证书
0 6 */7 * * root certbot-auto renew --no-self-upgrade --agree-tos --manual --manual-auth-hook "/脚本目录/authenticator.sh" --manual-cleanup-hook "/脚本目录/cleanup.sh" --server https://acme-v02.api.letsencrypt.org/directory
```

如果想在更新完证书之后重启一下Nginx

```
# 确保 service nginx restart 能使用
# 更新单个证书
0 6 */7 * * root certbot-auto certonly --no-self-upgrade --agree-tos --manual --deploy-hook "service nginx restart" --manual-auth-hook "/脚本目录/authenticator.sh" --manual-cleanup-hook "/脚本目录/cleanup.sh" -d "*.celerysoft.com暨通配符证书域名名称" --server https://acme-v02.api.letsencrypt.org/directory
# 更新所有证书
0 6 */7 * * root certbot-auto renew --no-self-upgrade --agree-tos --manual --deploy-hook "service nginx restart" --manual-auth-hook "/脚本目录/authenticator.sh" --manual-cleanup-hook "/脚本目录/cleanup.sh" --server https://acme-v02.api.letsencrypt.org/directory

```

## License

[Apache License 2.0](./LICENSE)