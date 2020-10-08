# Competition rules

* https://slingshot.filecoin.io/rules
* https://slingshot.filecoin.io/faq/ 
* https://filecoinproject.slack.com/archives/C01AK1J7TF1/p1601175016033800 


* Store real, valuable, and usable data to the Filecoin network. You can store data from a curated list of data collections that the Slingshot admin team maintains and create an accompanying UI to utilize / access this data. https://github.com/filecoin-project/slingshot/blob/master/datasets.md
 
* Build an application or UI that uses that data in a meaningful way (whether reading that data directly from Filecoin or from a cache of that data stored elsewhere, like on IPFS).

* Once you have successfully made your first storage deal to the Filecoin network, the Filecoin address you used to make that storage deal will automatically show up on the leaderboard. However, your project will not yet be eligible for rewards. 

* Register to participate: There are two registration steps to complete:
    * Submit a registration form at https://slingshot.filecoin.io/register containing information about your team.
    * Submit a PR to the filecoin-project/slingshot GitHub repo, containing information about your project, application/UI URL, and more. 
    * The repo contains a template and submission instructions. 
    * You need to fork the repo, push your project description to it, and then create a PR to merge your fork.

* Pass community review: The team of Slingshot community reviewers will review your project details in the filecoin-project/slingshot GitHub repo to make sure you are eligible to participate in the competition. They will leave feedback for your team in your PR. If your application is accepted, the review team will merge the PR, update the leaderboard with your project information only (no personal information), and mark your project as "Reviewed" on the leaderboard. If your application is not immediately accepted, the review team will ask for more information, which you can provide by updating your PR.

* Once you've submitted your application for community review and it is approved, your address on the leaderboard will be updated with your project information.

* The community panel will give feedback on how to make sure your application is eligible for the reward pools asap. You don’t need to wait until your Slingshot project PR is merged to get started, provided you have filled in the registration form and submitted a project PR then you can begin working.

* To change any project information, submit an update to your application PR using the same github account.

* To change any project information on https://slingshot.filecoin.io/ you can email slingshot@filecoin.org.

* Follow competition rules: If you have completed the prior steps, and follow the competition rules throughout the competition, you will become eligible for rewards. These rules are automatically checked by the Slingshot leaderboard software or, in some cases, manually checked by the Slingshot community reviewers. If you are eligible for rewards, the leaderboard will mark your project as "Eligible". Please note that Eligible projects can become ineligible for rewards throughout the competition if they fail to follow the competition rules on an ongoing basis.

* Participants should expect to improve their applications/UIs and grow their data storage on Filecoin throughout the course of the competition. Throughout the competition, the Slingshot leaderboard will be the source of truth, so monitor this leaderboard closely to make sure your project is properly represented there.

* You must participate in the Slingshot Showcase.

* There is no deadline specifically for applying. The defacto deadline is at the end of Phase 1 (October 14, 2020, at 1800 UTC).

* We will distribute rewards based on the aggregate data stored across deals made by each project marked Eligible on the leaderboard 
(meaning they passed Community Review stage).

* Deals do not have to be fully sealed to be counted at the deadline. However, the deals must at least be in preCommit phase 2. In other words, for a deal to be counted, the deal must be accepted, the data transferred to the miner, and sealing begun with preCommit phase 1 completed.

* Offline deals are eligible. They'll still show up on-chain (and consequently, on the leaderboard).

* You must make storage deals with at least 3 miners on the SR2 network. As long as, in aggregate, you have at least one deal stored with at least three miners, this rule is satisfied. There are no requirements with the number of miners with whom you have to store an individual CID. The total volume across these replicas will be counted towards your reward calculation. 

* You are allowed to store up to 10 replicas of the same piece of data on the network. Storing more than 10 replicas will be considered gaming the competition. One way we are checking this is by validating the ratio between the Number of storage deals and the Number of Unique CIDs stored that are shown on the leaderboard. For example, we've seen a client store 6 unique CIDs through 515 storage deals, or on average ~85 storage deals per CID. This address is ineligible for rewards.

* You must store each CID such that it can be retrieved from the Filecoin network. We will test for CID retrieval periodically throughout the course of the competition.

* You can upload files of any size, but we recommend you break larger files into chunks that are between 1-4GB. A single Filecoin deal cannot be more than 32GB, but again, you can have a larger file span multiple deals if you break it into smaller pieces.

* Miners can limit the minimum and maximum file size. You can query the maximum like this:
    `lotus client query-ask t01278`
        Ask: t01278
        Price per GiB: 0.0000000001 FIL
        Verified Price per GiB: 0.0000000001 FIL
        Max Piece size: 32 GiB

* Make sure that you can build an application or UI around the curated datasets so that others can use it too. If you’re able to do that with zipped files, it’s ok. But if not, then you’ll have to unzip and probably do batched deals.

* You can use IPFS as a caching layer but your app needs to demonstrate Filecoin retrieval functionality to qualify. 

*  If you are setting max price limits in Filecoin storage deals, please set these to greater than or equal to 100,000,000 attoFIL / GiB / epoch. This is the price that we are recommending storage miners set their asks to, and so will allow deals to go through in the marketplace. If you’re unfamiliar with the units described here, 1 FIL = 10^18 attoFIL (1,000,000,000,000,000,000) / GiB = gibibyte, and epoch = unit of time on the Filecoin blockchain that is equivalent to ~30 real world seconds. At this rate that we are recommending (100,000,000 attoFIL / GiB / epoch), you should be able to store ~18TiB for 6 months with 1 FIL. The top candidate on the leaderboard has currently stored 2TiB, so 1FIL should be more than enough to get you to the top of the leaderboard if you treat your funds carefully.

* It is up to developers to decide what a good storage deal price is. However, they should treat testnet Filecoin as extremely scarce. A heuristic of 100,000,000 attoFIL/GiB/epoch might be a good starting point.

* There is no minimum duration requirement for storage deals for Slingshot. Currently, individual storage deals in Filecoin must be between 6 months and 1.5 years.

* If you have run out of funds to make storage deals, please request additional FIL through the Filecoin faucet. https://spacerace.faucet.glif.io/ If you have already used the faucet, you can request additional FIL through this top-up form. We will be disbursing 1FIL at a time for teams that have less than 1FIL combined between their addresses. Please treat your testnet funds very carefully. 

* The Slingshot admin and Textile teams are helping to maintain a list of recommended miners that are available to make storage deals with. If you would like to make storage deals on testnet, please try storing data with these miners first. https://github.com/filecoin-project/slingshot/blob/master/miners.json

* There is a (semi) daily list of miner sealing times being posted at:
https://github.com/jimpick/workshop-client-testnet/blob/spacerace/src/annotations-spacerace.js

* Encrypted data need to follow a specific verification process to get Slingshot credit. This will need to be completed during the Showcase and final verification. More details on this process will be shared in Week 3 of Phase 1.

* Toward the end of SR2, we will confirm the process for pre-loading sectors sealed during testnet into mainnet.


# Hosted Powergate API
The APIs you will have access to are the same APIs made available in the Powergate Localnet. We recommend that you do most of your development, testing, and experimentation on that resource (Localnet). It's easy, free, and fast. When you need to start doing further experiments on the broader network, this instance is here. 

Additional Warning
------------------
We are providing you a very open Powergate instance. In particular, the top-level API is not protected by a token, meaning others could tamper with your wallets or create new FFS instances. Track this ticket for updates and improvements. Until then, we don't recommend sharing your endpoint URLs anywhere in public. For example, in support Slack, we have a record of your endpoints, so no need to share them.  This instance is currently connected to Testnet network and may require unannounced resets in the future.

Connecting
----------
The patterns for connecting and using the service should closely match what you had been doing locally with `localnet`. 
You can pass in a flag or environmental variable to use the CLI, indicating the remote API endpoint. 

 - Your endpoint is on `pow.deplatformr.textile.io`
 - To connect to it in your CLI, use: `POW_SERVERADDRESS=api.pow.deplatformr.textile.io:443 pow health`
 - You can find the index gateway at, https://pow.deplatformr.textile.io/asks
 - You can attach to the gRPC API using:   
   `client = PowerGateClient("api.pow.deplatformr.textile.io:443", is_secure=True)`


Autofunding FFS Wallets
-----------------------
All hosted Powergates have been tuned to work specifically for the ongoing Slingshot competition. As part of that, we fund all new Powergates with 1.1Fil in the master address. The master address is then set to fun new FFS Instances 0.25Fil on creation. So up to 4 FFS Instance addresses will be autofunded. After that, you will need to acquire funds and transfer them to new addresses (e.g. using the faucet). The 0.25FIL should have enough for storing a lot of data. But shouldn't think of their default FFS tokens as "dispensable".


Watching Powergate transactions
-------------------------------

* `pow ffs -t <token> log <data-cid>`

* provides a nicer output to what's happening:  
`pow ffs watch [jobid,...] [flags]`

* Watch Powergate Localnet when running in `nohup` mode. 
  `watch -n 2 ' tail -n 10 nohup.out'`


Report the Powergate FIL address to Slingshot
---------------------------------------------
* Use `pow ffs addrs list`. It implies the addresses from that ffs instance will be used to make the deals.

Hosted Powergate FIL
--------------------
* Each hosted Powergate instance has 1 FIL. Each new FFS instance you create will get 0.25FIL. So you can't create more than four FFS instances. You should be able to use a single FFS instance to store data many many times. So the amount that we fund each FFS instance should be enough to only need one FFS instance for storing lots of data.

FAQs
----
* What is the unit of measurement when you run `pow asks get`? Bytes.

* The EpochPrice is the price that the miner charge in attoFIL per GB per epoch. Minimal deal duration is 6 months defined by the Filecoin network. Miners doesn't announce accepted deal durations. They just reject the deal if they don't like the deal now. (but you can change this anyway in your StorageConfig).

* Assuming that EpochPrice is in attoFIL per GiB per epoch; if I want to store a file of 50 MiB, my storage cost will be (EpochPrice * 50 / 1024 attoFIL) per epoch.  The EpochPrice in MiB would be the number divided by 1024. 

* It's a bit more complicated since the the data size is not exactly the real data you send, since should have some padding etc.. Is it possible to know they amount of padding required? Also, I saw that there is a command in lotus which goes something like `lotus query-ask <miner>`, which gives the price per GiB per epoch. Is that possible in MiB? For example, would my small file be padded with some other user’s small file, and we pay just for our part. Or would it be padded with some garbage data, and I would have to pay a fixed minimum amount? No, the data you sent can't leverage other users data. Each data size is padded to the next power of 2 (yes.. in some cases that's a lot of padding), so that padding is "garbage".
https://github.com/textileio/powergate/issues/619 

* ActivactionEpoch is the epoch at which the deal is committed to the chain in a sealed sector, and StartEpoch is the epoch in which the real really is considered active on chain (which is decided by the client on the Deal).  

* If can find the CID in IPFS, but not it FFS, then this item is not stored in Filecoin. It means no miner stored the item, right? What should I do next? override or do something else to push the item to filecoin? ANSWER: `-o`

* On the hosted Powergate, I used the miners list from https://github.com/filecoin-project/slingshot/blob/master/miners.json and set replication factor to 10. However the deal gets proposed to only 2-3 miners. Is there any solution to fix this? The hosted Powergates are configured as the recommended settings for SR2 -- 3 deals per CID.

* In Slingshot, Powergate is using a custom miner-selector strategy by default: SR2-MinerSelector. Every time Powergate needs to create a deal, it will fetch this JSON file, and it will one miner at random from each region and make deals with them. https://github.com/filecoin-project/slingshot/blob/master/miners.json 

* This list is maintained by the Slingshot team to include miners that should be reasonably reliable to increase the odds of deal success. Powergate fetches this file every time it needs to do a deal. It will always select miners from the most up to date version of it. As you can notice, if you set TrustedMiners or RepFactor in your storage config those will be ignored by Powergate. If you want full control using your StorageConfig, you can run powd with --ffsminerselector="reputation" (or env POWD_FFSMINERSELECTOR) which switches to the previous unopinionated miner selector strategy used before SR2.

* Is it possible to obtain detailed information about the deal from storage? Like what is the miner is hosting? Where is from this miner? If you do `pow ffs show`  per Cid you successfully stored, you can see which miners have them. The miners index should also calculate an approximate location of each of them. I've lowered the load indexes are making on lotus node since this was affecting their syncing stability. Short answer: you could by mixing ffs APIs and index APIs. But now the metadata-index is not fully functional (for priority reasons for Lotus), I might take a look again at this next week to find a solution.

* What does this dealStartOffset parameter do in ffs? It is how much time we give miners to complete all the process of sealing and posting on chain. We use a bigger value than default since being too tight might make the deal fail since the miner is too clogged with work and can't make it on time. This can be tuned in your StorageConfig.

* `pow ffs config push [cid] --override` The --override flag is required to indicate you understand you're changing an existing StorageConfig with a new one... which might lead to making new deals or having some cost.

* You can configure cold storage retrieval using. See https://docs.textile.io/powergate/storageconfig/#storageconfig-details `AllowUnfreeze` tells Powergate, go pull from cold storage if you cannot find it on hot.

* The hosted Powergate default config has `Hot` `Enabled` set to `false`.  However, staging a file still gets me the response "Success! Cached file in FFS hot storage with cid: QmY4K9ac16CHqRKupfoWjXqhoryuaTu7VxNXGSnVgWiM32". How can this be if hot storage is not enabled? Is the staged file there for a temporary period of time before I push it to Cold storage? If so, how long is this window of time?  
  * the response message could be cleaned up. staging does cache it in the same layer that is your Hot layer, but it doesn’t not store it permanently there. recall “Hot” just means “ipfs node” here, so it is cached there until you make a deal with lotus (and garbage collection removes it).
cached. in hot. but not permanent unless you push a config that says to make it so

* If I change the Hot Enabled setting in my DefaultConfig to true and use it for all my file uploads, does that mean that all these files will be indefinitely cached in that Powergate server's IPFS node? If so, what's the maximum capacity of this IPFS cache on a hosted Powergate?  
  * Not much. We don’t recommend turning it on for all storage. but if you need select parts for the network to just do them specifically on. (or if you are testing the ability for an app to toggle them on/off)

* If I understand previous discussion threads in this channel correctly, adjusting `RepFactor`, `ExcludedMiners`, `TrustedMiners` , and `CountryCodes`  on a hosted Powergate will have no effect. Textile has defaulted the RepFactor to 3 and is "using a custom miner-selector strategy by default: SR2-MinerSelector. Every time Powergate needs to create a deal, it will fetch this JSON file (https://github.com/filecoin-project/slingshot/blob/master/miners.json), and it will select one miner at random from each region and make deals with them). But I should keep track of each of these 3 pushes to make sure that a deal hasn't failed, right? Let's say one of the three deals has failed. If I repush that file (with an -o overide flag), will it drop the two successful deals and start from scratch, trying to make deals with 3 new miners from that day's JSON file list? Or will the first two successful deals persist and then 3 new override deals may be added to make for 5 copies of the CID in the end?  
  * no, the pow will check to see how much of the new config is already fulfilled by the state of the storage deals. so if it detects 2 and y you ask for 3, it would just create 1 more

* `DealMinDuration` "DealDuration indicates the duration to be used when making new deals." To be clear, this is the amount of time, in Filecoin epochs, that I want a deal to persist my data, right? The hosted Powergate default for DealMinDuration is set to "518400". Is this equivalent to the minimum 6 month deal duration that is currently in effect on Testnet by default? If not, how much time is this in "real" time?  
  * that’s block count, but approx 6 months yes

* `MaxPrice`  from the Slingshot channel: "If you are setting max price limits in Filecoin storage deals, please set these to greater than or equal to 100,000,000 attoFIL / GiB / epoch. This is the price that we are recommending storage miners set their asks to, and so will allow deals to go through in the marketplace." So to compl with this my MaxPrice setting should be = "1000000000", right? i.e. it is using attoFIL denomination?  
  * Correct

* How do I get the Filecoin Lotus CID via IPFS CID or jobId?  
   `pow ffs storage -pf --cids <cid>`

* How do I retrieve data via data cid from cold storage directly?  
  * If you set HotStorage: true and AllowUnfreeze: true in the StorageConfig, that should retrieve the data from    
    Filecoin and place it in your go-ipfs node.  
  * From Lotus: https://docs.filecoin.io/store/lotus/retrieve-data/#making-a-retrieval-deal

* Is it possible sum all stored data using pow?  
  * You can use `pow ffs show` to get list of all currently stored data and its size. Yu'd have to sum them yourself.
  * Also, there is that bug with `pow ffs show` where it fails if there are any storage jobs in progress. 



REFERENCES:
===========

Powergate CLI
-------------
https://docs.textile.io/powergate/cli/pow/

Powergate storage workflow
--------------------------
https://docs.textile.io/powergate/ffs/

Powergate Slingshot FAQ
-----------------------
https://docs.textile.io/powergate/faq/

Powergate Slingshot Masterclass
--------------------------------
video:  https://www.youtube.com/watch?v=synHYG4AnJk. 

notes:  https://github.com/textileio/workshops/tree/master/20-09-28-powergate-masterclass

