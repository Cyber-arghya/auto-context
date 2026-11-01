"""
Autonomous Test Runner for auto-context test suite.
Executes all test_*.py test files, supports both CI and local test execution without external dependencies.
"""
import importlib
import inspect
from pathlib import Path
import sys
import tempfile
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure src and root are in sys.path
TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
SRC_DIR = REPO_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(REPO_ROOT))

def run_all_tests() -> int:
    start_time = time.time()
    test_files = sorted(TESTS_DIR.glob("test_*.py"))
    total_passed = 0
    total_failed = 0
    failures = []

    print(f"\n==================== Running auto-context test suite ====================")
    print(f"Target: {REPO_ROOT}")
    print(f"Discovered test files: {len(test_files)}\n")

    for tf in test_files:
        mod_name = f"tests.{tf.stem}"
        try:
            mod = importlib.import_module(mod_name)
        except Exception as e:
            print(f"[FAIL] Error importing {mod_name}: {e}")
            total_failed += 1
            failures.append((mod_name, "import", str(e)))
            continue

        test_funcs = [
            (name, func) for name, func in inspect.getmembers(mod, inspect.isfunction)
            if name.startswith("test_")
        ]

        print(f"Running {tf.name} ({len(test_funcs)} tests):")
        for test_name, func in test_funcs:
            sig = inspect.signature(func)
            kwargs = {}
            td = None
            if "tmp_path" in sig.parameters:
                td = tempfile.TemporaryDirectory()
                kwargs["tmp_path"] = Path(td.name)

            try:
                func(**kwargs)
                print(f"  [PASS] {test_name}")
                total_passed += 1
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                print(f"  [FAIL] {test_name}: {e}")
                total_failed += 1
                failures.append((tf.name, test_name, tb))
            finally:
                if td:
                    try:
                        td.cleanup()
                    except Exception:
                        pass

    elapsed = time.time() - start_time
    print(f"\n==================== Test Summary ====================")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Time:   {elapsed:.2f}s")

    if failures:
        print("\nFailures:")
        for mod, name, tb in failures:
            print(f"\n--- {mod} :: {name} ---")
            print(tb)
        return 1

    print("\n[SUCCESS] 100% Tests Passed!\n")
    return 0

if __name__ == "__main__":
    sys.exit(run_all_tests())
