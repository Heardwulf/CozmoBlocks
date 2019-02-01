#import the cozmo and image libraries
import cozmo


#import libraries for movement and asynchronous behavior
import asyncio
from cozmo.util import degrees, distance_mm

from colors import Colors
from woc import WOC
import _thread
import time

# talk speed
talkSpeed = 0.5

def moveToCube(robot, cube):
	action = robot.go_to_object(cube, distance_mm(100.0))
	action.wait_for_completed()
	robot.say_text("Moved to the cube", duration_scalar= talkSpeed).wait_for_completed()
	return

#def OLD_on_object_tapped(self, event, *, obj, tap_count, tap_duration, **kw):
#	robot.say_text("The cube was tapped", duration_scalar= talkSpeed).wait_for_completed()
#	return

#def on_object_tapped(self):
#	robot.say_text("The cube was tapped. Bravo.", duration_scalar= talkSpeed).wait_for_completed()
#	return

def cozmo_program(robot: cozmo.robot.Robot):
	
	# Move lift down and tilt the head up
	robot.move_lift(-3)
	robot.set_head_angle(degrees(0)).wait_for_completed()
	
	#turn backpack lights to RED
	robot.set_all_backpack_lights(Colors.RED)
	
	#settings for signals from Cozmo's camera
	robot.camera.image_stream_enabled = True
	
	#initially, we may not be connected to our cubes
	cube = None

	#connect to the cubes
	robot.world.connect_to_cubes()
	
	# look around and try to find a cube
	look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
	
	#assign a block to the variable cube
	cube = robot.world.wait_for_observed_light_cube(timeout=30)
	
	#we can adjust this to wait until 1, 2 or 3 cubes have been observed
	# cubes = robot.world.wait_until_observe_num_objects(1, object_type = cozmo.objects.LightCube, timeout = 60)
	
	robot.say_text("I found a cube", duration_scalar= talkSpeed).wait_for_completed()
	print("Found cube: %s" % cube)
	
	robot.set_all_backpack_lights(Colors.BLUE)
	
	#Nexst, Cozmo will look for a cube. If there is a tap on
	#the cube, Cozmo will change the color of the lights
	
	if cube:
		#stop looking around
		look_around.stop()
		
		#if a cube is found, light the cube up
		cube.set_lights(Colors.BLUE)
		
		# Drive to 100mm away from the cube (much closer and Cozmo
		# will likely hit the cube) and then stop.
		moveToCube(robot, cube)
		
		cube.set_lights(Colors.BLUE)
		try:
			robot.say_text("Tap the cube so I know you are paying attention.", duration_scalar= talkSpeed).wait_for_completed()
			cube.wait_for_tap(timeout=20)
		except asyncio.TimeoutError:
			robot.say_text("No one tapped our cube.", duration_scalar= talkSpeed).wait_for_completed()
			print("No-one tapped our cube :-(")
		finally:
			cube.set_lights(Colors.RED)
			robot.set_all_backpack_lights(Colors.RED)
			robot.say_text("The cube was tapped", duration_scalar= talkSpeed).wait_for_completed()

			if cozmo.objects.EvtObjectTapped:
				robot.say_text("The cube was tapped. Bravo.", duration_scalar= talkSpeed).wait_for_completed()
			#cozmoString = "I am tired of this program."
			#robot.say_text(cozmoString, duration_scalar= talkSpeed).wait_for_completed()
			
			cube.set_lights_off()

			return

cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)