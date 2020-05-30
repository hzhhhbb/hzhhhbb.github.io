---
layout: default
title: 单例模式
nav_order: 1
parent: 设计模式
description: "单例模式"
---

# 单例模式
此文章第一次发布于[博客园](https://www.cnblogs.com/hzhhhbb/p/11373553.html)

## 引言
单例模式应该算是23种设计模式中比较简单的，它属于创建型的设计模式，关注对象的创建。

## 概念
单例模式是23个“Gang Of Four”的设计模式之一，它描述了如何解决重复出现的设计问题，以设计灵活且可复用的面向对象软件，使对象的实现、更改、测试和重用更方便。

### 单例模式解决了以下问题：
- 如何确保类只有一个实例？
- 如何轻松地访问类的唯一实例？
- 如何控制类的实例化？
- 如何限制类的实例数量？

### 单例模式是如何解决以上问题的呢？
- 隐藏类的构造函数。
- 定义一个返回类的唯一实例的公共静态操作。

这个设计模式的关键点在于使类控制其自身的实例化。

隐藏类的构造函数（定义私有构造函数）来确保类不能从外部实例化。

使用静态函数轻松访问类实例（Singleton.getInstance()）。

## 实现
- 懒汉式单例
```csharp
    using System.Threading;

    public class SingletonTest
    {
        private static SingletonTest instance = null;

        /// <summary>
        /// 隐藏类的构造函数（定义私有构造函数）来确保类不能从外部实例化
        /// </summary>
        private SingletonTest()
        {
            Console.WriteLine("******单例类被实例化******");
        }

        /// <summary>
        /// 使用静态函数轻松访问类实例
        /// </summary>
        /// <returns><see cref="SingletonTest"/></returns>
        public static SingletonTest GetInstance()
        {
            if (instance == null)
            {
                instance = new SingletonTest();
            }

            return instance;
        }

        public void PrintSomething()
        {
            Console.WriteLine($"当前线程Id为{Thread.CurrentThread.ManagedThreadId}");
            Console.WriteLine("Singleton Pattern Test");
        }
    }
```

上述代码在单线程的情况下是能正常运行的，符合单例模式的定义。

但是，多线程的情况呢？

我们使用以下代码进行测试
```csharp
           // 多线程情况
    for (int i = 0; i < 10; i++)
    {
        Task.Run(() =>
                    {
                        SingletonTest singleton1 = SingletonTest.GetInstance();
                        singleton1.PrintSomething();
                    });
    }
```
结果如下

![多线程执行结果](/assets/images/docs/design-pattern/singleton-pattern/1.png)

不出所料，类SingletonTest被实例化了多次，不符合单例模式的要求，那如何解决这个问题呢？

既然是多线程引起的问题，那就要使用线程同步。我们在这里使用锁来实现。
```csharp
    using System;
    using System.Threading;

    public class SingletonTest
    {
        private static SingletonTest instance = null;

        private static object lockObject = new object();

        /// <summary>
        ///  隐藏类的构造函数（定义私有构造函数）来确保类不能从外部实例化
        /// </summary>
        private SingletonTest()
        {
            Thread.Sleep(500);
            Console.WriteLine("******单例类被实例化******");
        }

        /// <summary>
        /// 使用静态函数轻松访问类实例
        /// </summary>
        /// <returns><see cref="SingletonTest"/></returns>
        public static SingletonTest GetInstance()
        {
            // 双重检查锁定的方式实现单例模式
            if (instance == null)
            {
                lock (lockObject)
                {
                    if (instance == null)
                    {
                        instance = new SingletonTest();
                    }
                }
            }

            return instance;
        }

        public void PrintSomething()
        {
            Console.WriteLine($"当前线程Id为{Thread.CurrentThread.ManagedThreadId}");
            Console.WriteLine("Singleton Pattern Test");
        }
    }
```

上述代码在创建实例前，检查了两次实例是否为空，第一次判空是否有必要呢（上述代码26行）？为什么呢？我们想象这样的一种场景，在已经初始化类实例的情况下，是否还需要获取锁？答案是不需要，所以加第一个判断条件（上述代码26行）。

再次运行测试代码，结果如下：
![多线程执行结果2](/assets/images/docs/design-pattern/singleton-pattern/2.png)

从结果来看，类只被实例化了一次，解决了多线程下类被多次实例化的问题。***但是指令重排序是否对此有影响？是否需要volatile关键字？欢迎大佬来解答一下。***

- 饿汉式单例（推荐）

第一种方式有点繁琐，可以简单点吗？如下
```csharp
    using System;
    using System.Threading;

    public class SingletonTest2
    {
        // 静态变量的方式实现单例模式
        private static readonly SingletonTest2 Instance = new SingletonTest2();

        private SingletonTest2()
        {
            Thread.Sleep(1000);
            Console.WriteLine("******单例类被实例化******");
        }

        public static SingletonTest2 GetInstance()
        {
            return Instance;
        }

        public void PrintSomething()
        {
            Console.WriteLine($"当前线程Id为{Thread.CurrentThread.ManagedThreadId}");
            Console.WriteLine("Singleton Pattern Test");
        }
    }
```

这种实现方式利用的是.NET中静态关键字static的特性，使单例类在使用前被实例化，并且只实例化一次，这个由.NET框架保证。

这种方式存在问题，在没有使用到类中的成员时候就创建实例了，能否在使用到类成员的时候才创建实例呢？如下图，我们使用了Lazy关键字来延迟实例化。
```csharp
    using System;
    using System.Threading;

    public class SingletonTest2
    {
        // 静态变量的方式实现单例模式
        private static readonly Lazy<SingletonTest2> Instance = new Lazy<SingletonTest2>(() => new SingletonTest2());

        private SingletonTest2()
        {
            Thread.Sleep(1000);
            Console.WriteLine("******初始化单例模式实例*****");
        }

        public static SingletonTest2 GetInstance()
        {
            return Instance.Value;
        }

        public void PrintSomething()
        {
            Console.WriteLine($"当前线程Id为{Thread.CurrentThread.ManagedThreadId}");
            Console.WriteLine("Singleton Pattern Test");
        }
    }
```
- 例外

值得注意的是，反射会破坏单例模式，如下代码，能直接调用类的私有构造函数，再次实例化。
```csharp
// 反射破坏单例
 var singletonInstance = System.Activator.CreateInstance(typeof(SingletonTest2), true);
```
怎么避免呢？类的实例化都需要调用构造函数，那么我们在构造函数中加入判断标识即可。尝试实例化第二次的时候，就会抛异常。

```csharp
        private static bool isInstantiated;

        private SingletonTest2()
        {
            if (isInstantiated)
            {
                throw new Exception("已经被实例化了，不能再次实例化");
            }

            isInstantiated = true;
            Thread.Sleep(1000);
            Console.WriteLine("******单例类被实例化******");
        }
```
- 应用

那么实际应用中，哪些地方应该用单例模式呢？在这个类只应该存在一个对象的情况下使用。哪些地方用到了单例模式呢？

1. Windows任务管理器
2. HttpContext.Current

- 总结

俗话说，凡事都有两面性。单例模式确保了类只有一个实例，也引入了其他问题：

2. 单例模式中的唯一实例变量是使用static标记的，会常驻内存，不被GC回收，长期占用了内存
3. 在多线程的情况下，使用的都是同一个实例，所以需要保证类中的成员都是线程安全，不然可能会导致数据混乱的情况

代码下载：[https://github.com/hzhhhbb/SingletonPattern](https://github.com/hzhhhbb/SingletonPattern)

- 参考资料

1. [https://en.wikipedia.org/wiki/Singleton_pattern](https://en.wikipedia.org/wiki/Singleton_pattern)
2. [https://docs.microsoft.com/zh-cn/dotnet/api/system.lazy-1?view=netcore-3.0](https://docs.microsoft.com/zh-cn/dotnet/api/system.lazy-1?view=netcore-3.0)