---
layout: default
title: 建造者模式
nav_order: 3
parent: 设计模式
description: "建造者模式"
---

# 建造者模式
此文章第一次发布于[博客园](https://www.cnblogs.com/hzhhhbb/p/11397501.html)

## 概念
建造者模式属于创建型设计模式。

指的是将一个复杂的构建与其表示相分离，使得同样的构建过程可以创建不同的表示。

建造者模式主要解决在软件系统中，有时候面临着"一个复杂对象"的创建工作，其通常由各个部分的子对象用一定的算法构成；由于需求的变化，这个复杂对象的各个部分经常面临着剧烈的变化，但是将它们组合在一起的算法却相对稳定。

建造者模式主要涉及几个角色：

1. 指挥者（Director），负责和客户（Client）对话

2. 之后指挥者将客户的产品需求划分为比较稳定的建造过程（AbstractBuilder）

3. 指挥者指挥具体的建造者（ConcreteBuilder）干活

4. 获取建造者建造的产品给客户

比如组装电脑这个场景，CPU、主板、硬盘和内存等配件是相对稳定的，组装过程也是相当稳定的，先装CPU、内存、硬盘和电源等等（AbstractBuilder），但是配件搭配的方式是多变的（Builder可以多个），如组装家用电脑、游戏电脑。

## 实现
1. 先来一个产品类（电脑）
```csharp
namespace BuilderPattern
{
    using System;
    using System.Collections.Generic;

    /// <summary>
    ///     电脑类
    /// </summary>
    public class Computer
    {
        /// <summary>
        ///  电脑组件集合
        /// </summary>
        private readonly IList<string> parts = new List<string>();

        /// <summary>
        /// 把单个组件添加到电脑组件集合中
        /// </summary>
        /// <param name="part">组件</param>
        public void Add(string part)
        {
            this.parts.Add(part);
        }

        public void Show()
        {
            Console.WriteLine("电脑组件清单：");
            foreach (var part in this.parts)
            {
                Console.WriteLine($"组件：{part}");
            }

            Console.WriteLine("****************");
        }
    }
}
```

2. 再来一个抽象Builder、两个具体的Builder

```csharp
namespace BuilderPattern
{
    /// <summary>
    ///     抽象建造者
    /// </summary>
    public abstract class AbstractBuilder
    {
        /// <summary>
        /// 装CPU
        /// </summary>
        public abstract void BuildPartCPU();

        /// <summary>
        /// 装主板
        /// </summary>
        public abstract void BuildPartMainBoard();

        /// <summary>
        /// 获得组装好的电脑
        /// </summary>
        /// <returns>电脑</returns>
        public abstract Computer GetComputer();
    }
}

namespace BuilderPattern
{
    /// <summary>
    ///     具体建造者，具体的某个人为具体创建者，例如：装机小王
    /// </summary>
    public class ConcreteBuilder1 : AbstractBuilder
    {
        private readonly Computer computer = new Computer();

        public override void BuildPartCPU()
        {
            this.computer.Add("CPU1");
        }

        public override void BuildPartMainBoard()
        {
            this.computer.Add("Main board1");
        }

        public override Computer GetComputer()
        {
            return this.computer;
        }
    }
}

namespace BuilderPattern
{
    /// <summary>
    ///     具体建造者，具体的某个人为具体创建者，例如：装机小李啊
    /// </summary>
    public class ConcreteBuilder2 : AbstractBuilder
    {
        private readonly Computer computer = new Computer();

        public override void BuildPartCPU()
        {
            this.computer.Add("CPU2");
        }

        public override void BuildPartMainBoard()
        {
            this.computer.Add("Main board2");
        }

        public override Computer GetComputer()
        {
            return this.computer;
        }
    }
}
```
3. 指挥者登场（BOSS）
```csharp
namespace BuilderPattern
{
    /// <summary>
    ///   指挥者
    /// </summary>
    public class Director
    {
        /// <summary>
        /// 组装电脑
        /// </summary>
        /// <param name="abstractBuilder">建造者</param>
        public void Construct(AbstractBuilder abstractBuilder)
        {
            abstractBuilder.BuildPartCPU();
            abstractBuilder.BuildPartMainBoard();
        }
    }
}
```

4. 使用
```csharp
namespace BuilderPattern
{
    using System;

    class Program
    {
        static void Main(string[] args)
        {
            // 客户找到电脑城老板说要买电脑，这里要装两台电脑
            // 创建指挥者和构造者
            var director = new Director();
            AbstractBuilder b1 = new ConcreteBuilder1();
            AbstractBuilder b2 = new ConcreteBuilder2();

            Console.WriteLine("开始组装第一台电脑");
            director.Construct(b1);
            Console.WriteLine("获取第一台电脑");
            var computer1 = b1.GetComputer();
            computer1.Show();

            Console.WriteLine("开始组装第二台电脑");
            director.Construct(b2);
            Console.WriteLine("获取第二台电脑");
            var computer2 = b2.GetComputer();
            computer2.Show();

            Console.Read();
        }
    }
}
```
结果如下：

![结果](/assets/images/docs/design-pattern/builder-pattern/1.png)

## 总结

以上组装电脑的过程，把电脑零件和电脑组装分离了，电脑组装和电脑组装过程分离了，也就是我们常说的解耦。

BOSS可以随时修改电脑的组装过程，不影响交付给客户的产品；也可以随时换掉组装电脑的人（ConcreteBuilder1和ConcreBuilder2），不再依赖具体的人。也就是不依赖细节，都依赖于抽象，使整个电脑组装过程更稳定。

建造者模式适用于所创建的产品具有较多的共同点，其组成部分相似；如果产品之间的差异性很大，则不适合使用建造者模式，如造飞机和装电脑。

代码下载：[https://github.com/hzhhhbb/BuilderPattern](https://github.com/hzhhhbb/BuilderPattern)

