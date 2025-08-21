# GitHub仓库创建和代码推送指南

## 步骤1: 创建GitHub账号（如果还没有）

1. 访问 https://github.com/
2. 点击"Sign up"注册新账号
3. 填写必要信息并验证邮箱

## 步骤2: 创建新的GitHub仓库

1. 登录GitHub后，点击右上角"+"图标，选择"New repository"
2. 填写仓库信息：
   - Repository name: quality-control-system (或其他名称)
   - Description: Django quality control system with dryfilm, adhesive, and raw material modules
   - 选择Public（公开）或Private（私有）
   - 不要勾选"Initialize this repository with a README"（因为我们已经有代码）
3. 点击"Create repository"

## 步骤3: 获取仓库URL

创建仓库后，GitHub会显示仓库页面，复制HTTPS URL（格式如：`https://github.com/你的用户名/仓库名.git`）

## 步骤4: 连接到本地仓库并推送代码

使用以下命令连接到GitHub并推送代码：

```bash
# 添加远程仓库（将下面的URL替换为你的实际仓库URL）
git remote add origin https://github.com/bboy-bigeast/quality-control-system.git

# 验证远程仓库配置
git remote -v

# 推送代码到GitHub（第一次推送需要使用-u参数）
git push -u origin main
```

## 步骤5: 验证推送成功

1. 刷新GitHub仓库页面
2. 你应该能看到所有代码文件已经上传
3. 可以查看提交历史确认推送成功

## 注意事项

- 第一次推送可能需要输入GitHub用户名和密码（或个人访问令牌）
- 如果使用双因素认证，可能需要使用个人访问令牌代替密码
- 确保网络连接正常

## 后续操作

推送成功后，你可以：
- 在GitHub上查看代码
- 邀请协作者
- 创建issues和pull requests
- 设置GitHub Pages或Actions等
