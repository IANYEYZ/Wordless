# Wordless
Wordless is a programming language that has no reserved words

It was designed specifically for fast prototyping and concept proving

## Syntax
There's no reserved word in Wordless(there is some pre-defined ones, for something like print(x)).

```
~ Function define:
sum = (x, y) |> (x + y)
~ Matching:
a = [
    b == 1 -> c,
    d == 1 -> e
]
~ Array construction:
{
    x = x + 1,
    print(x)
}
~ For? Recursion!
fact = x |> [
    x == 0 -> 1
    x != 0 -> x * fact(x - 1)
]

~ IO
input(x)
print(x)

~ For comment
```

## Build
First:

`pip install click`

Second:

`python wordless.py {filename}`
