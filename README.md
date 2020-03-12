# NAIVE FEM

- Environment managed with conda.

- Use Python 3.7

- Create environment with conda:  
  `$ conda env create -f environment.yml`  
  Run the program with run:  
  `$ python __init__.py`

- Output images and videos are in `/out` directory.

---

### Code structure:

**`__init__.py`**  
The main stuff.

**`Obj.py`**  
Object loading/creation and initial deformation.  
`load_obj()` : create a cube  
`load_single()` : create a single tetrahedral

**`Formula.py`**  
All the physical formulae. Including Alg 1 and 2 in paper.  
`precompute()` : correspond to the "precomputation" procedure in the paper  
`compute_P()`, 
`compute_dP()`,
`compute_F()`,
`compute_dF()`  
`update_XV()` : update the parameters X (configuration) and V (velocity)

**`Render.py`**  
Rendering to image and video.

**`Operator.py`**  
Basic vector operations.


---


Currently using 

**St. Venant-Kirchhoff model** as contitutive model for stress (P) and stress differentials (dP).

**Implicit Euler** to update velocity and position.


