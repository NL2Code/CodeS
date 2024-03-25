htpwdScan 1.0
====

**htpwdScan** 是一个HTTP暴力破解、撞库测试工具。

### 特性

- 支持常见的认证模式：Basic/Digest/NTLM 等
- 支持对 GET / POST 参数进行暴力破解，支持使用占位符选定参数或参数的一部分
- 支持批量校验和导入HTTP代理，通过大量IP低频撞库，绕过IP策略
- 支持导入互联网上泄露的社工库，对接口发起撞库
- 支持编写python函数对参数进行预处理，解决密码策略较苛刻的破解场景，如 Microsoft OWA
- 支持字典文件中的占位符替换
- 支持优先固定密码，遍历用户名，以降低账号被锁定概率
- 支持导入超大字典文件

### 使用示例 ###

* #### **Basic / Digest / NTLM 破解**

  可以分别设置用户名、密码字典，也可以设置包含用户名密码的单个字典

  ```
  htpwdScan.py -u https://jigsaw.w3.org/HTTP/Basic/ --auth user.txt passwd.txt
  
  htpwdScan.py -u https://jigsaw.w3.org/HTTP/Basic/ --auth tests/leaked_db.txt
  
  htpwdScan.py -u https://jigsaw.w3.org/HTTP/Digest/ --auth user.txt passwd.txt --pass-first
  
  htpwdScan.py -u https://mail.owa-domain.com/ews --auth user.txt pass.txt --pass-first
  ```