import simulation as sim


def try_prisoner(scene: sim.Scene) -> None:
	prisoner_id = scene.current_prisoner

	box_id = prisoner_id
	while True:
		try:
			box_id = scene.try_open_box(box_id)
		except sim.OutOfGuessesException:
			return
