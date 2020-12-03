# ConcreteXSection
Service and Ultimate level force analysis of concrete cross sections

ToDo:
- [x] Repository Licensing - ** 3-Clause BSD **
- [x] Programming Languages to Support - ** Python and VBA **
- [x] National Building Codes to Support
 - ACI 318
 - EN 1992-1-1 December 2004
 - CSA

Concrete Compression Stress Block Formulations for Sections defined by straight lines:
- [x] Whitney Block
  - [x] verified - Area * 0.85 * F'c
- [x] PCA Parabolic+Linear Stress Block
  - [x] verified - see backup material verified against 3 point Gauss Integration
- [ ] Eurocode 2 Parabolic + Linear Stress Block (eq 3.17) - **Parametric Formula derived needs verification**

Concrete Compression Stress Block Formulations for Circular Sections:
- [x] Whitney Block
  - [x] verified - Segment area * 0.85 * F'c
- [x] PCA Parabolic + Linear Stress Block
  - [x] verified - verification via 100 discrete trapezoid slices through parabolic region
- [ ] Eurocode 2 Parabolic + Linear Stress Block (eq 3.17) - **Researching, When n=2 similar to PCA when n<2 numeric integration may be the best option**
