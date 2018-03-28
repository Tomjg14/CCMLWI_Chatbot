# WeatherBot
WeatherBot by Tom Janssen Groesbeek (s4229738) and Max Moons (). Two students from the Radboud University Nijmegen.

## Idea

This blogpost describes our own implementation of a weather bot. It is a telegram based bot specialized in the weather domain. This means that you can send it a location or placename via the Telegram app and the bot will be able to respond with location related weather information. The development of the bot is partially based on part 1 and 2 of the following tutorial: [www.codementor.io](https://www.codementor.io/garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay). We also made use of the [openweathermap.org](openweathermap.org/api) to let the bot retrieve weather information. 

## Telegram Tutorial

To get started on our bot we followed the tutorial by Gareth Dwyer on codementor. The original tutorial explains how to make a todo bot using the telegram api. The todo bot simply keeps track of the input provided by a telegram user. It echos the input and if an input is repeated it removes this input from the memory. So the bot can be used to keep a 'todo' list from which items are removed when repeated. 

Because we followed this tutorial, our bot was created by making use:
* Python 3.5
* Telegram
* SQL

In order to get in contact with our telegram bot, simply add the following user to your telegram contacts:

@echo1493_bot

## Weather API

After finishing the tutorial we thought it would be could to turn or todo bot into a 'weatherbot'. We envisioned the bot being able to provide information on the weather when a placename or location is given. The most basic version of our bot should at least return this weather information. But we were already brainstorming about possible improvements and additional functionality. Like that it should be able to recognize a placename in a sentence. Or that it should respond with either more positive or more negative tone depending on weather in Nijmegen.

To get started on our weatherbot, we decided to take a look at the openweathermap api. 

## Creating The Bot

This section provides in-depth information on our weatherbot code. Here we explain the different classes that the bot is made up of and what packages were included to ensure that the bot functions correctly. At the end of this section you will find information on the normal workflow of the code when the bot is being used. The next section includes a demo of our bot.

### Different Classes

### Important Packages

### Simple Workflow

## Demo
