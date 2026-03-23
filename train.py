import os

import mlflow
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def build_dataset(df: pd.DataFrame):
    target_candidates = ["target", "label", "y", "class"]
    target_col = next((c for c in target_candidates if c in df.columns), None)

    if target_col is not None:
        y = df[target_col]
        x = df.drop(columns=[target_col])
    else:
        # Fallback for unlabeled CSV files: create a deterministic synthetic label.
        x = df.copy()
        row_sum = x.sum(axis=1)
        y = (row_sum > row_sum.median()).astype(int)

    x = x.fillna(0)
    return x, y


def main() -> int:
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if not tracking_uri:
        raise RuntimeError(
            "MLFLOW_TRACKING_URI is not set. Refusing to log to a local default store."
        )

    mlflow.set_tracking_uri(tracking_uri)
    print("Using MLflow tracking URI from environment")

    df = pd.read_csv("data.csv")
    x, y = build_dataset(df)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    with mlflow.start_run() as run:
        model = LogisticRegression(max_iter=300)
        model.fit(x_train, y_train)
        preds = model.predict(x_test)
        accuracy = float(accuracy_score(y_test, preds))

        mlflow.log_param("model", "LogisticRegression")
        mlflow.log_param("rows", int(len(df)))
        mlflow.log_metric("accuracy", accuracy)

        run_id = run.info.run_id
        with open("model_info.txt", "w", encoding="utf-8") as f:
            f.write(run_id)

        print(f"RUN_ID={run_id}")
        print(f"ACCURACY={accuracy:.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())