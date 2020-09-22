# -*-coding:utf-8 -*-
import sys
import time

from aliyun_dns_manager import dns_toolkit

if __name__ == '__main__':
    # 添加TXT记录
    file_name, domain_name, acme_challenge, validation = sys.argv
    dns_toolkit.add_or_update_domain_record(domain_name=domain_name, host_record_keyword=acme_challenge,
                                            type_keyword='TXT', value=validation)
    # 确保DNS记录已经刷新
    time.sleep(0.05)
