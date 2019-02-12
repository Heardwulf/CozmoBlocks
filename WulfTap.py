#import the cozmo and image libraries
import cozmo


#import libraries for movement and asynchronous behavior
import asyncio
from cozmo.util import degrees, distance_mm

# make sure to import lightcubes
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id

from colors import Colors
from woc import WOC
import _thread
import time

# talk speed
talkSpeed = 0.5

def cozmo_program(robot: cozmo.robot.Robot):
	
	# Move lift down and tilt the head up
	robot.move_lift(-3)
	robot.set_head_angle(degrees(0)).wait_for_completed()
	
	#turn backpack lights to RED
	# robot.set_all_backpack_lights(Colors.RED)
	
	#settings for signals from Cozmo's camera
	robot.camera.image_stream_enabled = True
	
	#initially, we may not be connected to our cubes
	cube = None

	#connect to the cubes
	robot.world.connect_to_cubes()
	
	# WULF: Let's comment out this code and see what happens
	# look around and try to find a cube
	look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
	
	#assign a block to the variable cube
	#cube = robot.world.wait_for_observed_light_cube(timeout=30)
	
	#we can adjust this to wait until 1, 2 or 3 cubes have been observed
	cubes = robot.world.wait_until_observe_num_objects(3, object_type = cozmo.objects.LightCube, timeout = 60)
	
	#robot.say_text("I found a cube", duration_scalar= talkSpeed).wait_for_completed()
	#print("Found cube: %s" % cube)
	
	# robot.set_all_backpack_lights(Colors.BLUE)
	
	#Nexst, Cozmo will look for a cube. If there is a tap on
	#the cube, Cozmo will change the color of the lights
	
	if cubes:
		#stop looking around
		look_around.stop()
		
		#if a cube is found, light the cube up
		#cubes.set_lights(Colors.BLUE)
		
		# Drive to 100mm away from the cube (much closer and Cozmo
		# will likely hit the cube) and then stop.
		# moveToCube(robot, cube)
		
		#cube.set_lights(Colors.BLUE)

		cube1 = robot.world.get_light_cube(LightCube1Id)  # looks like a paperclip
		cube2 = robot.world.get_light_cube(LightCube2Id)  # looks like a lamp / heart
		cube3 = robot.world.get_light_cube(LightCube3Id)  # looks like the letters 'ab' over 'T'

		try:
			robot.say_text("Please tap a cube.", duration_scalar= talkSpeed).wait_for_completed()
			#cube.wait_for_tap(timeout=20)
			time.sleep(5)
		except asyncio.TimeoutError:
			robot.say_text("You don't want to play? Game over.", duration_scalar= talkSpeed).wait_for_completed()
			print("No cubes tapped. Game over.")
		finally:
			#cube.set_lights(Colors.RED)
			robot.set_all_backpack_lights(Colors.RED)
			
			#if cube_id == 
			#	robot.say_text("The cube was tapped", duration_scalar= talkSpeed).wait_for_completed()

			if cozmo.objects.EvtObjectTapped == cube1:
				robot.say_text("Block 1 was tapped.", duration_scalar= talkSpeed).wait_for_completed()
			if cozmo.objects.EvtObjectTapped == cube2:
				robot.say_text("Cube 2 was tapped.", duration_scalar= talkSpeed).wait_for_completed()
			if cozmo.objects.EvtObjectTapped == cube3:
				robot.say_text("Hey! Don't touch my block.", duration_scalar= talkSpeed).wait_for_completed()
			if cozmo.objects.EvtObjectTapped == cube:
				robot.say_text("Sweet, but I that's not what I want.", duration_scalar= talkSpeed).wait_for_completed()
			else:
				robot.say_text("I'm confused. Sorry.", duration_scalar= talkSpeed).wait_for_completed()
			#cozmoString = "I am tired of this program."
			#robot.say_text(cozmoString, duration_scalar= talkSpeed).wait_for_completed()


			# Keep the lights on for 10 seconds until the program exits
						
			cube.set_lights_off()

			return

cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)