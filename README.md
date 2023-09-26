# NHL Game Data Analysis Twitter Bot

![NHL Logo](https://www.example.com/nhl_logo.png)

## Overview

This Python bot is designed to analyze NHL game data, sourced from the undocumented NHL API, and generate analytical plots using Pandas and Matplotlib. The bot then automatically exports and posts these visualizations on Twitter using the Twitter API. This README provides an overview of the bot's functionality, usage instructions, and prerequisites.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [License](#license)

## Features

- Fetches NHL game data from the undocumented NHL API.
- Analyzes and processes the data using Pandas.
- Generates various analytical plots using Matplotlib.
- Automatically posts the plots on Twitter using the Twitter API.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/TWright-28/NHL_TwitterBot.git
   ```

2. Change to the project directory:

   ```shell
   cd NHL_TwitterBot
   ```

3. Install the required Python dependencies:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

1. Set up your Twitter Developer account and obtain API keys and access tokens.

2. Configure the bot with your Twitter API credentials (see [Configuration](#configuration)).

3. Run the bot:

   ```shell
   python main.py
   ```

   The bot will fetch NHL game data, process it, create analytical plots, and post them on your Twitter account.

## Configuration

Before running the bot, you need to configure it by providing your Twitter API credentials. Create a `keys.py` file in the project directory and add the following information:

```ini
[Twitter]
consumer_key = your_consumer_key
consumer_secret = your_consumer_secret
access_token = your_access_token
access_token_secret = your_access_token_secret
bearer_token  = your_bearer_token
```

Replace `your_consumer_key`, `your_consumer_secret`, `your_access_token`, and `your_access_token_secret` with your actual Twitter API credentials.

## Dependencies

The bot relies on the following Python libraries:

- Pandas
- Matplotlib
- Requests
- Numpy
- Tweepy (for Twitter integration)

You can install these dependencies using the `requirements.txt` file, as mentioned in the [Installation](#installation) section.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Happy NHL data analysis and Twitter posting!.
