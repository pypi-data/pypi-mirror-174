# Burner

![PyPI](https://img.shields.io/pypi/v/burner) ![PyPI - License](https://img.shields.io/pypi/l/burner) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/burner)

Easy to use script to determine the cheapest price for [SimSMS](https://simsms.org/) codes.

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
burner services
```

Then use the following command to find the price list for the service.

```bash
burner prices opt29 # This will get the price list for Telegram.
```

If you want to refresh the cache for the prices to a newer version, run the following command.

```bash
burner --authorization <apikey> reset
```

If you'd like to buy a phone number, use the following format. An API key with available funds is necessary for this command.

```bash
burner -a <apikey> number <countrycode> <servicecode>
```

For example, you could type the following to get a Russian [Signal](https://signal.org/) code.

```bash
burner -a <apikey> number RU opt127
```

You can also set your API key with the `SMS_AUTHORIZATION` environment variable.

For more information simply type `burner --help`.
