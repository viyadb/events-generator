events-generator
=================

Framework for simulating mobile application user activity, and generating events from this activity.
The project covers the following phases:

 * Engagement with a mobile app advertisement (clicking or viewing)
 * Installing mobile application (as a result of the engagement or organically)
 * Opening application (generating a session)
 * Generating custom event in application
 * Uninstalling the application

Generated events can be used for testing purposes, when a big volume of real (or close to real)
data is required.

## Flow

The framework tries to emulate real-world humans interacting with mobile applications, while
taking predefined parameters into consideration.

### Participants

 * Ad network (through which an advertisement was published)
 * Ad campaign
 * Mobile application
 * Mobile user

Relations between them are the following:


    +--------------+            +---------------+
    |              |    N:N     |               |
    |  Ad Network  +------------+  Ad Campaign  |
    |              |            |               |
    +--------------+            +-------+-------+
                                        |
                                        |  N:1
                                        v
               +--------+           +---+---+
               |        |   N:N     |       |
               |  User  +-----------+  App  |
               |        |           |       |
               +--------+           +-------+


### Parameters

There are multiple coefficients taken into account when generating events:

 * Click to install rate (conversion rate) per application, ad network
 * App popularity
 * User activity and retention rate per app

### Output Fields

| Field Name | Description |
|------------|-------------|
| app\_id | Mobile application ID |
| user\_id | 32-bit integer user ID (unique on a single app level) |
| event\_time | Event time in milliseconds from epoch |
| country | Two letter country code |
| city | City name |
| device\_type | Mobile device type (iOS, Android, etc.) |
| device\_vendor | Mobile device vendor (HP, Asus, etc.) |
| ad\_network | Ad network, which has led to the app install |
| campaign | Ad campaign, which has led to the app install |
| site\_id | Website that shown the original ad about the app |
| event\_type | Event type (install, click, inapp, etc.) |
| event\_name | In-app event name |
| organic | Whether the install was organic or not (False or True) |
| days\_from\_install | Number of days passed since install till event\_time |
| revenue | Optional In-app event revenue |

## Running

### Using Docker image

There's Docker image that has all the needed environment, and runs the script for you.
To have it produce JSON events to standard output, run:

```bash
docker run --log-driver=none --rm -ti viyadb/events-generator:latest
```

For example, to have your Kafka populated with generated events run:

```bash
docker run --log-driver=none --rm -ti viyadb/events-generator:latest | kafka-console-producer.sh --broker-list <kafka-broker>:9092 --topic <topic name>
```

#### Configuration

To configure events generator behavior when running in Docker use the following environment variables:

| Environment Variable | Description  | Default value |
| -------------------- | ------------ | ------------- |
| CLICK\_THROUGH\_RATE | Click-through rate | 0.005 |
| CAMPAIGNS\_NUM | Number of running campaigns at any time | 10000 |
| START\_DATE | Events start date in format YYYY-MM-DD | 2015-01-01 |
| OUTPUT\_FORMAT | Events output format. Supported formats: json, tsv | json |
| OUTPUT\_HEADER | Whether to print TSV header | False |

For example, to have events generator produce content in TSV format use:

```bash
docker run --log-driver=none --rm -ti -e OUTPUT\_FORMAT=tsv viyadb/events-generator:latest
```

### Without Docker

#### Prerequisites

Please make sure you have the following dependencies installed on your computer.

 * Python 2.7
 * [SimPy](http://simpy.readthedocs.io/en/latest/) >= 3.0.10
 * [NumPy](http://www.numpy.org/) >= 1.12.1
 * [SciPy](https://scipy.org/) >= 0.19.1

#### Configuration

To list all available options, please run:

```bash
./generate.py --help
```

#### Generating events

```bash
./generate.py
```

