# Flask-SocketIO Chat

A simple real-time chat app using Flask and Socket.IO.

## Features

*   User registration and login.
*   Real-time chat.
*   Room creation via URL params.

## Endpoints

*   `/reg`: Register.
*   `/login`: Log in.
*   `/`: Chat.

## Setup

1.  `git clone [repo-url]`
2.  `python3 -m venv venv && source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
3.  `pip install -r requirements.txt`
4.  `flask --app app.py run`

## Usage

*   Register/login at `/reg` and `/login`.
*   Access the chat at `/`.
*   Create rooms via URL, e.g., `/?room=myroom&username=user`.

## Contributing

Fork, branch, commit, and submit a pull request.