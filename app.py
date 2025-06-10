import queue
import extract
from pull_request_converter import PullRequestConverter
import transform
def run():
    input_queue = queue.Queue() 
    converter = PullRequestConverter(input_queue) #Thread
    converter.start()
    page = 1 #Used to generate the api request for the pull requests list

    #The loop for each iteration generates a pr list and transfroms the information to csv
    while True:
        pull_requests = extract.fetch_merged_pull_requests(page)
        if not pull_requests:
            break
        transform.compute_pull_requests(pull_requests, converter.input_queue)
        page+=1
        
    #Putting in the queue something different then Report object signals the Thread to stop
    converter.input_queue.put("")
    converter.join()

if __name__ == "__main__":
    run()
