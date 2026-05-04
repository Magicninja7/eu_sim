This is a simulated politics game. It is based on events, some are random, and others are chained, meaning you choices will impact what further events you may get.
Furthermore, each choice results in a slight policies and stat change, which slowly tick towards you general stats of a country, and if any reaches zero, you lose!
![stuff](https://cdn.hackclub.com/019df3b1-b554-783c-a24c-1da713d60bb0/image.png)

## Explanations for what files do
### app
This folder has the app.py file, which is the backend flask file. It import functions from basically all other python files. It handles processing the event, and has functions such as a day counter.

### chain_of_events
This folder contains the chain of event logic. In the 'events' folder there are chain of events, where each file create a tree of events that can happen depentent on your previous decisions. 

### generaliser
it generalises specific stats of your country to a single number of a category, ex economy.

### pol_2_stat
this one translates how your policy looks likes (changed by the decisions you take), and translate it into stats about your country

### random_events_gen
A WIP feature, which generates unique random events, by using a set of places, actions, and states, to create an event. Like Putin Bombs Kiev, from a set of the Ukraine war.

### other files
the rest of the files, js css and html, are for the frontend.
