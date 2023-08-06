# Burner

Easy to use script to determine the cheapest price for [SimSMS](https://simsms.org/).

## Installation

### With Pip

```bash
pip install burner
```

### With Poetry

```bash
poetry add git+https://github.com/ramadan8/Burner.git
```

### Manual

```bash
git clone https://github.com/ramadan8/Burner --depth 1
poetry install
```

## Usage

Use the following command to find the code for the service you want.

```bash
poetry run burner --authorization <api_key> services
```

Then use the following command to find the price list for the service.

```bash
poetry run burner --authorization <api_key> prices opt29 # This will get the price list for Telegram.
```

You can omit the `--authorization` argument once you have populated the database once.
