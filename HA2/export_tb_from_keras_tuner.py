# export_tb_from_keras_tuner.py
import json, os, glob, shutil, datetime, tensorflow as tf, pathlib

# 手动改成自己的路径 ────────────────────────────────────────────────
FULL_DIR = "/home/cxy_otto/xuanyou/ABGA2/HA2/tune_all/cnn_full"        # 40 trial
AUG_DIR  = "/home/cxy_otto/xuanyou/ABGA2/HA2/aug_search/cnn_best_aug"  # 15 trial
# --------------------------------------------------------------------

OUTROOT = "tb_export"                         # 导出的 event 文件总目录
shutil.rmtree(OUTROOT, ignore_errors=True)    # 清空旧结果
os.makedirs(OUTROOT, exist_ok=True)


def export_trials(trial_root: str, subdir: str) -> int:
    """
    把 <trial_root>/<trial_id>/trial.json 中的标量写成 event 文件
    每个 trial → 一个 run 目录：tb_export/<subdir>/<trial_id>/events…
    """
    exported = 0
    for tj in glob.glob(os.path.join(trial_root, "*", "trial.json")):
        with open(tj) as f:
            trial = json.load(f)

        run_dir = pathlib.Path(OUTROOT, subdir, f"trial_{trial['trial_id']}")
        run_dir.mkdir(parents=True, exist_ok=True)
        writer = tf.summary.create_file_writer(str(run_dir))

        # Keras-Tuner 2.x：metrics → metrics → <name> → observations
        for m_name, m_dict in trial["metrics"]["metrics"].items():
            for obs in m_dict.get("observations", []):
                step  = int(obs["step"])
                value = float(obs["value"][0])     # value 是 list
                with writer.as_default():
                    tf.summary.scalar(m_name, value, step=step)
        writer.close()
        exported += 1

    print(f"[✓] {subdir}: exported {exported} trials")
    return exported


def main():
    n_full = export_trials(FULL_DIR, "full")
    n_aug  = export_trials(AUG_DIR,  "aug")
    print(f"\n全部完成，共写入 {n_full + n_aug} 个 trial ✨")


if __name__ == "__main__":
    main()
# export_tb_from_keras_tuner.py
import json, os, glob, shutil, datetime, tensorflow as tf, pathlib

# 手动改成自己的路径 ────────────────────────────────────────────────
FULL_DIR = "/home/cxy_otto/xuanyou/ABGA2/HA2/tune_all/cnn_full"        # 40 trial
AUG_DIR  = "/home/cxy_otto/xuanyou/ABGA2/HA2/aug_search/cnn_best_aug"  # 15 trial
# --------------------------------------------------------------------

OUTROOT = "tb_export"                         # 导出的 event 文件总目录
shutil.rmtree(OUTROOT, ignore_errors=True)    # 清空旧结果
os.makedirs(OUTROOT, exist_ok=True)


def export_trials(trial_root: str, subdir: str) -> int:
    """
    把 <trial_root>/<trial_id>/trial.json 中的标量写成 event 文件
    每个 trial → 一个 run 目录：tb_export/<subdir>/<trial_id>/events…
    """
    exported = 0
    for tj in glob.glob(os.path.join(trial_root, "*", "trial.json")):
        with open(tj) as f:
            trial = json.load(f)

        run_dir = pathlib.Path(OUTROOT, subdir, f"trial_{trial['trial_id']}")
        run_dir.mkdir(parents=True, exist_ok=True)
        writer = tf.summary.create_file_writer(str(run_dir))

        # Keras-Tuner 2.x：metrics → metrics → <name> → observations
        for m_name, m_dict in trial["metrics"]["metrics"].items():
            for obs in m_dict.get("observations", []):
                step  = int(obs["step"])
                value = float(obs["value"][0])     # value 是 list
                with writer.as_default():
                    tf.summary.scalar(m_name, value, step=step)
        writer.close()
        exported += 1

    print(f"[✓] {subdir}: exported {exported} trials")
    return exported


def main():
    n_full = export_trials(FULL_DIR, "full")
    n_aug  = export_trials(AUG_DIR,  "aug")
    print(f"\n全部完成，共写入 {n_full + n_aug} 个 trial ✨")


if __name__ == "__main__":
    main()
