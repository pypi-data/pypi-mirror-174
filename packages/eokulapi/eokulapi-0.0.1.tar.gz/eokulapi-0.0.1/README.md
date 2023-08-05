# eokulapi
eokul vbs api

## yükleme
`pip install eokulapi`

## basit kullanım
```python
from eokulapi.eokulapi import EokulAPI

user=EokulAPI(uid=...)
user.update_student_list()
st=user.students[0]
user.update_student_data(st)
```