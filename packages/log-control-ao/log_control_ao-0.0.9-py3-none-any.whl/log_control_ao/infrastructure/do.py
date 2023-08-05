from typing import List, Optional
from pydantic import BaseModel

class LogRecordDO(BaseModel):
    log_type: str
    log_domain: str
    log_location: str
    log_line: int
    log_inhalt: str
    creation_time: str
    log_label: List[str]=[]
    log_keywords: List[str]=[]
    combine_keywords: bool = False

class LogItemDO(BaseModel):
    id: str
    log_record: Optional[LogRecordDO]
    status: str