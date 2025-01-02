from controller2 import *
import threading

if __name__ == '__main__':
    thread1 = threading.Thread(target=daq_task)
    thread1.start()
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
    
    
        
