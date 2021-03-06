Route6_Object:
	db $f ; border block

	def_warps
	warp 11,  1, 2, ROUTE_6_GATE
	warp 10,  1, 2, ROUTE_6_GATE
	warp 10,  7, 0, ROUTE_6_GATE
	warp 17, 13, 0, UNDERGROUND_PATH_ROUTE_6

	def_signs
	sign 19, 15, 7 ; Route6Text7

	def_objects
	object SPRITE_COOLTRAINER_M, 10, 21, STAY, RIGHT, 1, OPP_JR_TRAINER_M, 4
	object SPRITE_COOLTRAINER_F, 11, 21, STAY, LEFT, 2, OPP_JR_TRAINER_F, 2
	object SPRITE_YOUNGSTER, 0, 15, STAY, RIGHT, 3, OPP_BUG_CATCHER, 10
	object SPRITE_COOLTRAINER_M, 11, 31, STAY, LEFT, 4, OPP_JR_TRAINER_M, 5
	object SPRITE_COOLTRAINER_F, 11, 30, STAY, LEFT, 5, OPP_JR_TRAINER_F, 3
	object SPRITE_YOUNGSTER, 19, 26, STAY, LEFT, 6, OPP_BUG_CATCHER, 11

	def_warps_to ROUTE_6
