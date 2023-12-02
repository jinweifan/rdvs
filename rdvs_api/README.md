# RDVS

## 问题
### Spider
#### Selenium在MAC下去驱动需配置localhost文件
## FastAPI



### Pydantic 模型

我们使用 [Pydantic](https://pydantic-docs.helpmanual.io/) 模型来声明**请求**体，并能够获得它们所具有的所有能力和优点

#### 创建数据模型

用标准的Python类型来声明所有属性，声明的数据模型应继承BaseModel类或其子类；

~~~python
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
      
app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
~~~

**使用标准的Python类型的优势**，FastAPI将会：

1. 将请求体作为JSON数据读取；
2. 转换为响应的类型；
3. 校验数据：若数据无效，将返回一条清晰易读的错误信息，指出不正确数据的确切位置和内容；
4. 将接收的数据赋值到参数`item`中，因为函数中将`item`声明为`Item`类型，若使用了智能编辑器还将获得其所有属性的代码补全



### 安全性

#### 简介

##### OAuth2

OAuth2是一个规范，它定义了几种处理身份认证和授权的方法。它是一个相当广泛的规范，涵盖了一些复杂的使用场景。它包括了使用「第三方」进行身份认证的方法。

##### OpenAPI

OpenAPI（以前称为 Swagger）是用于构建 API 的开放规范（现已成为 Linux Foundation 的一部分）。

**FastAPI** 基于 **OpenAPI**，这就是使多个自动交互式文档界面，代码生成等成为可能的原因。

OpenAPI 有一种定义多个安全「方案」的方法。

通过使用它们，你可以利用所有这些基于标准的工具，包括这些交互式文档系统。

OpenAPI 定义了以下安全方案：

-  apiKey：一个特定于应用程序的密钥，可以来自：

  - 查询参数。
  - 请求头。
  - cookie。
- http：标准的 HTTP 身份认证系统，包括：
  - `bearer`: 一个值为 `Bearer` 加令牌字符串的 `Authorization` 请求头。这是从 OAuth2 继承的。
  - HTTP Basic 认证方式。
  - HTTP Digest，等等。



> Password 流是 OAuth2 定义的，用于处理安全与身份验证的方式（流）。
> OAuth2 的设计目标是为了**让后端或 API 独立于服务器验证用户身份**tokenUrl 参数，包含客户端（用户浏览器中运行的前端） 的 URL，用于发送 username 与 password，并获取令牌。
>
> OAuth2 规定在使用（我们打算用的）「password 流程」时，客户端/用户必须将 `username` 和 `password` 字段作为表单数据发送。
>
> 规范还写明了 `username` 和 `password` 必须作为表单数据发送（因此，此处不能使用 JSON）。
>
> `scope`在 OAuth2 中「作用域」只是一个声明所需特定权限的字符串。



### OAuth2 实现密码哈希与 Bearer JWT 令牌验证

#### JWT

JWT 即**JSON 网络令牌**（JSON Web Tokens）， JWT 是一种将 JSON 对象编码为没有空格，且难以理解的长字符串的标准，JWT 字符串没有加密，任何人都能用它恢复原始信息，但 JWT 使用了签名机制。接受令牌时，可以用签名校验令牌。

在FastAPI中安装 `python-jose`来生成和校验 JWT 令牌，因为 Python-jose 支持 PyJWT 的所有功能，还支持与其它工具集成时可能会用到的一些其它功能

~~~bash
pip install python-jose
~~~

在终端中创建用于 **JWT 令牌签名的随机密钥**

~~~bash
openssl rand -hex 32 # 如，b342662c541cba035b904055e0be4f86a17cdce2dfd2967eed3807f4ff5f87ad
~~~

然后，把生成的密钥复制到变量**SECRET_KEY**， 并创建指定 JWT 令牌签名算法的变量 **ALGORITHM**，本例中的值为 `"HS256"`。

1. 创建设置令牌过期时间的变量。

2. 定义令牌端点响应的 Pydantic 模型。
3. 创建生成新的访问令牌的工具函数。

~~~python
from jose import JWTError, jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" # 生产的随机密码
ALGORITHM = "HS256" # 签名算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 过期时间


class Token(BaseModel):
  """ 令牌响应Pydanic模型 """
    access_token: str
    token_type: str
      
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
  """ 工具函数 """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
~~~



#### 密码哈希

> **哈希**是指把`特定内容`转换为`乱码形式的字节序列`（其实就是字符串），每次传入完全相同的密码，返回的都是完全相同的乱码，但这个乱码无法转换回传入的密码，常用于用户密码加密。
>
> FastAPI推荐使用`Passlib` 库中**Bcrypt**算法实现加密，
>
> **Passlib**是处理密码哈希的 Python 包，它支持很多安全哈希算法及配套工具。



<font color="red">**特别注意:**</font> 若使用的是Passlib上下文创建密码Hash和身份验证，需要其支持的上下文环境中加密密码和验证身份。若不在一个上下文语境中加密密码后，在不兼容的另一个上下文语境中验证身份，即使输入正确的密码，但加密后Hash密码无法通过身份验证。简而言之，需要在同一系统环境或支持的系统环境中加密Hash和进行身份验证。