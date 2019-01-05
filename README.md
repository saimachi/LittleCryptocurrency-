# LittleCryptocurrency-
A tiny cryptocurrency implemented in Python. 

This is a work in progress--I still need to implement a system which ensures that each node in the decentralized system has the same ledger. Currently, the program allows for clients to mine a coin (block) via a HTTP GET request and send a transaction to a node via a POST request. Block hashes are generated with SHA256. The proof of work algorithm is quite basic, as indicated by the code, but I am working on implementing a stronger PoW algorithm, one that may leverage multiple cores.

This experimental currency uses the flask framework to implement communication between the nodes. Install flask via "pip install flask". Once you have flask installed on your system, just run "python little_crypto.py". Enjoy!

