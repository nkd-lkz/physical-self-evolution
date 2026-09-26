import unittest

from memory import AttemptMemory, CompletedTransition, EpisodeKey


class AttemptMemoryTest(unittest.TestCase):
    def setUp(self):
        self.key = EpisodeKey("session-1", "hammer", 7, "controller-v1")
        self.memory = AttemptMemory(bit_capacity=2, pim_capacity=3)
        self.memory.start_episode(self.key)
        self.memory.start_attempt(0)

    def record(self, decision=0, observed=4, phase=(1.0, 0.0), attempt=0, key=None):
        return CompletedTransition(key or self.key, attempt, decision, observed, phase,
                                   (0.1, 0.2), (0.0, 0.5), (0.3, 0.2), "sim-observation")

    def test_no_effect_before_observation(self):
        self.assertEqual(self.memory.read((1.0, 0.0), 0), ((), ()))
        self.memory.write_completed(self.record())
        self.assertEqual(self.memory.read((1.0, 0.0), 3), ((), ()))
        self.assertEqual(len(self.memory.read((1.0, 0.0), 4)[1]), 1)
        with self.assertRaises(ValueError):
            self.memory.write_completed(self.record(4, 4))

    def test_attempt_and_episode_scope(self):
        self.memory.write_completed(self.record())
        self.memory.start_attempt(1)
        recent, persistent = self.memory.read((1.0, 0.0), 0)
        self.assertEqual(len(recent), 0)
        self.assertEqual(len(persistent), 1)
        next_key = EpisodeKey("session-2", "hammer", 7, "controller-v1")
        self.memory.start_episode(next_key)
        self.memory.start_attempt(0)
        self.assertEqual(self.memory.read((1.0, 0.0), 0), ((), ()))
        with self.assertRaises(ValueError):
            self.memory.write_completed(self.record())

    def test_phase_retrieval_and_provenance(self):
        self.memory.write_completed(self.record())
        self.memory.write_completed(self.record(4, 8, (0.0, 1.0)))
        _, matches = self.memory.read((0.0, 1.0), 8)
        self.assertEqual(matches[0].transition.decision_step, 4)
        self.assertEqual(matches[0].transition.label_source, "sim-observation")
        with self.assertRaises(ValueError):
            self.memory.write_completed(self.record(7, 9))


if __name__ == "__main__":
    unittest.main()
