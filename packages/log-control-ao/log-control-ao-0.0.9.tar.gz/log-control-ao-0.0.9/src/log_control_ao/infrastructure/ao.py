import datetime
from inspect import getframeinfo, stack
from typing import List
import requests, json
from ddd_objects.infrastructure.ao import exception_class_dec
from ddd_objects.domain.exception import return_codes
from ddd_objects.lib import Logger as _Logger
from .do import LogItemDO, LogRecordDO

logger = _Logger()
logger.set_labels(file_name=__file__)
class LogController:
    def __init__(self, ip: str=None, port: int=None) -> None:
        if port is None:
            port = 8080
        if ip is None:
            ip = 'log-control-svc.system-service.svc.cluster.local'
        self.url = f"http://{ip}:{port}"

    def _check_error(self, status_code, info):
        if status_code>299:
            if isinstance(info['detail'], str):
                return_code = return_codes['OTHER_CODE']
                error_info = info['detail']
            else:
                return_code = info['detail']['return_code']
                error_info = info['detail']['error_info']
            logger.error(f'Error detected by log-control-ao:\nreturn code: {return_code}\n'
                f'error info: {error_info}')

    @exception_class_dec(max_try=1)
    def add_record(self, record: LogRecordDO, timeout=3):
        data = json.dumps(record.dict())
        response=requests.post(f'{self.url}/record', data=data, timeout=timeout)
        succeed = json.loads(response.text)
        print(succeed)
        self._check_error(response.status_code, succeed)
        return succeed

    @exception_class_dec(max_try=1)
    def find_unprocessed_items(self, timeout=3):
        response=requests.get(f'{self.url}/unprocessed_items', timeout=timeout)
        items = json.loads(response.text)
        self._check_error(response.status_code, items)
        if items is None:
            return None
        else:
            return [LogItemDO(**m) for m in items]

    @exception_class_dec(max_try=1)
    def update_items_processed(self, items:List[LogItemDO], timeout=3):
        data = json.dumps([m.dict() for m in items])
        response=requests.post(f'{self.url}/items/processed', data=data, timeout=timeout)
        succeed = json.loads(response.text)
        self._check_error(response.status_code, succeed)
        return succeed

class Logger:
    def __init__(
        self, 
        domain, 
        location=None, 
        labels=None,
        keywords=[],
        controller_ip=None, 
        controller_port=None, 
        local:bool=False,
        combine_keywords=False,
    ) -> None:
        self.domain = domain
        self.location = location
        if labels is None:
            labels = ['default']
        self.labels = labels
        self.local = local
        self.keywords = keywords
        self.controller = LogController(controller_ip, controller_port)
        self.combine_keywords = combine_keywords

    def _send_record(
        self, 
        content, 
        record_type, 
        domain=None, 
        location=None, 
        labels=None, 
        keywords=None,
        combine_keywords=None,
    ):
        if domain is None:
            domain = self.domain
        if location is None:
            location = self.location
        if labels is None:
            labels = self.labels
        if keywords is None:
            keywords = self.keywords
        if combine_keywords is None:
            combine_keywords = self.combine_keywords
        caller = getframeinfo(stack()[2][0])
        line_num = caller.lineno
        fn = caller.filename
        if location is None and self.location is None:
            location = fn
        record = LogRecordDO(
            log_type = record_type,
            log_domain = domain,
            log_location = location,
            log_line = line_num,
            log_inhalt = content,
            log_label = labels,
            log_keywords = keywords,
            creation_time = datetime.datetime.utcnow().isoformat(),
            combine_keywords=combine_keywords
        )
        result = self.controller.add_record(record)
        if result.succeed:
            return result.get_value()
        else:
            return False

    def info(
        self, 
        content, 
        domain=None, 
        location=None, 
        labels=None, 
        keywords=None,
        combine_keywords=None,
    ):
        if self.local:
            logger.info(content)
        return self._send_record(content, 'info', domain, location, labels, keywords, combine_keywords)

    def error(
        self, 
        content, 
        domain=None, 
        location=None, 
        labels=None, 
        keywords=None,
        combine_keywords=None,
    ):
        if self.local:
            logger.error(content)
        return self._send_record(content, 'error', domain, location, labels, keywords, combine_keywords)

