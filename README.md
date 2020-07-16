# OSS Livestream API Demo

通过阿里云对象储存 OSS 进行直播推流的后端 API 例子。

- [x] 通过 [aliyun-oss-python-sdk](https://github.com/aliyun/aliyun-oss-python-sdk) 创建 LiveChannel -> 直播
- [x] 通过 [aliyun-oss-python-sdk](https://github.com/aliyun/aliyun-oss-python-sdk) 关闭 LiveChannel 并合并指定时间内的所有 ts 文件（默认为7200秒） -> 回放 


## Usage

```bash
# Clone this repository
git clone https://github.com/Evilran/oss-livestream-api-demo.git
# Go into the repository
cd oss-livestream-api-demo
# run bash script
bash docker.sh
```



**/livestream/create:**

```
{
  "play_url": "http://[BUCKET].[REGION].aliyuncs.com/[CHANNEL]/playlist.m3u8",
  "signed_publish_url": "rtmp://[BUCKET].[REGION].aliyuncs.com/[PREFIX]/[CHANNEL]?playlistName=[LIVESTREAM].m3u8&OSSAccessKeyId=[ACCESSKEYID]&Expires=[TIMESTAMP]&Signature=[SIGNATURE]"
}
```

* *使用 OBS 或其他软件进行推流：*

*Server*: rtmp://[BUCKET].[REGION].aliyuncs.com/[PREFIX]

*Stream key:* [CHANNEL]?playlistName=[LIVESTREAM].m3u8&OSSAccessKeyId=[ACCESSKEYID]&Expires=[TIMESTAMP]&Signature=[SIGNATURE]



* *拉流*

http://[BUCKET].[REGION].aliyuncs.com/[CHANNEL]/[LIVESTREAM].m3u8



**/livestream/delete**

```
start_time = end_time - 7200 # combine all ts files during two hours
```

默认将结束时间前两个小时（7200秒）到结束时间的所有 ts 文件合并为 [LIVESTREAM].m3u8，访问原拉流地址可以观看直播回放。



## Reference

Eletron 客户端：[**electron-oss-livestream**](https://github.com/Evilran/electron-oss-livestream) 


