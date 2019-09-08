#-*- coding: utf-8 -*-
from freeproxy.settings import REVISE_DICT

class CustomerBase:
    def __init__(self):
        pass

    def fix_security_type(self, value):
        """Revise the security value

        Use dict REVISE_DICT to update the security value as English word

        Args:
            value: Security type value
        
        Returns:
            result is a english words
        """
        return REVISE_DICT[value]
    
    def fix_area(self, value):
        """Revise the area value

        If it's china, use inside. Another is outside
        Args:
            value: Area value
        """
        if value in [u"中国", "cn", "CN", "China", "china"]:
            return "inside"
        else:
            return "outside"