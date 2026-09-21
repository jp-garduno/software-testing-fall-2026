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
|P2|Starts with https://|Valid|https://kahoot.com|  
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
InNoHttp

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
VHasHttp

###### Description
The url correctly starts with header http://

###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type http://google.com
2) Get "Valid" as result


#### T03

###### Test Name
VHasHttps

###### Description
The url correctly starts with header https://

###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type https://kahoot.com
2) Get "Valid" as result

#### T04

###### Test Name
VDomain

###### Description
The url has a domain that contains letters, numbers, hyphens or dots

###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type http://clo9d_p4ge.com
2) Get no error

#### T05

###### Test Name
InDomain

###### Description
The url has a domain that contains a character that isn't letters, numbers, hyphens or dots
###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type http://kahoot^?&.com 
2) Expect an error

#### T06

###### Test Name
InBVTLDLessThan2

###### Description
The TLD has less than two characters
###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type http://invalid.g 
2) Expect an error

#### T07

###### Test Name
InBVTLDExactly2

###### Description
The TLD has exactly 2 characters
###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type https://youtube.go
2) Expect an error

#### T08

###### Test Name
InBVTLDMoreThan6

###### Description
The TLD has more than six characters
###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type http://kahoot.criminalrizz
2) Expect an error

#### T09

###### Test Name
InBVTLDExactly6

###### Description
The TLD has six characters
###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type https://slowApi.slowly
2) Expect an error