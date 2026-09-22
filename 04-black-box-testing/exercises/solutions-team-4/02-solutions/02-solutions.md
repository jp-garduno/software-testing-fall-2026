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
|P2|Url has 0 length path|Valid|https://netflix.com//  

#### Query params

|PartitionID|Description|Type|Example Values|
|---|---|---|---|
|P1|Url includes a query param|Valid|https://amazon.net/s3?memory=5:ttl=true
|P2|Url has empty query param|Valid|https://netflix.com/watch? 


#### Fragment

|PartitionID|Description|Type|Example Values|
|---|---|---|---|
|P1|Url includes a fragment|Valid|http://amazon.net#neverskiplegday
|P2|Url has empty fragemnt|Valid|https://amazon.com/cart#  

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

1) Type "htp://crunchyroll.net/watch"
2) Get "Invalid" as result

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

1) Type "http://google.com"
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

1) Type "https://kahoot.com"
2) Get "Valid" as result

#### T04

###### Test Name
VDomain1

###### Description
The url has a domain that contains letters, numbers, hyphens or dots

###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type "http://clo9d_p4ge.com"
2) Get "Valid" as result

#### T05

###### Test Name
InDomain1

###### Description
The url has a domain that contains a character that isn't letters, numbers, hyphens or dots
###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type "http://kahoot^?&.com"
2) Get "Invalid" as result

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

1) Type "http://invalid.g"
2) Get "Invalid" as result

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

1) Type "https://youtube.go"
2) Get "Invalid" as result

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

1) Type "http://kahoot.criminalrizz"
2) Get "Invalid" as result

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

1) Type "https://slowApi.slowly"
2) Get "Invalid" as result

#### T10

###### Test Name
VBContainsPath

###### Description
The url contains a path

###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type "http://amazon.net/ec2/create"
2) Get "Valid" as result

#### T11

###### Test Name
InBContainsPath1

###### Description
The url contains an empty path

###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type "https://netflix.com//"
2) Get "Valid" as result

#### T12

###### Test Name
InContainsPath2

###### Description
The url contains an empty path

###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type "https://mail.google.com/mail//0/#inbox"
2) Get "Invalid" as result

#### T013

###### Test Name
VDomain2

###### Description
The url has a domain that contains letters, numbers, hyphens or dots

###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type "https://various.example.com/substantial/pricey"
2) Get "Valid" as result

#### T14

###### Test Name
InDomain2

###### Description
The url has a domain that contains a character that isn't letters, numbers, hyphens or dots
###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type "https://slim.exam-ple.org/bottle"
2) Get "Invalid" as result

#### T15

###### Test Name
VContainsQuery

###### Description
The url contains a query

###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type "https://music.youtube.com/watch?v=_qur4p4qV7E&list=RDAMVM_qur4p4qV7E"
2) Get "Valid" as result

#### T16

###### Test Name
InContainsEmptyQuery

###### Description
The url contains an empty query

###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type "https://netflix.com/watch?"
2) Get "Valid" as result

#### T17

###### Test Name
VContainsFragment

###### Description
The url contains a fragment

###### Type
Valid

###### Prerequesites
None

###### Steps

1) Type "https://mail.google.com/mail/u/0/#trash"
2) Get "Valid" as result

#### T18

###### Test Name
InContainsEmptyFragment

###### Description
The url contains an empty fragment

###### Type
Invalid

###### Prerequesites
None

###### Steps

1) Type "https://pomofocus.io/start#"
2) Get "Invalid" as result

