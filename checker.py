from pymongo import MongoClient
from datetime import datetime
from leapc_cffi import ffi, libleapc
import serial
import time 

# Connect to MongoDB Atlas

uri = "mongodb+srv://thecargaming:notpassword@cluster0.jepcu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

# Specify the database name you want to print
database_name = "test"  # Replace with your actual database name

# Access the specific database
db = client[database_name]

database_name = "test"  # Replace with your actual database name
collection_name = "users"  # Replace with your collection name

access_request_database = "access_request"
collection_access = "req"

# Access the specific database and collection
db = client[database_name]
collection = db[collection_name]

db2 = client[access_request_database]
collection2 = db[collection_access]

print(f"📂 Contents of Database: {database_name}")
print(f"📄 Collection: {collection_name}")

# Find all documents in the 'users' collection, and retrieve only the 'passwordSequence' field
documents = collection.find({}, {"name": 1,"passwordSequence": 1, "_id": 0})  # Exclude _id field


def password_checker():
     # Initialize a connection configuration
    connection_config = ffi.new("LEAP_CONNECTION_CONFIG *", {"size": ffi.sizeof("LEAP_CONNECTION_CONFIG")})

    # Create a Leap Motion connection
    connection = ffi.new("LEAP_CONNECTION *")
    result = libleapc.LeapCreateConnection(connection_config, connection)
    if result != libleapc.eLeapRS_Success:
        print(f"Error creating connection: {result}")
        return

    print("Connection created successfully.")

    # Open the connection
    result = libleapc.LeapOpenConnection(connection[0])
    if result != libleapc.eLeapRS_Success:
        print(f"Error opening connection: {result}")
        return

    print("Connection opened successfully. Waiting for frames...")

    # Variables for frame data and pausing
    password_data = []  # Array to store password data
    frame_counter = 0  # Tracks the current frame number
    frame_range = 400  # Number of frames per password segment
    swipe_threshold = 500  # Minimum velocity (in mm/s) for a rightward swipe

    while True:
        # Poll for connection messages
        message = ffi.new("LEAP_CONNECTION_MESSAGE *")
        result = libleapc.LeapPollConnection(connection[0], 1000, message)

        if result == libleapc.eLeapRS_Success:
            if message.type == libleapc.eLeapEventType_Tracking:
                # Cast message data to tracking event
                tracking_event = ffi.cast("LEAP_TRACKING_EVENT *", message.tracking_event)
                print(f"Frame ID: {tracking_event.info.frame_id}")
                print(f"Number of hands detected: {tracking_event.nHands}")

                extended_fingers = 0  # Count the number of extended fingers

                for i in range(tracking_event.nHands):
                    hand = tracking_event.pHands[i]
                    hand_type = "Left" if hand.type == libleapc.eLeapHandType_Left else "Right"
                    print(f"  {hand_type} hand detected.")

                    for j in range(5):  # Iterate through all 5 fingers
                        finger = hand.digits[j]
                        if finger.is_extended:  # Check if the finger is extended
                            extended_fingers += 1

                    # Check palm velocity for a rightward swipe
                    velocity_x = hand.palm.velocity.x
                    print(f"  Palm velocity (x-axis): {velocity_x:.2f} mm/s")

                    # Wait for a rightward swipe to proceed
                    if velocity_x > swipe_threshold:
                        print("Rightward swipe detected! Proceeding to the next segment.")
                        break

                print(f"Fingers extended in this frame: {extended_fingers}")

                # Increment the frame counter
                frame_counter += 1

                # Store data every `frame_range` frames
                if frame_counter % frame_range == 0:
                    password_data.append(extended_fingers)
                    print(f"Stored {extended_fingers} fingers for frames {frame_counter - frame_range + 1} to {frame_counter}.")

                    # Wait for a rightward swipe or finish the password
                    if len(password_data) == 4:
                        print("Complete! Swipe your hand to the right to continue.")
                    else:
                        print("Segment complete! Swipe your hand to the right to continue.")
                    while True:
                        # Poll for connection messages to detect a swipe
                        message = ffi.new("LEAP_CONNECTION_MESSAGE *")
                        result = libleapc.LeapPollConnection(connection[0], 1000, message)

                        if result == libleapc.eLeapRS_Success and message.type == libleapc.eLeapEventType_Tracking:
                            tracking_event = ffi.cast("LEAP_TRACKING_EVENT *", message.tracking_event)
                            for i in range(tracking_event.nHands):
                                hand = tracking_event.pHands[i]
                                velocity_x = hand.palm.velocity.x
                                if velocity_x > swipe_threshold:
                                    print("Rightward swipe detected! Proceeding to the next digit.")
                                    break
                            else:
                                continue
                            break

                # Stop after collecting 4 segments
                if len(password_data) >= 4:  # Adjust this number as needed
                    print("Password collected:", password_data)
                    break
            else:
                print(f"Unhandled event type: {message.type}")
        else:
            print(f"No frame data. Error code: {result}")

    # Print the final password
    print("Final Password Array:", password_data)
    return password_data



# Print all the 'passwordSequence' arrays
password = password_checker()
for doc in documents:
    if password == doc["passwordSequence"]:
        password_found = 'Password\n'
        data = {
            'name': doc["name"],
            'date':  datetime.utcnow()
        }
        insert_result = collection2.insert_one(data)
        break
else:
    password_found = 'noPassword\n'
     
arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)

def send_to_arduino(message):
    arduino.write(message.encode())  # Send data to Arduino
    time.sleep(0.1)  # Small delay for Arduino to process

send_to_arduino(password_found)  # Send result to Arduino
print(f"Sent to Arduino: {password_found}")