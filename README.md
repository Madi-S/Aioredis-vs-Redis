# Script to compare the speed of **_Aioredis_** and **_Redis_** packages for python in real-life conditions

---

## To setup program on your machine:

1. Download files to your local machine
2. Download necessary packages: `pip install -r requirements.txt`

---

## To run file:

- For help: `python main.py -h`
- Structure: `python main.py -r <number of requests> <type> <number of tests>`
- Example: `python main.py -r 500 zs 8` - program will test only sorted set commands 8 times with 500 requests

---

## Ready data:

If you do not want to compare the packages manually, here is preliminary ready data for 50 requests:

| Indicator, time/sec | Aioredis (asynchronous) | Redis (synchronous) |
| ------------------- | :---------------------: | ------------------: |
| Number of tests     |            5            |                   5 |
| Overall time        |        38.98096         |            97.52228 |
| Average time        |         7.79619         |            19.50446 |
| Minimum time        |         7.48271         |            19.36946 |
| Maximum time        |         7.96106         |            19.65107 |
| First quartile      |         7.83469         |            19.39387 |
| Second quartile     |         7.83868         |            19.51609 |
| Third quartile      |         7.86382         |            19.59179 |
| Interquartile range |         0.02913         |             0.19792 |
| Low limit           |          7.791          |            19.09699 |
| Up limit            |         7.90751         |            19.88867 |

- [ ] Add verbosity
