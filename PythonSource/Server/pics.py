from PIL import ImageGrab
import struct
import io


def sendScreenShot(clientSocket):

    print("loading..")
    screenshot = ImageGrab.grab()
    screenshot_bytes = io.BytesIO()
    screenshot.save(screenshot_bytes, format='PNG')
    screenshot_bytes = screenshot_bytes.getvalue()

    # # Send the size of the image data first
    size = len(screenshot_bytes)
    size_bytes = struct.pack('!I', size)
    clientSocket.send(size_bytes)

    # clientSocket.sendall(struct.pack('!I', size))
    # # Then send the image data
    # clientSocket.sendall(screenshot_bytes)

    chunk_size = 1024
    offset = 0
    while offset < size:
        end_offset = offset + chunk_size
        if end_offset > size:
            end_offset = size
        clientSocket.send(screenshot_bytes[offset:end_offset])
        offset = end_offset


    print("Screenshot sent successfully")

