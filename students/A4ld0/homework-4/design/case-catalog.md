# Executable case catalog

These are human-authored expected outcomes, shared by pytest and Jest.
See `cases.json` for exact arguments, results, and public-state checkpoints.

| ID | Technique | Scenario |
| --- | --- | --- |
| EP01 | EP | valid transfer amount |
| EP02 | EP | invalid transfer representative 0 |
| EP03 | EP | invalid transfer representative -100 |
| EP04 | EP | invalid transfer representative 5001 |
| EP05 | EP | invalid transfer representative 501 |
| EP06 | EP | invalid transfer representative '10' |
| EP07 | EP | invalid transfer representative True |
| EP08 | EP | invalid transfer representative 0.001 |
| EP09 | EP | supported type Savings |
| EP10 | EP | supported type Checking |
| EP11 | EP | supported type Premium |
| EP12 | EP | unsupported account type Business |
| EP13 | EP | unsupported account type None |
| EP14 | EP | opening below minimum |
| EP15 | EP | opening above minimum |
| EP16 | EP | invalid opening balance -1 |
| EP17 | EP | invalid opening balance '100' |
| EP18 | EP | invalid opening balance 0.001 |
| EP19 | EP | registered payee |
| EP20 | EP | invalid payee 'stranger' |
| EP21 | EP | invalid payee '' |
| EP22 | EP | invalid payee None |
| EP23 | EP | history range contains activity |
| EP24 | EP | history range without activity |
| EP25 | EP | reversed history dates |
| EP26 | EP | invalid history start '09/22/2026' |
| EP27 | EP | invalid history start '2026-02-30' |
| EP28 | EP | invalid history start None |
| EP29 | EP | invalid destination '' |
| EP30 | EP | invalid destination '   ' |
| EP31 | EP | invalid destination None |
| EP32 | EP | invalid destination 12 |
| EP33 | EP | named own-account destination |
| EP34 | EP | valid owner update trims whitespace |
| EP35 | EP | invalid owner '' |
| EP36 | EP | invalid owner '  ' |
| EP37 | EP | invalid owner 100 |
| EP38 | EP | invalid owner None |
| EP39 | EP | invalid bill amount 0 |
| EP40 | EP | invalid bill amount -1 |
| EP41 | EP | invalid bill amount '5' |
| EP42 | EP | invalid bill amount 0.001 |
| EP43 | EP | invalid deposit 0 |
| EP44 | EP | invalid deposit -1 |
| EP45 | EP | invalid deposit '5' |
| EP46 | EP | invalid deposit 0.001 |
| EP47 | EP | nonfinite transfer NaN |
| EP48 | EP | nonfinite opening NaN |
| EP49 | EP | nonfinite transfer Infinity |
| EP50 | EP | nonfinite opening Infinity |
| EP51 | EP | nonfinite transfer -Infinity |
| EP52 | EP | nonfinite opening -Infinity |
| EP53 | EP | amount exceeds arithmetic cap |
| EP54 | EP | deposit would exceed balance cap |
| EP55 | EP | invalid payment date |
| EP56 | EP | history returns independent records |
| EP57 | EP | CSV escapes comma and quotes |
| EP58 | EP | empty CSV retains header |
| EP59 | EP | CSV rejects reversed range |
| EP60 | EP | invalid date edge '2026-09-22\n' |
| EP61 | EP | invalid date edge '0000-01-01' |
| EP62 | EP | invalid date edge '2026-02-29' |
| EP63 | EP | invalid date edge '2026-09-31' |
| EP64 | EP | history validates end date too |
| EP65 | EP | boolean opening balance rejected |
| EP66 | EP | account type object rejected |
| BV01 | BV | Checking transfer boundary 0 |
| BV02 | BV | Checking transfer boundary 0.01 |
| BV03 | BV | Checking transfer boundary 4999.99 |
| BV04 | BV | Checking transfer boundary 5000 |
| BV05 | BV | Checking transfer boundary 5000.01 |
| BV06 | BV | Checking transfer boundary 10000 |
| BV07 | BV | Savings transfer boundary 0 |
| BV08 | BV | Savings transfer boundary 0.01 |
| BV09 | BV | Savings transfer boundary 1999.99 |
| BV10 | BV | Savings transfer boundary 2000 |
| BV11 | BV | Savings transfer boundary 2000.01 |
| BV12 | BV | Savings transfer boundary 4000 |
| BV13 | BV | Savings minimum 0 |
| BV14 | BV | Savings minimum 99.98 |
| BV15 | BV | Savings minimum 99.99 |
| BV16 | BV | Savings minimum 100 |
| BV17 | BV | Savings minimum 100.01 |
| BV18 | BV | Savings minimum 200 |
| BV19 | BV | Savings fee threshold 999.98 |
| BV20 | BV | Savings fee threshold 999.99 |
| BV21 | BV | Savings fee threshold 1000 |
| BV22 | BV | Savings fee threshold 1000.01 |
| BV23 | BV | Savings fee threshold 1000.02 |
| BV24 | BV | Savings fee threshold 2000 |
| BV25 | BV | Checking fee threshold 4999.98 |
| BV26 | BV | Checking fee threshold 4999.99 |
| BV27 | BV | Checking fee threshold 5000 |
| BV28 | BV | Checking fee threshold 5000.01 |
| BV29 | BV | Checking fee threshold 5000.02 |
| BV30 | BV | Checking fee threshold 10000 |
| BV31 | BV | cumulative remaining allowance 0 |
| BV32 | BV | cumulative remaining allowance 0.01 |
| BV33 | BV | cumulative remaining allowance 99.99 |
| BV34 | BV | cumulative remaining allowance 100 |
| BV35 | BV | cumulative remaining allowance 100.01 |
| BV36 | BV | cumulative remaining allowance 200 |
| BV37 | BV | available funds 0 |
| BV38 | BV | available funds 0.01 |
| BV39 | BV | available funds 99.99 |
| BV40 | BV | available funds 100 |
| BV41 | BV | available funds 100.01 |
| BV42 | BV | available funds 101 |
| BV43 | BV | Premium minimum 0 |
| BV44 | BV | Premium minimum 9999.98 |
| BV45 | BV | Premium minimum 9999.99 |
| BV46 | BV | Premium minimum 10000 |
| BV47 | BV | Premium minimum 10000.01 |
| BV48 | BV | Premium minimum 20000 |
| BV49 | BV | UTC midnight resets cumulative limit |
| BV50 | BV | history includes both endpoints only |
| BV51 | BV | payment yesterday rejected |
| BV52 | BV | payment today debits immediately |
| BV53 | BV | payment tomorrow executes once when due |
| BV54 | BV | valid leap-day history interval |
| BV55 | BV | fee only on first and once per month |
| BV56 | BV | cent arithmetic does not accumulate binary drift |
| BV57 | BV | exact maximum balance deposit allowed |
| BV58 | BV | Premium daily limit inclusive |
| DT01 | DT | transfer active=True funds=True within-limit=True |
| DT02 | DT | transfer active=True funds=True within-limit=False |
| DT03 | DT | transfer active=True funds=False within-limit=True |
| DT04 | DT | transfer active=True funds=False within-limit=False |
| DT05 | DT | transfer active=False funds=True within-limit=True |
| DT06 | DT | transfer active=False funds=True within-limit=False |
| DT07 | DT | transfer active=False funds=False within-limit=True |
| DT08 | DT | transfer active=False funds=False within-limit=False |
| DT09 | DT | monthly fee Savings balance=1000.01 |
| DT10 | DT | monthly fee Savings balance=1000 |
| DT11 | DT | monthly fee Savings balance=100 |
| DT12 | DT | monthly fee Savings balance=5 |
| DT13 | DT | monthly fee Savings balance=4.99 |
| DT14 | DT | monthly fee Checking balance=5000.01 |
| DT15 | DT | monthly fee Checking balance=5000 |
| DT16 | DT | monthly fee Checking balance=10 |
| DT17 | DT | monthly fee Checking balance=9.99 |
| DT18 | DT | monthly fee Premium balance=10000 |
| DT19 | DT | monthly fee Premium balance=9999 |
| DT20 | DT | bill active=True payee=True funds=True |
| DT21 | DT | bill active=True payee=True funds=False |
| DT22 | DT | bill active=True payee=False funds=True |
| DT23 | DT | bill active=True payee=False funds=False |
| DT24 | DT | bill active=False payee=True funds=True |
| DT25 | DT | bill active=False payee=True funds=False |
| DT26 | DT | bill active=False payee=False funds=True |
| DT27 | DT | bill active=False payee=False funds=False |
| DT28 | DT | failed fee attempt is consumed for the month |
| DT29 | DT | waiver checked at fee time and processed once |
| DT30 | DT | scheduled payment rechecks funds and fails once |
| DT31 | DT | scheduled payment rechecks Frozen state |
| DT32 | DT | scheduled payments run in insertion order |
| DT33 | DT | invalid scheduling does not enqueue payment |
| ST01 | ST | transfer below minimum suspends |
| ST02 | ST | exact deposit restoration reactivates |
| ST03 | ST | partial restoration remains suspended |
| ST04 | ST | Frozen rejects monetary operations and repeated freeze |
| ST05 | ST | unfreeze restores transfers |
| ST06 | ST | Closed is terminal and viewable |
| ST07 | ST | Suspended may close |
| ST08 | ST | Frozen may close |
| ST09 | ST | Suspended rejects outgoing transactions and invalid transitions |
| ST10 | ST | Active cannot unfreeze |
| ST11 | ST | unaffordable fee suspends without overdraft |
| ST12 | ST | fee suspension followed by deposit recovery |
| ST13 | ST | bill debit can suspend Savings |
| ST14 | ST | Suspended owner update is allowed |
| ST15 | ST | Closed rejects scheduled queue processing |
