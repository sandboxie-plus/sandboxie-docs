# Fake Admin Rights

**FakeAdminRights** は [Sandboxie Ini](SandboxieIni.md) のサンドボックス設定で、0.7.1 / 5.48.5 以降で利用できます。Sandboxie がこのサンドボックス内で実行されるプログラムに対して管理者権限をシミュレートするかどうかを指定します。

## 構文

```ini
FakeAdminRights=[process,]y|n
```

* **process** (省略可能): ルールを適用する実行可能ファイルの名前。省略した場合、ルールはすべてのサンドボックス化されたアプリケーションに適用されます。
* **y|n**:

    - `y` は指定されたプロセス (何も指定しない場合はすべてのプロセス) に対して偽の管理者権限を有効にします
    - `n` は指定されたプロセスに対して偽の管理者権限を無効にします


このオプションは、セキュリティを向上させるために [DropAdminRights](DropAdminRights.md) と組み合わせて使用することをお勧めします。ほとんどのインストーラーは両方のオプションを有効にしても機能するはずです。

## 使用例

### 1. すべてのサンドボックス化されたプログラムに対して偽の管理者権限を有効にする

これにより、サンドボックス内のすべてのアプリケーションが管理者権限を持っていると信じ込まされます:

```ini
[DefaultBox]
FakeAdminRights=y
```

### 2. 特定のインストーラーに対して偽の管理者権限を有効にする

一部のインストーラーは続行するために管理者権限を必要とします。これにより、偽の管理者権限が `installer.exe` にのみ付与され、他のプログラムは通常どおり実行されます:

```ini
[DefaultBox]
FakeAdminRights=installer.exe,y
```

### 3. グローバルに偽の管理者権限を有効にしつつ、セキュリティ上重要なプログラムでは無効にする

この構成では、`CredentialUIBroker.exe` のようなセキュリティ上重要なプログラムを除くすべてのプログラムに偽の管理者権限が付与されます:

```ini
[DefaultBox]
FakeAdminRights=y
FakeAdminRights=CredentialUIBroker.exe,n
```

### 4. 否定 (!) を使用してルールを反転させる

`!` を使用してルールの論理を反転させることができます。これは例外を作成する場合に特に便利です:

```ini
[DefaultBox]
FakeAdminRights=!Start.exe,y
```

これは「Start.exe を除くすべてのプログラムに対して偽の管理者権限を有効にする」ことを意味します。

これらの例は次を示しています:

1. グローバルな偽の管理者権限
2. 特定のアプリケーションに対する対象を絞った偽の管理者権限
3. セキュリティ上重要なプログラムとの互換性のための混合アプローチ
4. 例外ベースのルールのための否定の使用

3 番目の例は、ほとんどのプログラムが昇格された権限を必要とするが、特定のシステム コンポーネントが正しく機能するために実際のアクセス許可で実行される必要がある場合に特に便利です。

### FakeAdmin は何をしますか?

**FakeAdmin** が有効な場合:

- サンドボックス化されたプロセスは、管理者権限で実行されていると信じ込まされます。
- これは、実際の管理者アクセスを付与せずに、管理者権限を必要とするアプリケーションをテストまたは実行する場合に便利です。
- 管理者権限をチェックするが実際には機能するためにそれを必要としないプログラムの互換性に役立ちます。

## 関連する構成

この設定は、**Sandboxie Plus** の次のパスにある GUI オプションに対応します:

**Sandbox Options** > **Security Options** > **Security Hardening**: _Make applications think they are running elevated (allows to run installers safely)_

**Sandbox Options** > **Advanced Options** > **Miscellaneous** > **Add Option**: _FakeAdminRights_
