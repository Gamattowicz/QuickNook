<div align="center">
<h1 align="center">QuickNook</h1></div>

## Table of contents

* [General info](#general-info)
* [Technologies](#technologies)
* [Setup & Installation](#setup-&-installation)
* [Running The App](#running-the-app)
* [Viewing The App](#viewing-the-app)
* [Viewing The API Documentation](#viewing-the-api-documentation)
* [Features](#features)
* [Status](#status)
* [Contact](#contact)

## General info

A modern fullstack eCommerce application, built in FastAPI and React (Next.js) with Typescript, provides advanced eCommerce functionality with an intuitive user interface thanks to the Shadnc UI library. Unit tests in Pytest are embedded into the design to ensure code stability, and an advanced logging system for monitoring application performance and debugging.

## Technologies

* Python 3.11.x
* FastAPI 0.104.1
* SQLite3
* Node.js v18.17.x
* TypeScript 5.4.x
* React 18.0.x
* Next.js 14.1.x
* TailwindCSS 3
* shadcn-ui 0.8.0
* HTML5
* CSS3

## Setup & Installation

**Backend configuration**

Make sure you have the latest version of Python and pip and installed

Clone the repository using the following command

```bash
git clone https://github.com/Gamattowicz/QuickNook
```

Move to the app directory

```bash
cd QuickNook
```

Create a virtual environment

```bash
python -m venv venv
```

Active the virtual environment

```bash
.\venv\Scripts\activate
```

Install all the project Requirements

```bash
pip install -r requirements.txt
```

**Frontend configuration**

[Install Node.js](https://nodejs.org/en/) and Node Modules:

Move to directory ```frontend```.

```bash
cd frontend
```

Next install all dependencies.

```bash
npm install
```

## Running The App

In main directory run uvicorn web server:

```bash
uvicorn api.main:app --reload
```

Move to directory ```frontend```.

```bash
cd frontend
```

Run the for development (the application is not currently designed for production):

```bash
npm run dev
```

## Viewing The App

Go to `http://localhost:3000/`

## Viewing The API Documentation

Go to `http://127.0.0.1:8000/docs`

## Status

The application is under development.

## Contact

Created by [@Gamattowicz](https://github.com/Gamattowicz) - feel free to contact me!
