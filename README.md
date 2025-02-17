# Abylon
Abylon is a dynamically typed compiled programming language.
Actually, it is transpiled, meaning your Abylon code is translated into C, before then being compiled, this holds it back, but, this is more of a demo then anything until I build my compiler (coming soon)

# Tutorial

## Getting started

To start, make sure you have gcc installed, I am going to update this to add support for any compiler installed by the user.<br>
Make sure that `main.py` is installed, obviously.<br>
<b>(Keep in mind, Abylon requires no dependencies beyond gcc and python, pretty neat)</b><br>
After all these requirements are satisfied, you can start writing your first program, create a file ending with `.abyl` and you're ready!<br>

## Writing your first program
Lets start by doing a simple "Hello World!" in Abylon.<br>
Begin by initialising the `main` function, this is where your code will run.<br>
<b>*(Keep in mind, Abylon doesnt support functions yet, sadly, only the `main` function is supported, sorry, I plan on introducing functions later)*</b><br>
This is what the main function looks like:
```kotlin
fun main(){
}
```
Lets actually do stuff here, this is how you would print out hello world:
```kotlin
fun main(){
write "Hello, World!"
}
```
In Abylon, you can use `write` or `put` to output things. `write` will output values with a newline at the end, wheras `put` will output values with no newline.<br>
This is an example to show the difference:<br>
```kotlin
fun main(){
  write "Hello, "
  write "World!"
}
```
This would output:
```
Hello,
World!
```
But, if your program used `put` like this:
```kotlin
fun main(){
  put "Hello, "
  put "World!"
}
```
This would output:
```
Hello, World!
```

## Variables
```kotlin
fun main(){
  var hello = "Hello, World!"
  write hello
}
```
And as you can see, writing variables is as simple as that. Heres an example with some numbers:
```kotlin
fun main(){
  var x = 100
  var y = 100
  var z = x+y
  write z * z
}
```
You can reassign variables and assign variables to other variables, another example with strings:

```kotlin
fun main(){
  var hello = "Hello, " + "World!"
  write hello
  var hello = "Sup, World!"
  write hello
}
```
You can also assign a variable to be the sum of others, heres an example:
```kotlin
fun main(){
  var hello = "Hello, "
  var world = "World!"
  var greeting = hello + world

  var num1 = 100
  var num2 = 200
  var sum = num1 + num2

  write greeting
  write sum
}
```

### Other Variable types
This is an example of floats and booleans in Abylon
```kotlin
fun main(){
  var bool1 = true
  var bool2 = false
  write bool1 + bool2
  var flt = 1.1
  write flt*flt
}
```
## Input
Getting input with Abylon is easy, for example, if I wanted to get the users name, this is what it would look like:
```kotlin
fun main(){
  var name = read "Enter your name> "
}
```
In my example I have some text that will be displayed before getting input, you dont need this though, for example:
```kotlin
fun main(){
  var name = read
}
```
However, when getting input of different types, you need to specify.`read` will by default get string input, but if you wanted to get an integer or a float, you would have to use different keywords, for example:

```kotlin
fun main(){
  var userName = read "Enter your name>"
  var userSecondName = readStr "Enter your second name>"
  var userAge = readInt "Enter your age>"
  var userBalance = readFlt "Enter your account balance>"
}
```
(*Keep in mind, `read` and `readStr` do the same thing in Abylon*)<br>
As you can see, getting input is pretty simple, here is a real life example of an Abylon program that uses input:
```kotlin
fun main(){
    // Getting user values, they're strings so we can use read
    var userName = read "Enter your name: "
    var enemyName = read "Enter the name of your enemy: "

    // Writing with a newline, the opening text
    write "Word on the street is "+userName
    // Using put will print them all on one line.
    put " is a cool dude and "+enemyName
    put " is a doofus."
}
```
## Arrays
Abylon has array support, and although limited, I plan to expand this.<br>
So, to set a variable to be an array, it would look like this:
```kotlin
fun main(){
  var array = [1,2,3,4,5]
}
```
We can access a value from this array like so:
```kotlin
fun main(){
  var array = [1,2,3,4,5]
  write array[0]
  write array[1]
  // This would output '1' then '2'
}
```
We can replace a value from an array using the `replace` keyword:
```kotlin
fun main(){
  var array = ["Hello, ", "World", "!"]
  // Array is "Hello, World!"
  replace array[0] = "Goodbye, "
  // Array is "Goodbye, World!"
}
```
Much more array support will be added, such as an inbuilt sort function and more.
# Compiling
To <s>compile</s> Transpile your code, run the command<br>
`py main.py yourfile.abyl`<br>
There are a few flags you can use, I will use this program and show you how it looks with some of the included flags.<br>
<br>
***test.abyl***
```kotlin
fun main(){
    var hello = "Hello, "
    write hello + "World!"
}
```
### -t flag (Outputs compile speed)
```
py main.py test.abyl -t
Compiled in 0.116s
```

### -c flag (Outputs c code)
```
py main.py test.abyl -c

═════════C CODE═════════
0:   #include <stdio.h>
1:   #include <stdbool.h>
2:   #include <string.h>
3:   #include <stdlib.h>
4:   void main(){
5:   char *hello = "Hello, ";
6:   printf("%s%s\n", hello , "World!");
7:   }
═══════════════════════════
```

### -v flag (Outputs variable table)
```
py main.py test.abyl -v

═════════VARIABLE TABLE═════════
VARIABLE NAME: hello VARIABLE TYPE: STRING:  VARIABLE VALUE: "Hello, "
════════════════════════════════
```

### -r flag (Runs the executable)
```
py main.py test.abyl -r
Hello, World!

```
### -f flag (Keeps the c translated code instead of removing it)
```
py main.py test.abyl -f

```
### In closing
In closing, this is tiny, so small, 500 lines and I want to add more, This is just a tester project and I thought I would get it up here for some community feedback as I want to create my own compiler in c at some point<br>
Thats why I made this project, I want to learn C better and I thought a transpiler from my own baby language into it would help me learn, I was wrong lmao, this was just alot of errors and barely works.
## Thank you for reading though - any contributions are GREATLY appreciated!!!
