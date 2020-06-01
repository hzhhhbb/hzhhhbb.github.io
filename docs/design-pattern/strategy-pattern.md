---
layout: default
title: 策略模式
nav_order: 6
parent: 设计模式
description: "策略模式"
---

# 策略模式
此文章第一次发布于[博客园](https://www.cnblogs.com/hzhhhbb/p/11538083.html)

## 引言
在讲策略模式之前，我们来看零售行业软件的一个针对客户类型打折的功能。

vip客户打八折，svip客户打七折。

```csharp
if (customer == "vip")
 {
       amount = amount * 0.8;
 }
 else if (customer == "svip")
 {
       amount = amount * 0.7;
 }
```

看代码，挺简单的，但是如果今天vip打八折，明天要打7折，那还得改变原有的代码，这样就违背了开闭原则。这里变化的是折扣的计算方式（策略），策略模式就可以解决这类问题。

## 概念
策略模式是一种对象行为型模式。策略模式(Strategy Pattern)：定义一系列算法，将每一个算法封装起来，并让它们可以相互替换。

## 实现
策略模式包含三种角色：Context: 上下文类、Strategy: 抽象策略类、ConcreteStrategy: 具体策略类

抽象策略类：

```csharp
    public abstract class AbstractDiscountStrategy
    {
        public abstract decimal Discount(decimal amount);
    }
```

具体策略类：

```csharp
    public class VipDiscountStrategy:AbstractDiscountStrategy
    {
        public override decimal Discount(decimal amount)
        {
            return amount * 0.8M;
        }
    }

    public class SVipDiscountStrategy:AbstractDiscountStrategy
    {
        public override decimal Discount(decimal amount)
        {
            return amount * 0.7M;
        }
    }
```
环境类：

```csharp
    public class StrategyContext
    {
        private AbstractDiscountStrategy discountStrategy;

        public StrategyContext(AbstractDiscountStrategy concreteDiscountStrategy)
        {
            this.discountStrategy = concreteDiscountStrategy;
        }

        public decimal ExecuteStrategy(decimal amount)
        {
            return this.discountStrategy.Discount(amount);
        }
    }
```

调用：

```csharp
    if (customer == "vip")
    {
        context = new StrategyContext(new VipDiscountStrategy());
        amount = context.ExecuteStrategy(amount);
    }
    else if (customer == "svip")
    {
        context = new StrategyContext(new SVipDiscountStrategy());
        amount = context.ExecuteStrategy(amount);
    }
```
可以看到，应用策略模式后，如果要修改vip客户的折扣计算方式，只需要修改对应的策略即可，不需要修改客户端的调用代码，也不会影响到svip的折扣计算方式，符合开闭原则。

再来一个ssvip客户，只需要增加一个对应的策略实现类，并且修改客户端的调用方法即可。

vip和svip的策略可以互换。

## 总结
从上面的例子可以看出来，策略模式的优点是提供了对“开闭原则”的完美支持，用户可以在不修改原有系统的基础上选择算法或行为，也可以灵活地增加新的算法或行为。

缺点也很明显，客户端必须清楚知道每一个策略的用途，并且自行决定使用哪一个策略，增加了客户端的负担，这个问题可以使用配置的方式来解决。每一个策略都需要一个类，会使策略类增多。

代码下载：[https://github.com/hzhhhbb/StrategyPattern](https://github.com/hzhhhbb/StrategyPattern)