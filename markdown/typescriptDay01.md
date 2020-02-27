TypeScript note day01

## typescrip 的基本数据类型和js相同：

1. boolean：布尔值，true和false
2. null：表名null值的特殊关键字
3. undefind：变量未定义时的属性
4. number：数字，整数和浮点数
5. symbol：实例是唯一的不可变的
6. object：对象，可视为存放值的容器

## 变量的类型和定义

typescript是类型跟js相同，定义是可以指定变量的类型，课可以忽略，typescript会自动推断

```typescript
// defind a number
let num: number 5;
let bigNum: number = 1_000_000;
// defind a string
let name: string = "xiaoming";
let anotherName = "xiaohong";
// defind a templete string
let sentence: string `Hello, my name is ${name}. I'll be ${age + 1} years old next month`;  // use `` to excute a templete
// equal to
let sentenceTwo: string = "Hello, my name is " + name + ". I'll be" + (age + 1) + "ears old next month";
```



```typescript
// defind an array
let list: number[] = [1, 2, 3];
// equal to
let list: Array<number> = [1, 2, 3];
```

typescript也支持any类型的定义，如果你想控制变量的数据类型，可以使用断言：

```typescript
let oneString: any = "this is a string";
let stringLength: number = (<string>oneString).length;
// or use as to assert
let stringLength: number = (oneString as string).length;  // 推荐使用as
```

## 泛型

