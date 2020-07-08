# -*-coding:utf-8 -*-
import json

from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest

import configs


class AliYunDNSManager:
    def __init__(self):
        self.client = AcsClient(configs.ALIYUN_ACCESS_KEY_ID, configs.ALIYUN_SECRET)

    @staticmethod
    def _data_valid(data) -> bool:
        if type(data) == str:
            return data is not None and len(data) > 0
        else:
            return data is not None

    def add_or_update_domain_record(self, domain_name: str, host_record_keyword: str, type_keyword: str = 'A',
                                    old_value_keyword: str = None, value: str = None):
        response_data = self.get_domain_records(domain_name, host_record_keyword, type_keyword, old_value_keyword)
        record_count = response_data['TotalCount']
        if record_count == 0:
            response_data = self._add_domain_record(
                domain_name=domain_name, host_record=host_record_keyword, record_type=type_keyword, value=value)
            print(response_data)
            return
        elif record_count > 1:
            raise RuntimeError('匹配的解析记录大于1条，无法确定需要修改的记录，请提高搜索精度')

        record = response_data['DomainRecords']['Record'][0]
        record_id = record['RecordId']

        response_data = self._update_domain_record(
            record_id=record_id, host_record=host_record_keyword, record_type=type_keyword, value=value)
        print(response_data)

    def delete_domain_record(self, domain_name: str, host_record_keyword: str, type_keyword: str = 'A',
                             value_keyword: str = None):
        response_data = self.get_domain_records(domain_name, host_record_keyword, type_keyword, value_keyword)
        record_count = response_data['TotalCount']
        if record_count == 0:
            raise RuntimeError('无法找到需要删除的解析记录')
        elif record_count > 1:
            raise RuntimeError('匹配的解析记录大于1条，无法确定需要修改的记录，请提高搜索精度')

        record = response_data['DomainRecords']['Record'][0]
        record_id = record['RecordId']

        response_data = self._delete_domain_record(record_id)
        print(response_data)

    def _add_domain_record(self, domain_name: str, host_record: str, record_type: str, value: str):
        request = AddDomainRecordRequest()
        request.set_accept_format('json')

        request.set_DomainName(domain_name)
        request.set_RR(host_record)
        request.set_Type(record_type)
        request.set_Value(value)

        response = self.client.do_action_with_exception(request)
        response = response.decode('utf-8')
        return json.loads(response)

    def _update_domain_record(self, record_id: str, host_record: str, record_type: str, value: str):
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')

        request.set_RecordId(record_id)
        request.set_RR(host_record)
        request.set_Type(record_type)
        request.set_Value(value)

        response = self.client.do_action_with_exception(request)
        response = response.decode('utf-8')
        return json.loads(response)

    def _delete_domain_record(self, record_id: str):
        request = DeleteDomainRecordRequest()
        request.set_accept_format('json')

        request.set_RecordId(record_id)

        response = self.client.do_action_with_exception(request)
        response = response.decode('utf-8')
        return json.loads(response)

    def get_domain_records(self, domain_name: str, host_record_keyword: str = None, type_keyword: str = 'A',
                           value_keyword: str = None) -> dict:
        if not self._data_valid(domain_name):
            raise RuntimeError('缺少域名名称')

        request = DescribeDomainRecordsRequest()
        request.set_accept_format('json')

        request.set_DomainName(domain_name)
        # request.set_PageSize('100')
        if self._data_valid(host_record_keyword):
            request.set_RRKeyWord(host_record_keyword)
        request.set_TypeKeyWord(type_keyword)
        if self._data_valid(value_keyword):
            request.set_ValueKeyWord(value_keyword)

        response = self.client.do_action_with_exception(request)  # type: bytes
        response_data = json.loads(response.decode('utf-8'))
        return response_data


dns_toolkit = AliYunDNSManager()


if __name__ == '__main__':
    dns_toolkit.add_or_update_domain_record(domain_name='celerysoft.com', host_record_keyword='www',
                                            type_keyword='A', value='1.2.3.4')
    dns_toolkit.delete_domain_record(domain_name='celerysoft.com', host_record_keyword='www',
                                     type_keyword='A', value_keyword='1.2.3.4')
