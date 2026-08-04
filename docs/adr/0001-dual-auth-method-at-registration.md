# Registration 同时创建 PASSWORD 与 EMAIL 两条 Auth Method

注册时在一个事务内创建一条 User 和两条 Auth Method：PASSWORD（identifier=username，credential=bcrypt hash）与 EMAIL（identifier=email，credential=null），两者初始均为 UNVERIFIED；用户点击验证链接后两条同时变为 VERIFIED，方可登录。

这样 username 与 email 各自通过 `(ttype, identifier)` 唯一索引约束，登录凭据与邮箱验证解耦，且忘记密码流程可交叉校验 username + email。备选方案是单条 Auth Method 或在 User 上直接存 email——前者无法复用现有 UserAuth 模型与索引，后者会把档案字段与认证边界混在一起。
