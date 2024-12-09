
# IGPSPORT骑行记录同步行者(ActivitySync.py)

- [功能说明和操作流程说明](https://abigeater.com/archives/511)
- 支持把佳明数据同步到行者
- 支持国际版IGPSPORT

# 佳明大陆区同步跑步数据到国际区(GarminSync.py)
- 账号设计复用上面的操作文档，要求大陆区和国际区同一个账号密码（可自行修改代码成不同的）
- 变量名修改成：GARMIN_RUN_EMAIL(登录邮箱)，GARMIN_RUN_PASSWORD(登录密码)
- 脚本默认仅同步执行的前5条大陆区数据
- 如果需要同步全部数据 clone 到本地后 修改大陆区limit条件大于你的记录数并且即可
- 该脚本为同步跑步数据，需要骑行数据修改获取的type（已注释）即可。
- 已知问题：偶尔可能登录失败，需重新执行