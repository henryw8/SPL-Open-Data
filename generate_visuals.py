#!/usr/bin/env python3
"""Generate visuals manifest for the free throw biomechanics viewer."""

import json
import os

DATA_DIR = "basketball/freethrow/data"
OUTPUT_DIR = "visuals"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    shots = []
    for session in sorted(os.listdir(DATA_DIR)):
        session_path = os.path.join(DATA_DIR, session)
        if not os.path.isdir(session_path):
            continue
        for participant in sorted(os.listdir(session_path)):
            participant_path = os.path.join(session_path, participant)
            if not os.path.isdir(participant_path):
                continue
            for filename in sorted(os.listdir(participant_path)):
                if not filename.endswith(".json"):
                    continue
                filepath = os.path.join(session_path, participant, filename)
                with open(filepath) as f:
                    data = json.load(f)
                shots.append(
                    {
                        "path": f"basketball/freethrow/data/{session}/{participant}/{filename}",
                        "session": data["trial_date"],
                        "participant": data["participant_id"],
                        "trial": data["trial_id"],
                        "result": data["result"],
                        "sampling_rate": data["sampling_rate"],
                        "landing_x": data.get("landing_x"),
                        "landing_y": data.get("landing_y"),
                        "entry_angle": data.get("entry_angle"),
                        "num_frames": len(data["tracking"]),
                    }
                )

    manifest = {"shots": shots, "total": len(shots)}
    with open(os.path.join(OUTPUT_DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f)

    print(f"Generated manifest with {len(shots)} shots in {OUTPUT_DIR}/manifest.json")
    print(f"Open the viewer:  cd {OUTPUT_DIR} && python3 -m http.server 8000")
    print(f"Then visit:       http://localhost:8000")


if __name__ == "__main__":
    main()
