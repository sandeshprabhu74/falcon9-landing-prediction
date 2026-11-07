"""Runs steps 3, 4, 5, 6 and 8 in order (steps 1-2 need internet APIs; step 7 is the dashboard)."""
import subprocess, sys
for script in ["03_data_wrangling.py", "04_eda_visualization.py", "05_eda_sql.py",
               "06_folium_map.py", "08_predictive_analysis.py"]:
    print(f"\n===== {script} =====")
    if subprocess.run([sys.executable, script]).returncode != 0:
        sys.exit(f"{script} failed - fix the error above and re-run.")
print("\nAll done. Check the outputs/ folder.")
