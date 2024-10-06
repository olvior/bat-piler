var px = 15
var py = 21

var vx = 4
var vy = 4

var ax = 0
var ay = -1

var change_y = 0

var floor = 0

var input_var = 0 
var is_a = 0
var was_a = 0

var is_d = 0
var was_d = 0

var is_w = 0
var was_w = 0


.main
	call .clear

	input LOAD_CONTROLLER input_var
	set was_a = is_a
	set is_a = input_var && 1

	set was_d = is_d
	set is_d = input_var && 4

	set was_w = is_w
	set is_w = input_var && 8

	if is_a == 1
		if was_a != 1
			set vx = vx - 6
		endif
	endif


	if is_d == 4
		if was_d != 4
			set vx = vx + 6
		endif
	endif


	if is_w == 8
		if was_w != 8
			set vy = 6
		endif
	endif

	set vx = vx + ax
	set vy = vy + ay

	set px = px + vx
	set py = py + vy

	if py >= 128
		negate vy
		set vy = vy - 2
		negate py
		set py = py - 1
	endif

	if py >= 30
		negate vy
		set py = 60 - py
	endif

	if px >= 128
		negate vx
		set vx = vx - 1
		negate px
		set px = px - 1
	endif

	if px >= 30
		negate vx
		set vx = vx + 1
		set px = 60 - px
	endif


	call .draw_player

	call .push

	goto .main

	halt

.draw_player
	var cursorx = px
	var cursory = py
	call .draw_pixel

	set cursorx = cursorx + 1
	call .draw_pixel

	set cursory = cursory + 1
	call .draw_pixel

	set cursorx = cursorx - 1
	call .draw_pixel

	return

.draw_pixel
	output SCREEN_SET_PIXEL_X cursorx
	output SCREEN_SET_PIXEL_Y cursory

	output SCREEN_DRAW_PIXEL
	return

.clear
	output SCREEN_CLEAR
	return

.push
	output SCREEN_PUSH
	return
