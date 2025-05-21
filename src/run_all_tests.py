
import unittest

# Discover and run all test cases in the current directory
loader = unittest.TestLoader()
suite = loader.discover(start_dir='.', pattern='test_*.py')

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Save results summary
with open("test_results_summary.txt", "w") as f:
    f.write(f"Tests run: {result.testsRun}\n")
    f.write(f"Failures: {len(result.failures)}\n")
    f.write(f"Errors: {len(result.errors)}\n")
    if result.failures or result.errors:
        f.write("\nDetailed Failures and Errors:\n")
        for test, err in result.failures + result.errors:
            f.write(f"\n{test.id()}\n{err}\n")
