<h1>Orbital Propagator</h1>


<h2>Description</h2>
An interactive 3D orbital mechanics visualizer built in Python. This script simulates the trajectory of a satellite in Low Earth Orbit (LEO) by numerically integrating Newton's laws of universal gravitation alongside the J2 analytical perturbation model, capturing the orbital drift caused by Earth's oblate shape.

---
<br />

<h2>Languages and Utilities Used</h2>

- <b>Python</b> 

<h2>The Physics Behind It:</h2>

Standard orbital models assume Earth is a perfect sphere. In reality, Earth is an oblate spheroid, fatter at the equator due to its rotation. This equatorial mass bulge exerts an asymmetric gravitational pull, causing the satellite's orbital plane to twist over time (nodal precession). 

This propagator accounts for this by adding the $J_2$ perturbation acceleration to standard two-body mechanics:

$$a_{total} = a_{2body} + a_{J_2}$$

When running the 24-hour simulation, you will visibly observe the orbital path shift, creating a dynamic loop pattern rather than a single repeating oval.

<h2>Visual Preview </h2>


https://github.com/user-attachments/assets/466183fb-cd67-47a4-91ef-8e0403830dcd









