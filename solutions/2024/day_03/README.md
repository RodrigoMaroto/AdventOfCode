# Day 3 (2024)

`Mull It Over` ([prompt](https://adventofcode.com/2024/day/3))

Day 3 looked at first like I would need to do a parser/compiler, but the problem wasn't as complex in the end.

## Part 1
In this first part, we are given a long text, very unstructured that looks like some type of broken code. For this first part we only need to focus on the `mul(X,Y)` instructions, where X and Y are integers and the syntax has to be very exact, not allowing even spaces.  

The best way to deal with this is a **Regular Expression (RegEx)** to find all instances that fit this pattern.  
In the pattern used, we can note the use of `\d{1,3}` because the problem stated that integers should have between 1-3 digits, but if this wasn't a restriction it would be better to use `\d+` (in the input I recieved both would work correctly).   
Also by putting the digits between parenthesis, the `re.findall()` function will just return them ignoring the `mul()` which will only be used to find the expressions. This will return a list of tuples containing two strings that are the integers that will be multiplied.  

```
"mul(12,36)"  ->  [('12', '36')]  
```

To obtain the solution we just need to multiply and sum all the results.
```py
class Solution(TextSolution):
    def part_1(self) -> int:
        valid_expr = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", self.input)
        return sum(int(x[0]) * int(x[1]) for x in valid_expr)
```

## Part 2
For this second part, we can reuse the code from Part 1, but we now have to take into account the `do()` and `don't()` calls. We should ignore all multiplications that come after a don't before reaching another do. Also, we can suppose that the code starts with a do.  

My approach to this was to get rid of all the *disabled* code and then simply do the same as in Part 1.  

First of all if we split the text by `do()` we can treat each like a mini program where it will be enabled unless stated otherwise. In each of this programs, we can guarantee that everything before a `don't()` will be enabled and after it will be disabled, se we can simply split the string again and only keep the first element.  

Afterwards we can simply concatenate all the strings and run the same RegEx as before.
```py
class Solution(TextSolution):
    def part_2(self) -> int:
        valid_code = self.input.split("do()")
        valid_code = [x.split("don't()")[0] for x in valid_code]
        valid_code = "".join(valid_code)
        valid_expr = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", valid_code)
        return sum(int(x[0]) * int(x[1]) for x in valid_expr)
```
