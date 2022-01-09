# Ex4-OOP - Pokemon Game
#### Authors: Lior Shacohach & Moriya Barel & Liel Biton

In this project we were required to implement a pokemon "game" using our previous task which was implementing directed weighted graph, graphic representation of the graph
as well as various applicable algorithms.

## About the Game

The game is about agents catching as many pokemons as possible, agents are "running" from node to node on the graph's edges, while pokemons are spawning on edges in between nodes.


| Class | Description |
| ------ | ------ |
| mynode | Represents the graphs vertices |
| DiGraph | Represents the Directed Weighted Graph |
| GraphAlgo | Holds a DiGraph to run desired algorithms on |
| GUI | Represents the board, paints the graph, the agents and the pokemons |
| Agent | Represents our Agent object |
| Pokemon | Represents our Pokemons |
| Game | Using all the other classes to execute our algorithm |

## GUI Example
![pokemon](https://user-images.githubusercontent.com/92747945/148688959-e3550506-dc02-4484-bbca-2afef3297a04.gif)


## UML
![uml](https://i.imgur.com/Gcr4XoE.png)

## How to Run:

Download the zip, extract the files, open terminal / cmd, use the cd command to change directory to src folder:
```sh
cd src
```
now to run the server type:
```sh
java -jar Ex4_Server_v0.0.jar 11
(11 represents the case we are running, could be any number between 0-15)
```
now run our main program:
```sh
python main.py
```

