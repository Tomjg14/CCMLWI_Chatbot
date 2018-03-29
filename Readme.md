# WeatherBot
WeatherBot by Tom Janssen Groesbeek (s4229738) and Max Moons (s4256417). Two students from the Radboud University Nijmegen.

This document contains the following sections:
* [Idea](#Idea)
* [Telegram Tutorial](#telegram-tutorial)
* [Weather API](#weather-api)
* [Creating The Bot](#creating-the-bot)
    * [General Approach](#general-approach)
    * [Different Classes](#different-classes)
    * [Simple Workflow](#simple-workflow)
* [What The Bot Does](#what-the-bot-does)
* [How To Use The Bot](#how-to-use-the-bot)
* [Demo](#demo)
* [Future Improvements](#future-improvements)

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

After finishing the tutorial we thought it would be interesting to see if we could turn or todo bot into a 'weatherbot'. We envisioned the bot being able to provide information on the weather when a placename or location is given. The most basic version of our bot should at least return this weather information. But we were already brainstorming about possible improvements and additional functionality. Like that it should be able to recognize a placename in a sentence. Or that it should respond with either more positive or more negative tone depending on the weather in Nijmegen.

To get started on our weatherbot, we decided to take a look at the openweathermap api. In order to use it with python, you first need to get your own personal OWM API key, which can be obtained by creating account at the openweathermap website. This API key can then be used to create an global OWM object in Python:

```
>>> from pyowm import OWM
>>> API_key = 'PLACE_PERSONAL_API_KEY_HERE'
>>> owm = OWM(API_key)
```

The default language in which the weather information is returned is set at English. This can be adjusted by using the following line of code:

```
>> owm = OWM(language='LANGUAGE') #for example 'en' or 'ru'
```

Now in order to get the weather information of a certain place, the following lines of code can be used:

```
>>> observation = owm.weather_at_place('PLACE,COUNTRY') #e.g. 'London,GB' 
>>> observation = owm.weather_at_id(0123456) #City ID
>>> observation = owm.weather_at_coords(lat,lon) #lat and lon are floats
```

While it is always better to include a country, it is not necessary to obtain a weather observation. By simply providing the function with 'London' would already returned a weather observation. But there might be more than one cities sharing the same name. Therefore, it is better to include the country as well.

Telegram but also other chat apps make it possible for the user to send a location. This location includes a latitude and longitude attribute, which can be used to obtain a observation by making use of the weather_at_coords function. 

The cityID can be obtained by making use of the following code:

```
>>> reg = owm.city_id_registry()
>>> reg.ids_for(PLACENAME)
```

Finally, the API can also be used to get a location object:

```
>>> reg = owm.city_id_registry()
>>> location = reg.locations_for(PLACENAME)
```

In turn this location object can be used to get an city ID:

```
>>> city_id = location.get_ID()
```

These were the functions we made use of when developing our weatherbot. While more information can be found at the openweathermap website, we got most of the above mentioned information from the following github: [csparpa](https://github.com/csparpa/pyowm/blob/master/pyowm/docs/usage-examples.md).

## Creating The Bot

This section provides in-depth information on our weatherbot code. Here we explain the different classes that the bot is made up of and what packages were included to ensure that the bot functions correctly. At the end of this section you will find information on the normal workflow of the code when the bot is being used. The next section includes a demo of our bot.

### General Approach

The bot should at least be able to answer weather related questions. As we were able to use the openweathermap API, we decided not to use any dataset. Mainly, because we could use the NLTK package with python to recognize placenames in a sentence and then we could use this information in combination with the API to get weather information. The bot did not need any large dataset to learn itself the different placenames. We could have used a dataset to learn it to respond to user messages. Instead we made use of predefined queries that were stored in a database. This makes the responses by the bot less natural. But decided to first focus on getting the bot running and then to add more functionality. Sadly, we did not have enough time to add more sophisticated functionalities like text generation. 

Neither did we use any model for our bot. The bot is very basic in that it responds to every new message send by the user. It then searches for certain keywords and reacts on them. We made sure to implement certain functions in order to make it possible to create a sort of memory for the bot. Unfortunately, we ended up not using these functions, which means that the bot only responds to the last message. It does however, remember previous mentioned locations.

### Different Classes

The most important classes that make up the bot are:
* main
* weatherBot

The main class is used to run the bot and the weatherBot class is used in the main class to make a weatherbot object. From this object the different functionalities that are included can be called.

Next to these classes we have several other that can be grouped under different libraries. The different librariers are:
* config
* database
* handlers

The config library contains a config script that is used to store the telegram API key and the openweathermap API key. We made sure to store these keys in seperate .txt files which were note pushed to our git. With the config script we read these keys into the main code in order to create a connection with the different API's.

The database library contains two scripts dedicated to setting up databases that are used by the bot. These scripts are:
* dbhelper.py
* userDB.py

The dbhelper script is used to setupt the basic query database. This database is used by the bot to collect basic responses to the input of an user. Because we had little experience with SQL, we wrote the script in such a way that we can write the basic responses in the .txt file named queries. The database script then reads in this .txt file with the different queries. The output database by this script is a table with 3 columns. The first column relates to the sentiment related to the response, the second column relates to the specific reponse tag and the final column is the response itself. Each row is then a specific response.

The userDB script is used to store the different input responses the bot receives by different users. The database created by this script is a table with 5 columns. The first column holds the chatid which is linked to an user. The second column holds the messageid which is different for every message an user sends. Then the third column is used to store the message itself. The fourth column will hold the location that was included in the message, or nothing if no location was included. Finally, the fifth column will hold the time that the message was received.

Then moving on to the final library, the handlers. The handlers library contains different sort of handler classes. Like the names states, these classes are used to handle certain situations. The different handlers are:
* inputHandler.py
* textHandler.py
* weatherHandler.py

The inputHandler.py class is used to handle new updates (messages send by user). It will check if the message is a text or a location and deal with each type of message accordingly. This class will also prepare the messages that the bot will send to the user.

The textHandler.py class is used to analyze the text send by an user. At first we created this class to be able to recognize a placename in a sentence. But eventually we also decided to use this class to let the bot recognize different forms of greetings or farewells. This is done by making use of regular expressions. The user could also ask how the bot is doing or what mood it has and this can also be recognized by a regular expression.

Then moving on to the final class of the Handlers library, the weatherHandler. As we wanted to create a weatherbot, we also need to make sure that the bot can collect weather information if a placename or location is provided by an user. This class will store previous named locations and related weather information in a dictionary. Moreover, this class is also used to collect weather information on Nijmegen. This information is then used to update the mood of the bot. If the weather is bad, the bot will be sad. If the weather is nice, the bot will be happy. Otherwise, the bot's mood is neutral. These moods are used to generate different forms of responses by the bot.

### Simple Workflow

The flowchart below gives a general idea of how our code works. To run the bot one should run the main class. This class creates a weatherbot object. The weatherbot in turn initializes the different databases and the config file is called in order to get the necessary keys. Then while the entire system runs, the inputhandler is used to deal with new messages and returns appropriate responses to the weatherbot that will send them via telegram to the user.

![alt text](https://github.com/Tomjg14/Tomjg14.github.io/blob/master/Untitled%20Diagram.jpg "workflow")

## What The Bot Does

The bot can do the following:
* greet the user
* say farewell to the user
* provide instructions
* provide (specific) weather information when a location is provided
* provide  (specific) weather information when a placename is given
* react when the user asks about its mood
* change its mood depending on the weather in Nijmegen

The bot can react to different types of greetings and farewells. It is also able to respond when asked about its mood. If a location is provided or if a placename is entered, the bot will be able to provide the user with specific weather information. This could be: only the temperature, only the status or both. The user will need to specify which information is needed. The bot also changes its mood depending on the weather status in Nijmegen. This is done every new hour. When the bot is sad (because it is rainy), it will react more moody. But if the sky is clear, the bot will be happy and change its responses. 

Finally, it is important to note that the bot will only recognize messages written in English. If the bot does not understand the message, it will state this and tell the user to type 'help' if the user needs instructions.

## How To Use The Bot

This bot can mainly be used to aqcuire information on the weather of a specified location. The user could greet the bot and say farewell. But this is not necessary and the user could immediately provide the bot with a location for which the weather information is needed. As the bot will change its mood depending on the weather in Nijmegen, one could also ask the bot about its mood to get the weather status from Nijmegen. 

Example input:
* Different types of English greetings: hi, hello, how are you
* Different types of English farewells: bye, see ya, good night
* location
* placename: either in a full sentence or just the name
* help: to get instructions
* 'How are you' or 'What is your current mood?': to get the mood of the bot
* something unclear: the bot will not understand it, but ask if instructions are needed

## Demo

This section contains a short demo for the different functionalities our bot can handle.

### basic chit-chat

![greeting](https://github.com/Tomjg14/Tomjg14.github.io/blob/master/images/hello.JPG "greetings")

![farewell](https://github.com/Tomjg14/Tomjg14.github.io/blob/master/images/bye.JPG "farewells")

![unclear](https://github.com/Tomjg14/Tomjg14.github.io/blob/master/images/unclear.JPG "unclear")

![help](https://github.com/Tomjg14/Tomjg14.github.io/blob/master/images/help.JPG "help")

![mood](https://github.com/Tomjg14/Tomjg14.github.io/blob/master/images/mood.JPG "mood")

### domain specific questions

![location](https://github.com/Tomjg14/Tomjg14.github.io/blob/master/images/location.JPG "location")

![placename singular](https://github.com/Tomjg14/Tomjg14.github.io/blob/master/images/placename_singular.JPG "placename")

![placename in sentence](https://github.com/Tomjg14/Tomjg14.github.io/blob/master/images/placename_sentence.JPG "placename2")


## Future Improvements

At the moment the bot has very little sophisticated functionality. It does parse the sentence with natural language processing, but only to search for any placenames/locations in the sentence. --> Vermeld misschien nog andere slimme dingen die de bot wel doet. Maakt niet uit hoe klein. Zoals de regular expressions waardoor hij meerdere input kan begrijpen!
* improve1
* improve2
