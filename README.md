instelation and run instructions:
  1. download the cones csv file here: https://drive.google.com/file/d/14zf1NcsGg393nkl0z_9ne07OgAHEfGKa/view?usp=drive_link
  2. downloud the py files
  3. change the csv file path to your machine path
  4. run the preprocess file
  5. go to optimazation_trials file and find the optimal path


 about the building process:
   1. first step was to preprocess the data:
      1.1 cluster to right and left sides
      1.2 concate rhe tabels
      1.3 find center path
   
   2. my first mission was to find a smoth path so the center path was a good and simple solution to this problem.
   
   3. my secound mission was to find an optima path with minimum curveture:
      3.1 first i study what curveture is and how to musere it. and find out that to strait line the curvature = 0
      3.2 i tried to find a balance between stay in track to minimize the curvature and my aproach was try many combinations those parameters:
          1. how far to "lock" - my path designed base on the next center as one of the parameters and its reflect the general direction of the track
             my control is on how many section away is the center point i aimed for.
          2. minimize the curvature - the secound parameter was the tangent of the path, like i mention before if the car keep going in the tangent direction
             the curvature is 0 so my secound parameter is the "ratio" that control on how weight to put on the tangent infferse to the next point
      3.3 after i designed multiple function that calculate the path base on the parameters i mentioned i also made a curvature calculation function and i
          was ready to start to optimized.

    4. i run a few expirements and succseed to upgrade the avarege curvature here are my results:

    the center path plot representing the start point of the path before any optimaztion:
    ![center_path_plot](https://github.com/user-attachments/assets/1245df33-3541-4d68-b9aa-8d5bfb85c3ab)
     

     the optimal avarage path: 
     ![best_avg_curv](https://github.com/user-attachments/assets/350b689a-2b3c-41c0-a6b7-df51bb08a686)

     as you can see its not smoth in all sections i think it could get better with more work on the next point calculation function

     here you can see how change in the parameters afect the path and the avarage curvature:
     ![smother_path](https://github.com/user-attachments/assets/39c52675-5588-4c8e-a43c-56ce10ef8dd9)


     to sum up, althogh the program is still not perfect i created a basic tool to optimaize pathes its modular so with a short pre process you can optimize any
     track you would like.

     i used in pycharm de on windows 64 pc.

      

