import settings
import time
from api.bi.utils.CacheChart import Cachechart

c = Cachechart.create(ttype=1, key="qwed")
time.sleep(1)
c.update(ttype=2)
