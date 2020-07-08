# -*-coding:utf-8 -*-
import sys

from aliyun_dns_manager import dns_toolkit

if __name__ == '__main__':
    # 删除TXT记录
    file_name, domain, acme_challenge, validation = sys.argv
    dns_toolkit.delete_domain_record(domain_name=domain, host_record_keyword=acme_challenge, type_keyword='TXT',
                                     value_keyword=validation)
