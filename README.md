#JSNAPy Sample code

It's sample code to use Juniper JSNAPy(https://github.com/Juniper/jsnapy).

## Run JSNAPy by Command Line Tool
run JSNAPy

```
jsnapy --snapcheck snap01 -f config_router1.yml
```

output

```
Connecting to device 192.168.34.16 ................
Taking snapshot of COMMAND: show version
*************************** Device: 192.168.34.16 ***************************
Tests Included: test_hostname
*************************** Command: show version ***************************
PASS | All "host-name" is equal to "firefly1" [ 1 matched ]
------------------------------- Final Result!! -------------------------------
Total No of tests passed: 1
Total No of tests failed: 0
Overall Tests passed!!!
```


## Run JSNAPy by Python module
run JSNAPy via python script(but include bug)

```
python run_jsnapy.py
```

output

```
test: 1
Connecting to device 192.168.34.16 ................
Taking snapshot of COMMAND: show version
*************************** Device: 192.168.34.16 ***************************
Tests Included: test_hostname
*************************** Command: show version ***************************
PASS | All "host-name" is equal to "firefly1" [ 1 matched ]
------------------------------- Final Result!! -------------------------------
Total No of tests passed: 1
Total No of tests failed: 0
Overall Tests passed!!!

(snip)
```
