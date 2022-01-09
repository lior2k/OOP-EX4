# Ex4-OOP - Pokemon Game
#### Authors: Lior Shacohach & Moriya Barel

In this project we were required to implement a pokemon "game" using our previous task which was implementing directed weighted graph, graphic representation of the graph
as well as various applicable algorithms.

## About the Game

The game is about agents catching as many pokemons as possible, agents are "running" from node to node on the graph's edges, while pokemons are spawning on edges in between nodes.


| Class | Description |
| ------ | ------ |
| mynode | Represents the graphs vertices |
| DiGraph | Represents the Directed Weighted Graph |
| GraphAlgo | Holds a DiGraph to run desired algorithms on |

## GUI Example
![image](https://i.imgur.com/s8MhtOM.png)


## UML
![uml](https://i.imgur.com/51xr2pf.png)

## How to Run:
Option 1:
Download the zip, extract the files, open the project and run the main.py class or the tests classes in the tests directory.

Option 2:
Download the zip, extract the files, open terminal / cmd, use the cd command to change directory to src folder for example:
```sh
cd C:\Users\97250\PycharmProjects\Ex3\src
```
now type:
```sh
python main.py
```
> aside from the 3 check functions given, we added a check4 function, to use check4() you can type: "python main.py 20 4",
> this check inits a random graph into the algorithm using our random graph function and run center and isconnected on it. the first argument (20) stands for the amount of nodes in the random graph
> and then second argument (4) stands for the average amount of out edges per node.
```sh
python main.py 20 4
