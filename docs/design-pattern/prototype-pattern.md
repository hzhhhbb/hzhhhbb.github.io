---
layout: default
title: 原型模式
nav_order: 1
parent: 设计模式
description: "原型模式"
---

# 原型模式

此文章第一次发布于[博客园](https://www.cnblogs.com/hzhhhbb/p/11386236.html)

## 概念

原型模式属于创建型设计模式。当要创建的对象类型由原型实例确定时使用它，该实例被克隆以生成新对象。

此模式用于

- 避免客户端应用程序中的对象创建者的子类，如工厂方法模式。
- 避免以标准方式创建新对象的固有成本（例如，使用'new'关键字），当它对于给定的应用程序来说过于昂贵时。

上述定义来自[wiki](https://en.wikipedia.org/wiki/Prototype_pattern)，简单来说，***就是创建一个全新的对象代价太高时，比如耗时太长时，能直接从现有实例中以较小的代价克隆出一个对象。***

## 实现

实现原型模式的方式之一为克隆，下面我们来实现一下

1. 先定义一个抽象原型，包含两个克隆的虚方法（方便子类重写）
```csharp
namespace PrototypePattern
{
    using System;
    using System.IO;
    using System.Runtime.Serialization.Formatters.Binary;

    [Serializable]
    public abstract class AbstractPrototype 
    {
        /// <summary>
        /// 浅克隆
        /// <remarks>使用objectMemberwiseClone</remarks>
        /// </summary>
        /// <returns>当前对象副本</returns>
        public virtual AbstractPrototype Clone()
        {
            return (AbstractPrototype)this.MemberwiseClone();
        }

        /// <summary>
        /// 深克隆
        /// <remarks>使用二进制序列化反序列化实现</remarks>
        /// </summary>
        /// <returns>当前对象副本</returns>
        public virtual AbstractPrototype DeepClone()
        {
            MemoryStream stream = new MemoryStream();
            BinaryFormatter binaryFormatter = new BinaryFormatter();
            binaryFormatter.Serialize(stream, this);
            stream.Position = 0;
            var instance = (AbstractPrototype)binaryFormatter.Deserialize(stream);
            stream.DisposeAsync();
            return instance;
        }
    }
}
```
2. 需要实现原型模式的类继承此抽象类即可

```csharp
namespace PrototypePattern
{
    using System;

    [Serializable]
    public class ConcretePrototype : AbstractPrototype
    {
        public int Number { get; set; }

        public Person Person { get; set; }
    }
}
```

Person类

```csharp
namespace PrototypePattern
{
    using System;

    [Serializable]
    public class Person
    {
        public string Name { get; set; }

        public int Age { get; set; }
    }
}
```

以上代码就实现了原型模式。

其中的克隆方式又分为浅克隆，深克隆，深克隆使用的是序列化反序列化的方式（需要在类上增加[Serializable]特性）。

浅克隆
复制出来的对象的所有变量都含有与原来的对象相同的值，而所有的对其他对象的引用仍然指向原来的对象。

深克隆
复制出来的所有变量都含有与原来的对象相同的值，那些引用其他对象的变量将指向复制出来的新对象，是一个全新的副本。

我们来测试一波

```csharp
{
                ConcretePrototype no0 = new ConcretePrototype() { Number = 0, Person = new Person() { Age = 17, Name = "Vincent" } };
                Console.WriteLine("第一次构造");
                Console.WriteLine($"No0：Number:{no0.Number}，Age:{no0.Person.Age}，Name:{no0.Person.Name}");

                Console.WriteLine("从No0浅克隆到No1");
                ConcretePrototype no1 = (ConcretePrototype)no0.Clone();

                Console.WriteLine("修改No1");
                no1.Person.Age = 18;
                no1.Person.Name = "Vincent1";
                Console.WriteLine($"No0：Number:{no0.Number}，Age:{no0.Person.Age}，Name:{no0.Person.Name}");
                Console.WriteLine($"No1：Number:{no1.Number}，Age:{no1.Person.Age}，Name:{no1.Person.Name}");
                Console.WriteLine("******************");

                Console.WriteLine("从No0浅克隆到No2");
                ConcretePrototype no2 = (ConcretePrototype)no0.DeepClone();
                Console.WriteLine("修改No2");
                no2.Person.Age = 19;
                no2.Person.Name = "Vincent2";
                Console.WriteLine($"No0：Number:{no0.Number}，Age:{no0.Person.Age}，Name:{no0.Person.Name}");
                Console.WriteLine($"No2：Number:{no2.Number}，Age:{no2.Person.Age}，Name:{no2.Person.Name}");
                Console.WriteLine("******************");
            }
```

看看结果

![结果](/assets/images/docs/design-pattern/prototype-pattern/1.jpg)

可以看到，通过浅克隆得到的对象和原对象共享引用对象，深克隆的反之。

以上是一般的实现方式，但是这里使用的是继承抽象原型类的方式。我们知道，C#里是单继承，我们这里继承了抽象的原型类，就不能继承其他类了，难免会有些不方便。下面我们来改进一下。

## 改进

我们知道.NET框架里为我们提供了ICloneable接口，此接口只包含一个返回值为object的Clone方法。object类中提供了返回值为object、访问级别为protected的MemberwiseClone方法。那么我们只需要继承ICloneable接口，实现Clone方法，把Clone方法访问级别改为public即可实现原型模式，如下

```csharp
namespace PrototypePattern
{
    using System;

    [Serializable]
    public class ConcretePrototype2 : ICloneable
    {
        public int Number { get; set; }

        public Person Person { get; set; }

        /// <summary>Creates a new object that is a copy of the current instance.</summary>
        /// <returns>A new object that is a copy of this instance.</returns>
        public object Clone()
        {
           return this.MemberwiseClone();
        }
    }
}
```

这里只有浅克隆，没有深克隆，怎么办？我们使用扩展方法，为ICloneable接口扩展一个深克隆方法，如下

```csharp
namespace PrototypePattern
{
    using System;
    using System.IO;
    using System.Runtime.Serialization.Formatters.Binary;

    public static class ICloneableExtension
    {
        public static T DeepClone<T>(this ICloneable instance)
        {
            MemoryStream stream = new MemoryStream();
            BinaryFormatter binaryFormatter = new BinaryFormatter();
            binaryFormatter.Serialize(stream, instance);
            stream.Position = 0;
            var duplicate = binaryFormatter.Deserialize(stream);
            stream.DisposeAsync();
            return (T)duplicate;
        }
    }
}
```

## 总结
以上的实现只能应对一般的情况，如果需要应对复杂的情况，如克隆对象中指定的对象（例如单据的复制），就需要改进或增加克隆的实现方式。

文中的代码下载：[https://github.com/hzhhhbb/PrototypePattern](https://github.com/hzhhhbb/PrototypePattern)

## 参考资料
[https://en.wikipedia.org/wiki/Prototype_pattern](https://en.wikipedia.org/wiki/Prototype_pattern)