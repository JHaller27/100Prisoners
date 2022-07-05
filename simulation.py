from dataclasses import dataclass
import random
from typing import Iterator


class OutOfGuessesException(Exception):
	pass


class PrisonerNotDoneException(Exception):
	pass


@dataclass
class _Box:
	slip: int
	is_open: bool

	def copy(self) -> '_Box':
		return _Box(self.slip, self.is_open)


class _Room:
	_boxes: list[_Box]

	def __init__(self, boxes: list[_Box]) -> None:
		self._boxes = boxes

	@property
	def size(self) -> int:
		return len(self._boxes)

	def _get_box(self, id: int) -> _Box:
		return self._boxes[id-1]

	def box_is_open(self, id: int) -> bool:
		box = self._get_box(id)
		return box.is_open

	def open_box(self, id: int) -> int:
		"""
		:param id: 1-indexed box number
		:return: Slip value
		"""
		box = self._get_box(id)
		box.is_open = True
		return box.slip


class _RoomTemplate:
	_boxes: list[_Box]

	def __init__(self, size: int) -> None:
		slips = list(range(1, size+1))
		random.shuffle(slips)

		self._boxes = []
		for _ in range(size):
			box = _Box(slips.pop(), False)
			self._boxes.append(box)

	@property
	def size(self) -> int:
		return len(self._boxes)

	def create(self) -> _Room:
		return _Room([b.copy() for b in self._boxes])


class Scenario:
	_room_template: _RoomTemplate
	_prisoners: list[int]

	def __init__(self, room: _RoomTemplate) -> None:
		self._room_template = room
		self._prisoners = [i+1 for i in range(self.size)]

	def __iter__(self):
		return self

	def __next__(self) -> 'Scene':
		if not self.has_prisoners_left():
			raise StopIteration

		return self.get_next_scene()

	@property
	def size(self) -> int:
		return self._room_template.size

	def has_prisoners_left(self) -> bool:
		return len(self._prisoners) > 0

	def get_next_scene(self) -> 'Scene':
		"""
		:returns: Next scene
		"""
		current_prisoner = self._prisoners.pop(0)
		room = self._room_template.create()
		scene = Scene(self, room, current_prisoner)

		return scene

	def get_all_scenes(self) -> Iterator['Scene']:
		while self.has_prisoners_left():
			yield self.get_next_scene()


class Scene:
	_scenario: Scenario
	_room: _Room
	_tries_left: int
	_current_prisoner: int
	_failed: bool

	def __init__(self, scenario: Scenario, room: _Room, prisoner_id: int) -> None:
		self._scenario = scenario
		self._room = room

		self._done = False
		self._failed = False

		self._tries_left = self._scenario.size // 2
		self._current_prisoner = prisoner_id

	@property
	def size(self) -> int:
		return self._scenario.size

	@property
	def current_prisoner(self) -> int:
		return self._current_prisoner

	@property
	def is_done(self) -> bool:
		return self._tries_left <= 0

	@property
	def is_success(self) -> bool:
		return self.is_done and not self._failed

	def _clean_up(self, slip: int) -> None:
		if slip == self._current_prisoner:
			self._tries_left = 0
			return

		self._tries_left -= 1

		if self.is_done and slip != self._current_prisoner:
			self._failed = True

	def try_open_box(self, box_id: int) -> int:
		"""
		Opens a box and returns the number on the contained slip
		:param id: 1-indexed box id
		:return: slip value, if box was not opened
		:raises OutOfGuessesException: if out of guesses
		:raises ValueError: if the box was already open
		"""
		if self.is_done:
			raise OutOfGuessesException()

		if self._room.box_is_open(box_id):
			raise ValueError(f'Box #{box_id} is already open')

		slip = self._room.open_box(box_id)

		self._clean_up(slip)
		return slip


def new_scenario(size: int) -> Scenario:
	room_template = _RoomTemplate(size)
	scenario = Scenario(room_template)

	return scenario
