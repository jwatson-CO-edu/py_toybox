# ~ Standard Imports ~
import time
# ~ Minecraft Imports ~
from mcpi.minecraft import Minecraft # Import the MCPI interface library
from mcpi import block # Import the MCPI block library

mc = Minecraft.create() # Create a minecraft interface object

# == Status and Chat ==

mc.postToChat( "Hello World!" ) # Post a chat / status message

# == End Status ==


# == Player Position ==

if False: # Set to True to test player position functions
	pos = mc.player.getPos() # Store the player pos as pos.x/.y/.z # y is vertical
	mc.postToChat( "Player Position: " + str( pos.x ) + " , " + str( pos.y ) + " , " + str( pos.z ) )

	x , y , z = mc.player.getPos() # Store the player pos as x , y , z  # y is vertical
	mc.player.setPos( x , y + 200 , z ) # Teleport the player 200 blocks UP

# == End Player ==

# time.sleep(5)

# == Block Editing ==

if True: # Set to true to test block editing
	x , y , z = mc.player.getPos() # Store the player pos as x , y , z  # y is vertical
	mc.setBlock( x+1 , y+2 , z , 1 	)
	#            x   , y   , z , block_id
	# Create a 10x10x10 block of lapus lazuli
	mc.setBlocks( x+1 , y+1 , z+1 , x+11 , y+11 , z+11 , block.LAPIS_LAZULI_BLOCK.id )
	
	# Drop blocks wherever the player walks
	while True:
		x , y , z = mc.player.getPos()
		mc.setBlock( x , y , z , block.STONE_SLAB.id)
		time.sleep(0.1)

# == End Blocks ==


# == Reference ==

	# Get the api number for the following: mcpi.block.MELON.id

	#API Blocks
	#=======================
	#AIR                   0
	#STONE                 1
	#GRASS                 2
	#DIRT                  3
	#COBBLESTONE           4
	#WOOD_PLANKS           5
	#SAPLING               6
	#BEDROCK               7
	#WATER_FLOWING         8
	#WATER                 8
	#WATER_STATIONARY      9
	#LAVA_FLOWING         10
	#LAVA                 10
	#LAVA_STATIONARY      11
	#SAND                 12
	#GRAVEL               13
	#GOLD_ORE             14
	#IRON_ORE             15
	#COAL_ORE             16
	#WOOD                 17
	#LEAVES               18
	#GLASS                20
	#LAPIS_LAZULI_ORE     21
	#LAPIS_LAZULI_BLOCK   22
	#SANDSTONE            24
	#BED                  26
	#COBWEB               30
	#GRASS_TALL           31
	#WOOL                 35
	#FLOWER_YELLOW        37
	#FLOWER_CYAN          38
	#MUSHROOM_BROWN       39
	#MUSHROOM_RED         40
	#GOLD_BLOCK           41
	#IRON_BLOCK           42
	#STONE_SLAB_DOUBLE    43
	#STONE_SLAB           44
	#BRICK_BLOCK          45
	#TNT                  46
	#BOOKSHELF            47
	#MOSS_STONE           48
	#OBSIDIAN             49
	#TORCH                50
	#FIRE                 51
	#STAIRS_WOOD          53
	#CHEST                54
	#DIAMOND_ORE          56
	#DIAMOND_BLOCK        57
	#CRAFTING_TABLE       58
	#FARMLAND             60
	#FURNACE_INACTIVE     61
	#FURNACE_ACTIVE       62
	#DOOR_WOOD            64
	#LADDER               65
	#STAIRS_COBBLESTONE   67
	#DOOR_IRON            71
	#REDSTONE_ORE         73
	#SNOW                 78
	#ICE                  79
	#SNOW_BLOCK           80
	#CACTUS               81
	#CLAY                 82
	#SUGAR_CANE           83
	#FENCE                85
	#GLOWSTONE_BLOCK      89
	#BEDROCK_INVISIBLE    95
	#STONE_BRICK          98
	#GLASS_PANE          102
	#MELON               103
	#FENCE_GATE          107
	#GLOWING_OBSIDIAN    246
	#NETHER_REACTOR_CORE 247

	# Not accessible through the API but integer numbers correspond to the following:
	
	#Non-API Blocks
	#=======================
	#PAINTING            321
	#STONE_STAIRS         67
	#OAK_STAIRS           53
	#OAK_STAIRS           59
	#NETHERRACK           87
	#TRAPDOOR             96
	#MELON_SEEDS         105
	#BRICK_STAIRS        108
	#SANDSTONE_STAIRS    128
	#STONE_BRICK_STAIRS  109
	#NETHER_BRICK        112
	#NETHER_BRICK_STAIRS 114
	#QUARTZ_BLOCK        155
	#QUARTZ_STAIRS       156
	#STONE_CUTTER        245
	#BONE_MEAL           351

# == End Ref ==
