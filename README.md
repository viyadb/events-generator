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

## Running

### Using Docker image

This is the simplest way for running the script.
There's Docker image that has all the needed environment, and runs the script for you.
To have it produce JSON events to standard output, run:

```bash
docker run --log-driver=none --rm -ti viyadb/events-generator:latest
```

For example, to have your Kafka populated with generated events run:

```bash
docker run --log-driver=none --rm -ti viyadb/events-generator:latest | kafka-console-producer.sh --broker-list <kafka-broker>:9092 --topic <topic name>
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

