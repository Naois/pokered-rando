DungeonMons2:
	db $0F
	IF !_YELLOW
		db 51,DODRIO
		db 51,VENOMOTH
		db 51,KADABRA
		db 52,RHYDON
		IF _RED || _GREEN || (_BLUE && !_JAPAN)
			db 52,MAROWAK
		ENDC
		IF (_BLUE && _JAPAN)
			db 52,MAROWAK
		ENDC
		db 52,ELECTRODE
		db 56,CHANSEY
		db 54,WIGGLYTUFF
		db 55,DITTO
		db 60,DITTO
	ENDC

	IF _YELLOW
		db 52,GOLBAT
		db 57,GOLBAT
		db 50,GRAVELER
		db 56,SANDSLASH
		db 50,RHYHORN
		db 60,DITTO
		db 58,GLOOM
		db 58,WEEPINBELL
		db 60,RHYDON
		db 58,RHYDON
	ENDC

	db $00
