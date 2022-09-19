# 基于 VirtualBox 的网络攻防基础环境搭建

## 实验目的
  - 掌握 VirtualBox 虚拟机的安装与使用
  - 掌握 VirtualBox 虚拟网络类型和按需配置
  - 掌握 VirtualBox 虚拟硬盘多重加载

## 实验环境
  - VirtualBox 虚拟机
  - 攻击者主机（Attacker）：Kali
  - 网关（Gateway, GW）：Debian
  - 靶机（Victim）：Debian 、 Windows-xp 、 Kali


## 实验要求
  ####  1. 虚拟硬盘配置成多重加载
  
  - 由于上学期的Linux课程已经配置过 `多重加载` ，故在此不详细描述，只记录一些关键操作，具体操作详见 [Virtualbox 多重加载](https://blog.csdn.net/jeanphorn/article/details/45056251)
  - 一些主要步骤
  >虚拟机管理 -> 虚拟介质管理
  选中虚拟盘，属性-> 类型，修改类型为 *多重加载*

  ![虚拟介质管理的多重加载](img\mulload1.jpg)  

  ![虚拟机相关设置中的多重加载](img\mulload2.jpg)
  
  ---

  #### 2. 搭建虚拟机网络拓扑
  - ##### 搭建满足如下拓扑图所示的虚拟机网络拓扑：
  ![虚拟机网络拓扑](img\topo.png)
  ---

  - ##### 网关配置

     - 2.1 ==网关gwdebian== 
       - 2.1.1 需要的四块网卡
         - NAT网络，使网关可访问攻击者主机
         - 仅主机（Host-Only）网络，进行网卡设置
         - 内部网络intnet1，搭建局域网1
         - 内部网络intnet2，搭建局域网2
       ![gw的网关配置](img\gw_network.jpg)

       - 观察IP
       ![gwdebian的ip](img\gwdebian_ip.jpg)
       这个时候我们就可以先配置 `ssh` 免密登录, 之后就可以根据 黄大 给的资料愉快的复制粘贴更改配置啦~（but 我真没找到黄大的资料，操作之后发现Debian的似乎已经配置好了（？），而视频是前几届师哥师姐的视频，所以我们是直接享受了一波福利hhh~
       ---


     - 2.2 ==攻击者kali==需要的三块网卡
       - NAT网络
       - Host-Only 1
       - Host-Only 2
        注：这里Host-Only 是两块不同的Host-Only网卡，1 、2 是区分

       ![kali攻击者的网关配置](img\attack_network.jpg)
       ---

     - 2.3 ==两个victim==各需要一块网卡
       - 内部网络，使不同组的victim在不同局域网内
       - xp-victim1 与 kali 在同一局域网内（intnet1）； x-victimp2 与 Debian 在同一局域网内（intnet2）

       ![victim1网关配置](img\vim_network1.jpg)

       ![victim2网关配置](img\vim_network1.jpg)

       ![关闭防火墙](img\xp1_information.png)

       注意：①启动Windows时顺手关闭 `防火墙设置` ，目的是方便后续连通性测试时可以 ping 通
            ② Windows 设置网络时，选择 `高级 -> 芯片控制 ->PCnet-FAST ` 设置
  - 查看IP
    ![debian的IP信息](img\debian_ip.png)
    ![xp1的IP信息](img\xp1_ip.png)
    ![xp2的IP信息](img\xp2_ip.png)
    
    整理出相应的各IP：
    | 虚拟机名称 | IP地址 |
    |--|--|
    |kali-attacker| 10.0.2.5 |
    |kali-victim1| /24(intnet1) |
    |xp-victim1| 172.16.111.110/24(intnet1) |
    |xp-victim2| 172.16.222.141/24(intnet2) |
    |debian-victim2| 169.254.7.180(intnet2) |
    |gwdabian| 10.0.2.15/24(net) |
    | | 192.168.56.101/24(host-only) |
    | | 172.16.111.1/24(intnet1) |
    | | 172.16.222.1/24(intnet2) |


---

 #### 3.连通性测试
  - 完成以下网络连通性测试：
    - 靶机可以直接访问攻击者主机
     ![victim1可以访问attacker](img\xp1_ping_attacker.png)
     ![victim2可以访问attacker](img\debianvim2_ping_attacker.png)

    - 攻击者主机无法直接访问靶机
     ![attacker无法访问victim](img\attacker_ping_victim.png)

    - 网关可以直接访问攻击者主机和靶机
     ![gwdebian可以访问attacker&victim](img\gwdebian_ping_attack&vim.png)

    - 靶机的所有对外上下行流量必须经过网关
      这里我看舍友都是用上学期计算机网络实验的 `wireshark` 软件监控，但是由于上学期网课就在家里台式机上做了，~~太懒了不想再次安装wireshark，所以采取别的办法hhh~~
      网关安装 `tcpdump` ,同时对网卡进行监控。
      ```
      apt update&apt install tcpdump
      /usr/sbin/tcpdump -i 网卡
      ```
      如何说明靶机的对外上下行流量必须经过网关？对网卡进行监控，各节点访问互联网，观察是否捕获到上下行的包；关闭网关，发现所有节点无法访问互联网。

    - 所有节点均可以访问互联网
     ![attacker访问互联网](img\attacker_ping_net.png)

     ![victim1访问互联网](img\vim1_ping_net.png)
     ![victim1上下行流量监测](img\vim1_pass_gw.png)

     ![victim2访问互联网](img\debianvim2_ping_net.png)
     ![victim2上下行流量监测](img\vim2_pass_gw.png)

---
## 课后习题及思考
   ### 1.以下⾏为分别破坏了CIA和AAA中哪⼀个属性或多个属性？
   - 小明抄小强的作业
     CIA:机密性 和 AAA:认证,授权
   - 小明把小强的系统折腾死机了
     CIA:可用性 
   - 小明修改了小强的淘宝订单
     CIA:完整性 和 AAA:认证，授权
   - 小明冒充小强的信用卡账单签名
     CIA:完整性 AAA:认证，授权
   - 小明把自⼰电脑的IP修改为小强电脑的IP，导致小强的电脑⽆法上⽹
     CIA:可用性 AAA:认证，授权

   ### ⼀次，小明⼝袋里有100元，因为打瞌睡，被小偷偷⾛了，搞得晚上没饭吃。又⼀天，小明⼝袋里有200元，这次小明为了防范小偷，不打瞌睡了，但却被强盗持⼑威胁抢⾛了，搞得⼀天没饭吃，小明当天就报警了。
   - 试分析两次失窃事件中的：风险、资产、威胁、弱点、攻击、影响
     风险：钱被小偷偷走、钱被强盗抢走 
     资产：口袋中的钱 
     威胁：小偷，强盗 
     弱点:打瞌睡,没有工具or能力对付强盗 
     攻击:偷窃、抢劫 
     影响:一天没饭吃
   - 试用P2DR模型分析以上案例中的“现⾦被抢”事件中的安全策略、安全防护、安全检测和安全响应
     第一次 
     安全策略：睡着->没有策略；安全防护: 放口袋里->藏起来; 安全检测: 睡着->没有检测; 安全响应: 没有采取措施->无响应
     第二次 
     安全策略: 钱放口袋，不打瞌睡，被抢报警->入侵检测，报警响应； 安全防护: 钱放口袋->藏起来,不打瞌睡->入侵检测； 安全检测: 监视“钱”的完整性、机密性； 安全响应: 报警

   ### 某⼤型软件开发公司的总裁担⼼公司的专利软件设计⽅法被内部员⼯泄露给其他公司，他打算防⽌泄密事件的发⽣。于是他设计了这样⼀个安全机制： 所有员⼯必须每天向他汇报自⼰和其他竞争对⼿公司员⼯的所有联系(包括IM、电⼦邮件、电话等等) 。你认为该安全机制能达到总裁的预期安全效果吗？为什么？
   我认为该安全机制不能达到总裁的预期安全效果。
   - 安全机制的部署和管理过于繁琐，不一定能得到员工的配合,管理极其困难
   - 安全机制的集合不能够实现所有的安全策略,因为员工仍然可以通过其他方式泄漏(比如面谈交易)
   - 安全机制的实现是不一定正确(每天下班汇报，第二天上班又是新的一天了，过于频繁员工会厌倦…


---
## 问题及解决
  - 修改网络为 `网络地址转换NAT` 时 报错 `无效按钮` ：
    ![无效按钮](img\无效按钮_报错1.jpg)

    解决方式： 管理 ->全局设定 ->网络 ->点击右侧 ‘+’ 号 ->点击 ‘OK’ ->返回主界面点击设置 即可解决问题。
    （主要是之前的课程实验相同操作没遇到这样的问题，所以个人认为值得记录一下…

  - ssh 免密登录失败，报错：Permission denied, please try again（忘记截图了…
    原因及解决方式：root用户没有权限ssh，看了一些教程说要更改配置，但是root更改风险是不是有点大（？而且观看 黄大 的讲解视频时发现他的是 `cuc` 而非 `root` ，当时感觉有点子不对劲but没有注意，没想到这也是一个坑哇…），所以勉强忍受一下在 `黑框框` 里操作吧，但是体验感实在太差。后来突然想到，`是不是可以新建一个用户`？最后 ssh 成功！泪目…
    Debian创建用户：
    ```
    useradd -d /home/your_username -m your_username # 添加用户
    passwd your_username # 添加密码
    userdel your_username # 删除用户
    ```


---
## 参考文献
 - [Debian上创建新用户](https://www.cnblogs.com/OneFri/p/10201990.html)
 - [黄大第一章课后实验讲解](http://courses.cuc.edu.cn/course/90732/learning-activity/full-screen#/378195)
 - [张师哥的作业](https://github.com/CUCCS/2021-ns-public-Zhang1933/blob/ch0x01/ch0x01/0x01.md)