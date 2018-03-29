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
* inputHandler
* textHandler
* timeHandler
* weatherHandler



### Important Packages

### Simple Workflow

## Demo
