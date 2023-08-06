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
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from datetime import datetime
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
        privateKeyPath: str = None,
        privateKeyPass: str = None,
        publicKeyPath: str = None,
        publicKeyPass: str = None
    ):
        '''
        
        '''
        self.privateKeyPath = privateKeyPath
        self.privateKeyPass = privateKeyPass
        self.publicKeyPath = publicKeyPath
        self.publicKeyPass = publicKeyPass
        self.licensePath = None
        self.private_key = None
        self.public_key = None
        self.license_content = None

        self.load_private_key()
        self.load_public_key()

    def load_private_key(self):
        if not self.privateKeyPath:
            return

        with open(self.privateKeyPath, 'rb') as f:
            self.private_key = RSA.importKey(f.read())

    def load_public_key(self):
        if not self.publicKeyPath:
            return
        
        with open(self.publicKeyPath, 'rb') as f:
            self.public_key = RSA.importKey(f.read())
    
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
            print(b)
            print(signature)
            signature_bin = base64.b64decode(signature)
            print(signature_bin)
            # self.public_key.verify(signature_bin, b, hashes.SHA256())
            verifier = PKCS1_signature.new(self.public_key)  # 生成验证信息的类
            digest = SHA256.new()  # 创建一个sha加密的类
            digest.update(b)  # 将获取到的数据进行sha加密
            f = verifier.verify(digest, signature_bin)  # 对数据进行验证，返回bool值
            if f is not True:
                raise LicenseException('证书验证失败，请重新申请证书')
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
        signer = PKCS1_signature.new(self.private_key)
        digest = SHA256.new()
        digest.update(b)
        signature = signer.sign(digest)
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
        privateKeyPath='keystores/private.pem'
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
        publicKeyPath='keystores/public.pem',
    )

    license.install('./license.lic')
    print('证书安装成功')
