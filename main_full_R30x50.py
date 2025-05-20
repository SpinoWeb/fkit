import fiberkit as fkit

#########################################
# Step 1: Define fiber material properties
#########################################
# define patch fiber material properties
fcd = .85 * 25 / 1.5
Ec = 31.5e3
fyd = 450 / 1.15
Es = 210e3

fiber_concrete = fkit.patchfiber.Hognestad(fpc=fcd, take_tension=True)
fiber_steel    = fkit.nodefiber.Bilinear(fy=fyd, Es=Es)

b = 300
h = 500
c = 30

As = 201


#########################################
# Step 2: Define sections
#########################################
# create a rectangular beam section with SectionBuilder
section1 = fkit.sectionbuilder.rectangular(width = b, 
                                           height = h, 
                                           cover = c, 
                                           top_bar = [As, 2, 1, 0], 
                                           bot_bar = [As, 4, 1, 0],  
                                           concrete_fiber = fiber_concrete, 
                                           steel_fiber = fiber_steel)


#########################################
# Step 3: Moment curvature analysis
#########################################
# roughly estimate target curvature to which we will push the section
# Estimate yield curvature which will be our target
depth = h
phi_yield_approximate = 0.003 / (0.25*depth)
print("phi_yield_approximate: ", phi_yield_approximate)

Pmin = -b * h * fcd - As * 6 * fyd
print("Pmin: ", Pmin)
p = 0.4

# start moment curvature analysis
MK_results = section1.run_moment_curvature(phi_target = phi_yield_approximate, P = p * Pmin)
df_nodefibers, df_patchfibers = section1.get_all_fiber_data()

# cracked moment of inertia
Icr_results = section1.calculate_Icr(Es=Es, Ec=Ec)

# PM Interaction surface analysis
PM_results = section1.run_PM_interaction(fpc=fcd, fy=fyd, Es=Es)

# plot results
fig = fkit.plotter.plot_MK(section1)
fig.show()
#fkit.plotter.plot_PM(section1)
#fkit.plotter.plot_Icr(section1)
#fkit.plotter.plot_MK_3D(section1) # NEW IN VERSION 2.0.0

input("Press Enter to exit...")