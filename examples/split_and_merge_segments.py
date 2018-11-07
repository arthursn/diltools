import diltools as dt
import matplotlib.pyplot as plt

df = dt.load_asc_file('01_Isabelle_QP_Q328oC_P350oC_t10s_09.28.17.asc')
bd = dt.BahrData(df, l0=10e3)

# Split into segments
bdlist = dt.split_segments(bd)

fig, ax = plt.subplots()
for i, bd_ in enumerate(bdlist):
    line, = ax.plot(bd_.t, bd_.Tnom, label=i)
    ax.plot(bd_.t, bd_.T, color=line.get_color(), ls='--')

ax.legend()

plt.show()

fig, ax = plt.subplots()

for bd_ in bdlist[2:]:
    ax.plot(bd_.T, bd_.dll0)

# Merge segments
bd_ = dt.merge_segments(bdlist[2:])

ax.plot(bd_.T, bd_.dll0 + .002, 'k-')

plt.show()