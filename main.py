import multiprocessing as mp

import simulation as sim
import strategies.random as rand_strat
import strategies.loop as loop_strat

from typing import Callable


Strategy = Callable[[sim.Scene], None]


def run_scenario(scenario: sim.Scenario, strat: Strategy) -> bool:
	for scene in scenario:
		strat(scene)

		success = scene.is_success
		if not success:
			return False

	return True


def main(size: int, strat: Strategy):
	with mp.Pool() as pool:
		results = pool.starmap(run_scenario, [(sim.new_scenario(size), strat) for _ in range(10**5)])

	success_count = results.count(True)
	total_count = len(results)

	rate = float(success_count) / total_count
	print(f"Success rate: {rate:01.3%}")


if __name__ == '__main__':
	main(100, loop_strat.try_prisoner)
