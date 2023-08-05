# -*- coding: utf-8 -*-
"""
    * vcf-tools
    * Created by liuxiaodong on 2022/10/16.
    * Change Activity:
    *     liuxiaodong   2022/10/16.
"""

import json
import base64
import re
from datetime import datetime
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import hashes
from license_manager.utils import Hardware

class LicenseException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


LICENSE_CHECK_LIST = ['mac']

class License():
    def __init__(
        self,
        privateStorePath: str = None,
        privateStorePass: str = None,
        publicStorePath: str = None,
        publicStorePass: str = None
    ):
        '''
        
        '''
        self.privateStorePath = privateStorePath
        self.privateStorePass = privateStorePass
        self.publicStorePath = publicStorePath
        self.publicStorePass = publicStorePass
        self.licensePath = None
        self.private_key = None
        self.public_key = None
        self.license_content = None

        self.load_private_key()
        self.load_public_key()

    def load_private_key(self):
        if not self.privateStorePath or not self.privateStorePass:
            return

        with open(self.privateStorePath, 'rb') as f:
            private_key, _, _ = pkcs12.load_key_and_certificates(f.read(), self.privateStorePass.encode('utf-8'))
            self.private_key = private_key

    def load_public_key(self):
        if not self.publicStorePath or not self.publicStorePass:
            return
        
        with open(self.publicStorePath, 'rb') as f:
            _, _, additional_certificates = pkcs12.load_key_and_certificates(f.read(), self.publicStorePass.encode('utf-8'))
            self.public_key = additional_certificates[0].public_key()
    
    def install(self, licensePath: str, params=None):
        self.licensePath = licensePath
        if not self.licensePath:
            raise LicenseException('licensePath missing')

        with open(self.licensePath, 'rb') as f:
            text = f.read()
            b = base64.b64decode(text)
            license_data = json.loads(b.decode('utf-8'))
            content = license_data.get('content')
            signature = license_data.get('signature')
            if not content or not signature:
                raise LicenseException('license file invalid')

            b = content.encode('utf-8')
            signature_bin = base64.b64decode(signature)

            self.public_key.verify(signature_bin, b, hashes.SHA256())
            self.license_content = json.loads(content)
            self.verify(params)

    def init_license_data(self, subject, consumerType, consumerAmount, description, issuedTime: str, expiryTime: str, params: dict = None):
        data = {
            'subject': subject,
            'consumerType': consumerType,
            'consumerAmount': consumerAmount,
            'description': description,
            'validation': {}
        }
        keys = set()
        params = params or {}

        if issuedTime is not None:
            if not re.match('\d{4}-\d{2}-\d{2}', issuedTime):
                raise LicenseException('issuedTime 格式错误，比如： 2022-01-01')
            data['issuedTime'] = issuedTime
        if expiryTime is not None:
            data['expiryTime'] = expiryTime
            if not re.match('\d{4}-\d{2}-\d{2}', expiryTime):
                raise LicenseException('expiryTime 格式错误，比如： 2022-01-01')
        
        for k, _ in params.items():
            data['validation'][k] = params[k]

        return data

    def create(self, subject: str = 'castiron', consumerType: str = 'customer', consumerAmount: int = 1, description: str = '', issuedTime: str = None, expiryTime: str = None, params: dict = None, output: str = None):
        if not self.private_key:
            raise LicenseException('private store info not found')  
        data = self.init_license_data(subject, consumerType, consumerAmount, description, issuedTime, expiryTime, params)
        s = json.dumps(data)
        b = s.encode('utf-8')
        signature = self.private_key.sign(b, hashes.SHA256())
        base_code = base64.b64encode(signature).decode()
        license_data = {
            'content': s,
            'signature': base_code
        }
        r = json.dumps(license_data).encode('utf-8')
        c = base64.b64encode(r)
        if output is not None:
            with open(output, 'wb') as f1:
                f1.write(c)
        
        return c

    def verify(self, params: dict = None):
        if not self.license_content:
            raise LicenseException('not found license')
        hardware_info = Hardware.get_info()
        params = params or {}
        params = {**hardware_info, **params}
        issuedTime = self.license_content.get('issuedTime')
        expiryTime = self.license_content.get('expiryTime')
        now  = datetime.now()
        if issuedTime:
            issuedDate = datetime.strptime(issuedTime, "%Y-%m-%d")
            if now < issuedDate:
                raise LicenseException(f'证书还未到生效时间: {issuedTime} ~ {expiryTime}')

        if expiryTime:
            expiryDate = datetime.strptime(expiryTime, "%Y-%m-%d")
            if now > expiryDate:
                raise LicenseException(f'证书已过期: {issuedTime} ~ {expiryTime}，请重新申请证书！')
        
        params = params or {}
        if self.license_content.get('validation'):
            validation = self.license_content['validation']
            for k, v in validation.items():
                if params.get(k) != v:
                    errmsg = f'证书 {k} 不匹配，请重新申请证书！'
                    raise LicenseException(errmsg)
            

if __name__ == '__main__':
    license = License(
        privateStorePath='keystores1/privateKeys.store',
        privateStorePass='castironPrivateKey2022'
    )

    hardware_info = Hardware.get_info()
    r = license.create(
        subject='test',
        issuedTime='2022-10-01',
        expiryTime='2023-10-03',
        params = {
            'mac': hardware_info.get('mac')
        },
        output='license.lic'
    )

    ######

    license = License(
        publicStorePath='keystores1/publicCerts.store',
        publicStorePass='castironPublicKey2022'
    )

    license.install('./license.lic')
    print('证书安装成功')
