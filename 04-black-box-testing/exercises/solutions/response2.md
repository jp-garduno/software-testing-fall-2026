## Scenario 4: URL Validator

1. **Identify all partitions** for each component

- **Protocol**: 3
- **Domain**: 2
- **TLD**: 3
- **Path**: 2
- **Query params**: 2
- **Fragment**: 2

2. **Create partition table**
Protocol
|PartitionID|Description|Type|Example Values|
|---|---|---|---|
|P1|Starts with http://|Valid|http://google.com|  
|P2|Starts with https://|Valid|http://kahoot.com|  
|P3|Dosen't start with http or https//|Valid|lol://yahoo.com|  

Domain

| PartitionID | Description | Type | Example Values |
|---|---|---|---|
| P1 | Contains letters, numbers, hyphens or dots | Valid | http://clo9d_p4ge.com |  
| P2 | Contains a character that isn't a letters, numbers, hyphens or dots | Valid | http://kahoot^?&.com |  

TLD

|PartitionID|Description|Type|Example Values|
|---|---|---|---|
|P1|TLD has less than two characters|Valid|http//:invalid.go  
|P2|Starts with https://|Valid|http://kahoot.com|  
|P3|Dosen't start with http or https//|Valid|lol://yahoo.com| 


