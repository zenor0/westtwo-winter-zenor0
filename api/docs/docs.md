## /西二Python组寒假单人作业/用户/注册

```text
暂无描述
```
#### 接口状态
> 已完成

#### 接口URL
> http://127.0.0.1:8000/user

#### 请求方式
> POST

#### Content-Type
> json

#### 请求Body参数
```javascript
{
    "username": "admin",
    "password": "123456",
    "checkPassword": "123456"
}
```
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
username | admin | String | 是 | 用户名
password | 123456 | String | 是 | 密码，6-18位
checkPassword | 123456 | String | 是 | 重复密码，需要和密码形同
#### 认证方式
```text
noauth
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": {
		"id": 1,
		"username": "admin"
	}
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Integer | 
message | success | String | 
data | - | Object | 
data.id | 1 | Integer | 用户id
data.username | admin | String | 用户名
## /西二Python组寒假单人作业/用户/登录
```text
暂无描述
```
#### 接口状态
> 已完成

#### 接口URL
> http://127.0.0.1:8000/user/login

#### 请求方式
> POST

#### Content-Type
> json

#### 请求Body参数
```javascript
{
    "username": "admin",
    "password": "123456"
}
```
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
username | admin | String | 是 | 用户名
password | 123456 | String | 是 | 密码，6-18位
#### 认证方式
```text
noauth
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": {
		"id": 1,
		"username": "admin",
		"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjczNDQ4NTcyfQ.UVcR7CULoyQ101mZ5B1FmaXb9fpZ-2k4hX_ueW4Qe2I"
	}
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Integer | 
message | success | String | 
data | - | Object | 
data.id | 1 | Integer | 用户id
data.username | admin | String | 用户名
data.token | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjczNDQ4NTcyfQ.UVcR7CULoyQ101mZ5B1FmaXb9fpZ-2k4hX_ueW4Qe2I | String | token值
## /西二Python组寒假单人作业/搜索/搜索

```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> http://127.0.0.1:8000/search?text=周杰伦

#### 请求方式
> GET

#### Content-Type
> json

#### 请求Header参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
Authorization | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjczNDQ4NTcyfQ.UVcR7CULoyQ101mZ5B1FmaXb9fpZ-2k4hX_ueW4Qe2I | String | 是 | token值
#### 请求Query参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
text | 周杰伦 | String | 是 | 搜索文本
#### 请求Body参数
```javascript

```
#### 认证方式
```text
noauth
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": {
		"list": [
			{
				"name": "兰亭序",
				"artist": "周杰伦",
				"album": "魔杰座",
				"duration": "04:13",
				"rid": 1
			},
			{
				"name": "晴天",
				"artist": "周杰伦",
				"album": "叶惠美",
				"duration": "04:29",
				"rid": 2
			},
			{
				"name": "青花瓷",
				"artist": "周杰伦",
				"album": "我很忙",
				"duration": "03:57",
				"rid": 324244
			},
			{
				"name": "稻香",
				"artist": "周杰伦",
				"album": "魔杰座",
				"duration": "03:43",
				"rid": 440613
			}
		]
	}
}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Integer | 
message | success | String | 
data | - | Object | 
data.list | - | Array | 
data.list.name | 兰亭序 | String | 歌名
data.list.artist | 周杰伦 | String | 歌手
data.list.album | 魔杰座 | String | 专辑
data.list.duration | 04:13 | String | 时长
data.list.rid | 1 | Integer | 下载id
## /西二Python组寒假单人作业/搜索/下载音乐
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> http://127.0.0.1:8000/search/download/:rid

#### 请求方式
> GET

#### Content-Type
> none

#### 请求Header参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
Authorization | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjczNDQ4NTcyfQ.UVcR7CULoyQ101mZ5B1FmaXb9fpZ-2k4hX_ueW4Qe2I | String | 是 | token值
#### 路径变量
参数名 | 示例值 | 参数描述
--- | --- | ---
rid | 324244 | 路径id
#### 认证方式
```text
noauth
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
返回一个文件
```
## /西二Python组寒假单人作业/历史记录
```text
暂无描述
```
#### Header参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### Query参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### Body参数
参数名 | 示例值 | 参数描述
--- | --- | ---
暂无参数
#### 认证方式
```text
noauth
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
## /西二Python组寒假单人作业/历史记录/删除历史记录
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> http://127.0.0.1:8000/user/history

#### 请求方式
> DELETE

#### Content-Type
> json

#### 请求Header参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
Authorization | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjczNDQ4NTcyfQ.UVcR7CULoyQ101mZ5B1FmaXb9fpZ-2k4hX_ueW4Qe2I | String | 是 | token值
#### 请求Body参数
```javascript
{
    "type": 0,
    "id": 1,
    "list": [
        1,
        2,
        3,
        4,
        5
    ]
}
```
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
type | 0 | Integer | 是 | 0或1，type为0时根据id删除，1时删除id为list中的所有数字
id | 1 | Integer | 否 | 历史记录id
list | 1 | Array | 否 | 历史记录id列表
#### 认证方式
```text
noauth
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{"code":200,"message":"success"}
```
## /西二Python组寒假单人作业/历史记录/获取历史记录
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> http://127.0.0.1:8000/user/history?page=1

#### 请求方式
> GET

#### Content-Type
> none

#### 请求Header参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
Authorization | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjczNDQ4NTcyfQ.UVcR7CULoyQ101mZ5B1FmaXb9fpZ-2k4hX_ueW4Qe2I | String | 是 | token值
#### 请求Query参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
page | 1 | String | 是 | 当前页数
#### 认证方式
```text
noauth
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{"code":200,"message":"success","data":{"list":[{"name":"兰亭序","artist":"周杰伦","album":"魔杰座","duration":"04:13","fav":0,"rid":1,"id":123442},{"name":"晴天","artist":"周杰伦","album":"叶惠美","duration":"04:29","fav":1,"rid":2,"id":354325},{"name":"兰亭序","artist":"周杰伦","album":"魔杰座","duration":"04:13","fav":0,"rid":1,"id":123442},{"name":"晴天","artist":"周杰伦","album":"叶惠美","duration":"04:29","fav":1,"rid":2,"id":354325},{"name":"兰亭序","artist":"周杰伦","album":"魔杰座","duration":"04:13","fav":0,"rid":1,"id":123442},{"name":"晴天","artist":"周杰伦","album":"叶惠美","duration":"04:29","fav":1,"rid":2,"id":354325},{"name":"兰亭序","artist":"周杰伦","album":"魔杰座","duration":"04:13","fav":0,"rid":1,"id":123442},{"name":"晴天","artist":"周杰伦","album":"叶惠美","duration":"04:29","fav":1,"rid":2,"id":354325},{"name":"兰亭序","artist":"周杰伦","album":"魔杰座","duration":"04:13","fav":0,"rid":1,"id":123442},{"name":"晴天","artist":"周杰伦","album":"叶惠美","duration":"04:29","fav":1,"rid":2,"id":354325}],"count":2}}
```
参数名 | 示例值 | 参数类型 | 参数描述
--- | --- | --- | ---
code | 200 | Integer | 
message | success | String | 
data | - | Object | 
data.list | - | Array | 数据列表，由于演示所以会有重复，实际情况不应该有重复
data.list.name | 兰亭序 | String | 歌名
data.list.artist | 周杰伦 | String | 歌手
data.list.album | 魔杰座 | String | 专辑
data.list.duration | 04:13 | String | 时长
data.list.fav | 0 | Integer | 是否收藏，0表示没收藏，1表示已经收藏
data.list.rid | 1 | Integer | 下载id
data.list.id | 123442 | Integer | 历史记录id
data.count | 2 | Integer | 总页数
#### 错误响应示例
```javascript
{
    "code": 403,
    "messages": "无法检验token"
}
```
## /西二Python组寒假单人作业/历史记录/修改历史记录收藏
```text
暂无描述
```
#### 接口状态
> 开发中

#### 接口URL
> http://127.0.0.1:8000user/history/lc

#### 请求方式
> PUT

#### Content-Type
> json

#### 请求Header参数
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
Authorization | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjczNDQ4NTcyfQ.UVcR7CULoyQ101mZ5B1FmaXb9fpZ-2k4hX_ueW4Qe2I | String | 是 | token值
#### 请求Body参数
```javascript
{
    "id": 1,
    "fav": 0
}
```
参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述
--- | --- | --- | --- | ---
id | 1 | Integer | 是 | 历史记录id
fav | 0 | Integer | 是 | 修改为的值，0为取消收藏，1为收藏
#### 认证方式
```text
noauth
```
#### 预执行脚本
```javascript
暂无预执行脚本
```
#### 后执行脚本
```javascript
暂无后执行脚本
```
#### 成功响应示例
```javascript
{
	"code": 200,
	"message": "success",
	"data": {
        "name": "兰亭序",
        "artist": "周杰伦",
        "album": "魔杰座",
        "duration": "04:13",
        "rid": 0
	}
}
```