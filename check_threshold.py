import os
import sys

import mlflow

THRESHOLD = 0.70


def main() -> int:
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if not tracking_uri:
        raise RuntimeError("MLFLOW_TRACKING_URI is not set")

    mlflow.set_tracking_uri(tracking_uri)

    with open("model_info.txt", "r", encoding="utf-8") as f:
        run_id = f.read().strip()

    run = mlflow.get_run(run_id)
    accuracy = run.data.metrics["accuracy"]

    print(f"Run ID: {run_id}")
    print(f"Accuracy: {accuracy}")

    if accuracy < THRESHOLD:
        print(f"Accuracy {accuracy} is below threshold {THRESHOLD}")
        sys.exit(1)

    print("Threshold check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())