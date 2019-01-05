import hashlib as hasher
import datetime as date
from flask import Flask, request
from multiprocessing import Process 
import math, json, time

class Block:
	def __init__(self, timestamp, index, data, prev_hash):
		self.timestamp = timestamp
		self.index = index
		self.data = data
		self.prev_hash = prev_hash
		self.hash = self.hash_block()

	def hash_block(self):
		sha = hasher.sha256()
		sha.update(str(self.timestamp) + 
			   str(self.index) +
			   str(self.data) +
			   str(self.prev_hash))
		return sha.hexdigest()

class BlockChain:
	def __init__(self):
		self.blocks = []
		
	def append_block(self, block):
		self.blocks.append(block)

	def create_block(self, data={"pow": 10, "tactions": None}):
		if len(self.blocks) == 0:
			self.blocks.append(Block(date.datetime.now(), 0, data, "0"))
		else:
			prev = self.blocks[-1]
			self.blocks.append(Block(date.datetime.now(), prev.index + 1, data, prev.hash))

	def return_block_info(self, index=0):
		if len(self.blocks) <= index:
			raise IndexError("list index out of range!")
		else:
			curr = self.blocks[index]
			print("Index: {0}; Data: {1}; Hash: {2}; Timestamp: {3}".format(curr.index, curr.data, curr.hash, curr.timestamp))

b = BlockChain()
b.create_block()	#Genesis block

app = Flask(__name__)
transactions = [] 	#Transactions that this node has made/received; emptied after new block is created and process starts all over again

@app.route('/taction', methods=['POST'])
def transaction():
	if request.method == 'POST':
		taction = request.get_json() 	#Extract transaction data
		transactions.append(taction)
		print("From {}".format(taction['from']))
		print("Amount {}".format(taction['amount']))
		return 'Received transaction!\n'

def sqrt_iterations(val):
	sum_t = 0
	for i in range(1, int(val)):
		sum_t += math.sqrt(i)
	return sum_t/val

address = 'abcdefghijklmnopqrstuvwxyz-123456789'	#Pretend this is the address of some other node

@app.route('/mine', methods=['GET'])
def mine():
	transactions.append({"from": "network", "to": address, "amount": 1})

	pow_n = sqrt_iterations(b.blocks[-1].data['pow'])

	b.create_block({"pow": pow_n, "tactions": transactions})
	
	return json.dumps({"index": b.blocks[-1].index,	#Let client know a block was mined
			   "timestamp": time.asctime(time.localtime(time.time())),
			   "data": b.blocks[-1].data,
			   "hash": b.blocks[-1].hash})

	transactions[:] = []	#Clear transactions for next block

#We now need to make sure that the blockchains on the other nodes are identical
###WORK IN PROGRESS###

app.run()
