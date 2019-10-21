
class Message():

    def __init__(self, action=0, comment='', information=None):
        if information is None:
            information = []
        self.action = action
        self.comment = comment
        self.information = information


def verify_ip(ip):
    try:
        digits = ip.split('.')
        for item in digits:
            if not item.isdigit():
                return False
            if int(item) > 255:
                return False
    except:
        return False
    return True


def verify_port(port):
    if not port.isdigit():
        return False
    else:
        return True
