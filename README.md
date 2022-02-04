# Fiend_or_Foe_SLAM
**Authors:** Muhammad Haris Ikram, Saran Khaliq, Muhammad Latif Latif Anjum, Wajahat Hussain


Friend_or_Foe SLAM is modified version of ORB-SLAM with inclusion of adversarial database to detect and prevent false loop closures. Whenever a loop closure is detected by ORB-SLAM, the loop closing candidate is matched with adversarial database. If the match is found with adversarial database, the pipeline is terminated and loop closure is prevented. If the match is not found with adversarial database, the Freind_or_Foe SLAM works as ordinary ORB-SLAM.


#1. Prerequisites (ORB-SLAM Installation)

In order to run Friend-or-Foe SLAM, you will have to successfully install and run the ORB-SLAM. The github link for installation and running ORB-SLAM is given below:

		https://github.com/raulmur/ORB_SLAM


#2. Modifying ORB-SLAM
1. Make sure that ORB-SLAM is running correctly.
2. Clone the repository:

		git clone https://github.com/hkhanr/Friend_or_Foe_SLAM.git

3. Navigate to Friend_or_Foe_SLAM directory and do the following:

Copy the "Adv_database" and "Deciever_code" folders and paste them in ORB_SLAM folder.
Also replace the files in "include" directory of ORB-SLAM with that of Friend_or_Foe_SLAM directory.
In ORB_SLAM  root directory, open "CMakeLists.txt" and do the following:
	
Replace the line
	
		src/LoopClosing.cc
		
by following line

		#src/LoopClosing.cc
		
Paste the following line just below it
	
		Deciever_code/LoopClosing.cc

All the necessary modification are done. Now we need to build the ORB-SLAM again.

#3. Installation
1. Build ORB_SLAM. Go into the ORB_SLAM root and execute the following:

		cd build
		cmake ..
		make

#4. Run SLAM

Launch the SLAM using following command:

		roslaunch ExampleGroovyOrNewer.launch

#5. Example Bag Files
		
Instrucions for running an example bag file on SLAM are given in the following link
		
		https://github.com/raulmur/ORB_SLAM
		
Our example bag files can be download from the following link

		https://drive.google.com/drive/folders/17o6nZJU3RpP6oHx6aoihJ07kfceP3NGU?usp=sharing
		
Also the camera setting file for our example bag can be downloaded from above link and the default setting file should be replaced by it.
