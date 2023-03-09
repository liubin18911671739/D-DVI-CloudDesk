

#!/usr/bin/env python
# coding=utf-8

# ~ ''' Check for new certificates and update db if needed '''
from initdb.lib import Certificates

c = Certificates()
c.update_hyper_pool()
