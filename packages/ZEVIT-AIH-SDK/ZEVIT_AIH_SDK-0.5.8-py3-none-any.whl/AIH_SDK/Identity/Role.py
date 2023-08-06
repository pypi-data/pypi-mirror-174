from AIH_SDK.Identity.IdentityObject import IdentityObject


class Role(IdentityObject):
    
    def __init__(self):
        super().__init__()
        self._endpoint = 'Roles'
    
    
