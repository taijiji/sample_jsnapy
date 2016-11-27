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


## Sample 2 : Run JSNAPy by Python script
Before run this script, you need edit '/etc/jsnapy/logging.yml'.

```yaml:/etc/jsnapy/logging.yml
 61 root:
 62     level: DEBUG
 63     #handlers: [console, debug_file_handler]
 64     handlers: [debug_file_handler]
```

Run JSNAPy via python script

```
python run_jsnapy_test_hostname_model.py
```

output

```
% python run_jsnapy_test_hostname_model.py
                                                                                                                                               (git)-[master]
##### JSNAPy Test : Start #####
Devece :  192.168.34.16
Final result :  Passed
Total passed :  2
Total failed :  0
snapcheck test_details :
------------------------------
{'show version': [{'count': {'fail': 0, 'pass': 1},
                   'expected_node_value': 'firefly1',
                   'failed': [],
                   'node_name': 'host-name',
                   'passed': [{'actual_node_value': 'firefly1',
                               'id': {},
                               'post': {'host-name': 'firefly1'},
                               'pre': {'host-name': 'firefly1'}}],
                   'result': True,
                   'testoperation': 'is-equal',
                   'xpath': '/software-information'},
                  {'count': {'fail': 0, 'pass': 1},
                   'expected_node_value': 'firefly-perimeter',
                   'failed': [],
                   'node_name': 'product-model',
                   'passed': [{'actual_node_value': 'firefly-perimeter',
                               'id': {},
                               'post': {'product-model': 'firefly-perimeter'},
                               'pre': {'product-model': 'firefly-perimeter'}}],
                   'result': True,
                   'testoperation': 'is-equal',
                   'xpath': '/software-information'}]}
------------------------------
##### JSNAPy Test : End #####
```
