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
No brackets are needed when printing or assigning variables. Speaking of which...
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
hello = "Sup, World!"
write hello
}
```
There are a few problems, just with the C transpiling, but, this is a small project and I am working on a larger compiler soon, this is literally only 500 lines or so
### Thank you for reading though - any contributions are GREATLY appreciated!!!
