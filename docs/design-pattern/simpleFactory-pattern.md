---
layout: default
title: 简单工厂模式
nav_order: 4
parent: 设计模式
description: "简单工厂模式"
---

# 简单工厂模式
此文章第一次发布于[博客园](https://www.cnblogs.com/hzhhhbb/p/11406771.html)

## 概念
简单工厂模式是属于创建型设计模式，关注于对象的创建。

我们来考虑一个支付的场景，在点外卖的时候，可以使用选择支付宝、微信支付、ApplePay等支付方式。

这些支付方式虽然名字不一样，但是用法和流程基本类似，都包括了验证账号的合法性、检查支付环境的安全性、验证支付密码、从账号里扣款、通知用户支付结果等功能。

有共性，我们就抽象出一个基类，然后各种支付方式子类继承它，再实现自己的业务逻辑。

如果我们希望在使用这些支付方式时，不需要知道这些具体支付方式子类的名字，只需要知道支付方式名字，把该名字传入一个方法即可返回一个相应的对象，此时，就可以使用简单工厂模式。

## 实现
1. 首先定义一个各种支付方式的抽象类，简单起见，定义了判断账号是否正常、支付、通知用户几个方法

```csharp
namespace SimpleFactory
{
    using System;

    public abstract class AbstractPaymentMethod
    {
        /// <summary>
        /// 判断用户的账号是否正常
        /// </summary>
        /// <param name="accountNumber">账号</param>
        /// <returns>账号是否正常</returns>
        public abstract bool IsAccountNormal(string accountNumber);

        /// <summary>
        /// 通知用户
        /// </summary>
        /// <param name="message">通知内容</param>
        public abstract void NoticeUser(string message);

        /// <summary>
        /// 支付过程
        /// </summary>
        /// <param name="accountNumber">用户账号</param>
        /// <param name="amount">金额</param>
        public virtual void Pay(string accountNumber, decimal amount)
        {
            if (this.IsAccountNormal(accountNumber))
            {
                Console.WriteLine($"账号：{accountNumber}已支付{amount}元");
                this.NoticeUser($"尊敬的{accountNumber}，您已成功支付{amount}元");
            }
        }
    }
}
```

2. 实现支付宝支付、微信支付

```csharp
using System;

namespace SimpleFactory
{
    public class AliPay : AbstractPaymentMethod
    {
        public override bool IsAccountNormal(string accountNumber)
        {
            return true;
        }

        public override void NoticeUser(string message)
        {
            Console.WriteLine("支付宝支付");
            Console.WriteLine(message);
        }

    }
}

using System;

namespace SimpleFactory
{
    public class WeiXinPay : AbstractPaymentMethod
    {
        public override bool IsAccountNormal(string accountNumber)
        {
            return true;
        }

        public override void NoticeUser(string message)
        {
            Console.WriteLine("微信支付");
            Console.WriteLine(message);
        }
    }
}
```

3. 再定义一个工厂，用来创建这两种支付方式。这里的工厂方法通过判断一个枚举值（PaymentMethodEnum ），来确定需要使用的支付方式

```csharp
namespace SimpleFactory
{
    using System;

    public class PaymentMethodFactory
    {
        public static AbstractPaymentMethod GetPaymentMethod(PaymentMethodEnum paymentMethod)
        {
            switch (paymentMethod)
            {
                case PaymentMethodEnum.AliPay:
                    return new AliPay();
                case PaymentMethodEnum.WeiXinPay:
                    return new WeiXinPay();
                default:
                    throw new NotImplementedException();
            }
        }
    }
}
// 枚举类
namespace SimpleFactory
{
    public enum PaymentMethodEnum
    {
        /// <summary>
        /// 支付宝
        /// </summary>
        AliPay = 0,

        /// <summary>
        /// 微信支付
        /// </summary>
        WeiXinPay = 1
    }
}
```

4. 模拟客户端调用一下

```csharp
namespace SimpleFactory
{
    using System;

    class Program
    {
        static void Main(string[] args)
        {
            AbstractPaymentMethod aliPay = PaymentMethodFactory.GetPaymentMethod(PaymentMethodEnum.AliPay);
            AbstractPaymentMethod weiXinPay = PaymentMethodFactory.GetPaymentMethod(PaymentMethodEnum.WeiXinPay);
            aliPay.Pay("Vincent", 700M);
            Console.WriteLine("*********************************");
            weiXinPay.Pay("123456", 1000M);
            Console.ReadKey();
        }
    }
}
```

看看结果

![结果](/assets/images/docs/design-pattern/simpleFactory-pattern/1.png)

## 总结
### 简单工厂模式的优点
- 工厂类含有必要的判断逻辑，可以决定在什么时候创建哪一个产品类的实例，客户端可以免除直接创建产品对象的责任，而仅仅“消费”产品；简单工厂模式通过这种做法实现了对责任的分割，它提供了专门的工厂类用于创建对象。
- 客户端无须知道所创建的具体产品类的类名，只需要知道具体产品类所对应的参数即可，对于一些复杂的类名，通过简单工厂模式可以减少使用者的记忆量。
- 通过引入配置文件，可以在不修改任何客户端代码的情况下更换和增加新的具体产品类，在一定程度上提高了系统的灵活性。

### 简单工厂模式的缺点
- 由于工厂类集中了所有产品创建逻辑，一旦不能正常工作，整个系统都要受到影响。
- 使用简单工厂模式将会增加系统中类的个数，在一定程序上增加了系统的复杂度和理解难度。
- 系统扩展困难，一旦添加新产品就不得不修改工厂逻辑，在产品类型较多时，有可能造成工厂逻辑过于复杂，不利于系统的扩展和维护。
- 简单工厂模式由于使用了静态工厂方法，造成工厂角色无法形成基于继承的等级结构。

### 基于以上的优缺点，简单工厂模式适用于以下场景
- 工厂类负责创建的对象比较少：由于创建的对象较少，不会造成工厂方法中的业务逻辑太过复杂。
- 客户端只知道传入工厂类的参数，对于如何创建对象不关心：客户端既不需要关心创建细节，甚至连类名都不需要记住，只需要知道类型所对应的参数。

代码下载：[https://github.com/hzhhhbb/SimpleFactory](https://github.com/hzhhhbb/SimpleFactory)

## 参考资料
　[https://design-patterns.readthedocs.io/zh_CN/latest/creational_patterns/simple_factory.html#id2](https://design-patterns.readthedocs.io/zh_CN/latest/creational_patterns/simple_factory.html#id2)
