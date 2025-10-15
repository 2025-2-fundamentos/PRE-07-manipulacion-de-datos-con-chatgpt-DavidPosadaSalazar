
# %%
# Cargue los datos de las tabla "files/input/drivers.csv" a una variable llamada
# drivers, usando pandas 
import os
import pandas as pd
import matplotlib.pyplot as plt

# Load drivers and timesheet data
# use paths relative to this file's parent so tests run from repo root
drivers = pd.read_csv(os.path.join("files", "input", "drivers.csv"))


# %%
# Cargue los datos de las tabla "files/input/timesheet.csv" a una variable llamada
# timesheet, usando pandas
timesheet = pd.read_csv(os.path.join("files", "input", "timesheet.csv"))

# %%
# Calcule el promedio de las columnas "hours-logged" y "miles-logged" en la 
# tabla "timesheet", agrupando los resultados por cada conductor (driverId).
avg_timesheet = timesheet.groupby("driverId")[["hours-logged", "miles-logged"]].mean().reset_index()
avg_timesheet

# %%
# Cree una tabla llamada "timesheet_with_means" basada en la tabla "timesheet", 
# agregando una columna con el promedio de "hours-logged" para cada conductor (driverId).
timesheet_with_means = timesheet.merge(avg_timesheet[["driverId", "hours-logged"]], on="driverId", suffixes=("", "_mean"))

# %%
# Cree una tabla llamada "timesheet_below" a partir de "timesheet_with_means", filtrando los registros 
# donde "hours-logged" sea menor que "mean_hours-logged".
timesheet_below = timesheet_with_means[timesheet_with_means["hours-logged"] < timesheet_with_means["hours-logged_mean"]]

# --- Produce outputs required by the tests ---
# Ensure output directories exist
output_dir = os.path.join("files", "output")
plots_dir = os.path.join("files", "plots")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

# Create a summary.csv with basic aggregated metrics per driver
summary = timesheet.groupby("driverId")[['hours-logged', 'miles-logged']].agg(['sum', 'mean', 'count'])
# flatten MultiIndex columns
summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
summary = summary.reset_index()
summary = summary.merge(drivers, how='left', left_on='driverId', right_on='driverId')

summary_csv_path = os.path.join(output_dir, 'summary.csv')
summary.to_csv(summary_csv_path, index=False)

# Create a plot: top 10 drivers by total miles-logged
top10 = summary.nlargest(10, 'miles-logged_sum')
plt.figure(figsize=(8, 5))
plt.bar(top10['driverId'].astype(str), top10['miles-logged_sum'], color='C0')
plt.xlabel('driverId')
plt.ylabel('total miles logged')
plt.title('Top 10 drivers by miles logged')
plt.tight_layout()
plot_path = os.path.join(plots_dir, 'top10_drivers.png')
plt.savefig(plot_path)
plt.close()

# If this module is run directly, print where outputs were written
if __name__ == '__main__':
	print(f'Wrote summary to: {summary_csv_path}')
	print(f'Wrote plot to: {plot_path}')

# %%






