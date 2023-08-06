from license_manager.license import License
from license_manager.utils import Hardware

def create(privateKeyPath: str, privateKeyPass: str = None, subject: str = 'castiron', consumerType: str = 'customer', consumerAmount: int = 1, description: str = '', issuedTime: str = None, expiryTime: str = None, params: dict = None, output: str = None):
    '''
    生成 license 证书

    Arguments:
        privateKeyPath {str}    -- 私钥地址
        privateKeyPass {str}    -- 私钥密码
        subject {str}           -- license 证书主题，默认 castiron
        consumerType {str}      -- license 证书类型，默认 customer
        consumerAmount {int}    -- license 证书授权客户数量，默认 1
        description {str}       -- license 证书描述信息
        issuedTime {str}        -- license 证书生效起始时间
        expiryTime {str}        -- license 证书生效结束时间
        params {str}            -- license 验证的附加参数
        output {str}            -- license 生成后输出路径文件名
    '''
    license = License(privateKeyPath=privateKeyPath, privateKeyPass=privateKeyPass)
    license.create(
        subject=subject,
        consumerType=consumerType,
        consumerAmount=consumerAmount,
        description=description,
        issuedTime=issuedTime,
        expiryTime=expiryTime,
        params=params,
        output=output
    )

def verify(licensePath: str, publicKeyPath: str, publicKeyPass: str = None, params: dict = None):
    '''
    验证 license 证书

    Arguments:
        licensePath {str}       -- license 证书地址
        publicKeyPath {str}     -- 公钥库地址
        publicKeyPass {str}     -- 公钥库密码
        params {str}            -- license 验证的附加参数, mac 地址验证参数不传递，验证工具会自动获取
    '''
    license = License(publicKeyPath=publicKeyPath, publicKeyPass=publicKeyPass)
    license.install(licensePath, params=params)
    print('license 证书验证通过')

def hardware():
    '''
    获取当前机器硬件信息
    '''
    hardwar_info = Hardware.get_info()
    print('\n')
    for k, v in hardwar_info.items():
        print(f'\t{k}:\t{v}')
    print('\n')