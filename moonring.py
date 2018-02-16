import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anm

G = 6.674e-20 # km^3 kg^-1 s^-2
day = 60.0 * 60.0 * 24.0
dt = day / 10.0 # 1/10th of a day
Mearth = 5.972e24
Mmoon = 7.342e22

N = 10000
delta = np.random.random(1) * 2.0 * np.pi / N
angles = np.linspace(0.0, 2.0 * np.pi, N) + delta

ringrad = np.random.uniform(low = 10.0e3, high = 1000.0e3, size = (N))
xrings, yrings = ringrad * np.cos(angles), ringrad * np.sin(angles)
vxrings, vyrings = np.sqrt(G * Mearth / ringrad) * -np.sin(angles), np.sqrt(G * Mearth / ringrad) * np.cos(angles)

xmoon, ymoon = 384.0e3, 0.0
vxmoon, vymoon = 0.0, np.sqrt(G * Mearth / xmoon)

fig, ax = plt.subplots()
xdata, ydata = [], []

moon, = plt.plot([xmoon], [ymoon], 'r.', animated = True)
earth, = plt.plot([0.0], [0.0], 'g.', animated = True)
rings, = plt.plot(xrings, yrings, 'b,', animated = True)
lab = ax.text(0.5, 1.05, '', transform = ax.transAxes, va = 'center', animated = True)

def init():
	ax.set_xlim(-1500.0e3, 1500.0e3)
	ax.set_ylim(ax.get_xlim())
	ax.set_aspect('equal')
	lab.set_position(( 0.0e3, -900.0e3 ))
	return moon,earth,rings,lab

def update(frame):
	global xmoon, ymoon, vxmoon, vymoon, Mearth, Mmoon, G
	global xrings, yrings, vxrings, vyrings, dt, day
	
	lab.set_text('Day {0:d}'.format(int(frame * dt / day)))
	moon.set_data([ xmoon ],  [ ymoon ])
	rings.set_data(xrings, yrings)
	
	xmoon += vxmoon * dt
	ymoon += vymoon * dt
	
	dmoon = np.hypot(xmoon, ymoon)
	vxmoon -= G * Mearth / (dmoon ** 2.0) * (xmoon / dmoon) * dt
	vymoon -= G * Mearth / (dmoon ** 2.0) * (ymoon / dmoon) * dt
	
	xrings += vxrings * dt
	yrings += vyrings * dt
	
	drings1 = np.hypot(xrings, yrings)
	drings2 = np.hypot(xmoon - xrings, ymoon - yrings)
	vxrings -= G * Mearth / (drings1 ** 2.0 + 1.0e3) * (xrings / drings1) * dt + G * Mmoon / (drings2 ** 2.0 + 1.0e3) * (xrings / drings2) * dt
	vyrings -= G * Mearth / (drings1 ** 2.0 + 1.0e3) * (yrings / drings1) * dt + G * Mmoon / (drings2 ** 2.0 + 1.0e3) * (yrings / drings2) * dt
	
	return moon,earth,rings,lab

ani = anm.FuncAnimation(fig, update, frames = np.arange(0.0, 10000.0), init_func = init, blit = True, interval = 1000 / 60)
plt.show()
