import argparse
import cv2
import time


def parse_arguments():
	ap = argparse.ArgumentParser()
	
	ap.add_argument("-v", "--video", type=str, required=True, 
					help="path to input video file")
	ap.add_argument("-fps", "--processing_fps", type=int, required=True, 
					help="number of processing frames per second")
	args = vars(ap.parse_args())
	
	return args


if __name__ == '__main__':
	# Parse command line arguments
	args = parse_arguments()
	
	# Set local variables
	video_name = args["video"]
	processing_fps = args["processing_fps"]

	# Initialize OpenCV video capture object and get video FPS
	video = cv2.VideoCapture(video_name)
	video_fps = video.get(cv2.CAP_PROP_FPS)

	# Calculate and set the skip rate
	if video_fps > processing_fps:
		skip_rate = round(video_fps/processing_fps)*0.75  #SETTING FRAME RATE
	else:
		skip_rate = 1

	frame_no = 0  # Local variable to keep track of video frame number
	processed_frame_count = 0  # Local variable to count total processing frames

	total_grab_time = 0 # Local variable to save the total frame grab time
	total_retrieve_time = 0 # Local variable to save the total frame retreive time

	start = time.time()  # Capture start time, this will be used for processing fps calculation
	
	while True:
		tmp = time.time()
		ret = video.grab()
		total_grab_time += (time.time() - tmp)
		if not ret:
			break  # Video ended
		
		frame_no += 1
		
		if (frame_no % skip_rate == 0):  # Processing frame
			processed_frame_count += 1
			
			tmp = time.time()
			status, frame = video.retrieve()  # Decode processing frame
			total_retrieve_time += (time.time() - tmp)
			
			# Some image processing operations; resize, convert to gray scale and show frame
			frame = cv2.resize(frame, (1280,720))
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			cv2.imshow("Frame", frame)
			cv2.waitKey(1)  # Wait for 1 ms, this is to clearly see the frame on screen

	video.release()
	
	end = time.time()  # Capture end time
	
	# Average frame grab time
	print("Average frame grab time: " + str(1000*total_grab_time/frame_no) + " ms")
	
	# Average frame retrieve time
	print("Average frame retrieve time: " + str(1000*total_retrieve_time/processed_frame_count) + " ms")
	
	# Processing time
	print("Processing Time (.grab()): " + str(end - start) + " sec")
	
	# Processing FPS = Total Processing Frames / Time to process
	print("Processing Speed (.grab()): " + str(processed_frame_count/(end - start)) + " FPS")
