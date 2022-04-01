# Smart Neighborhood

IoT university project developed for the MSc course of Internet of Things and 3D Intelligent Systems.

The application is used to automatically open or close the shutter of a house depending on weather conditions.
The system is scalable in order to be used in a neighborhood, aiming to control the shutters of several houses simultaneously.
The users are notified by a Telegram bot when a decision is taken by the system. Moreover, the inhabitants can control the shutters manually thanks to specific buttons and/or a web application..
The decision is based on the following parameters:
- Light -> the value is read from a photoresistor
- Wind -> the wind speed is simulated using a potentiometer
- Weather conditions -> taken from OpenWeather API
- Temperature -> taken from OpenWeather API

A prototype is built using Arduino and simulating the shutters with servomotors.
