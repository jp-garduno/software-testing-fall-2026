## Scenario 4: URL Validator

1. **Identify all partitions** for each component

- **Protocol**: 3
- **Domain**: 2
- **TLD**: 3
- **Path**: 2
- **Query params**: 2
- **Fragment**: 2

2. **Create partition table**

#### Protocol

|PartitionID|Description|Type|Example Values|
|---|---|---|---|
|P1|Starts with http://|Valid|http://google.com|  
|P2|Starts with https://|Valid|http://kahoot.com|  
|P3|Dosen't start with http or https//|Valid|lol://yahoo.com|  

#### Domain

| PartitionID | Description | Type | Example Values |
|---|---|---|---|
| P1 | Contains letters, numbers, hyphens or dots | Valid | http://clo9d_p4ge.com |  
| P2 | Contains a character that isn't a letters, numbers, hyphens or dots | Valid | http://kahoot^?&.com |  

#### TLD

|PartitionID|Description|Type|Example Values|
|---|---|---|---|
|P1|TLD has less than two characters|Invalid|http://invalid.g  
|P2|TLD Has more than 6 characters|Invalid|http://kahoot.criminalrizz|  
|P3|TLD Has 2 to 6 characters|Valid|http://yahoo.com| 

#### Path

|PartitionID|Description|Type|Example Values|
|---|---|---|---|
|P1|Url includes a path|Valid|http://amazon.net/ec2/create  
|P2|Url has no path|Valid|http://netflix.com  

#### Query params

|PartitionID|Description|Type|Example Values|
|---|---|---|---|
|P1|Url includes a query param|Valid|http://amazon.net/s3?memory=5:ttl=true
|P2|Url has no query params|Valid|http://netflix.com  


#### Fragment

|PartitionID|Description|Type|Example Values|
|---|---|---|---|
|P1|Url includes a fragment|Valid|http://amazon.net#neverskiplegday
|P2|Url has no fragments|Valid|http://netflix.com  

3. **Identify test cases**

#### T01

###### Test Name
InUsesHttp

###### Description
The url incorrectly starts with a header different from http:// or http://

###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type htp://crunchyroll.net/watch
2) Expect an error

#### T02

###### Test Name
InShortDomain

###### Description
The url has a domain that contains letters, numbers, hyphens or dots

###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type http://clo9d_p4ge.com
2) Get no error

#### T03

###### Test Name
InLongDomain

###### Description
The url has a domain that contains a character that isn't a letters, numbers, hyphens or dots
###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type http://kahoot^?&.com 
2) Expect an error
