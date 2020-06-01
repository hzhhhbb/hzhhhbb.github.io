---
layout: default
title: 模板模式
nav_order: 5
parent: 设计模式
description: "模板模式"
---
# 模板模式
此文章第一次发布于[博客园](https://www.cnblogs.com/hzhhhbb/p/11489382.html)

## 概念
模板方法模式属于行为类设计模式。

定义：定义一个操作中的算法框架，而将一些步骤延迟到子类中。使子类可以不改变一个算法的结构即可重定义该算法的某些步骤。

简单来说，它就是抽象类（模板）和子类（具体的实现）组成，抽象类中定义了这个类需要完成的功能和逻辑，子类负责重写某些特定业务的方法。

例如，在日常开发工作中，会有很多数据需要保存到数据库中。保存数据一般需要经过校验数据合法性、保存数据到数据库、返回数据到客户端这三个步骤。保存的数据不一样，它的校验规则也是不一样的。在这种情况下，我们就可以把这三个逻辑放在一个抽象类里，把校验数据这个方法写成虚方法，供不同的子类去重写。从而达到代码复用和不同的数据有不同的校验规则的效果。

## 实现
1. 定义一个抽象类

```csharp
public abstract class AbstractSave
   {
       public abstract void BeforeSave();

       public abstract void AfterSave();

       public void SaveData()
       {
           Console.WriteLine("数据成功保存到数据库");
       }

       public void Save()
       {
           this.BeforeSave();
           this.SaveData();
           this.AfterSave();
       }
   }
```
2. 定义子类

```csharp
public class ConcreteSave : AbstractSave
    {
        public override void BeforeSave()
        {
            Console.WriteLine("数据A保存前的校验");
        }

        public override void AfterSave()
        {
            Console.WriteLine("数据A保存后的操作");
        }
    }
```

3. 调用一下

```csharp
static void Main(string[] args)
        {
            AbstractSave data1 = new ConcreteSave();
            data1.Save();

            Console.WriteLine();

            AbstractSave data2 = new ConcreteSave();
            data2.Save();
        }
```

## 总结
我觉得这个设计模式挺好懂的。一般用在什么场景呢？例如在实际工作中，一个需求来了，架构师或者高级工程师把业务逻辑理清楚，搭建好基本框架，然后分配具体的实现任务给其他工程师。这个时候，模板方法模式就能派上用场了，既能保证大方向不出错，又能把具体的实现任务分离出去，一举两得。

上面的实现比较简单，在实际工作中，一般会结合泛型来使用，在抽象类中，把要保存的数据类型声明为泛型，返回的数据也声明为泛型。

代码下载：[https://github.com/hzhhhbb/TemplateMethodPattern](https://github.com/hzhhhbb/TemplateMethodPattern)