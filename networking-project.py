import Queue

class Host :

	# in_link is null for H2, out_link is null for H1
	def __init__(self, in_link, out_link) : # TODO need smarter way to handle in and out links
		self.in_link = in_link
		self.out_link = out_link

	# Packet is added to the host
	def recieved_packet(self, packet) :
		print 'Recieved packet'


class Router :
	# routing_table is map of destination to Link
	# buffer is a Queue.Queue
	def __init__(self, routing_table) :
		self.routing_table = routing_table

	# Packet is added to the router
	def recieved_packet(packet) :
		return # TODO


class Link :

	# capacity is an int in bytes per ms
	# delay is an int in ms
	# buffer_size is an int, total size of buffer in bytes
	def __init__(self, left_host_or_router, right_host_or_router, capacity, delay, buffer_size) :
		self.capacity = capacity
		self.delay = delay
		self.buffer_size = buffer_size
		self.left_buffer = Queue.Queue() # queue of packets in buffer
		self.right_buffer = Queue.Queue() # queue of packets in buffer
		self.left_host_or_router = left_host_or_router
		self.right_host_or_router = right_host_or_router
		self.packet_positions = {} # maps packet to its position on the link in % of link travelled

	# Packet is added to the link
	# packet is a Packet
	# direction is a boolean, true=right, false=left
	def recieved_packet(self, packet, direction) :
		# TODO add packet to link buffer if a previous packet was recently sent
		self.packet_positions[packet] = 0.

	# Simulate the packet positions on the link after another dt time change
	# dt is thousands of milliseconds
	def update_packet_positions(self, dt) :
		for packet in self.packet_positions.keys() :
			self.packet_positions[packet] += 1. / self.delay / 1000. * dt # 1 full length / number of ms to move 1 length / 1000 ms thousandths per ms * number of ms thousands passed
			if self.packet_positions[packet] >= 1. : # reached full length of link
				del self.packet_positions[packet] # packet isnt on link anymore
				self.right_host_or_router.recieved_packet(packet) # add packet to next router/host or TODO put on buffer


class Packet :

	# global size value
	size = 1024 # TODO not true for ack

	# source is a host
	# destination is a host
	# data is a list of floats
	# ack is a boolean (TODO questionable design choice)
	def __init__(self, source, destination, data, ack) :
		self.source = source
		self.destination = destination
		self.data = data
		self.ack = ack

	# packet has no functions because it does no actions, is just passively moved


class Flow :

	# source is a host
	# destination is a host
	# data_amt is an int defining number of bytes
	# flow_start is an int defining number of ms
	def __init__(self, source, destination, data_amt, flow_start) :
		self.source = source
		self.destination = destination
		self.data_amt = data_amt
		self.flow_start = flow_start


# define Case 0 network topology
source = Host(None, None) # TODO function sig probably wrong
destination = Host(None, None) # TODO function sig probably wrong
link = Link(source, destination, 10*1024*1024/1000, 10, 64*1024)
flow = Flow(source, destination, 20*1024*1024, 1000) # TODO function sig probably wrong


# loop time steps in thousandths of ms
for t in range(1,3000) :

	# occasionally add packets to link
	if t/10==0 :
		packet = Packet(source, destination, [], False)
		link.recieved_packet(packet,True)

	# update movement of packets along link
	link.update_packet_positions(1)




