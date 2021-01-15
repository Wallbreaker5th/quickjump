# A Quick Jump Tool for OIers
由于作者在打开 OJ 等时候懒得动鼠标，就写了这玩意。~~懒是第一生产力~~

暂时只有 Windows 的脚本，Linux 用户请耗子尾汁（）

`pip install -r requirements.txt` 以安装需要的库。

使用方法：
- `oj name_of_the_OJ [-s keyword] [-p problem_id] [-b]`
  - `-s` 用于搜索特定关键字
  - `-p` 可以跳转到指定题目
  - `-b` 在浏览器打开标签页
  - 例：
    - `oj luogu -p 2333`
    - `oj loj -s 斗地主 -b`
  - 目前支持/打算支持的 OJ：
    - [x] 洛谷（`luogu`/`lg`）
    - [x] Libre OJ（`loj`/`l`）
    - [x] Universal OJ（`uoj`/`u`）
    - [x] 黑暗爆炸 OJ（`darkbzoj`/`bzoj`/`bz`/`db`）
- `wa sth`
  - 使用 Wolfram Alpha 搜索特定内容
  - 例：`wa "sum i, i=0 to n"`
