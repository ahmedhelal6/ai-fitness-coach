class RepCounter:
    def __init__(self, config, min_frames_confirm=3):
        self.config = config
        self.reps = 0
        self.stage = config.get("start_stage", None)
        self.last_angle = None

        self.min_frames_confirm = min_frames_confirm
        self.candidate_stage = None
        self.candidate_count = 0

    def reset(self, new_config=None):
        if new_config is not None:
            self.config = new_config
        self.reps = 0
        self.stage = self.config.get("start_stage", None)
        self.last_angle = None
        self.candidate_stage = None
        self.candidate_count = 0

    def _set_stage_with_confirm(self, new_stage):
        if new_stage is None:
            self.candidate_stage = None
            self.candidate_count = 0
            return False, self.stage

        if self.candidate_stage != new_stage:
            self.candidate_stage = new_stage
            self.candidate_count = 1
            return False, self.stage

        self.candidate_count += 1

        if self.candidate_count >= self.min_frames_confirm and self.stage != new_stage:
            old_stage = self.stage
            self.stage = new_stage
            self.candidate_stage = None
            self.candidate_count = 0
            return True, old_stage

        return False, self.stage

    def update(self, angle):
        self.last_angle = angle

        full_angle = self.config["full_angle"]
        contract_angle = self.config["contract_angle"]
        mode = self.config["mode"]

        if mode == "down_up":
            if angle >= full_angle:
                self._set_stage_with_confirm("down")

            elif angle <= contract_angle:
                changed, old_stage = self._set_stage_with_confirm("up")
                if changed and old_stage == "down":
                    self.reps += 1

        elif mode == "up_down_up":
            if angle <= contract_angle:
                self._set_stage_with_confirm("down")

            elif angle >= full_angle:
                changed, old_stage = self._set_stage_with_confirm("up")
                if changed and old_stage == "down":
                    self.reps += 1

        return {
            "reps": self.reps,
            "stage": self.stage,
            "angle": self.last_angle
        }