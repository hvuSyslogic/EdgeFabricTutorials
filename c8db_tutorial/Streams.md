Macrometa Streams provide realtime pub/sub messaging capabilities for the Macrometa Edge Fabric. They allow client programs to send and receive messages to/from the fabric servers and allow for communication between different fabric components.

### Stream enumeration/listing and existence check
```bash
$from c8 import C8Client
$client = C8Client(protocol='https', host='MY-C8-EDGE-DATA-FABRIC-URL', port=443)
$tennt = client.tenant(name='mytenant', fabricname='_system', username='root', password='root_pass')
$sys_fabric = client.fabric(tenant='mytenant', name='_system', username='root', password='root_pass')
$streams = sys_fabric.streams()
```
### List all persistent local streams.
print( sys_fabric.persistent_streams(local=True) )

# List all persistent global streams.
print( sys_fabric.persistent_streams(local=False) )

# List all nonpersistent local streams.
print( sys_fabric.nonpersistent_streams(local=True) )

# List all nonpersistent global streams.
print( sys_fabric.nonpersistent_streams(local=False) )

# Check if a given stream exists.
sys_fabric.has_stream('testfabricPersLocal')

### Stream creation and publish/subscribe messages on stream 
```bash
$sys_fabric.create_stream('test-stream', persistent=True, local=False)    

```
With persistent topics, all messages are durably persisted on disk (that means on multiple disks unless the broker is standalone), whereas data for non-persistent topics isn’t persisted to storage disks.
In the above example, we created a new global persistent stream called test-stream. If persistent flag set to False,
a non-persistent stream gets created. Similarly a local stream gets created if local 
flag is set to True. By default persistent is set to True and local is set to False .

###Create a StreamCollection object to invoke stream management functions.
```bash
$stream_collection = sys_fabric.stream()
```
'StreamCollection' object permits you to perform all stream-related activities.We will see some examples below.

###Create producer for the given persistent/non-persistent and global/local stream that is created.
```bash

$producer1 = stream_collection.create_producer('test-stream', persistent=True, local=False)
$producer2 = stream_collection.create_producer('test-stream-1', persistent=False, local=True)
```
A producer is a process that attaches to a topic and publishes messages to a Pulsar broker for processing.
Topics are named channels for transmitting messages from producers to consumers. They have a defined URL structure. Topic generation is taken care of by create_producer function.You just need to pass a stream name.
 
###Send: publish/send a given message over stream in bytes.
```bash
$for i in range(10):
    msg1 = "Persistent: Hello from " + region + "("+ str(i) +")"
    msg2 = "Non-persistent: Hello from " + region + "("+ str(i) +")"
    producer1.send(msg1.encode('utf-8'))
    producer2.send(msg2.encode('utf-8'))
```
The producer object allows you to send messages to the topic you created. Remember to convert message to bytes before sending.

#Create a subscriber to the given persistent/non-persistent and global/local stream with the given subscription name.
substream_collection = sys_fabric.stream()
subscriber1 = substream_collection.subscribe('test-stream', persistent=True, local=False, subscription_name="test-subscription-1")
subscriber2 = substream_collection.subscribe('test-stream-1', persistent=False, local=True, subscription_name="test-subscription-2")

You can subscribe to a particular topic. You become a consumer of that topic by subscribing.Consumers can then subscribe to those topics, process incoming messages, and send an acknowledgement when processing is complete.
NOTE - If no subscription new is provided then a random name is generated based on tenant and fabric information.

###Receive: read the published messages over stream.
```bash
$for i in range(10):
   msg1 = subscriber1.receive()  #Listen on stream for any receiving msg's
   msg2 = subscriber2.receive()
   print("Received message '{}' id='{}'".format(msg1.data(), msg1.message_id())) #Print the received msg over stream
   print("Received message '{}' id='{}'".format(msg2.data(), msg2.message_id()))
   subscriber1.acknowledge(msg1) #Acknowledge the received msg.
   subscriber2.acknowledge(msg2)
```
Once a subscription has been created, all messages will be retained , even if the consumer gets disconnected. Retained messages will be discarded only when a consumer acknowledges that they’ve been successfully processed.

###Get the list of subscriptions for a given persistent/non-persistent local/global stream.
```bash
$stream_collection.get_stream_subscriptions('test-stream-1', persistent=True, local=False) #for global persistent stream
```

###get_stream_stats
```bash
$stream_collection.get_stream_stats('test-stream-1', persistent=True, local=False) #for global persistent stream

```
You can get stream statistics for a particular stream by passing the stream name.

###Expire messages for a given subscription of a stream.
```bash
stream_collection.expire_messages_for_subscription('test-stream-1', 'test-subscription-1', 3600)

```
By default, unacknowledged messages are stored forever. This can lead to heavy disk space usage in cases where a lot of messages are going unacknowledged. If disk space is a concern, you can set a time to live (TTL) that determines how long unacknowledged messages will be retained.
For 'test-stream-1', if 'test-subscription-1' subscriber doesnt consume the messages withing 60mins, it is expired.

###Expire messages on all subscriptions of stream
```bash
stream_collection.expire_messages_for_subscriptions('test-stream-1',3600)
```
If messages aren't acknowledged in 60mins ,messages are expired for all subscriptions. 

###trigger compaction status
```bash
stream_collection.put_stream_compaction_status('test-stream-5')

```
By default,all unacknowledged/unprocessed messages produced on a topic are stored forever. Accumulating many unacknowledged messages on a topic is necessary for many Pulsar use cases but it can also be very time intensive for consumers to “rewind” through the entire log of messages.
Topic compaction feature enables you to create compacted topics in which older, “obscured” entries are pruned from the topic, allowing for faster reads through the topic’s history (which messages are deemed obscured/outdated/irrelevant will depend on your use case).
You can trigger compaction on a stream with this method call.

###Unsubscribes the given subscription on all streams on a stream fabric
```bash
stream_collection.unsubscribe('test-subscription-1')
```

###delete subscription of a stream
```bash
stream_collection.delete_stream_subscription('test-stream-1', 'test-subscription-1' ,persistent=True, local=False)
```
