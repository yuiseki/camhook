# -*- encoding: utf8 -*-

import traceback
import sys

class TracebackMiddleware():
    def process_exception(self, request, exception):
        print '######################## Exception ##################'
        print '\n'.join(traceback.format_exception(*sys.exc_info()))
        print '-----------------------------------------------------'
#        print repr(request)
        print '#####################################################'
