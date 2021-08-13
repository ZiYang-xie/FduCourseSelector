# FduCourseSelector 📝
![版本号](https://img.shields.io/badge/Version-Beta--0.0.1-blue) ![作者](https://img.shields.io/badge/Author-Xzy-orange)  
---

复旦自动选课脚本，仅用于学习交流，禁止使用脚本干扰正常选课流程

### Usage
#### Step0: clone 脚本至本地
```shell
git clone https://github.com/ZiYang-xie/FduCourseSelector.git
cd FduCourseSelector
```

#### Step1: 安装 Requirements
```shell
pip install -r requirements.txt
```

#### Step2: 填入账号信息
- 在 config/account.json 中输入账号和密码

```json
{
    "UserName": "your account",
    "PassWord": "your password"
}
```

#### Step3: 填入课程信息
- 在 config/lesson.json 中输入想要选择的课程代码

```json
{
    "LessonID": [
        "COMP130166.02" // Just an Example
        ...
    ]
}
```
#### Step4: 启动脚本
```shell
python main.py
```

---
#### TODO
目前验证码验证使用 easyocr 模块，可能验证准确率较低，目前正在解决中