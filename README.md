#JSNAPy Sample code

Sample code for using Juniper JSNAPy(https://github.com/Juniper/jsnapy).

## Sample 1 : Run JSNAPy by Command Line Tool
sample for testing hostname and product-model.

run sample by JSNAPy command line tool

```
jsnapy --snapcheck snap01 -f config_firefly1.yml
```

```:config_firefly1.yml
hosts:
  - device: 192.168.34.16 
    username : user1
    passwd: password1
    port: 22
tests:
  - ./tests/test_hostname.yml
  - ./tests/test_model.yml
```

```:./tests/test_hostname.yml
test_hostname:
  - command: show version
  - item:
      xpath: '/software-information'
      tests:
        - is-equal: host-name, firefly1
          info: "Test : OK, host-name is <{{pre['host-name']}}>"
          err:  "Test : NG, host-name is <{{pre['host-name']}}>"
```

```:./tests/test_model.yml
test_hostname:
  - command: show version
  - item:
      xpath: '/software-information'
      tests:
        - is-equal: product-model, firefly-perimeter
          info: "Test : OK, Model is <{{pre['product-model']}}>"
          err:  "Test : NG, Model is <{{pre['product-model']}}>"
```
```

output
( -v is option to display debug level messages)

```
% jsnapy --snapcheck snap01 -f config_firefly1.yml -v 
                                                                                                                                   (git)-[master]
Connecting to device 192.168.34.16 ................
Tests Included: test_hostname
Taking snapshot of COMMAND: show version
Tests Included: test_model
Taking snapshot of COMMAND: show version
*************************** Device: 192.168.34.16 ***************************
Tests Included: test_hostname
*************************** Command: show version ***************************
----------------------Performing is-equal Test Operation----------------------
Test : OK, host-name is <firefly1>
PASS | All "host-name" is equal to "firefly1" [ 1 matched ]
*************************** Device: 192.168.34.16 ***************************
Tests Included: test_hostname
*************************** Command: show version ***************************
----------------------Performing is-equal Test Operation----------------------
Test : OK, Model is <firefly-perimeter>
PASS | All "product-model" is equal to "firefly-perimeter" [ 1 matched ]
------------------------------- Final Result!! -------------------------------
Total No of tests passed: 2
Total No of tests failed: 0
Overall Tests passed!!!
```


## Run JSNAPy by Python script
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
