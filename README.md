# FROM INSTITUTE
python version 3.8
___

## Calculator
simple realisation of calculator
```py
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
```
> ![Image](https://github.com/zuzuka28/mtuci_prog/raw/main/doc/calc.png)

## Translator with azure
Using the Text-to-speech API
Creating a route using flask, JavaScript  allows users to interact with the Flask application
> ![Image](https://github.com/zuzuka28/mtuci_prog/raw/main/doc/withazure.png)


## Registration form
Registration and login form with saving to the database. 
```py
from flask import Flask, render_template, url_for, jsonify, request, redirect
import psycopg2
```
> ![Image](https://github.com/zuzuka28/mtuci_prog/raw/main/doc/regform0.png)
> ![Image](https://github.com/zuzuka28/mtuci_prog/raw/main/doc/regform1.png)

## Simple telegram bot
Work with pyTelegramBotAPI

commands:
* /news -- send news of mtuci
* /cat -- send cat pic
* /yapic [request] -- send a pic on request
```py
import telebot
from bs4 import BeautifulSoup
```

## Timetable tg bot
Telegram bot that send schedule of the institute 's activities
For each day or for the whole week
```py
import telebot
import psycopg2
```
> ![Image](https://github.com/zuzuka28/mtuci_prog/raw/main/doc/tgbottimetable.png)
> ![Image](https://github.com/zuzuka28/mtuci_prog/raw/main/doc/tgbottimetable1.png)

## Timetable ui
UI for database which allows to change, delete or insert fields
```py
import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox,
                             QAbstractButton, QButtonGroup)
```
> ![Image](https://github.com/zuzuka28/mtuci_prog/raw/main/doc/timetableui.png)

