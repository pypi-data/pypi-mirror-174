from ddd_objects.infrastructure.ao import exception_class_dec
from ddd_objects.infrastructure.repository_impl import error_factory
from ddd_objects.domain.exception import return_codes
import json, requests
from typing import List, Optional
from .do import (
    CommandContextDO,
    CommandSettingDetailDO,
    CommandHostDO,
    BanInstanceTypeRequestDO,
    BannedInstanceTypeResponseDO,
    CommandItemDO,
    CommandRequestDO,
    ConditionDO,
    DNSRecordDO,
    InstanceCreationItemDO,
    InstanceCreationRequestDO,
    InstanceInfoDO,
    InstanceUserSettingDO,
    CommandResponseDO,
)

class VPCController:
    def __init__(self, ip:str, port:str, token:str) -> None:
        self.url = f"http://{ip}:{port}"
        self.header = {"api-token":token}
        result = self.check_connection()
        if not result.succeed or not result.get_value():
            raise ConnectionError(f'Fail to connect vpc control server: {result.error_traceback}')

    def _check_error(self, status_code, info):
        print(status_code)
        if status_code>299:
            if isinstance(info['detail'], str):
                return_code = return_codes['OTHER_CODE']
                error_traceback = info['detail']
            else:
                return_code = info['detail']['return_code']
                error_traceback = info['detail']['error_traceback']
            raise error_factory.make(return_code)(error_traceback)

    @exception_class_dec()
    def check_connection(self, timeout=3):
        response=requests.get(f'{self.url}', headers=self.header, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        if info['message']=='Hello World':
            return True
        else:
            return False

    @exception_class_dec()
    def new_instance(self, condition:ConditionDO, setting:InstanceUserSettingDO, timeout=400):
        data = {
            "condition": condition.dict(),
            "setting": setting.dict()
        }
        data = json.dumps(data)
        response=requests.post(f'{self.url}/instances', 
            headers=self.header, data=data, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        if infos is None:
            return None
        else:
            return [InstanceInfoDO(**info) for info in infos]

    @exception_class_dec()
    def get_instance_by_name(self, region_id: str, name: str, timeout=60):
        response=requests.get(f'{self.url}/instances/region_id/{region_id}/name/{name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [InstanceInfoDO(**info) for info in infos]

    @exception_class_dec()
    def release_instances(self, instance_infos: List[InstanceInfoDO], timeout=60):
        instance_infos = [info.dict() for info in instance_infos]
        data = json.dumps(instance_infos)
        response=requests.delete(f'{self.url}/instances', 
            headers=self.header, data=data, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    @exception_class_dec()
    def run_command(
        self, 
        hosts: List[CommandHostDO],
        commands: List[CommandSettingDetailDO],
        context: Optional[CommandContextDO]=None,
    ):
        timeout = 5
        for c in commands:
            timeout += c.timeout
        hosts = [h.dict() for h in hosts]
        commands = [c.to_json() for c in commands]
        data = {
            "hosts": hosts,
            "commands": commands
        }
        if context is not None:
            context = context.dict()
            data['context'] = context
        data = json.dumps(data)
        response=requests.post(f'{self.url}/instances/command', 
            headers=self.header, data=data, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [CommandResponseDO(**r) if r else None for r in infos]


    @exception_class_dec()
    def create_dns_record(
        self,
        record: DNSRecordDO,
        timeout=30
    ):
        data = record.to_json()
        data = json.dumps(data)
        response = requests.post(f'{self.url}/dns_record',
            headers = self.header, data=data, timeout=timeout
        )
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return DNSRecordDO(**info)

    @exception_class_dec()
    def get_dns_records(
        self,
        domain_name: str,
        timeout=20
    ):
        response = requests.get(f'{self.url}/dns_records/domain_name/{domain_name}', 
            headers=self.header, timeout=timeout)
        infos = json.loads(response.text)
        self._check_error(response.status_code, infos)
        return [DNSRecordDO(**info) for info in infos]

    @exception_class_dec()
    def update_dns_record(self, record: DNSRecordDO, timeout=30):
        data = json.dumps(record.to_json())
        response = requests.put(f'{self.url}/dns_record', 
            headers=self.header, data=data, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return DNSRecordDO(**info)

    @exception_class_dec()
    def delete_dns_record(self, record_id: str, timeout=30):
        response = requests.delete(f'{self.url}/dns_record/record_id/{record_id}',
            headers=self.header, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        return info

    @exception_class_dec()
    def send_instance_creation_request(self, request: InstanceCreationRequestDO, timeout=3):
        data = json.dumps(request.dict())
        response=requests.post(f'{self.url}/instance/request', 
            headers=self.header, data=data, timeout=timeout)
        id = json.loads(response.text)
        self._check_error(response.status_code, id)
        if id is None:
            return None
        else:
            return id

    @exception_class_dec()
    def find_instance_creation_item(self, id: str, timeout=3):
        response=requests.get(f'{self.url}/instance/item/id/{id}', 
            headers=self.header, timeout=timeout)
        item = json.loads(response.text)
        self._check_error(response.status_code, item)
        if item is None:
            return None
        else:
            return InstanceCreationItemDO(**item)

    @exception_class_dec()
    def find_unprocessed_instance_creation_item(self, timeout=3):
        response=requests.get(f'{self.url}/instance/item/unprocessed', 
            headers=self.header, timeout=timeout)
        item = json.loads(response.text)
        self._check_error(response.status_code, item)
        if item is None:
            return None
        else:
            return InstanceCreationItemDO(**item)

    @exception_class_dec()
    def update_instance_creation_item(self, item:InstanceCreationItemDO, timeout=10):
        data = json.dumps(item.dict())
        response=requests.put(f'{self.url}/instance/item', 
            headers=self.header, data=data, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, succeed)
        return succeed

    @exception_class_dec()
    def clear_instance_creation_item(self, timeout=3):
        response=requests.get(f'{self.url}/instance/item/clear', 
            headers=self.header, timeout=timeout)
        n = json.loads(response.text)
        self._check_error(response.status_code, n)
        return n

    @exception_class_dec()
    def delete_instance_creation_item(self, item_id:str, timeout=3):
        response=requests.delete(f'{self.url}/instance/item/id/{item_id}', 
            headers=self.header, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, succeed)
        return succeed

    @exception_class_dec()
    def send_ban_instance_type_request(self, request: BanInstanceTypeRequestDO, timeout=3):
        data = json.dumps(request.dict())
        response=requests.post(f'{self.url}/instance_type/ban_queue/request', 
            headers=self.header, data=data, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, id)
        if succeed is None:
            return None
        else:
            return succeed

    @exception_class_dec()
    def find_banned_instance_types(self, region_id:str, zone_id:str, timeout=3):
        response=requests.get(f'{self.url}/instance_type/ban_queue/region_id/{region_id}/zone_id/{zone_id}', 
            headers=self.header, timeout=timeout)
        item = json.loads(response.text)
        self._check_error(response.status_code, item)
        if item is None:
            return None
        else:
            return BannedInstanceTypeResponseDO(**item)

    @exception_class_dec()
    def check_instance_type_banned(self, request: BanInstanceTypeRequestDO, timeout=3)->Optional[bool]:
        data = json.dumps(request.dict())
        response=requests.get(f'{self.url}/instance_type/check_banned', 
            headers=self.header, data=data, timeout=timeout)
        banned = json.loads(response.text)
        self._check_error(response.status_code, banned)
        if banned is None:
            return None
        else:
            return banned

    @exception_class_dec()
    def get_command_queue_info(self, timeout=3):
        response=requests.get(f'{self.url}/command/queue/info', 
            headers=self.header, timeout=timeout)
        info = json.loads(response.text)
        self._check_error(response.status_code, info)
        if info is None:
            return None
        else:
            return info

    @exception_class_dec()
    def send_command_request(self, request: CommandRequestDO, timeout=3):
        data = json.dumps(request.dict())
        response=requests.post(f'{self.url}/command/queue/request', 
            headers=self.header, data=data, timeout=timeout)
        id = json.loads(response.text)
        self._check_error(response.status_code, id)
        if id is None:
            return None
        else:
            return id

    @exception_class_dec()
    def find_command_item(self, id: str, timeout=3):
        response=requests.get(f'{self.url}/command/queue/id/{id}', 
            headers=self.header, timeout=timeout)
        item = json.loads(response.text)
        self._check_error(response.status_code, item)
        if item is None:
            return None
        else:
            return CommandItemDO(**item)

    @exception_class_dec()
    def find_unprocessed_command_item(self, timeout=3):
        response=requests.get(f'{self.url}/command/queue/unprocessed', 
            headers=self.header, timeout=timeout)
        item = json.loads(response.text)
        self._check_error(response.status_code, item)
        if item is None:
            return None
        else:
            return CommandItemDO(**item)

    @exception_class_dec()
    def update_command_item(self, item:CommandItemDO, timeout=10):
        data = json.dumps(item.dict())
        response=requests.put(f'{self.url}/command/queue', 
            headers=self.header, data=data, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, succeed)
        return succeed

    @exception_class_dec()
    def clear_command_item(self, timeout=3):
        response=requests.get(f'{self.url}/command/queue/clear', 
            headers=self.header, timeout=timeout)
        n = json.loads(response.text)
        self._check_error(response.status_code, n)
        return n

    @exception_class_dec()
    def delete_command_item(self, item_id:str, timeout=3):
        response=requests.delete(f'{self.url}/command/queue/id/{item_id}', 
            headers=self.header, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, succeed)
        return succeed
