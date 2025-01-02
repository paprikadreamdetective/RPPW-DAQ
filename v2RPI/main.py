from controller import *
import threading

if __name__ == '__main__':
    daq_procedure_thread = threading.Thread(target=daq_task)
    daq_procedure_thread.start()
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
    
    
        
