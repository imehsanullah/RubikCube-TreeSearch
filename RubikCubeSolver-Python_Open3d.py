import math
import random
import threading
import time
from collections import deque
from dataclasses import dataclass

import numpy as np
import open3d as o3d


WINDOW_TITLE = "Rubik Cube Tree Search - Open3D"
CUBIE_SIZE = 0.56
GAP = 0.06
TURN_ANGLE_DEGREES = 90
TURN_STEP_DEGREES = 10
PLAYBACK_INTERVAL_SECONDS = 0.18
DEFAULT_SCRAMBLE_LENGTH = 5
MAX_SEARCH_DEPTH = 12
MAX_SEARCH_STATES = 200000
BODY_COLOR = np.array([0.08, 0.08, 0.09])
GLFW_PRESS = 1
GLFW_REPEAT = 2
GLFW_MOD_SHIFT = 0x0001

STICKER_COLORS = {
    "W": np.array([0.95, 0.95, 0.95]),
    "Y": np.array([0.96, 0.86, 0.20]),
    "O": np.array([0.92, 0.42, 0.14]),
    "R": np.array([0.75, 0.12, 0.12]),
    "G": np.array([0.12, 0.55, 0.24]),
    "B": np.array([0.10, 0.28, 0.70]),
}

SOLVED_FACE_COLORS = {
    "U": "W",
    "D": "Y",
    "L": "O",
    "R": "R",
    "F": "G",
    "B": "B",
}

MOVE_SPECS = {
    "U": ("z", 1, -1),
    "D": ("z", -1, 1),
    "L": ("x", -1, 1),
    "R": ("x", 1, -1),
    "F": ("y", 1, -1),
    "B": ("y", -1, 1),
}

INVERSE_LABELS = {
    "U": "U'",
    "D": "D'",
    "L": "L'",
    "R": "R'",
    "F": "F'",
    "B": "B'",
}

FACE_VECTORS = {
    "L": (-1, 0, 0),
    "R": (1, 0, 0),
    "B": (0, -1, 0),
    "F": (0, 1, 0),
    "D": (0, 0, -1),
    "U": (0, 0, 1),
}

VECTOR_TO_FACE = {vector: face for face, vector in FACE_VECTORS.items()}
MOVE_ORDER = ["F", "f", "B", "b", "L", "l", "R", "r", "U", "u", "D", "d"]


def axis_index(axis: str) -> int:
    return {"x": 0, "y": 1, "z": 2}[axis]


def rotation_matrix(axis: str, angle_radians: float) -> np.ndarray:
    c = math.cos(angle_radians)
    s = math.sin(angle_radians)

    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    if axis == "z":
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

    raise ValueError(f"Unsupported axis: {axis}")


def rotate_lattice_vector(vector: tuple[int, int, int], axis: str, direction: int) -> tuple[int, int, int]:
    matrix = rotation_matrix(axis, math.radians(TURN_ANGLE_DEGREES * direction))
    rotated = np.rint(matrix @ np.array(vector, dtype=float)).astype(int)
    return tuple(int(value) for value in rotated)


def centered_box(width: float, height: float, depth: float, color: np.ndarray) -> o3d.geometry.TriangleMesh:
    mesh = o3d.geometry.TriangleMesh.create_box(width=width, height=height, depth=depth)
    mesh.translate((-width / 2, -height / 2, -depth / 2))
    mesh.paint_uniform_color(color)
    mesh.compute_vertex_normals()
    return mesh


def local_sticker(face: str, color_key: str) -> o3d.geometry.TriangleMesh:
    sticker_size = CUBIE_SIZE * 0.78
    sticker_depth = CUBIE_SIZE * 0.08
    half_body = CUBIE_SIZE / 2
    offset = half_body + sticker_depth / 2 + 0.002

    if face in {"L", "R"}:
        mesh = centered_box(sticker_depth, sticker_size, sticker_size, STICKER_COLORS[color_key])
    elif face in {"F", "B"}:
        mesh = centered_box(sticker_size, sticker_depth, sticker_size, STICKER_COLORS[color_key])
    else:
        mesh = centered_box(sticker_size, sticker_size, sticker_depth, STICKER_COLORS[color_key])

    centers = {
        "L": (-offset, 0.0, 0.0),
        "R": (offset, 0.0, 0.0),
        "F": (0.0, offset, 0.0),
        "B": (0.0, -offset, 0.0),
        "U": (0.0, 0.0, offset),
        "D": (0.0, 0.0, -offset),
    }
    mesh.translate(centers[face])
    return mesh


def inverse_move(move: str) -> str:
    return move.lower() if move.isupper() else move.upper()


@dataclass
class CubieState:
    lattice_pos: tuple[int, int, int]
    stickers: dict[str, str]


class CubeState:
    def __init__(self, cubies: dict[tuple[int, int, int], CubieState] | None = None) -> None:
        self.cubies = cubies if cubies is not None else self._build_solved_cubies()

    @staticmethod
    def _build_solved_cubies() -> dict[tuple[int, int, int], CubieState]:
        cubies: dict[tuple[int, int, int], CubieState] = {}

        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                for z in (-1, 0, 1):
                    stickers: dict[str, str] = {}
                    if x == -1:
                        stickers["L"] = SOLVED_FACE_COLORS["L"]
                    if x == 1:
                        stickers["R"] = SOLVED_FACE_COLORS["R"]
                    if y == 1:
                        stickers["F"] = SOLVED_FACE_COLORS["F"]
                    if y == -1:
                        stickers["B"] = SOLVED_FACE_COLORS["B"]
                    if z == 1:
                        stickers["U"] = SOLVED_FACE_COLORS["U"]
                    if z == -1:
                        stickers["D"] = SOLVED_FACE_COLORS["D"]

                    lattice_pos = (x, y, z)
                    cubies[lattice_pos] = CubieState(lattice_pos=lattice_pos, stickers=stickers)

        return cubies

    def copy(self) -> "CubeState":
        return CubeState(
            {
                pos: CubieState(lattice_pos=cubie.lattice_pos, stickers=dict(cubie.stickers))
                for pos, cubie in self.cubies.items()
            }
        )

    def apply_move(self, move: str) -> "CubeState":
        face = move.upper()
        axis, layer, sign = MOVE_SPECS[face]
        direction = sign * (1 if move.isupper() else -1)
        axis_idx = axis_index(axis)
        rotated_cubies: dict[tuple[int, int, int], CubieState] = {}

        for cubie in self.cubies.values():
            position = cubie.lattice_pos
            if position[axis_idx] != layer:
                rotated_cubies[position] = CubieState(position, dict(cubie.stickers))
                continue

            new_position = rotate_lattice_vector(position, axis, direction)
            new_stickers: dict[str, str] = {}

            for sticker_face, color_key in cubie.stickers.items():
                vector = FACE_VECTORS[sticker_face]
                rotated_vector = rotate_lattice_vector(vector, axis, direction)
                new_stickers[VECTOR_TO_FACE[rotated_vector]] = color_key

            rotated_cubies[new_position] = CubieState(new_position, new_stickers)

        return CubeState(rotated_cubies)

    def is_solved(self) -> bool:
        for face, expected_color in SOLVED_FACE_COLORS.items():
            colors = self.visible_face_colors(face)
            if any(color != expected_color for color in colors):
                return False
        return True

    def visible_face_colors(self, face: str) -> list[str]:
        positions = []
        for position, cubie in self.cubies.items():
            if face == "F" and position[1] == 1:
                positions.append((position[2], position[0], cubie.stickers["F"]))
            elif face == "B" and position[1] == -1:
                positions.append((position[2], -position[0], cubie.stickers["B"]))
            elif face == "R" and position[0] == 1:
                positions.append((position[2], -position[1], cubie.stickers["R"]))
            elif face == "L" and position[0] == -1:
                positions.append((position[2], position[1], cubie.stickers["L"]))
            elif face == "U" and position[2] == 1:
                positions.append((-position[1], position[0], cubie.stickers["U"]))
            elif face == "D" and position[2] == -1:
                positions.append((position[1], position[0], cubie.stickers["D"]))

        positions.sort(key=lambda item: (-item[0], item[1]))
        return [item[2] for item in positions]

    def state_key(self) -> tuple[tuple[tuple[int, int, int], tuple[tuple[str, str], ...]], ...]:
        return tuple(
            (position, tuple(sorted(cubie.stickers.items())))
            for position, cubie in sorted(self.cubies.items())
        )


@dataclass
class SearchOutcome:
    moves: list[str] | None
    states_explored: int
    elapsed_seconds: float
    message: str


def solve_bidirectional(
    start_cube: CubeState,
    max_depth: int = MAX_SEARCH_DEPTH,
    max_states: int = MAX_SEARCH_STATES,
) -> SearchOutcome:
    started = time.perf_counter()
    goal_cube = CubeState()
    start_key = start_cube.state_key()
    goal_key = goal_cube.state_key()

    if start_key == goal_key:
        return SearchOutcome([], 1, time.perf_counter() - started, "Cube is already solved.")

    visited_start: dict[tuple, list[str]] = {start_key: []}
    visited_goal: dict[tuple, list[str]] = {goal_key: []}
    frontier_start: dict[tuple, CubeState] = {start_key: start_cube.copy()}
    frontier_goal: dict[tuple, CubeState] = {goal_key: goal_cube}
    depth_start = 0
    depth_goal = 0
    explored = 2

    def expand_frontier(
        frontier: dict[tuple, CubeState],
        visited_self: dict[tuple, list[str]],
        visited_other: dict[tuple, list[str]],
        from_start: bool,
    ) -> tuple[list[str] | None, dict[tuple, CubeState]]:
        nonlocal explored
        next_frontier: dict[tuple, CubeState] = {}

        for state_key, cube in frontier.items():
            path = visited_self[state_key]
            last_move = path[-1] if path else None

            for move in MOVE_ORDER:
                if last_move is not None and move == inverse_move(last_move):
                    continue

                next_cube = cube.apply_move(move)
                next_key = next_cube.state_key()

                if next_key in visited_self:
                    continue

                next_path = path + [move]
                visited_self[next_key] = next_path
                next_frontier[next_key] = next_cube
                explored += 1

                if next_key in visited_other:
                    if from_start:
                        solution = next_path + [inverse_move(item) for item in reversed(visited_other[next_key])]
                    else:
                        solution = visited_other[next_key] + [inverse_move(item) for item in reversed(next_path)]
                    return solution, next_frontier

                if explored >= max_states:
                    return None, next_frontier

        return None, next_frontier

    while frontier_start and frontier_goal and (depth_start + depth_goal) < max_depth and explored < max_states:
        if len(frontier_start) <= len(frontier_goal):
            solution, frontier_start = expand_frontier(frontier_start, visited_start, visited_goal, True)
            depth_start += 1
        else:
            solution, frontier_goal = expand_frontier(frontier_goal, visited_goal, visited_start, False)
            depth_goal += 1

        if solution is not None:
            return SearchOutcome(solution, explored, time.perf_counter() - started, "Solution found.")

    elapsed_seconds = time.perf_counter() - started
    if explored >= max_states:
        return SearchOutcome(None, explored, elapsed_seconds, "Search stopped after reaching the state limit.")
    return SearchOutcome(None, explored, elapsed_seconds, "No solution found within the configured depth limit.")


@dataclass
class VisualCubie:
    lattice_pos: np.ndarray
    meshes: list[o3d.geometry.TriangleMesh]

    def rotate(self, matrix: np.ndarray, center: tuple[float, float, float]) -> None:
        for mesh in self.meshes:
            mesh.rotate(matrix, center=center)

    def update_lattice_pos(self, matrix: np.ndarray) -> None:
        self.lattice_pos = np.rint(matrix @ self.lattice_pos).astype(int)


@dataclass
class MoveAnimation:
    move: str
    label: str
    axis: str
    layer: int
    direction: int
    cubies: list[VisualCubie]
    source: str
    applied_degrees: float = 0.0


class RubiksCubeSolverOpen3D:
    def __init__(self) -> None:
        self.cube_state = CubeState()
        self.turn_step = TURN_STEP_DEGREES
        self.visual_cubies = self._build_visual_cubies(self.cube_state)
        self.axis_helper = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.7)
        self.show_axis = True
        self.pending_moves: deque[tuple[str, str]] = deque()
        self.active_move: MoveAnimation | None = None
        self.pending_solution: SearchOutcome | None = None
        self.solver_thread: threading.Thread | None = None
        self.next_move_at = 0.0

    def _log(self, message: str) -> None:
        print(message, flush=True)

    def _build_visual_cubies(self, cube_state: CubeState) -> list[VisualCubie]:
        cubies: list[VisualCubie] = []
        offset = CUBIE_SIZE + GAP

        for position, cubie_state in sorted(cube_state.cubies.items()):
            world_center = np.array([position[0] * offset, position[1] * offset, position[2] * offset], dtype=float)
            meshes = [centered_box(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE, BODY_COLOR)]

            for face, color_key in sorted(cubie_state.stickers.items()):
                meshes.append(local_sticker(face, color_key))

            for mesh in meshes:
                mesh.translate(world_center)

            cubies.append(VisualCubie(lattice_pos=np.array(position, dtype=int), meshes=meshes))

        return cubies

    def _all_meshes(self) -> list[o3d.geometry.TriangleMesh]:
        meshes: list[o3d.geometry.TriangleMesh] = []
        for cubie in self.visual_cubies:
            meshes.extend(cubie.meshes)
        return meshes

    def _add_scene(self, vis: o3d.visualization.Visualizer) -> None:
        meshes = self._all_meshes()
        for index, mesh in enumerate(meshes):
            vis.add_geometry(mesh, reset_bounding_box=index == 0)
        if self.show_axis:
            vis.add_geometry(self.axis_helper, reset_bounding_box=False)

    def _refresh(self, vis: o3d.visualization.Visualizer) -> None:
        for mesh in self._all_meshes():
            vis.update_geometry(mesh)
        vis.update_renderer()

    def _reset_visual_state(self, vis: o3d.visualization.Visualizer) -> None:
        self.visual_cubies = self._build_visual_cubies(self.cube_state)
        vis.clear_geometries()
        self._add_scene(vis)
        vis.reset_view_point(True)
        view = vis.get_view_control()
        view.set_zoom(0.70)
        view.set_front([0.0, 1.0, 0.0])
        view.set_lookat([0.0, 0.0, 0.0])
        view.set_up([0.0, 0.0, 1.0])
        vis.update_renderer()

    def _is_busy(self) -> bool:
        return self.active_move is not None or bool(self.pending_moves) or (
            self.solver_thread is not None and self.solver_thread.is_alive()
        )

    def _queue_move(self, move: str, source: str) -> bool:
        self.pending_moves.append((move, source))
        self.next_move_at = time.monotonic()
        label = INVERSE_LABELS[move.upper()] if move.islower() else move.upper()
        self._log(f"Queued {source.lower()}: {label}")
        return False

    def _manual_move(self, vis: o3d.visualization.Visualizer, move: str) -> bool:
        if self._is_busy():
            self._log("Manual moves are disabled while a scramble, solution playback, or search is active.")
            return False
        return self._queue_move(move, "Manual move")

    def _handle_face_key(
        self,
        vis: o3d.visualization.Visualizer,
        action: int,
        mods: int,
        face: str,
    ) -> bool:
        if action not in {GLFW_PRESS, GLFW_REPEAT}:
            return False
        move = face.lower() if (mods & GLFW_MOD_SHIFT) else face
        return self._manual_move(vis, move)

    def _queue_scramble(self, vis: o3d.visualization.Visualizer) -> bool:
        if self._is_busy():
            self._log("Scramble ignored because the cube is busy.")
            return False

        sequence: list[str] = []
        last_face = None
        for _ in range(DEFAULT_SCRAMBLE_LENGTH):
            choices = [face for face in MOVE_SPECS if face != last_face]
            face = random.choice(choices)
            direction = random.choice((1, -1))
            move = face if direction == 1 else face.lower()
            self.pending_moves.append((move, "Scramble"))
            sequence.append(INVERSE_LABELS[face] if direction == -1 else face)
            last_face = face

        self.next_move_at = time.monotonic()
        self._log(f"Queued scramble: {' '.join(sequence)}")
        return False

    def _reset(self, vis: o3d.visualization.Visualizer) -> bool:
        if self.solver_thread is not None and self.solver_thread.is_alive():
            self._log("Reset ignored while search is running.")
            return False

        self.pending_moves.clear()
        self.active_move = None
        self.pending_solution = None
        self.next_move_at = 0.0
        self.cube_state = CubeState()
        self._reset_visual_state(vis)
        self._log("Cube reset")
        return False

    def _toggle_axis(self, vis: o3d.visualization.Visualizer) -> bool:
        if self.show_axis:
            vis.remove_geometry(self.axis_helper, reset_bounding_box=False)
        else:
            vis.add_geometry(self.axis_helper, reset_bounding_box=False)
        self.show_axis = not self.show_axis
        vis.update_renderer()
        return False

    def _solve_background(self, cube_snapshot: CubeState) -> None:
        self.pending_solution = solve_bidirectional(cube_snapshot)

    def _start_solver(self, vis: o3d.visualization.Visualizer) -> bool:
        if self._is_busy():
            self._log("Solve ignored because the cube is busy.")
            return False

        snapshot = self.cube_state.copy()
        self.pending_solution = None
        self.solver_thread = threading.Thread(target=self._solve_background, args=(snapshot,), daemon=True)
        self.solver_thread.start()
        self._log("Tree search started...")
        return False

    def _start_next_move(self) -> None:
        if self.active_move is not None or not self.pending_moves:
            return

        move, source = self.pending_moves.popleft()
        face = move.upper()
        axis, layer, sign = MOVE_SPECS[face]
        direction = sign * (1 if move.isupper() else -1)
        axis_idx = axis_index(axis)
        cubies = [cubie for cubie in self.visual_cubies if cubie.lattice_pos[axis_idx] == layer]
        label = INVERSE_LABELS[face] if move.islower() else face
        self.active_move = MoveAnimation(
            move=move,
            label=label,
            axis=axis,
            layer=layer,
            direction=direction,
            cubies=cubies,
            source=source,
        )

    def _step_active_move(self, vis: o3d.visualization.Visualizer) -> None:
        if self.active_move is None:
            return

        remaining = TURN_ANGLE_DEGREES - self.active_move.applied_degrees
        step_degrees = min(self.turn_step, remaining)
        signed_degrees = step_degrees * self.active_move.direction
        matrix = rotation_matrix(self.active_move.axis, math.radians(signed_degrees))

        for cubie in self.active_move.cubies:
            cubie.rotate(matrix, center=(0.0, 0.0, 0.0))

        self.active_move.applied_degrees += step_degrees
        self._refresh(vis)

        if self.active_move.applied_degrees >= TURN_ANGLE_DEGREES:
            final_matrix = rotation_matrix(
                self.active_move.axis,
                math.radians(TURN_ANGLE_DEGREES * self.active_move.direction),
            )
            for cubie in self.active_move.cubies:
                cubie.update_lattice_pos(final_matrix)

            self.cube_state = self.cube_state.apply_move(self.active_move.move)
            self._log(f"{self.active_move.source}: {self.active_move.label}")

            if self.active_move.source == "Solution" and not self.pending_moves and self.cube_state.is_solved():
                self._log("Solution playback completed. Cube is solved.")
            elif self.active_move.source == "Scramble" and not self.pending_moves:
                self._log("Scramble completed.")

            if self.active_move.source in {"Solution", "Scramble"}:
                self.next_move_at = time.monotonic() + PLAYBACK_INTERVAL_SECONDS
            else:
                self.next_move_at = time.monotonic()
            self.active_move = None

    def _handle_solution_ready(self) -> None:
        if self.pending_solution is None:
            return

        outcome = self.pending_solution
        self.pending_solution = None
        self.solver_thread = None
        self._log(f"{outcome.message} explored={outcome.states_explored} elapsed={outcome.elapsed_seconds:.2f}s")

        if outcome.moves is None:
            return

        if not outcome.moves:
            self._log("Cube is already solved.")
            return

        move_labels = [INVERSE_LABELS[item.upper()] if item.islower() else item for item in outcome.moves]
        self._log(f"Solution sequence: {' '.join(move_labels)}")
        for move in outcome.moves:
            self.pending_moves.append((move, "Solution"))
        self.next_move_at = time.monotonic()
        if self.active_move is None and self.pending_moves:
            self._log("Queued solution playback.")

    def _animation_tick(self, vis: o3d.visualization.Visualizer) -> bool:
        self._handle_solution_ready()

        if self.active_move is None and self.pending_moves and time.monotonic() >= self.next_move_at:
            self._start_next_move()

        if self.active_move is not None:
            self._step_active_move(vis)

        return False

    def run(self) -> None:
        vis = o3d.visualization.VisualizerWithKeyCallback()
        vis.create_window(window_name=WINDOW_TITLE, width=1280, height=900)

        render_option = vis.get_render_option()
        render_option.background_color = np.array([0.06, 0.07, 0.09])
        render_option.mesh_show_back_face = True

        self._add_scene(vis)
        vis.reset_view_point(True)
        vis.register_animation_callback(self._animation_tick)

        view = vis.get_view_control()
        view.set_zoom(0.70)
        view.set_front([0.0, 1.0, 0.0])
        view.set_lookat([0.0, 0.0, 0.0])
        view.set_up([0.0, 0.0, 1.0])

        for face in MOVE_SPECS:
            vis.register_key_action_callback(
                ord(face),
                lambda vis_, action, mods, f=face: self._handle_face_key(vis_, action, mods, f),
            )

        vis.register_key_callback(ord("S"), self._queue_scramble)
        vis.register_key_callback(ord("T"), self._start_solver)
        vis.register_key_callback(ord("A"), self._toggle_axis)
        vis.register_key_callback(ord("X"), self._reset)

        self._log("Controls:")
        self._log("  U D L R F B: clockwise face turns")
        self._log("  Shift+U/D/L/R/F/B: inverse face turns")
        self._log(f"  S: queue a random {DEFAULT_SCRAMBLE_LENGTH}-move scramble")
        self._log("  T: solve the current cube state with tree search")
        self._log("  X: reset the cube")
        self._log("  A: toggle axis helper")
        self._log("  Q or window close: exit")

        vis.run()
        vis.destroy_window()


if __name__ == "__main__":
    RubiksCubeSolverOpen3D().run()
