# Process Limit

_ProcessLimit_ は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、v0.9.7 / 5.52.1 以降で使用できます。この設定により、Sandboxie がサンドボックス内で同時に許可するプロセスの最大数を制限できます。

**注:** 設定された制限の 80% に達すると、新しいプロセスの開始が 3 秒間遅延されます。制限に達すると、別のプロセスが終了されるまで、新しいプロセスは開始できなくなります。

_ProcessLimit_ は [ProcessNumberLimit](ProcessNumberLimit.md) とは別個です。_ProcessLimit_ は Sandboxie のプロセス初期化ロジックによって強制されますが、_ProcessNumberLimit_ は Windows Job オブジェクトのアクティブ プロセス制限を使用します。

```
   .
   .
   .
   [DefaultBox]
   ProcessLimit=100
```
