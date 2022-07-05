import multiprocessing as mp
import simulation as sim
import random


DEBUG=False
def debug(*args, **kwargs):
	if DEBUG:
		print(*args, **kwargs)


def try_prisoner(scene: sim.Scene) -> sim.Scene:
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
			return scene
		except ValueError:
			continue
		else:
			debug(f"{slip=}")

	return scene


def run_scenario(scenario: sim.Scenario) -> bool:
	done_scenes = map(try_prisoner, scenario)
	for scene in done_scenes:
		success = scene.is_success
		print(f"Prisoner #{scene.current_prisoner}", "successfully found" if success else "failed to find", "their slip")
		if not success:
			return False

	print("All prisoners found their slips!")
	return True


def try_first_prisoner(scenario: sim.Scenario) -> bool:
	scene = next(scenario)
	scene = try_prisoner(scene)
	return scene.is_success


def main(size: int):
	with mp.Pool() as pool:
		results = pool.map(try_first_prisoner, [sim.new_scenario(size) for _ in range(100000)])

	success_count = results.count(True)
	total_count = len(results)

	rate = float(success_count) / total_count
	print(f"Prisoner #1 success rate: {rate:01.2%}")


if __name__ == '__main__':
	main(100)
