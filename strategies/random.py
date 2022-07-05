import simulation as sim
import random


DEBUG=False
def debug(*args, **kwargs):
	if DEBUG:
		print(*args, **kwargs)


def try_prisoner(scene: sim.Scene) -> None:
	prisoner_id = scene.current_prisoner
	debug(f"{prisoner_id=}")

	boxes_left = list(range(1, scene.size+1))
	random.shuffle(boxes_left)

	boxes_seen = set()

	slip = -1
	while slip != prisoner_id:
		box_id = boxes_left.pop()
		debug(f"\t{box_id=}", end=' | ')

		assert box_id not in boxes_seen
		boxes_seen.add(box_id)

		try:
			slip = scene.try_open_box(box_id)
		except sim.OutOfGuessesException:
			return
		except ValueError:
			continue
		else:
			debug(f"{slip=}")
