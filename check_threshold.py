import os
import sys

import mlflow


def main() -> int:
    threshold = float(os.getenv("ACCURACY_THRESHOLD", "0.85"))
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")

    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)

    with open("model_info.txt", "r", encoding="utf-8") as f:
        run_id = f.read().strip()

    run = mlflow.get_run(run_id)
    metrics = run.data.metrics
    accuracy = float(metrics.get("accuracy", 0.0))

    print(f"Run ID: {run_id}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Threshold: {threshold:.2f}")

    if accuracy < threshold:
        print("Accuracy is below threshold. Failing deployment.")
        return 1

    print("Accuracy meets threshold. Deployment may continue.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())