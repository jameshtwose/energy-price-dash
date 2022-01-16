#%%
import pandas as pd
import seaborn as sns
import numpy as np
# %%
gas_price=1.20
electricity_price=0.26 
hours_used=5
space_for_energy=50

# numbers based on: https://www.ad.nl/geld/schade-blijft-beperkt-gas-en-licht-vanaf-januari-tientjes-per-maand-duurder-bij-energiereuzen~a43c56dcf/?referrer=https%3A%2F%2Fwww.google.com%2F

df = pd.DataFrame({"provider": ["user_choice", "essent", "vattenfall", "eneco"],
"gas_price": [gas_price, 1.11, 1.259, 1.80],
"electricity_price": [electricity_price, 0.25, 0.236, 0.49]})

# user_plot_df = pd.DataFrame({
# "hours_used": np.arange(hours_used, hours_used+5, step=0.5),
# }).assign(**{
#     "provider": lambda x: np.repeat("user_choice", repeats=x.shape[0]),
#     "energy_amount": lambda x: np.repeat(energy_amount, repeats=x.shape[0]),
#     "price_per_day": lambda x: x["energy_range"] * x["hours_used"] *  space_for_energy})

_ = sns.barplot(data=df.melt(id_vars="provider"), x="provider", y="value", hue="variable")
    

# %%
